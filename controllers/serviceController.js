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
