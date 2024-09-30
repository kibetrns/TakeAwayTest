# Take Away Test API

Welcome to the **Customer Order API**!

This API is built using [FastAPI.](https://fastapi.tiangolo.com/)

## Table of Contents

- [Live Site](#live-site)
- [Setting up the project](#setting-up-the-project)
- [Environment Variables](#environment-variables)
- [Running the program](#running-the-program)
- [Building and Deploying the API](#building-and-deploying-the-api)
- [TODOs](#todos)

## Live Site
Find the deployed site [here](https://take-away-test-api-0-0-1.onrender.com/)


## Setting up the project

While on your desired folder/directory clone the project to your local machine by running the command

```
git clone https://github.com/kibetrns/TakeAwayTest.git
```

It would create a folder/directory named `TakeAwayTest`.

From the terminal/command prompt navigate to `TakeAwayTest`

Create a Python virtual environment and make it active. See details [here](https://fastapi.tiangolo.com/virtual-environments/)


Install the packages in the `requirements.txt` file using one of these the command:

```pip
pip install -r requirements.txt
```

``` uv
uv pip install -r requirements.txt
```


## Environment variables
Create a `.env` file in the root directory/folder, in our case `TakeAwayTest`.

Paste the following immediate code below and fill the appropriate values of the place holders used.

You'll need to have accounts of the following platforms:

  - Africastalking developer account. [Get it here](https://account.africastalking.com/auth/register?next=%2F])
  - dockerhub account [Get it here](https://app.docker.com/signup?)
  - render account [Get it here](https://dashboard.render.com/register)
  - MongoDB Cloud Atlas account. [Get it here](https://www.mongodb.com/cloud/atlas/register)

> Leaving out these environment variables will cause the app. not to function

```
MONGODB_URL=<your_mongodb_url>
MONGODB_DB=<your_mongodb_database_name>

AFRICASTALKING_USERNAME=<your_africastalking_username>
AFRICASTALKING_API_KEY=<your_africastalking_api_key>

DOCKER_USERNAME=<your_docker_username>
DOCKER_PASSWORD=<your_docker_password>
DOCKER_REGISTRY=<your_docker_registry>
DOCKER_ACCESS_TOKEN=<your_docker_access_token>

ON_RENDER_API_KEY=<your_on_render_api_key>
ON_RENDER_SERVICE_ID=<your_on_render_service_id>

PORT=<your_desired_port>
```

## Running the program

Run the program using this command. ( You should in the parent directory/folder - `TakeAwayTest` in this case:

```
fastapi dev main.py
```

An alterntive way of runnint the app is to open the project using [fleet](https://www.jetbrains.com/fleet/download/#section=linux)


Click the run button that's near the menu bar, then add a configuration by clicking the text that says `Edit Run Configurations`

It opens a file called `run.json`. Paste the following to the file:
```
{
    "configurations": [
        {
            "type": "fastapi",
            "name": "Fastapi configuration",
            "module": "main",
            "application": "app",
        },

    ]
}
```
Now you'll just be clicking the run button on the `Fastapi Configuration` menu item to run the app



## Building and Deploying the API
Follow these steps to build the Docker image and deploy the API:

### Build the Image
```
docker build -t <your_docker_username>/take-away-test-api:<version> .
```

### Check Local Images
```
docker images
```

### Tag the Image (if necessary)
```
docker tag <your_docker_username>/take-away-test-api:<version> docker.io/<your_docker_username>/take-away-test-api:<version>
```

At this point you can procede and run the docker image

### Run the Docker Container
```
docker run \
    -e MONGODB_URL='<your_mongodb_url>' \
    -e MONGODB_DB='<your_mongodb_database_name>' \
    -e AFRICASTALKING_USERNAME='<your_africastalking_username>' \
    -e AFRICASTALKING_API_KEY='<your_africastalking_api_key>' \
    -e DOCKER_USERNAME='<your_docker_username>' \
    -e DOCKER_PASSWORD='<your_docker_password>' \
    -e DOCKER_REGISTRY='<your_docker_registry>' \
    -e DOCKER_ACCESS_TOKEN='<your_docker_access_token>' \
    -e ON_RENDER_API_KEY='<your_on_render_api_key>' \
    -e ON_RENDER_SERVICE_ID='<your_on_render_service_id>' \
    -p <host_port>:<container_port> \
    <your_docker_username>/take-away-test-api:<version>
```

Proceede witht the next steps below if you want to deploy it a registry in this case docker hub



### Log in to Docker Hub

```
docker login
```

### Push the Image
```
docker push docker.io/<your_docker_username>/take-away-test-api:<version>
```

## TODOs
Check out the open issues [here](https://github.com/kibetrns/TakeAwayTest/issues)