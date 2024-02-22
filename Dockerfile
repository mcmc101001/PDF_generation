# choose base image and give alias
FROM python:3.12-slim@sha256:fde1011b3a944e4e750982480905b563fd08a0f3fde49b963b05d8ebf6846ce8 AS python-base

# Ensure deterministic output/immutable
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  # yes to installs, disable unnecessary install, backslash escapes newline character
  # QUESTION: no need for sudo? why install font?
  && apt-get install -y --no-install-recommends \
  fonts-open-sans \
  # clean up local repository of packages
  && apt-get clean \
  # remove temp files
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Run container as non root for better security and PSP compatibility in Kube

# Customise build process with build args
ARG USER_UID
ARG USER_GID
ARG APP_NAME
LABEL internal.app_name=${APP_NAME}

# Set environment variables
ENV USER_UID=${USER_UID} \
  USER_GID=${USER_GID} \
  USER_USERNAME=${APP_NAME} \
  APP_NAME=${APP_NAME}

# add group and user, set user's home directory, no password auth and gecos (to disable prompt asking for it?)
RUN addgroup --gid ${USER_GID} app
RUN adduser \
  --home /home/${USER_USERNAME} \
  --uid ${USER_UID} \
  --gid ${USER_GID} ${USER_USERNAME} \
  --disabled-password \
  --gecos ''

# User specific setup
# Run app as user instead of root, setup working directory
USER ${USER_UID}
ENV WORKDIR=/home/${USER_USERNAME}/app
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

ENV PYTHONPATH=${WORKDIR}
ENV PATH=$PATH:/home/${USER_USERNAME}/.local/bin:/home/${USER_USERNAME}/.poetry/bin

# Download poetry installer into temp folderr and change owner and group owner (so that the user can run?)
ADD --chown=${USER_UID}:${USER_GID} https://install.python-poetry.org /tmp/install-poetry.py
# We need to force some setup tools version here otherwise flower doesn't start :sad:
RUN python3 /tmp/install-poetry.py && \
  poetry config virtualenvs.path /home/${USER_USERNAME}/venvs

# A bit of pip configuration for best performances / image size
ENV PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy the files needed for poetry to install dependencies (COPY only for local files, ADD can be used for remote)
COPY --chown=${USER_UID}:${USER_GID} pyproject.toml poetry.lock ./

# Docker image layer caches in order, so install dependencies first so 
# that image remains cached if dep dont change and source code changes

# Only prod dependencies (--only-main) to avoid installing dev dependencies
# Avoid installing the project itself (--no-root) to separate dependencies from the project

############################
# Image layer for prod-deps
############################
FROM python-base AS prod-deps

RUN poetry install --no-root --only main

############################
# Image layer for tests-deps
############################
FROM prod-deps AS test-deps

RUN poetry install --no-root

#######################
# Image layer for tests
#######################
FROM python-base AS test

# Wait for app to be ready before running tests
ADD --chown=${USER_UID}:${USER_GID} https://github.com/ufoscout/docker-compose-wait/releases/download/2.11.0/wait /wait
RUN chmod +x /wait

COPY --chown=${USER_UID}:${USER_GID} --from=test-deps /home/${USER_USERNAME}/venvs /home/${USER_USERNAME}/venvs

# Test files
COPY --chown=${USER_UID}:${USER_GID} setup.cfg setup.cfg

# prod files
COPY --chown=${USER_UID}:${USER_GID} pdf_api pdf_api

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

###########################
# Image layer with the prod
###########################
FROM python-base AS prod

# Copy dependencies from prod-deps layer to prod layer
COPY --chown=${USER_UID}:${USER_GID} --from=prod-deps /home/${USER_USERNAME}/venvs /home/${USER_USERNAME}/venvs

# prod files only here
COPY --chown=${USER_UID}:${USER_GID} pdf_generation pdf_generation

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

CMD ["poetry", "run", "gunicorn", "pdf_generation.main:app", "--workers=2", "--worker-class=uvicorn.workers.UvicornWorker", "--timeout=10000", "--bind=0.0.0.0:8000"]

#Question: No need to run tests?