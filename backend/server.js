const express = require("express");
const pool = require("./bd/conexion")

const app=express();
const PORT =3000;

app.use(express.json());
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