const connection = require('../config/db');
const bcrypt = require('bcrypt');

const User = {
    findByEmail: (email, callback) => {
        connection.query("SELECT * FROM users WHERE email = ?", [email], callback);
    },
    verifyPassword: (password, hash) => {
        return bcrypt.compareSync(password, hash);
    }
};

module.exports = User;
