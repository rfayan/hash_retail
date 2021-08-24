# --- Minimalist Debian 10 ("Buster") image with python3 pre-installed --- #
FROM python:3.8.11-slim as base


# --- Build Stage for installing/compiling OS dependencies and python modules --- #
FROM base as builder

# Install Debian compile-time dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    g++ \
    make \
    cmake \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install python packages defined in Pipfile under /.venv
COPY Pipfile .
COPY Pipfile.lock .

RUN pip install --no-cache-dir --upgrade pip pipenv \
  && PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


# --- Final Application Image with just the required dependencies and modules --- #
FROM base as application

# Install Debian runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
  && rm -rf /var/lib/apt/lists/*

# Create and switch to a new user to avoid potential security issues when running as root
RUN useradd --create-home appuser
USER appuser

# Copy installed dependencies at /install from builder stage to user PATH
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Set /hash_retail as work directory and copy the project source code
WORKDIR /app
COPY hash_retail /app/hash_retail
COPY ./VERSION.txt /app

# Expose port 80 and run Biometrics API with gunicorn WSGI as a manager for uvicorn ASGI server with 8 workers
EXPOSE 80
ENTRYPOINT ["gunicorn", "hash_retail.main:app", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "-w", "8", "--preload"]
