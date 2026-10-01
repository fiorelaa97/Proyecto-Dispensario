const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

router.post("/login", async (req, res) => {

    const { nombre_usuario, contrasena } = req.body;

    if (!nombre_usuario || !contrasena) {
        return res.status(400).json({
            error: "Debe ingresar usuario y contraseña"
        });
    }

    try {

        const [usuarios] = await pool.query(
            `SELECT * 
             FROM usuario 
             WHERE nombre_usuario = ?`,
            [nombre_usuario]
        );

        if (usuarios.length == 0) {
            return res.status(401).json({
                error: "Usuario o contraseña incorrectos"
            });
        }

        const usuario = usuarios[0];

        if (usuario.contrasena != contrasena) {
            return res.status(401).json({
                error: "Usuario o contraseña incorrectos"
            });
        }

        res.json({
            mensaje: "Inicio de sesión correcto",
            id_usuario: usuario.id_usuario,
            nombre_usuario: usuario.nombre_usuario,
            rol: usuario.rol,
            id_empleado: usuario.id_empleado
        });

    } catch (error) {

        console.log(error);

        res.status(500).json({
            error: "Error al validar el usuario"
        });
    }

});

module.exports = router;
