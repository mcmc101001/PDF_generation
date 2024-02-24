DOCKER_USERNAME = mcmc101001
APP_VERSION = v1
APP_NAME = pdf_generation
APP_NAME_TEST = pdf_generation_test
USER_UID = $(shell id -u)
USER_GID = $(shell id -g)
PWD = $(shell pwd)

build:
	docker build --tag ${DOCKER_USERNAME}/${APP_NAME}:${APP_VERSION} . \
		--build-arg USER_UID=${USER_UID} \
		--build-arg USER_GID=${USER_GID} \
		--build-arg APP_VERSION=${APP_VERSION} \
		--build-arg APP_NAME=${APP_NAME}\
	
	docker build --target test \
		--tag ${DOCKER_USERNAME}/${APP_NAME_TEST}:${APP_VERSION} . \
		--build-arg USER_UID=${USER_UID} \
		--build-arg USER_GID=${USER_GID} \
		--build-arg APP_VERSION=${APP_VERSION} \
		--build-arg APP_NAME=${APP_NAME}

format:
	docker run --rm --name ${APP_NAME_TEST} \
		-v ${PWD}/pdf_generation:/home/${APP_NAME}/app/pdf_generation \
		-p 8000:8000 ${DOCKER_USERNAME}/${APP_NAME_TEST}:${APP_VERSION} \
		sh -c	"cd ./pdf_generation && poetry run isort . && poetry run black ."

test:
	docker run --rm --name ${APP_NAME_TEST} -v ${PWD}/pdf_generation:/home/${APP_NAME}/app/pdf_generation -p 8000:8000 ${DOCKER_USERNAME}/${APP_NAME_TEST}:${APP_VERSION} \
		sh -c "poetry run pytest"

lint: 
	docker run --rm --name ${APP_NAME_TEST} -v ${PWD}/pdf_generation:/home/${APP_NAME}/app/pdf_generation -p 8000:8000 ${DOCKER_USERNAME}/${APP_NAME_TEST}:${APP_VERSION} \
		sh -c	"poetry run mypy . && poetry run flake8 ."

run:
	docker run --rm --name ${APP_NAME} -p 8000:8000 ${DOCKER_USERNAME}/${APP_NAME}:${APP_VERSION}