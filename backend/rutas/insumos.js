const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// ==========================
// AGREGAR UN INSUMO
// ==========================
router.post("/", async (req, res) => {
    const {
        nombre,
        categoria,
        cantidad,
        stock_minimo,
        fecha_vencimiento,
        estado
    } = req.body;

    try {
        await pool.execute(
            `INSERT INTO insumos
            (nombre, categoria, cantidad, stock_minimo, fecha_vencimiento, estado)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [
                nombre,
                categoria,
                cantidad,
                stock_minimo,
                fecha_vencimiento,
                estado
            ]
        );

        res.status(201).json({
            mensaje: "Insumo agregado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo agregar el insumo",
            detalle: error.message
        });
    }
});


// ==========================
// LEER TODOS LOS INSUMOS
// ==========================
router.get("/", async (req, res) => {
    try {
        const [insumos] = await pool.execute(
            "SELECT * FROM insumos"
        );

        res.status(200).json(insumos);

    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los insumos",
            detalle: error.message
        });
    }
});


// ==========================
// LEER UN INSUMO POR ID
// ==========================
router.get("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [insumos] = await pool.execute(
            "SELECT * FROM insumos WHERE id_insumo = ?",
            [id]
        );

        if (insumos.length === 0) {
            return res.status(404).json({
                error: "Insumo no encontrado"
            });
        }

        res.status(200).json(insumos[0]);

    } catch (error) {
        res.status(500).json({
            error: "No se pudo obtener el insumo",
            detalle: error.message
        });
    }
});


// ==========================
// EDITAR UN INSUMO
// ==========================
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
                fecha_vencimiento,
                estado,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Insumo no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Insumo actualizado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo actualizar el insumo",
            detalle: error.message
        });
    }
});


// ==========================
// ELIMINAR UN INSUMO
// ==========================
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM insumos WHERE id_insumo = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Insumo no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Insumo eliminado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo eliminar el insumo",
            detalle: error.message
        });
    }
});


module.exports = router;