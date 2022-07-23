# Test-Driven Development with FastAPI and Docker

![Continuous Integration and Delivery](https://github.com/dmsergio/fastapi-tdd-docker/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)

---

### Run tests with __pytest__
- Run all tests: `docker-compose exec web python -m pytest`
- Run all tests with verbosity: `docker-compose exec web python -m pytest -v`
- Check the quality of the tests: `docker-compose exec web python -m pytest --cov="."`

### Manual testing with __curl__

- Get all summaries: `curl https://frozen-island-62276.herokuapp.com/summaries/`
- Get summary by id: `curl https://frozen-island-62276.herokuapp.com/summaries/{summary_id}/`
- Create summary: `curl -H "Content-Type: application/json" -X POST -d '{"url": "https://github.com"}' https://frozen-island-62276.herokuapp.com/summaries/`
- Update summary: `curl -H "Content-Type: application/json" -X PUT -d '{"url": "https://github.com", "summary": "updated!"}' https://frozen-island-62276.herokuapp.com/summaries/{summary}/`
- Delete summary: `curl -X DELETE https://frozen-island-62276.herokuapp.com/summaries/3/`
