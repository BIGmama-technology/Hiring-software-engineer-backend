const express = require('express');
const schedule = require('node-schedule');
const bodyParser = require('body-parser');
const {executeScriptBasedOnType} = require("./docker-helpers");
const {authenticateUser} = require("./middleware");
const multer = require('multer');
const fs = require('fs');
const {listScheduledJobs} = require("./schedule-helpers");

const upload = multer({dest: 'uploads/'})

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.post("/execute", upload.fields([{name: 'script', maxCount: 1}, {name: 'requirements', maxCount: 1}]), authenticateUser, async (req, res) => {
    const scriptFile = req.files['script'] ? req.files['script'][0].path || "" : "";
    const requirementsFile = req.files['requirements'] ? req.files['requirements'][0].path || "" : "";
    const cronExpression = req.body.cronExpression || '';
    const title = req.body.title || '';
    const scriptType = req.body.scriptType || '';

    if(scriptType === '' || scriptFile === '' || (cronExpression !== "" && title === "")){
        res.status(400).json("missing required parameters");
    }

    if(cronExpression === ''){
        executeScriptBasedOnType(scriptType, scriptFile, requirementsFile)
            .then(() => {
                res.json("executed script");
            })
    }else{
        executeScriptBasedOnType(scriptType, scriptFile, requirementsFile)
            .then(() => {
                schedule.scheduleJob(title, cronExpression, async () => {
                    try {
                        await executeScriptBasedOnType(scriptType, scriptFile, requirementsFile)
                    } catch (error) {
                        console.error('Error executing scheduled task:', error);
                    }
                });
                res.json("executed script");
            })
    }

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



app.get('/jobs', (req, res) => {
    try{
        const scheduledJobsJSON = listScheduledJobs();
        res.status(200).json(scheduledJobsJSON);
    }
    catch(error){
        console.log(error);
        console.error('Error executing scheduled task:', error);
    }
})


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

module.exports = app;

