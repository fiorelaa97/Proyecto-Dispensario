const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// Agregar un empleado
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

        return res.status(201).json({
            mensaje: "Empleado agregado correctamente"
        });

    } catch (error) {
        return res.status(500).json({
            error: "No se pudo agregar el empleado",
            detalle: error.message
        });
    }
});

module.exports = router;