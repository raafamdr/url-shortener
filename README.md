# URL Shortener

A simple URL shortener service that creates a short URL for a given long URL. This service uses only English alphabet letters (a-z, A-Z) and digits (0-9). When the user accesses the shortened URL, they are redirected to the original URL. Additionally, the service keeps track of the number of times a shortened URL has been accessed.  

## Features

- Generate short URLs for long URLs
- Redirect users to the original URL when accessing the shortened URL
- Delete shortened URLs
- Track the number of times a shortened URL has been accessed

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**

### Development Tools

- **Docker**: for containerization.
- **Poetry**: for Python package and dependency management.
- **Taskipy**: used as a task runner.
- **Ruff**: for code linting and formatting.
- **Pydantic**: for data validation.
- **SQLAlchemy**: for database interactions and data modeling.
- **Alembic**: for managing database migrations.
- **pytest**: for testing.
- **testcontainers**: for running containers directly in the test code.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/raafamdr/url-shortener.git
    cd url-shortener
    ```

2. Create a `.env` file in the root directory based on the `.env.example` file and make sure to adjust the values according to your setup.

3. Make the `entrypoint.sh` file executable:

    ```bash
    chmod +x entrypoint.sh
    ```

4. Build and start Docker containers:

    ```bash
    docker-compose up --build
    ```

### Usage

Once the containers are up and running, you can access the application's API documentation at: 
[http://localhost:8000/docs](http://localhost:8000/docs)

## Testing

To run the tests, use:

```
task test
```