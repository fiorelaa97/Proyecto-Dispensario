const express = require 
("express");
const pool = require("../bd/conexion");

const router = express.
router();

//Agregar un empleado
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
});

