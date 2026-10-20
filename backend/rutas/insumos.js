const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// ==================================================
// VALIDAR Y CONVERTIR FECHAS
// Acepta DD/MM/AAAA o AAAA-MM-DD
// Devuelve AAAA-MM-DD para MySQL
// ==================================================
function convertirFecha(fecha) {
    if (!fecha || typeof fecha !== "string") {
        return null;
    }

    fecha = fecha.trim();

    let anio, mes, dia;

    if (/^\d{2}\/\d{2}\/\d{4}$/.test(fecha)) {
        // Formato DD/MM/AAAA
        [dia, mes, anio] = fecha.split("/");
    } else if (/^\d{4}-\d{2}-\d{2}$/.test(fecha)) {
        // Formato AAAA-MM-DD
        [anio, mes, dia] = fecha.split("-");
    } else {
        return null;
    }

    const fechaObjeto = new Date(
        Number(anio),
        Number(mes) - 1,
        Number(dia)
    );

    // Evitar fechas inexistentes, como 31/02/2026
    if (
        fechaObjeto.getFullYear() !== Number(anio) ||
        fechaObjeto.getMonth() !== Number(mes) - 1 ||
        fechaObjeto.getDate() !== Number(dia)
    ) {
        return null;
    }

    return `${anio}-${mes}-${dia}`;
}

// ==================================================
// AGREGAR UN INSUMO
// ==================================================
router.post("/", async (req, res) => {
    const {
        nombre,
        categoria,
        cantidad,
        stock_minimo,
        fecha_vencimiento,
        estado
    } = req.body;

    if (
        !nombre ||
        !categoria ||
        cantidad === undefined ||
        stock_minimo === undefined ||
        !fecha_vencimiento ||
        !estado
    ) {
        return res.status(400).json({
            error: "Faltan datos obligatorios."
        });
    }

    const fechaSQL = convertirFecha(fecha_vencimiento);

    if (!fechaSQL) {
        return res.status(400).json({
            error: "Fecha de vencimiento incorrecta.",
            detalle: "Ingresá una fecha válida en formato DD/MM/AAAA o AAAA-MM-DD."
        });
    }

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO insumos
            (nombre, categoria, cantidad, stock_minimo,
             fecha_vencimiento, estado)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [
                nombre,
                categoria,
                cantidad,
                stock_minimo,
                fechaSQL,
                estado
            ]
        );

        return res.status(201).json({
            mensaje: "Insumo agregado correctamente.",
            id_insumo: resultado.insertId
        });

    } catch (error) {
        console.error("Error al agregar insumo:", error);

        return res.status(500).json({
            error: "No se pudo agregar el insumo.",
            detalle: error.message
        });
    }
});

// ==================================================
// LEER TODOS LOS INSUMOS
// ==================================================
router.get("/", async (req, res) => {
    try {
        const [insumos] = await pool.execute(
            "SELECT * FROM insumos"
        );

        return res.status(200).json(insumos);

    } catch (error) {
        console.error("Error al obtener insumos:", error);

        return res.status(500).json({
            error: "No se pudieron obtener los insumos."
        });
    }
});

// ==================================================
// LEER UN INSUMO POR ID
// ==================================================
router.get("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [insumos] = await pool.execute(
            "SELECT * FROM insumos WHERE id_insumo = ?",
            [id]
        );

        if (insumos.length === 0) {
            return res.status(404).json({
                error: "Insumo no encontrado."
            });
        }

        return res.status(200).json(insumos[0]);

    } catch (error) {
        console.error("Error al consultar insumo:", error);

        return res.status(500).json({
            error: "No se pudo obtener el insumo."
        });
    }
});

// ==================================================
// MODIFICAR UN INSUMO
// ==================================================
router.put("/:id", async (req, res) => {
    const { id } = req.params;

    const {
        nombre,
        categoria,
        cantidad,
        stock_minimo,
        fecha_vencimiento,
        estado
    } = req.body;

    if (
        !nombre ||
        !categoria ||
        cantidad === undefined ||
        stock_minimo === undefined ||
        !fecha_vencimiento ||
        !estado
    ) {
        return res.status(400).json({
            error: "Faltan datos obligatorios."
        });
    }

    const fechaSQL = convertirFecha(fecha_vencimiento);

    if (!fechaSQL) {
        return res.status(400).json({
            error: "Fecha de vencimiento incorrecta.",
            detalle: "Ingresá una fecha válida en formato DD/MM/AAAA o AAAA-MM-DD."
        });
    }

    try {
        const [resultado] = await pool.execute(
            `UPDATE insumos SET
                nombre = ?,
                categoria = ?,
                cantidad = ?,
                stock_minimo = ?,
                fecha_vencimiento = ?,
                estado = ?
            WHERE id_insumo = ?`,
            [
                nombre,
                categoria,
                cantidad,
                stock_minimo,
                fechaSQL,
                estado,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Insumo no encontrado o sin cambios."
            });
        }

        return res.status(200).json({
            mensaje: "Insumo actualizado correctamente."
        });

    } catch (error) {
        console.error("Error al modificar insumo:", error);

        return res.status(500).json({
            error: "No se pudo actualizar el insumo.",
            detalle: error.message
        });
    }
});

// ==================================================
// ELIMINAR UN INSUMO
// ==================================================
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM insumos WHERE id_insumo = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Insumo no encontrado."
            });
        }

        return res.status(200).json({
            mensaje: "Insumo eliminado correctamente."
        });

    } catch (error) {
        console.error("Error al eliminar insumo:", error);

        return res.status(500).json({
            error: "No se pudo eliminar el insumo.",
            detalle: error.message
        });
    }
});

module.exports = router;
