
const express = require("express");
const router = express.Router();

const pool = require("../bd/conexion");

// =====================================
// REPORTE DE EMPLEADOS
// =====================================
router.get("/empleados", async (req, res) => {
    try {
        const [resultados] = await pool.query(`
            SELECT *
            FROM empleados
            ORDER BY apellido ASC
        `);

        res.json({
            total: resultados.length,
            empleados: resultados
        });

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});


// =====================================
// REPORTE DE INSUMOS
// =====================================
router.get("/insumos", async (req, res) => {
    try {
        const [resultados] = await pool.query(`
            SELECT *
            FROM insumos
            ORDER BY nombre ASC
        `);

        res.json({
            total: resultados.length,
            insumos: resultados
        });

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});


// =====================================
// REPORTE GENERAL DE MOVIMIENTOS
// =====================================
router.get("/movimientos", async (req, res) => {
    try {
        const { desde, hasta, tipo } = req.query;

        let sql = `
            SELECT
                m.id_movimiento,
                m.fecha,
                m.tipo_movimiento,
                i.nombre AS insumo,
                i.categoria,
                m.cantidad,
                e.nombre AS nombre_empleado,
                e.apellido AS apellido_empleado,
                m.motivo
            FROM movimientos_insumos m
            INNER JOIN insumos i
                ON m.id_insumo = i.id_insumo
            LEFT JOIN empleados e
                ON m.id_empleado = e.id_empleado
            WHERE 1 = 1
        `;

        const parametros = [];

        if (desde) {
            sql += " AND m.fecha >= ?";
            parametros.push(desde);
        }

        if (hasta) {
            sql += " AND m.fecha <= ?";
            parametros.push(hasta);
        }

        if (tipo) {
            sql += " AND LOWER(m.tipo_movimiento) = LOWER(?)";
            parametros.push(tipo);
        }

        sql += " ORDER BY m.fecha DESC, m.id_movimiento DESC";

        const [resultados] = await pool.query(sql, parametros);

        res.json({
            total: resultados.length,
            movimientos: resultados
        });

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});


// =====================================
// REPORTE DE ENTRADAS
// =====================================
router.get("/entradas", async (req, res) => {
    try {
        const [resultados] = await pool.query(`
            SELECT
                m.id_movimiento,
                m.fecha,
                i.nombre AS insumo,
                m.cantidad,
                e.nombre AS empleado,
                m.motivo
            FROM movimientos_insumos m
            INNER JOIN insumos i
                ON m.id_insumo = i.id_insumo
            LEFT JOIN empleados e
                ON m.id_empleado = e.id_empleado
            WHERE LOWER(m.tipo_movimiento) = 'entrada'
            ORDER BY m.fecha DESC
        `);

        res.json({
            total: resultados.length,
            entradas: resultados
        });

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});


// =====================================
// REPORTE DE SALIDAS
// =====================================
router.get("/salidas", async (req, res) => {
    try {
        const [resultados] = await pool.query(`
            SELECT
                m.id_movimiento,
                m.fecha,
                i.nombre AS insumo,
                m.cantidad,
                e.nombre AS empleado,
                m.motivo
            FROM movimientos_insumos m
            INNER JOIN insumos i
                ON m.id_insumo = i.id_insumo
            LEFT JOIN empleados e
                ON m.id_empleado = e.id_empleado
            WHERE LOWER(m.tipo_movimiento) = 'salida'
            ORDER BY m.fecha DESC
        `);

        res.json({
            total: resultados.length,
            salidas: resultados
        });

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});


// =====================================
// RESUMEN DE MOVIMIENTOS
// =====================================
router.get("/resumen", async (req, res) => {
    try {
        const { desde, hasta } = req.query;

        let sql = `
            SELECT
                COUNT(*) AS total_movimientos,

                COALESCE(SUM(
                    CASE
                        WHEN LOWER(tipo_movimiento) = 'entrada'
                        THEN cantidad ELSE 0
                    END
                ), 0) AS total_entradas,

                COALESCE(SUM(
                    CASE
                        WHEN LOWER(tipo_movimiento) = 'salida'
                        THEN cantidad ELSE 0
                    END
                ), 0) AS total_salidas

            FROM movimientos_insumos
            WHERE 1 = 1
        `;

        const parametros = [];

        if (desde) {
            sql += " AND fecha >= ?";
            parametros.push(desde);
        }

        if (hasta) {
            sql += " AND fecha <= ?";
            parametros.push(hasta);
        }

        const [resultados] = await pool.query(sql, parametros);

        res.json(resultados[0]);

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});


// =====================================
// VISTA PREVIA DEL REPORTE
// =====================================
router.get("/vista-previa", async (req, res) => {
    try {
        const [resultados] = await pool.query(`
            SELECT
                m.fecha,
                m.tipo_movimiento,
                i.nombre AS descripcion,
                m.cantidad,
                COALESCE(
                    CONCAT(e.nombre, ' ', e.apellido),
                    'Sin empleado'
                ) AS usuario
            FROM movimientos_insumos m
            INNER JOIN insumos i
                ON m.id_insumo = i.id_insumo
            LEFT JOIN empleados e
                ON m.id_empleado = e.id_empleado
            ORDER BY m.fecha DESC, m.id_movimiento DESC
            LIMIT 10
        `);

        res.json(resultados);

    } catch (error) {
        res.status(500).json({ mensaje: error.message });
    }
});

module.exports = router;
