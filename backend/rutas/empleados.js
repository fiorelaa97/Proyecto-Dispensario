const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// ==========================
// AGREGAR UN EMPLEADO
// ==========================
router.post("/", async (req, res) => {
    const {
        nombre,
        apellido,
        dni,
        telefono,
        cargo,
        fecha_ingreso,
        estado
    } = req.body;

    try {
        await pool.execute(
            `INSERT INTO empleados
            (nombre, apellido, dni, telefono, cargo, fecha_ingreso, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [
                nombre,
                apellido,
                dni,
                telefono,
                cargo,
                fecha_ingreso,
                estado
            ]
        );

        res.status(201).json({
            mensaje: "Empleado agregado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo agregar el empleado",
            detalle: error.message
        });
    }
});


// ==========================
// LEER TODOS LOS EMPLEADOS
// ==========================
router.get("/", async (req, res) => {
    try {
        const [empleados] = await pool.execute(
            "SELECT * FROM empleados"
        );

        res.status(200).json(empleados);

    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los empleados",
            detalle: error.message
        });
    }
});


// ==========================
// LEER UN EMPLEADO POR ID
// ==========================
router.get("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [empleados] = await pool.execute(
            "SELECT * FROM empleados WHERE id = ?",
            [id]
        );

        if (empleados.length === 0) {
            return res.status(404).json({
                error: "Empleado no encontrado"
            });
        }

        res.status(200).json(empleados[0]);

    } catch (error) {
        res.status(500).json({
            error: "No se pudo obtener el empleado",
            detalle: error.message
        });
    }
});


// ==========================
// EDITAR UN EMPLEADO
// ==========================
router.put("/:id", async (req, res) => {
    const { id } = req.params;

    const {
        nombre,
        apellido,
        dni,
        telefono,
        cargo,
        fecha_ingreso,
        estado
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE empleados SET
                nombre = ?,
                apellido = ?,
                dni = ?,
                telefono = ?,
                cargo = ?,
                fecha_ingreso = ?,
                estado = ?
            WHERE id = ?`,
            [
                nombre,
                apellido,
                dni,
                telefono,
                cargo,
                fecha_ingreso,
                estado,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Empleado no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Empleado actualizado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo actualizar el empleado",
            detalle: error.message
        });
    }
});


// ==========================
// ELIMINAR UN EMPLEADO
// ==========================
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM empleados WHERE id = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Empleado no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Empleado eliminado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo eliminar el empleado",
            detalle: error.message
        });
    }
});


module.exports = router;