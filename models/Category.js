const connection = require('../config/db');

const Category = {
    create: (name, callback) => {
        connection.query("INSERT INTO categories (name) VALUES (?)", [name], callback);
    },
    findAll: (callback) => {
        connection.query("SELECT * FROM categories", callback);
    },
    update: (id, name, callback) => {
        connection.query("UPDATE categories SET name = ? WHERE id = ?", [name, id], callback);
    },
    deleteIfEmpty: (id, callback) => {
        connection.query("SELECT * FROM services WHERE category_id = ?", [id], (err, results) => {
            if (results.length === 0) {
                connection.query("DELETE FROM categories WHERE id = ?", [id], callback);
            } else {
                callback(null, { message: "Category not empty" });
            }
        });
    }
};

module.exports = Category;
