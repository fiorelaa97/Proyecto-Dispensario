const express = require("express")

const app=express();
const PORT =3000;

app.use(express.jsonqq());

app.listen(PORT, async() => {
    console.log('servidor ejecutandose en http://localhost:${PORT')
})