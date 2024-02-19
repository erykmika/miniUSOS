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

### The whole process is made straightforward by using Docker and Docker Compose. Make sure you have the appropriate software installed first.

### Clone the repository and navigate into it.

```sh
git clone https://github.com/erykmika/miniUSOS.git
cd ./miniUSOS/
```

### Run 'docker compose'. This may take up a few minutes.
```sh
docker compose up
```

### Go to **127.0.0.1:5000** in your web browser.

### Sample credentials (included within **miniusos.sql**)
* student: login 'karolina.wojcik@example.com' password '123'
* prowadzacy (lecturer): login 'jan.kowalski@example.com' password '123'
* admin: login 'admin' password 'xyz'
