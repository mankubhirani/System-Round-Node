import os

# Project folder structure
folders = [
    "config",
    "controllers",
    "models",
    "routes",
    "middleware"
]

# File templates
files = {
    "config/db.js": """\
const mysql = require('mysql2');
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'your_database_name'
});
connection.connect(err => {
    if (err) throw err;
    console.log('MySQL connected.');
});
module.exports = connection;
""",
    "models/User.js": """\
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
""",
    "models/Category.js": """\
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
""",
    "models/Service.js": """\
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
""",
    "models/PriceOption.js": """\
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
""",
    "controllers/authController.js": """\
const jwt = require('jsonwebtoken');
const User = require('../models/User');

exports.login = (req, res) => {
    const { email, password } = req.body;
    if (email !== 'admin@codesfortomorrow.com' || password !== 'Admin123!@#') {
        return res.status(401).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign({ email }, 'your_secret_key', { expiresIn: '1h' });
    res.json({ token });
};
""",
    "controllers/categoryController.js": """\
const Category = require('../models/Category');

exports.create = (req, res) => {
    Category.create(req.body.name, (err, result) => {
        if (err) return res.status(500).send(err);
        res.json({ id: result.insertId, name: req.body.name });
    });
};

exports.getAll = (req, res) => {
    Category.findAll((err, rows) => {
        if (err) return res.status(500).send(err);
        res.json(rows);
    });
};

exports.update = (req, res) => {
    Category.update(req.params.categoryId, req.body.name, (err) => {
        if (err) return res.status(500).send(err);
        res.send({ message: "Updated" });
    });
};

exports.deleteIfEmpty = (req, res) => {
    Category.deleteIfEmpty(req.params.categoryId, (err, result) => {
        if (err) return res.status(500).send(err);
        res.send(result);
    });
};
""",
    "controllers/serviceController.js": """\
const Service = require('../models/Service');
const PriceOption = require('../models/PriceOption');

exports.create = (req, res) => {
    const data = {
        category_id: req.params.categoryId,
        name: req.body.name,
        type: req.body.type
    };
    Service.create(data, (err, result) => {
        if (err) return res.status(500).send(err);
        const serviceId = result.insertId;
        const priceOptions = req.body.priceOptions;

        priceOptions.forEach(option => {
            PriceOption.add(serviceId, option.duration, option.price, option.type, () => {});
        });

        res.send({ serviceId });
    });
};

exports.getAll = (req, res) => {
    Service.findByCategory(req.params.categoryId, (err, rows) => {
        if (err) return res.status(500).send(err);
        res.json(rows);
    });
};

exports.update = (req, res) => {
    const serviceId = req.params.serviceId;
    const data = {
        name: req.body.name,
        type: req.body.type
    };
    Service.update(serviceId, data, (err) => {
        if (err) return res.status(500).send(err);
        PriceOption.deleteAllByService(serviceId, () => {
            req.body.priceOptions.forEach(option => {
                PriceOption.add(serviceId, option.duration, option.price, option.type, () => {});
            });
            res.send({ message: "Updated" });
        });
    });
};

exports.delete = (req, res) => {
    Service.delete(req.params.serviceId, (err) => {
        if (err) return res.status(500).send(err);
        res.send({ message: "Deleted" });
    });
};
""",
    "routes/authRoutes.js": """\
const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

router.post('/login', authController.login);

module.exports = router;
""",
    "routes/categoryRoutes.js": """\
const express = require('express');
const router = express.Router();
const categoryController = require('../controllers/categoryController');
const serviceController = require('../controllers/serviceController');
const verifyToken = require('../middleware/auth');

router.post('/category', verifyToken, categoryController.create);
router.get('/categories', verifyToken, categoryController.getAll);
router.put('/category/:categoryId', verifyToken, categoryController.update);
router.delete('/category/:categoryId', verifyToken, categoryController.deleteIfEmpty);

router.post('/category/:categoryId/service', verifyToken, serviceController.create);
router.get('/category/:categoryId/services', verifyToken, serviceController.getAll);
router.put('/category/:categoryId/service/:serviceId', verifyToken, serviceController.update);
router.delete('/category/:categoryId/service/:serviceId', verifyToken, serviceController.delete);

module.exports = router;
""",
    "middleware/auth.js": """\
const jwt = require('jsonwebtoken');

module.exports = function(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) return res.status(403).send({ message: 'No token provided.' });

    jwt.verify(token, 'your_secret_key', (err, decoded) => {
        if (err) return res.status(500).send({ message: 'Failed to authenticate token.' });
        req.user = decoded;
        next();
    });
};
""",
    "server.js": """\
const express = require('express');
const bodyParser = require('body-parser');
const authRoutes = require('./routes/authRoutes');
const categoryRoutes = require('./routes/categoryRoutes');

const app = express();
app.use(bodyParser.json());

app.use('/api', authRoutes);
app.use('/api', categoryRoutes);

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
""",
    "package.json": """\
{
  "name": "category-service-api",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "bcrypt": "^5.0.1",
    "body-parser": "^1.20.0",
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.0",
    "mysql2": "^3.2.0"
  }
}
"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Write files
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ Project structure and JS files generated successfully.")
