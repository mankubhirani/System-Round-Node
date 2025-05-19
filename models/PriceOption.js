const connection = require('../config/db');

const PriceOption = {
    add: (service_id, duration, price, type, callback) => {
        connection.query("INSERT INTO price_options (service_id, duration, price, type) VALUES (?, ?, ?, ?)", [service_id, duration, price, type], callback);
    },
    deleteAllByService: (serviceId, callback) => {
        connection.query("DELETE FROM price_options WHERE service_id = ?", [serviceId], callback);
    }
};

module.exports = PriceOption;
