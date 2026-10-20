const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();



// ==================================================
// LISTAR ESTADOS
// GET /api/empleados/listas/estados
// ==================================================
router.get("/listas/estados", async (req, res) => {
    try {
        const [estados] = await pool.execute(
            `SELECT id_estado, nombre_estado
             FROM estados
             ORDER BY nombre_estado`
        );

        res.status(200).json(estados);
    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los estados",
            detalle: error.message
        });
    }
});

// ==================================================
// AGREGAR EMPLEADO
// POST /api/empleados
// ==================================================
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
        const [resultado] = await pool.execute(
            `INSERT INTO empleados
            (nombre, apellido, dni, telefono, cargo,
             fecha_ingreso, estado)
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
            mensaje: "Empleado agregado correctamente",
            id_empleado: resultado.insertId
        });
    } catch (error) {
        res.status(500).json({
            error: "No se pudo agregar el empleado",
            detalle: error.message
        });
    }
});

// ==================================================
// LISTAR TODOS LOS EMPLEADOS CON NOMBRES
// GET /api/empleados
// ==================================================
router.get("/", async (req, res) => {
    try {
       const [empleados] = await pool.execute(
    `SELECT
        id_empleado,
        nombre,
        apellido,
        dni,
        telefono,
        fecha_ingreso,
        cargo,
        estado
     FROM empleados
     ORDER BY id_empleado DESC`
);

        res.status(200).json(empleados);
    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los empleados",
            detalle: error.message
        });
    }
});

// ==================================================
// LISTAR UN EMPLEADO POR ID CON NOMBRES
// GET /api/empleados/:id
// ==================================================
router.get("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [empleados] = await pool.execute(
            `SELECT
                e.id_empleado,
                e.nombre,
                e.apellido,
                e.dni,
                e.telefono,
                c.nombre_cargo AS cargo,
                e.fecha_ingreso,
                es.nombre_estado AS estado
             FROM empleados e
             LEFT JOIN cargos c
                ON e.cargo = c.id_cargo
             LEFT JOIN estados es
                ON e.estado = es.id_estado
             WHERE e.id_empleado = ?`,
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

// ==================================================
// MODIFICAR EMPLEADO
// PUT /api/empleados/:id
// ==================================================
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
             WHERE id_empleado = ?`,
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
            const [existe] = await pool.execute(
                "SELECT id_empleado FROM empleados WHERE id_empleado = ?",
                [id]
            );

            if (existe.length === 0) {
                return res.status(404).json({
                    error: "Empleado no encontrado"
                });
            }
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

// ==================================================
// ELIMINAR EMPLEADO
// DELETE /api/empleados/:id
// ==================================================
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM empleados WHERE id_empleado = ?",
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