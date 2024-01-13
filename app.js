const express = require('express');
const schedule = require('node-schedule');
const bodyParser = require('body-parser');
const {runPythonScript,  runShellScript} = require("./docker-helpers");
const {authenticateUser} = require("./middleware");
const multer = require('multer');
const fs = require('fs');

const upload = multer({dest: 'uploads/'})

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


app.post('/execute-script', upload.single('script'), authenticateUser, async (req, res) => {
    const scriptFile = req.file.path;

    runShellScript(scriptFile)
        .then(() => {
            res.json("executed shell script");
        })
});

app.post('/execute-python-script', upload.fields([{name: 'script', maxCount: 1}, {name: 'requirements', maxCount: 1}]), authenticateUser, async (req, res) => {
    const scriptFile = req.files['script'][0].path;
    const requirementsFile = req.files['requirements'][0].path;


    runPythonScript(scriptFile, requirementsFile)
        .then(() => {
            res.json("executed python script");
        })

});

app.post('/schedule-python-script', upload.fields([{name: 'script', maxCount: 1}, {name: 'requirements', maxCount: 1}]), authenticateUser, async (req, res) => {
    const cronExpression = req.body.cronExpression || '0 0 * * *';
    const scriptFile = req.files['script'][0].path;
    const requirementsFile = req.files['requirements'][0].path;

    runPythonScript(scriptFile, requirementsFile)
        .then(() => {
            schedule.scheduleJob(cronExpression, async () => {
                try {
                    await runPythonScript(scriptFile, requirementsFile)
                } catch (error) {
                    console.error('Error executing scheduled task:', error);
                }
            });
            res.json("executed python script");
        })
});

app.get('/logs', (req, res) => {
    fs.readFile('logs.txt', 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        } else {
            res.send(data);
        }
    });
});


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

module.exports = app;

