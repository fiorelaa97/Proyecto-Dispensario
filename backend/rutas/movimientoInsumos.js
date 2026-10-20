
const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// Convierte y valida los datos del movimiento.
function validarMovimiento(datos) {
    const {
        id_insumo,
        id_empleado,
        tipo_movimiento,
        cantidad,
        fecha,
        motivo
    } = datos;

    const tipo = String(tipo_movimiento || "").trim().toLowerCase();
    const cantidadNum = Number(cantidad);

    if (!id_insumo || !id_empleado) {
        return { error: "Debés seleccionar un insumo y un empleado" };
    }

    if (!["entrada", "salida"].includes(tipo)) {
        return { error: "El tipo debe ser Entrada o Salida" };
    }

    if (!Number.isFinite(cantidadNum) || cantidadNum <= 0) {
        return { error: "La cantidad debe ser mayor que cero" };
    }

    if (!fecha) {
        return { error: "La fecha es obligatoria" };
    }

    return {
        datos: {
            id_insumo,
            id_empleado,
            tipo_movimiento:
                tipo === "entrada" ? "Entrada" : "Salida",
            cantidad: cantidadNum,
            fecha,
            motivo: motivo || null
        }
    };
}

// Devuelve el cambio de stock que representa un movimiento.
function impactoStock(tipo, cantidad) {
    return tipo.toLowerCase() === "entrada"
        ? Number(cantidad)
        : -Number(cantidad);
}

// ==========================
// AGREGAR UN MOVIMIENTO
// ==========================
router.post("/", async (req, res) => {
    const validacion = validarMovimiento(req.body);

    if (validacion.error) {
        return res.status(400).json({ error: validacion.error });
    }

    const movimiento = validacion.datos;
    let conexion;

    try {
        conexion = await pool.getConnection();
        await conexion.beginTransaction();

        // Bloquea el insumo para evitar que dos salidas simultáneas
        // utilicen el mismo stock disponible.
        const [insumos] = await conexion.execute(
            `SELECT cantidad
             FROM insumos
             WHERE id_insumo = ?
             FOR UPDATE`,
            [movimiento.id_insumo]
        );

        if (insumos.length === 0) {
            await conexion.rollback();
            return res.status(404).json({
                error: "El insumo seleccionado no existe"
            });
        }

        const stockActual = Number(insumos[0].cantidad);
        let nuevoStock;

        if (movimiento.tipo_movimiento === "Salida") {
            if (stockActual < movimiento.cantidad) {
                await conexion.rollback();
                return res.status(400).json({
                    error: "Stock insuficiente",
                    stock_disponible: stockActual,
                    cantidad_solicitada: movimiento.cantidad
                });
            }

            nuevoStock = stockActual - movimiento.cantidad;
        } else {
            nuevoStock = stockActual + movimiento.cantidad;
        }

        // Registra el movimiento.
        await conexion.execute(
            `INSERT INTO movimientos_insumos
             (id_insumo, id_empleado, tipo_movimiento,
              cantidad, fecha, motivo)
             VALUES (?, ?, ?, ?, ?, ?)`,
            [
                movimiento.id_insumo,
                movimiento.id_empleado,
                movimiento.tipo_movimiento,
                movimiento.cantidad,
                movimiento.fecha,
                movimiento.motivo
            ]
        );

        // Actualiza el stock dentro de la misma transacción.
        await conexion.execute(
            `UPDATE insumos
             SET cantidad = ?
             WHERE id_insumo = ?`,
            [nuevoStock, movimiento.id_insumo]
        );

        await conexion.commit();

        return res.status(201).json({
            mensaje: "Movimiento registrado y stock actualizado correctamente",
            stock_anterior: stockActual,
            stock_actual: nuevoStock
        });

    } catch (error) {
        if (conexion) await conexion.rollback();

        return res.status(500).json({
            error: "No se pudo registrar el movimiento",
            detalle: error.message
        });
    } finally {
        if (conexion) conexion.release();
    }
});

// ==========================
// LEER TODOS LOS MOVIMIENTOS
// ==========================
router.get("/", async (req, res) => {
    try {
        const [movimientos] = await pool.execute(
            "SELECT * FROM movimientos_insumos ORDER BY id_movimiento DESC"
        );

        res.status(200).json(movimientos);
    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los movimientos",
            detalle: error.message
        });
    }
});

// ==========================
// LEER UN MOVIMIENTO POR ID
// ==========================
router.get("/:id", async (req, res) => {
    try {
        const [movimientos] = await pool.execute(
            `SELECT *
             FROM movimientos_insumos
             WHERE id_movimiento = ?`,
            [req.params.id]
        );

        if (movimientos.length === 0) {
            return res.status(404).json({
                error: "Movimiento no encontrado"
            });
        }

        res.status(200).json(movimientos[0]);
    } catch (error) {
        res.status(500).json({
            error: "No se pudo obtener el movimiento",
            detalle: error.message
        });
    }
});

