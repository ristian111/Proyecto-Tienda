# Makefile para no tener que andar escribiendo mucho comando.

.PHONY: up down build logs restart status

# Start the docker containers in the background
up:
	docker-compose up -d

# Stop and remove the containers
down:
	docker-compose down

# Build the docker images
build:
	docker-compose build

# View logs from the containers
logs:
	docker-compose logs -f

# Restart the containers
restart:
	docker-compose restart

# Check the status of the containers
status:
	docker-compose ps
# Initiate the frontend
start:
	cd ./frontend && npm run dev
