const express = require("express");
const pool = require("./bd/conexion")
const empleadosRouter = require("./rutas/empleados")
const loginRouter = require("./rutas/login")
const insumosRouter = require("./rutas/insumos")
const movimientoinsumosRouter = require("./rutas/movimientoInsumos")

const app=express();
const PORT =3000;

app.use(express.json());

app.use("/api/empleados", empleadosRouter);
app.use("/api/login", loginRouter)
app.use("/api/insumos", insumosRouter)
app.use("/api/movimientoinsumos", movimientoinsumosRouter)

async function probarConexion(){
    try {
        await pool.query("SELECT 1");
        console.log("Conexion exitosa")
    } catch (error) {
        console.log("Error en la conexión")
        console.log(error.menssage)
        
    }
}
app.listen(PORT, async() => {
    console.log(`servidor ejecutandose en http://localhost:${PORT}`)
    await probarConexion()
})