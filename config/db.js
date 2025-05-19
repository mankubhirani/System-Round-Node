const mysql = require('mysql2');
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'codes for tomorrow'
});
connection.connect(err => {
    if (err) throw err;
    console.log('MySQL connected.');
});
module.exports = connection;
