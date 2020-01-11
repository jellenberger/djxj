# Base image
FROM python:3.7-slim

# Env vars
# NOTE: for pip cache env var, watch https://github.com/pypa/pip/issues/5735
ENV PIP_NO_CACHE_DIR false
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/appuser
ENV WORK=$HOME/code

# Install dependencies and create appuser
RUN apt-get update && apt-get install -y \
        wait-for-it \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pipenv \
    && mkdir -p $HOME \
    && mkdir $WORK \
    && groupadd -g 1000 appuser \
    && useradd -r -u 1000 -g appuser appuser \
    && chown -R appuser:appuser $HOME \
    && chown -R appuser:appuser $WORK

# Install project dependencies
# NOTE: --dev deps are being installed to install jupyter in container
WORKDIR $WORK
COPY --chown=appuser:appuser Pipfile Pipfile.lock $WORK/
RUN pipenv install --system --dev && \
    chown -R appuser:appuser $HOME

# Copy project files
COPY --chown=appuser:appuser . $WORK/

# Run as appuser
USER appuser
