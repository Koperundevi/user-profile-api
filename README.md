# User Profile Api

## Prerequisites:

- Python 3.7+
- Create Github Oauth application (https://docs.github.com/en/developers/apps/creating-an-oauth-app)
- Any sqlalchemy supported database [SQLite, Postgresql, MySQL, Oracle, MS-SQL, Firebird, Sybase]

To run the postgress database using docker in local server run the below command.

* docker run --name postgres-docker -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
* create the db named 'userprofileapp' in the server