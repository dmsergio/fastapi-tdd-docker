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
