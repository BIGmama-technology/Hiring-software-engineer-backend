
# Containerized Task Management with Docker API

An express REST API to run, schedule and get updates on your scripts inside a docker container.


## Run Locally

Clone the project

```bash
  git clone https://github.com/Bretis2019/Hiring-software-engineer-backend.git
```

You might have to pull python:3.9-alpine image

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

#### Run Shell script

```http
  POST /execute-script
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. just use 'admin' for now |
| `password`      | `string` | **Required**. just use 'admin' for now |
| `script`      | `shell file` | **Required**. your Shell script |

#### Run Python script

```http
  POST /execute-python-script
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. just use 'admin' for now |
| `password`      | `string` | **Required**. just use 'admin' for now |
| `script`      | `python file` | **Required**. your Python script |
| `requirements`      | `text file` | **Required**. your dependencies file |

#### schedule Python script

```http
  POST /schedule-python-script
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. just use 'admin' for now |
| `password`      | `string` | **Required**. just use 'admin' for now |
| `cronExpression`      | `text` | **Required**. cron expression for when to rerun the script |
| `script`      | `python file` | **Required**. your Python script |
| `requirements`      | `text file` | **Required**. your dependencies file |


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


## Related

Related stuff

[Cron expressions validator.](https://vercel.com/docs/cron-jobs#cron-expressions)

[How to upload files using postman.](https://www.youtube.com/watch?v=S7bwkys6D0E)

