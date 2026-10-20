
const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// ==========================
// AGREGAR UN USUARIO
// ==========================
router.post("/", async (req, res) => {
    const {
        nombre_usuario,
        contrasena,
        rol,
        id_empleado
    } = req.body;

    try {
        await pool.execute(
            `INSERT INTO usuario
            (nombre_usuario, contrasena, rol, id_empleado)
            VALUES (?, ?, ?, ?)`,
            [
                nombre_usuario,
                contrasena,
                rol,
                id_empleado || null
            ]
        );

        res.status(201).json({
            mensaje: "Usuario agregado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo agregar el usuario",
            detalle: error.message
        });
    }
});


// ==========================
// LISTAR TODOS LOS USUARIOS
// ==========================
router.get("/", async (req, res) => {
    try {
        const [usuarios] = await pool.execute(
            `SELECT id_usuario, nombre_usuario, rol, id_empleado
             FROM usuario`
        );

        res.status(200).json(usuarios);

    } catch (error) {
        res.status(500).json({
            error: "No se pudieron obtener los usuarios",
            detalle: error.message
        });
    }
});


// ==========================
// LEER UN USUARIO POR ID
// ==========================
router.get("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [usuarios] = await pool.execute(
            `SELECT id_usuario, nombre_usuario, rol, id_empleado
             FROM usuario
             WHERE id_usuario = ?`,
            [id]
        );

        if (usuarios.length === 0) {
            return res.status(404).json({
                error: "Usuario no encontrado"
            });
        }

        res.status(200).json(usuarios[0]);

    } catch (error) {
        res.status(500).json({
            error: "No se pudo obtener el usuario",
            detalle: error.message
        });
    }
});


// ==========================
// EDITAR UN USUARIO
// ==========================
router.put("/:id", async (req, res) => {
    const { id } = req.params;

    const {
        nombre_usuario,
        contrasena,
        rol,
        id_empleado
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE usuario SET
                nombre_usuario = ?,
                contrasena = ?,
                rol = ?,
                id_empleado = ?
             WHERE id_usuario = ?`,
            [
                nombre_usuario,
                contrasena,
                rol,
                id_empleado || null,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Usuario no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Usuario actualizado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo actualizar el usuario",
            detalle: error.message
        });
    }
});


// ==========================
// ELIMINAR UN USUARIO
// ==========================
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM usuario WHERE id_usuario = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Usuario no encontrado"
            });
        }

        res.status(200).json({
            mensaje: "Usuario eliminado correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo eliminar el usuario",
            detalle: error.message
        });
    }
});

module.exports = router;
