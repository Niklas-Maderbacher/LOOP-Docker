# FastAPI Project - Development

## Formatting script files (Windows only)

1. Open the script files located in /backend/scripts in VS-Code.
2. Look at the bottom-right corner and click on the CRLF.
3. Change it to LF.
4. Save the file.

## Docker Compose

* Build the docker container:

* Start the local stack with Docker Compose:

```bash
docker compose -f docker-compose.yml up --build
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://localhost:3000

Backend, JSON based web API based on OpenAPI: http://localhost:8000

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs

Adminer, database web administration: http://localhost:8080


**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run (in another terminal):

```bash
docker compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker compose logs backend
```

## Local Development

The Docker Compose files are configured so that each of the services is available in a different port in `localhost`.

For the backend and frontend, they use the same port that would be used by their local development server, so, the backend is at `http://localhost:8000` and the frontend at `http://localhost:3000`.

This way, you could turn off a Docker Compose service and start its local development service, and everything would keep working, because it all uses the same ports.

For example, you can stop that `frontend` service in the Docker Compose, in another terminal, run:

```bash
docker compose stop frontend
```

And then start the local frontend development server:

```bash
cd frontend
npm run dev
```

Or you could stop the `backend` Docker Compose service:

```bash
docker compose stop backend
```

And then you can run the local development server for the backend:

```bash
cd backend
fastapi dev app/main.py
```

## Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.

And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker compose` to apply overrides on top of `docker-compose.yml`.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker compose` command.

After changing variables, make sure you restart the stack:

```bash
docker compose watch
```

## The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.

## Adminer

Login credentials:

- Server: **db!!!!** not localhost as stated in .env file. The server is mapped from localhost to db!!
- Username: POSTGRES_USER located in .env file
- Password: POSTGRES_PASSWORD located in .env file
- Database: POSTGRES_DB located in .env file

## URLs

The production or staging URLs would use these same paths, but with your own domain.

### Development URLs

Development URLs, for local development.

Frontend: http://localhost:3000

Backend: http://localhost:8000

Automatic Interactive Docs (Swagger UI): http://localhost:8000/docs

Automatic Alternative Docs (ReDoc): http://localhost:8000/redoc

Adminer: http://localhost:8080
