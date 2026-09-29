const mysql = require ("mysql2/promise");

const pool = mysql.createPool({
    host: "localhost",
    port: 3306,
    user: "root",pç
    password: "1234",
    database: "dispensario_bd"


})

module.exports = pool;