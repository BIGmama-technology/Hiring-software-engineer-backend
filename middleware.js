const fs = require('fs');
const authenticateUser = (req, res, next) => {
    const { username, password } = req.body;

    const users = JSON.parse(fs.readFileSync('users.json', 'utf8'));

    const isValidUser = users.some(user => user.username === username && user.password === password);

    if (isValidUser) {
        next();
    } else {
        res.status(401).json({ message: 'Not authorized' });
    }
};

module.exports = { authenticateUser};