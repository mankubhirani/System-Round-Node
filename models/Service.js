const connection = require('../config/db');

const Service = {
    create: (data, callback) => {
        const { category_id, name, type } = data;
        connection.query("INSERT INTO services (category_id, name, type) VALUES (?, ?, ?)", [category_id, name, type], callback);
    },
    findByCategory: (categoryId, callback) => {
        connection.query("SELECT * FROM services WHERE category_id = ?", [categoryId], callback);
    },
    update: (id, data, callback) => {
        const { name, type } = data;
        connection.query("UPDATE services SET name = ?, type = ? WHERE id = ?", [name, type, id], callback);
    },
    delete: (id, callback) => {
        connection.query("DELETE FROM services WHERE id = ?", [id], callback);
    }
};

module.exports = Service;
