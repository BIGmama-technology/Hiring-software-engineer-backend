
# Containerized Task Management with Docker API

An express REST API to run, schedule and get updates on your scripts inside a docker container.


## Run Locally

Clone the project

```bash
  git clone https://github.com/Bretis2019/Hiring-software-engineer-backend.git
```
Make sure the docker engine is running on your machine.

You might have to pull python:3.9-alpine image.

```bash
  docker pull python:3.9-alpine
```


Install dependencies

```bash
  npm install
```


Start the server

```bash
  npm run dev
```


## API Reference

#### Get container logs

```http
  GET /logs
```

#### Get scheduled jobs

```http
  GET /jobs
```

#### Run or schedule a script

```http
  POST /execute
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. just use 'admin' for now |
| `password`      | `string` | **Required**. just use 'admin' for now |
| `scriptType`      | `string` | **Required**. the type of your script. either `python`, `shell` or `docker`|
| `script`      | `script file` | **Required**. your script that will be executed.|
| `requirements`      | `text file` |your dependencies file |
| `cronExpression`      | `string` | **Required if you want to schedule**. cron expression for when to rerun the script |
| `title`      | `string` | **Required if you want to schedule**. the title of your scheduled job. |


## Usage/Examples

#### python script example

```python
import time
import random2
import sys

while True:
    # Generate a random number between 1 and 100
    random_number = random2.randint(1, 100)

    # Print "Hello, World!" along with the random number
    print(f"Hello, World! Random Number: {random_number}")

    # Flush the output to ensure it is immediately sent to the Docker container
    sys.stdout.flush()

    # Pause for one second
    time.sleep(1)

```


#### requirements file example

```
random2==1.0.1
```

#### shell script example

```shell
echo "Hello from the Docker container!"

```

#### Run a shell script

```http
  POST /execute
```

| Parameter | Value     |
| :-------- | :------- |
| `username`      | `admin`|
| `password`      | `admin`|
| `scriptType`      | `shell`|
| `script`      | `script file`|

#### Schedule a python script

```http
  POST /execute
```

| Parameter | Value     |
| :-------- | :------- |
| `username`      | `admin` |
| `password`      | `admin` |
| `scriptType`      | `python`|
| `script`      | `script file`|
| `requirements`      | `text file`|
| `cronExpression`      | `0 8 * * *`|
| `title`      | `rng-test`|






## Related

Related stuff

[Cron expressions validator.](https://vercel.com/docs/cron-jobs#cron-expressions)

[How to upload files using postman.](https://www.youtube.com/watch?v=S7bwkys6D0E)

