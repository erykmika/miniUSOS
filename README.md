# **miniUSOS**

A project done for the Databases II course at college.    
It is a simplified version of an academic management system for students and lecturers. The application interface is all in Polish as it was done for classes led in Polish.

## Tech stack

* Python
* Flask and related Python packages 
* PostgreSQL and psycopg2 Python package
* pip
* plain HTML & CSS

## Setup

### Make sure you have Python installed. Also, you must have an instance of the PostgreSQL database.

### Clone the repository and navigate into it

```sh
git clone https://github.com/erykmika/miniUSOS.git
cd ./miniUSOS/
```

### Configure a database connection

Application code is contained within the */app* directory. The *database_creds.json* file with database credentials must be put into it. It should be of this format:

```json
{
    "database": "<database name>", 
    "user": "<username>",
    "password": "<password>",
    "host": "<server address>",
    "port": "<port number, usually 5432>"
}
```
  

The *miniusos.sql* file contains a script that creates a proper database schema in PostgreSQL and it inserts sample records into the database. All passwords of students ('student') and lecturers ('prowadzacy') are set to '123' in this case.

### Create and activate a virtual environment
```sh
cd ./app
python -m venv ./env
./env/scripts/activate
```

### Install dependecies from the requirements.txt file
```sh
pip install -r requirements.txt
```

### Run the application
```sh
flask --app strona run
```

### Go to **localhost:5000** in your web browser

### Sample credentials (included within **miniusos.sql**)
* student: login 'karolina.wojcik@example.com' password '123'
* prowadzacy (lecturer): login 'jan.kowalski@example.com' password '123'
