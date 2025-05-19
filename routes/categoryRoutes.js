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