// ==========================
// EDITAR UN MOVIMIENTO
// Recalcula el stock considerando el movimiento anterior.
// ==========================
router.put("/:id", async (req, res) => {
    const validacion = validarMovimiento(req.body);

    if (validacion.error) {
        return res.status(400).json({ error: validacion.error });
    }

    const nuevo = validacion.datos;
    let conexion;

    try {
        conexion = await pool.getConnection();
        await conexion.beginTransaction();

        const [anteriores] = await conexion.execute(
            `SELECT *
             FROM movimientos_insumos
             WHERE id_movimiento = ?
             FOR UPDATE`,
            [req.params.id]
        );

        if (anteriores.length === 0) {
            await conexion.rollback();
            return res.status(404).json({
                error: "Movimiento no encontrado"
            });
        }

        const anterior = anteriores[0];

        // Bloquear ambos insumos en orden de ID para reducir
        // la posibilidad de bloqueos cruzados.
        const ids = [
            Number(anterior.id_insumo),
            Number(nuevo.id_insumo)
        ].filter((id, index, arr) => arr.indexOf(id) === index).sort((a, b) => a - b);

        const stocks = {};

        for (const id of ids) {
            const [filas] = await conexion.execute(
                `SELECT cantidad
                 FROM insumos
                 WHERE id_insumo = ?
                 FOR UPDATE`,
                [id]
            );

            if (filas.length === 0) {
                await conexion.rollback();
                return res.status(404).json({
                    error: `No existe el insumo ${id}`
                });
            }

            stocks[id] = Number(filas[0].cantidad);
        }

        // Deshace el efecto del movimiento anterior.
        const stockBase =
            stocks[anterior.id_insumo] -
            impactoStock(anterior.tipo_movimiento, anterior.cantidad);

        // Calcula el stock resultante del movimiento editado.
        const stockResultante =
            stocks[nuevo.id_insumo] === undefined
                ? stockBase + impactoStock(
                    nuevo.tipo_movimiento,
                    nuevo.cantidad
                )
                : (
                    Number(nuevo.id_insumo) === Number(anterior.id_insumo)
                        ? stockBase + impactoStock(
                            nuevo.tipo_movimiento,
                            nuevo.cantidad
                        )
                        : stocks[nuevo.id_insumo] + impactoStock(
                            nuevo.tipo_movimiento,
                            nuevo.cantidad
                        )
                );

        if (stockResultante < 0) {
            await conexion.rollback();
            return res.status(400).json({
                error: "Stock insuficiente para editar este movimiento",
                stock_disponible: Number(nuevo.id_insumo) === Number(anterior.id_insumo)
                    ? stockBase
                    : stocks[nuevo.id_insumo],
                cantidad_solicitada: nuevo.cantidad
            });
        }

        // Comprueba que revertir el movimiento anterior no deje
        // negativo el stock del insumo original.
        if (stockBase < 0) {
            await conexion.rollback();
            return res.status(400).json({
                error: "No se puede editar: el stock actual ya depende de este movimiento anterior"
            });
        }

        // Si cambió de insumo, actualiza ambos stocks.
        if (Number(anterior.id_insumo) !== Number(nuevo.id_insumo)) {
            await conexion.execute(
                "UPDATE insumos SET cantidad = ? WHERE id_insumo = ?",
                [stockBase, anterior.id_insumo]
            );
        }

        await conexion.execute(
            "UPDATE insumos SET cantidad = ? WHERE id_insumo = ?",
            [stockResultante, nuevo.id_insumo]
        );

        await conexion.execute(
            `UPDATE movimientos_insumos SET
                id_insumo = ?,
                id_empleado = ?,
                tipo_movimiento = ?,
                cantidad = ?,
                fecha = ?,
                motivo = ?
             WHERE id_movimiento = ?`,
            [
                nuevo.id_insumo,
                nuevo.id_empleado,
                nuevo.tipo_movimiento,
                nuevo.cantidad,
                nuevo.fecha,
                nuevo.motivo,
                req.params.id
            ]
        );

        await conexion.commit();

        res.status(200).json({
            mensaje: "Movimiento actualizado y stock recalculado correctamente",
            stock_actual: stockResultante
        });

    } catch (error) {
        if (conexion) await conexion.rollback();

        res.status(500).json({
            error: "No se pudo actualizar el movimiento",
            detalle: error.message
        });
    } finally {
        if (conexion) conexion.release();
    }
});

// ==========================
// ELIMINAR UN MOVIMIENTO
// Revierte su efecto sobre el stock antes de borrarlo.
// ==========================
router.delete("/:id", async (req, res) => {
    let conexion;

    try {
        conexion = await pool.getConnection();
        await conexion.beginTransaction();

        const [movimientos] = await conexion.execute(
            `SELECT *
             FROM movimientos_insumos
             WHERE id_movimiento = ?
             FOR UPDATE`,
            [req.params.id]
        );

        if (movimientos.length === 0) {
            await conexion.rollback();
            return res.status(404).json({
                error: "Movimiento no encontrado"
            });
        }

        const movimiento = movimientos[0];

        const [insumos] = await conexion.execute(
            `SELECT cantidad
             FROM insumos
             WHERE id_insumo = ?
             FOR UPDATE`,
            [movimiento.id_insumo]
        );

        if (insumos.length === 0) {
            await conexion.rollback();
            return res.status(404).json({
                error: "El insumo asociado ya no existe"
            });
        }

        const stockActual = Number(insumos[0].cantidad);
        const stockResultante =
            stockActual -
            impactoStock(
                movimiento.tipo_movimiento,
                movimiento.cantidad
            );

        if (stockResultante < 0) {
            await conexion.rollback();
            return res.status(400).json({
                error: "No se puede eliminar este movimiento porque dejaría el stock en negativo"
            });
        }

        await conexion.execute(
            "UPDATE insumos SET cantidad = ? WHERE id_insumo = ?",
            [stockResultante, movimiento.id_insumo]
        );

        await conexion.execute(
            "DELETE FROM movimientos_insumos WHERE id_movimiento = ?",
            [req.params.id]
        );

        await conexion.commit();

        res.status(200).json({
            mensaje: "Movimiento eliminado y stock actualizado correctamente",
            stock_actual: stockResultante
        });

    } catch (error) {
        if (conexion) await conexion.rollback();

        res.status(500).json({
            error: "No se pudo eliminar el movimiento",
            detalle: error.message
        });
    } finally {
        if (conexion) conexion.release();
    }
});

module.exports = router;
