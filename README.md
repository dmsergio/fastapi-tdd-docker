# Test-Driven Development with FastAPI and Docker

![Continuous Integration and Delivery](https://github.com/dmsergio/fastapi-tdd-docker/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)

---

### Run tests with __pytest__
- Run all tests: `docker-compose exec web python -m pytest`
- Run all tests with verbosity: `docker-compose exec web python -m pytest -v`
- Check the quality of the tests: `docker-compose exec web python -m pytest --cov="."`
- Run tests in parallel: `docker-compose exec web python -m pytest -k "unit" -n auto` (-n flag tells pytest running tests with n processors)

### Manual testing with __curl__

- Get all summaries: `curl https://frozen-island-62276.herokuapp.com/summaries/`
- Get summary by id: `curl https://frozen-island-62276.herokuapp.com/summaries/{summary_id}/`
- Create summary: `curl -X POST -H "Content-Type: application/json" -d '{"url": "https://github.com"}' https://frozen-island-62276.herokuapp.com/summaries/`
- Update summary: `curl -X PUT -H "Content-Type: application/json" -d '{"url": "https://github.com", "summary": "updated!"}' https://frozen-island-62276.herokuapp.com/summaries/{summary}/`
- Delete summary: `curl -X DELETE https://frozen-island-62276.herokuapp.com/summaries/3/`

---

### Common commands

- Apply the migrations: `docker-compose exec web aerich upgrade`
- Lint: `docker-compose exec web flake8 .`
- Run Black and isort with check options:
  - `docker-compose exec web black . --check`
  - `docker-compose exec web isort . --check-only`
- To bring down the containers: `docker-compose down`
- Force a build: `docker-compose build --no-cache`
- Access to the database via psql: `docker-compose exec db psql -U postgres -d {database_name}`
- Execute a query to the database via psql: `docker-compose exec db psql -U postgres -d {database_name} -c "{sql command}"`

---

# Deploy the app to Heroku

1. A Heroku account is required ([sign up](https://signup.heroku.com/)).
2. Also is required the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
3. Create a new app: `heroku create`
   1. This step will create a new Heroku app. The app name is required for the next steps (heroku_app).
4. Log in to the [Heroku Container Registry](https://devcenter.heroku.com/articles/container-registry-and-runtime): `heroku container:login`
5. Provision a new Postgres database with the [hobby-dev](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier) plan: `heroku addons:create heroku-postgresql:hobby-dev --app {heroku_app}`
6. Build the production image and tag it with the following format: `docker build -f project/Dockerfile.prod -t registry.heroku.com/{heroku_app}/web ./project`
7. Push the image to the registry: `docker push registry.heroku.com/{heroku_app}/web:latest`
8. Release the image: `heroku container:release web --app {heroku_app}`
9. You should be able to view the app at _https://{heroku_app}.herokuapp.com/ping/_.
