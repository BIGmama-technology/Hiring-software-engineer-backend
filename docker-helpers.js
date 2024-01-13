const Docker = require('dockerode');
const fs = require('fs');

const docker = new Docker();

const imageName = 'python:3.9-alpine';
const pythonFilePath = 'app/run.py';
const shellFilePath = 'app/run.sh';

const runPythonScript = async (localPythonFilePath, requirementsFilePath) => {
    const container = await docker.createContainer({
        Image: imageName,
        Tty: true,
        Cmd: ['tail', '-f', '/dev/null'],
        HostConfig: {
            AutoRemove: true,
        },
    });

    await container.start();

    const requirementsFile = fs.readFileSync(requirementsFilePath);
    const pythonFile = fs.readFileSync(localPythonFilePath);


    const exec = await container.exec({
        Cmd: ['sh', '-c', `mkdir -p /app && echo '${requirementsFile}' > requirements.txt && pip install -r requirements.txt && echo '${pythonFile}' > ${pythonFilePath} && python -u ${pythonFilePath}`],
        AttachStdout: true,
        AttachStderr: true,
    });

    const stream = await exec.start({ hijack: true, stdin: true });

    const logsStream = fs.createWriteStream('logs.txt', { flags: 'a' });

    container.modem.demuxStream(stream, logsStream, logsStream);

    container.modem.demuxStream(stream, process.stdout, process.stderr);
};

const runShellScript = async (localShellFilePath) => {
    const container = await docker.createContainer({
        Image: imageName,
        Tty: true,
        Cmd: ['tail', '-f', '/dev/null'],
        HostConfig: {
            AutoRemove: true,
        },
    });

    await container.start();

    const shellFile = fs.readFileSync(localShellFilePath);


    const exec = await container.exec({
        Cmd: ['sh', '-c', `mkdir -p /app && echo '${shellFile}' > ${shellFilePath} && chmod +x ${shellFilePath} && ./${shellFilePath}`],
        AttachStdout: true,
        AttachStderr: true,
    });

    const stream = await exec.start({ hijack: true, stdin: true });

    const logsStream = fs.createWriteStream('logs.txt', { flags: 'a' });

    container.modem.demuxStream(stream, logsStream, logsStream);

    container.modem.demuxStream(stream, process.stdout, process.stderr);
};

module.exports = {runPythonScript, runShellScript}
