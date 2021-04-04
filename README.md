# User Profile Api

## Prerequisites:

- Python 3.7+
- Create Github Oauth application (https://docs.github.com/en/developers/apps/creating-an-oauth-app)
- Any sqlalchemy supported database

To run the postgress database using docker in local server run the below command.

* docker run --name postgres-docker -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
* create the db named 'userprofileapp' in the server


## Configuration

Configuration of the User Profile API is available at `config.py`. The following parameters can be set in config files:

| Config Variable     | Description      |
| ------------------- | -----------------|
| SQLALCHEMY_ECHO     | Logging of SQL   |
| DEBUG     | Logging level of the application   |
| GITHUB_AUTH_URI     | Git hub auth URI with credential details of Oauth app running in github   |
| SQLALCHEMY_DATABASE_URI     | Database uri   |
| SQLALCHEMY_TRACK_MODIFICATIONS     | Sql track modifications   |
| JWT_SECRET_KEY     | Secret Key of Jwt Auth    |
| JWT_ACCESS_TOKEN_EXPIRES     | Jwt Access token expiration time   |
| FLASK_RUN_HOST     | Running host of application   |
| FLASK_RUN_PORT     | Running port of application   |
| GITHUB_ACCESS_TOKEN_HEADER | header to get the access token from git hub |
| LOGIN_SUCCESS_REDIRECT_URI    |   URI to redirect after a successfull login jwt acces token   |
| PROPAGATE_EXCEPTIONS  |   To properly raise exceptions with jwt   |

## Setup

1. Install project dependencies, From the root of the project, execute
'pip install requirements.txt'

2. After changing DB details in config, run the below commands one by one.
'python manage.py db init'
'python manage.py db migrate'
'python manage.py db upgrade'

These commands, will create the required tables in mentioned database as per the models

3. Setup the environment variable
for linux
export FLASK_ENV=<Environment name> # production/development/testing
for windows
set FLASK_ENV=<Environment name>

4. To start API in localhost using https, run the command

"python app.py"
