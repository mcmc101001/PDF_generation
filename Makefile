DOCKER_USERNAME = mcmc101001
APP_VERSION = v1
APP_NAME = pdf_generation
USER_UID = $(shell id -u)
USER_GID = $(shell id -g)

build:
	docker build --tag ${DOCKER_USERNAME}/${APP_NAME}:${APP_VERSION} . \
		--build-arg USER_UID=${USER_UID} \
		--build-arg USER_GID=${USER_GID} \
		--build-arg APP_VERSION=${APP_VERSION} \
		--build-arg APP_NAME=${APP_NAME}

run:
	docker run --rm --name ${APP_NAME} -p 8000:8000 ${DOCKER_USERNAME}/${APP_NAME}:${APP_VERSION}