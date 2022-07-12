# Python Docker template

### Use this template to run a Python project inside a Docker container.

---

### Steps to build the project

1. `cp .env.dist ./.env`
2. Set the args on __.env__ file to custom your both Docker image and container.
3. Prepare your Python project:
   1. Locate it inside __src__ folder.
   2. Add the Python dependencies of your project inside __src/requirements.txt__ file.
4. Build the image: `docker-compose build --pull`
5. Run the container: `docker-compose up -d`

### Next steps

Once the container is running with your project, maybe you should want to set up another things, like enable ports, add entrypoints, etc.
