UID := $(shell id -u)
GID := $(shell id -g)

up:
	UID=$(UID) GID=$(GID) docker compose up

down:
	docker compose down

build:
	UID=$(UID) GID=$(GID) docker compose up --build

logs:
	docker compose logs -f

restart:
	docker compose down
	UID=$(UID) GID=$(GID) docker compose up
