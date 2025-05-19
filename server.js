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
