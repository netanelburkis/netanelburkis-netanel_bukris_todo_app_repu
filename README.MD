# *Todo List by Netanel Bukris* 📋
![Python](https://img.shields.io/badge/python-blue)
![Docker](https://img.shields.io/badge/docker-blue)
![Flask](https://img.shields.io/badge/Flask-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue)
![MySQL](https://img.shields.io/badge/MySQL-blue)
![Gunicorn](https://img.shields.io/badge/Gunicorn-blue)
![Nginx](https://img.shields.io/badge/Nginx-blue)
![Weather Widget](https://img.shields.io/badge/Weather%20Widget-brightgreen)
![Pytest](https://img.shields.io/badge/Pytest-yellowgreen)
![Selenium](https://img.shields.io/badge/Selenium-green)
![Coverage](https://img.shields.io/badge/Coverage-blue)

A simple to-do list web application built using Flask, SQLAlchemy, MySQL, Docker, Gunicorn, and Nginx. This app allows users to register, log in, and manage tasks. It uses a MySQL database to store user information and tasks.

## *Features*✨

* User Authentication: Register, login, and manage sessions.  
* Task Management: Add, delete, and mark tasks as completed.  
* Search: Search for tasks by description.  
* Weather Widget: Shows the weather for Israel.  
* Clock Widget: Displays the current time.

## *Prerequisites*🧰

* Python 3.9 or later  
* Docker and Docker Compose  
* MySQL or MariaDB for the database  
* Nginx (for reverse proxy setup)  
* Gunicorn (WSGI server for running Flask in production)

## *Project Structure* 📁
```bash
Todo_list/
├── README.md              # Project documentation
├── app/                   # Flask application directory
│   ├── Dockerfile         # Docker configuration for the Flask app
│   ├── app_project.py             # Main Flask application
│   ├── requirements.txt   # Python dependencies
│   ├── static/         # static file
│      ├── background-image.jpg      # background-image
│      └── css_style_main_page_todo_list.css     # css_style
│   ├── templates/         # HTML templates
│     ├── by-netanel-bukris.html     # by template file
│     ├── login-register.html     # login template file
│     └── main-page-todo-list.html     # Main template file
├── tests     # Test files and configurations
│   ├── requirements.txt     # Dependencies for test environment
│   └── test_selenium_in_parts.py     # Selenium test script for app
├── docker-compose.yaml    # Docker Compose configuration
├── nginx/                 # Nginx reverse proxy configuration
│   └── default.conf       # Nginx configuration file
├── .gitignore
└── Jenkinsfile             # Jenkins pipeline configuration
```

## **CI/CD Pipeline**⚙
The project includes a `Jenkinsfile` to automate the entire build, test, and deployment process using **Jenkins**.  
The pipeline performs the following steps:
- Run unit tests with **Pytest**
- Run end-to-end tests with **Selenium**
- Build a Docker image of the app
- Deploy to two separate environments:
  - **staging**: for testing and validation
  - **production (Release Final)**: production-ready deployment

All CI/CD configuration files (including Jenkins, Nginx, Docker, and deployment scripts) are stored in a separate repository:  
🔗 [CI/CD Configuration Repository](https://github.com/netanelburkis/todo_list-cd.git)

## *Installation* 🔧

*Clone the repository*:   
```bash   
git clone https://github.com/yourusername/todo-list-by-netanel-bukris.git  
cd todo-list-by-netanel-bukris
```

**Create a `requirements.txt`**:  
This file contains all the dependencies for the project. If it is not already created, you can generate it by running:
```bash   
pip freeze > requirements.txt
```

1. Set up the MySQL database:
Ensure you have a MySQL database running locally or use Docker to set up a MySQL container. Here are the details to configure in your app_project.py:
```python 
DB_HOST = os.environ.get("DB_HOST", "db")  # Default to 'db' if running in Docker
DB_USER = os.environ.get("DB_USER", "python_todo_list_app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123password")
DB_NAME = os.environ.get("DB_NAME", "todo_list_app_db")
```

Note: You can change the database connection settings by modifying the environment variables instead of using the default values. These variables can be set in multiple places:

~1 Using environment variables directly in your system:
```python 
export DB_HOST=your_custom_host
export DB_USER=your_custom_user
export DB_PASSWORD=your_custom_password
export DB_NAME=your_custom_db
```
~2 Note on Customizing Environment Variables in Docker Compose:

You can easily modify environment variables to customize your app's configuration. These values are defined within the docker-compose.yaml file in the app service section under environment. By editing these variables, you can control the database connection settings, such as DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME.
For example: 
```yaml 
services:  
  app:  
    build: .  
    environment:  
      - FLASK_APP=app_project.py  
      - FLASK_ENV=production  
      - DB_HOST=db  # You can change this value to your custom database host
      - DB_USER=python_todo_list_app  # Change as needed
      - DB_PASSWORD=123password  # Change as needed
      - DB_NAME=todo_list_app_db  # Change as needed 
    depends_on:  
      - db  
```
**Don't forget to also update the environment variables of the db accordingly:**
```yaml 
  db:  
    image: mysql:8.0 
    environment:  
      - MYSQL_ROOT_PASSWORD=rootpassword # Change as needed  
      - MYSQL_DATABASE=todo_list_app_db # Change as needed 
      - MYSQL_USER=python_todo_list_app # Change as needed 
      - MYSQL_PASSWORD=123password # Change as needed 
```
or with:
```python 
export MYSQL_ROOT_PASSWORD= your_custom_MYSQL_ROOT_PASSWORD
export MYSQL_USER=your_custom_user
export MYSQL_ROOT_PASSWORD=your_custom_password
export MYSQL_DATABASE=your_custom_db
```

This flexibility allows you to run the same code on different environments (e.g., local, staging, production) without changing the code itself.

2. Install dependencies:
Using pip to install the requirements:
```bash   
pip install -r requirements.txt
```

3. Run the Flask application:
You can run the application using the command:
```bash
flask run
```

Or if you want to run it in debug mode:
```bash   
flask run --debugger
```

4. ### **Docker Setup (optional):**

If you'd like to use Docker for setting up the application, use the provided Dockerfile and docker-compose.yaml to build and run the app.

Build the Docker image:
```bash 
docker-compose build
```

Start the application:
```bash 
docker-compose up
```

## **Docker Compose Setup**

The project includes a docker-compose.yaml file to set up all the services:
```yaml 
services:
  app_1:
    image: netanelbukris/to_do_list
    environment:
      FLASK_APP: app_project.py
      FLASK_ENV: production
      DB_HOST: db
      DB_USER: python_todo_list_app
      DB_PASSWORD: 123password
      DB_NAME: todo_list_app_db
    depends_on:
      db:
        condition: service_healthy
    networks:
    - front
    - back

  app_2:
    image: netanelbukris/to_do_list
    environment:
      FLASK_APP: app_project.py
      FLASK_ENV: production
      DB_HOST: db
      DB_USER: python_todo_list_app
      DB_PASSWORD: 123password
      DB_NAME: todo_list_app_db
    depends_on:
      db:
        condition: service_healthy
    networks:
    - front
    - back

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: todo_list_app_db
      MYSQL_USER: python_todo_list_app
      MYSQL_PASSWORD: 123password
    volumes:
    -  sql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5
      timeout: 5s
    networks:
    - back

  nginx:
    image: nginx:latest
    ports:
    -  "80:80"
    volumes:
    -  ./nginx/default.conf:/etc/nginx/templates/default.conf.template
    depends_on:
    -  app_1
    -  app_2
    environment:
      APP_1_HOST: app_1
      APP_2_HOST: app_2
    networks:
    - front

volumes:
  sql_data:

networks:
  back:
  front:
 ```

## **Dockerfile Overview**
```bash 
# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container  
COPY requirements.txt /app/

# Install the dependencies from the requirements file  
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container  
COPY . /app/

# Expose the Flask app's default port  
EXPOSE 5000

# Define the command to run the app using Gunicorn   
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app_project:todo_list_app"]
  ```

You can use the dockerfile or the image from docker: 
netanelbukris/to_do_list

## **Nginx Configuration**

To arrange the configuration we will create a folder called nginx in the root of the project and inside it we will create a file called default.conf:

 ```nginx  
# nginx/nginx.conf
upstream flask_backend {
	server ${APP_1_HOST}:5000;
	server ${APP_2_HOST}:5000;
    }

    server {
	listen 80;

	location / {
	    proxy_pass http://flask_backend;
	    proxy_set_header Host $host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
     }

 ```
We'll make sure we've created a volume for nginx in our Docker Compos like this:
```yaml 
  nginx:  
    image: nginx:latest
    ports:
    -  "80:80"  
    volumes:  
    -  ./nginx/default.conf:/etc/nginx/templates/default.conf.template   
```
 **Nginx Configuration File (default.conf)**
The default.conf file, located in the nginx/ directory, contains:

Upstream - Defining the Backend
upstream flask_backend defines a group of servers that Nginx will forward requests to.
${APP_1_HOST}:5000, {APP_2_HOST}:5000 is the address of our applications (Flask runs on port 5000).

**APP_1\2_HOST is an environment variable that is defined in docker-compose.yaml .**
**Note that it is set correctly**
```yaml 
 nginx:
    image: nginx:latest
    ports:
    -  "80:80"
    volumes:
    -  ./nginx/default.conf:/etc/nginx/templates/default.conf.template
    depends_on:
    -  app_1
    -  app_2
    environment:
      APP_1_HOST: app_1
      APP_2_HOST: app_2
```
Server Configuration (server)
listen 80; instructs Nginx to listen for incoming requests on port 80.
location / {} defines that all requests reaching / will be forwarded to flask_backend using proxy_pass http://flask_backend.
proxy_set_header is used to pass information such as:
Host - the original hostname of the request.
X-Real-IP - the real IP address of the client.
X-Forwarded-For - the IP addresses of the proxies the request has passed through..

We will create two back and front networks to separate our application nginx and database:
```yaml 
networks:
  back:
  front:
```
When the apps are connected to both the back and the front, the database will be connected to the back and nginx to the front.

## **testing**🧪
The project uses Selenium for automating browser tests and Pytest for running the tests.

To run the tests, follow these steps:

1.Install the required dependencies for testing:

```bash 
pip install -r app/test/requirements.txt
  ```

2.Run the Selenium-based tests with Pytest:

```bash
pytest app/test/test_selenium_in_parts.py
  ```
This will execute the tests and verify the app's functionality.

## **coverage**

## Installation

To install the necessary dependencies, including **coverage**, you can use pip:

```bash
pip install coverage
  ```
## **Usage with Pytest**
1.Running Tests with Coverage:
You can use coverage to run your tests with pytest by running the following command:

```bash
coverage run -m pytest
  ```
This will run all your tests and record which lines of code were covered during the test execution.

2.Running Selenium Tests:
If you're running Selenium-specific tests, you can specify your test file (for example, selenium.py) at the end:

```bash
coverage run -m pytest selenium.py
  ```
## **Viewing Coverage Report**
After running your tests with coverage, you can view a detailed report of the coverage:

1.Text Report:
To display the coverage report directly in the terminal, use:

```bash
coverage report
  ```
2.HTML Report:
You can generate an HTML version of the coverage report, which will allow you to see which lines were covered with color coding (green for covered, red for not covered):

```bash
coverage html
  ```
3.Opening HTML Report:
Once the HTML report is generated, you can view it by opening the index.html file in a web browser:

```bash
open htmlcov/index.html
  ```
This will give you a visual representation of your test coverage.

## **File Structure**🗂️

* `app_project.py`: Main Flask application file. 
* `requirements.txt`: Project dependencies. 
* `Dockerfile`: Instructions to build the Docker image for the app.  
* `docker-compose.yaml`: Docker Compose file to set up the app, MySQL services, and Nginx reverse proxy.  
* `nginx.conf`: Nginx configuration file.  
* `templates/`: Contains HTML files for the web app.  
* `static/`: Contains static files like CSS and images.  
* `.gitignore.`
* `Jenkinsfile`: Jenkins pipeline configuration
* `tests/`: Contains test files for the application, including Selenium-based browser tests.
   * `test_selenium_in_parts.py`: Selenium test script for app functionality.
   * `requirements.txt`: Dependencies for test environment.

## **Usage**🚀

1. **Start the application**: After setting up everything, navigate to the app's root directory and run it using Flask or Docker.  
2. **Login/Register**: Visit the app at `http://127.0.0.1` in your browser. You can register a new user or log in with an existing account.  
3. **Manage Tasks**: After logging in, you can add new tasks, delete tasks, or mark them as completed. Tasks will persist in the MySQL database.  
4. **Search**: Use the search bar to find tasks by keywords in the task description.

## **License**📜

This project is open-source and free to use.

## **Acknowledgments** 🛠️

* **Flask**: A micro web framework written in Python.  
* **SQLAlchemy**: An ORM that simplifies database interactions in Python.  
* **MySQL**: Relational database management system.  
* **Docker**: Platform for developing, shipping, and running applications in containers.  
* **Gunicorn**: WSGI HTTP server for running Flask in production.  
* **Nginx**: Web server used as a reverse proxy for the app.  
* **Weather Widget**: Displaying live weather information.
* **Pytest**: A testing framework for Python that allows for writing simple and scalable test cases. It supports fixtures and has a powerful plugin architecture to extend functionality. We use Pytest for unit testing our application and ensuring code quality.
* **Selenium**: A popular tool for automating web browsers. Selenium allows us to simulate user interactions with the web application and perform end-to-end testing to verify that the app behaves correctly in different scenarios.
* **Coverage**: A tool used to measure code coverage, which helps in ensuring that our tests are thorough and cover all areas of the code. Coverage provides detailed reports showing which parts of the code were executed during tests, and which were not, helping us identify untested areas and improve test coverage.
* **Jenkins Pipeline**: An automation tool used to define and run CI/CD workflows. Our Jenkins pipeline automatically builds, tests, and deploys the application using Docker and Pytest. It provides immediate feedback on code changes and ensures continuous integration and delivery with minimal manual intervention.
