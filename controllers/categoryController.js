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
