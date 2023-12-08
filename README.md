# FastAPI Starter Kit

## Description:
This is a pre-configured FastAPI framework designed to streamline rapid development in other projects. The basic setup is complete, allowing you to reference and build upon the codebase for quick development.

## Contents:
The current configuration includes several modules:

1. **MySQL CRUD Example:**
   - Find an example in `routers/mysql.py` showcasing CRUD operations using MySQL, including both synchronous and asynchronous methods.

2. **MongoDB CRUD Example:**
   - Explore the `routers/mongo.py` file for an example demonstrating CRUD operations using MongoDB, including both synchronous and asynchronous methods.

3. **CSRF Protection with Cookie Example:**
   - Discover an example of CORS protection using Cookies in `routers/csrf.py`. The comments include guidance on using dependencies, allowing you to configure them in other routers as needed. If you prefer not to use Cookies, `fastapi_csrf_protect` provides alternative methods.

## Additional Information:
- Notice that HTTPException from FastAPI is not used for handling exceptions in server responses. This is intentional, as custom response formats are preferred. Check the `models/base.py` file for details. If you don't have this requirement, you can switch to using HTTPException for handling exceptions.

## Usage:
1. Utilize the provided `docker-compose.yml` file. Simply copy this repository and use the command `docker-compose up -d` to start the service. However, for faster hot-reloading, it is recommended to run FastAPI locally.
2. If you wish to use your own SQL database or MongoDB, configure the settings in the `config` folder.

## Note on Deployment:
To deploy this server, it is advisable to have the following dependencies installed:

1. **Alembic:**
   - Used for SQL migration version control.

2. **Nginx:**
   - Popular choice for a reverse proxy server.

3. **Gunicorn:**
   - Better worker processes compared to Uvicorn.

These tools are not mandatory for using the FastAPI Starter Kit but are recommended for deployment purposes.

Feel free to explore, modify, and adapt this FastAPI Starter Kit to suit your project's needs. Happy coding!