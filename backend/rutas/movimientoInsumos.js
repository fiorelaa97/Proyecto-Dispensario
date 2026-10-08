const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// ==========================
// AGREGAR UN MOVIMIENTO
// ==========================
router.post("/", async (req, res) => {
    const {
        id_insumo,
        id_empleado,
        tipo_movimiento,
        cantidad,
        fecha,
        motivo
    } = req.body;

    try {
        await pool.execute(
            `INSERT INTO movimientos_insumos
            (id_insumo, id_empleado, tipo_movimiento, cantidad, fecha, motivo)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [
                id_insumo,
                id_empleado,
                tipo_movimiento,
                cantidad,
                fecha,
                motivo
            ]
        );

        res.status(201).json({
            mensaje: "Movimiento de insumo agregado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo agregar el movimiento de insumo",
            detalle: error.message
        });
    }
});


// ==========================
// LEER TODOS LOS MOVIMIENTOS
// ==========================
router.get("/", async (req, res) => {
    try {
        const [movimientos] = await pool.execute(
            "SELECT * FROM movimientos_insumos"
        );

        res.status(200).json(movimientos);

    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los movimientos de insumos",
            detalle: error.message
        });
    }
});


// ==========================
// LEER UN MOVIMIENTO POR ID
// ==========================
router.get("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [movimientos] = await pool.execute(
            "SELECT * FROM movimientos_insumos WHERE id_movimiento = ?",
            [id]
        );

        if (movimientos.length === 0) {
            return res.status(404).json({
                error: "Movimiento de insumo no encontrado"
            });
        }

        res.status(200).json(movimientos[0]);

    } catch (error) {
        res.status(500).json({
            error: "No se pudo obtener el movimiento de insumo",
            detalle: error.message
        });
    }
});


// ==========================
// EDITAR UN MOVIMIENTO
// ==========================
router.put("/:id", async (req, res) => {
    const { id } = req.params;

    const {
        id_insumo,
        id_empleado,
        tipo_movimiento,
        cantidad,
        fecha,
        motivo
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE movimientos_insumos SET
                id_insumo = ?,
                id_empleado = ?,
                tipo_movimiento = ?,
                cantidad = ?,
                fecha = ?,
                motivo = ?
            WHERE id_movimiento = ?`,
            [
                id_insumo,
                id_empleado,
                tipo_movimiento,
                cantidad,
                fecha,
                motivo,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Movimiento de insumo no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Movimiento de insumo actualizado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo actualizar el movimiento de insumo",
            detalle: error.message
        });
    }
});


// ==========================
// ELIMINAR UN MOVIMIENTO
// ==========================
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM movimientos_insumos WHERE id_movimiento = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Movimiento de insumo no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Movimiento de insumo eliminado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo eliminar el movimiento de insumo",
            detalle: error.message
        });
    }
});


module.exports = router;