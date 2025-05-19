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
