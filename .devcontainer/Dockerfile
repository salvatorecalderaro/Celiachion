ARG PYTHON_VERSION
FROM mcr.microsoft.com/vscode/devcontainers/python:${PYTHON_VERSION}

ARG REQUIREMENTS_FOLDER
ARG USER

COPY requirements*.txt ${REQUIREMENTS_FOLDER}

USER root

RUN chown -R ${USER}:${USER} /usr/local/

RUN pip install --upgrade pip
RUN pip install -q \
	-r ${REQUIREMENTS_FOLDER}requirements.txt \
	-r ${REQUIREMENTS_FOLDER}requirements-dev.txt
RUN rm -r ${REQUIREMENTS_FOLDER}

RUN apt update
RUN apt upgrade -y

USER ${USER}