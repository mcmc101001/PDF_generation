DOCKER_USERNAME = mcmc101001
APP_VERSION = v1
APP_NAME = pdf_generation
USER_UID = 1001
USER_GID = 1001

build:
	docker build --tag ${DOCKER_USERNAME}/${APP_NAME}:${APP_VERSION} . --build-arg USER_UID=${USER_UID} --build-arg USER_GID=${USER_GID} --build-arg APP_VERSION=${APP_VERSION} --build-arg APP_NAME=${APP_NAME}

run:
	docker run --name ${APP_NAME} --publish 127.0.0.1:8000:8000 ${DOCKER_USERNAME}/${APP_NAME}:${APP_VERSION}

start:
	docker start ${APP_NAME}

stop:
	docker stop ${APP_NAME}

remove:
	docker rm ${APP_NAME}