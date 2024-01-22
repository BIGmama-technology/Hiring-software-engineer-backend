const schedule = require("node-schedule");

function listScheduledJobs() {
    const scheduledJobs = schedule.scheduledJobs;
    const jobsArray = [];

    console.log('List of scheduled jobs:');
    for (const jobName in scheduledJobs) {
        const job = scheduledJobs[jobName];
        const jobInfo = {
            name: jobName,
            nextRun: job.nextInvocation(),
        };

        jobsArray.push(jobInfo);

        console.log(`${jobName}: next run at ${jobInfo.nextRun}, cron expression: ${jobInfo.cronExpression}`);
    }

    return jobsArray;
}

module.exports = {listScheduledJobs}