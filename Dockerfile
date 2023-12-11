FROM quay.io/rofrano/python:3.11-slim 


# Install PostgreSQL development packages
RUN apt-get update \
    && apt-get install -y libpq-dev gcc


# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip wheel && \
    pip install psycopg2 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY service/ ./service/

# Switch to a non-root user
RUN useradd --uid 1000 flask && chown -R flask /app
USER flask

# Expose any ports the app is expecting in the environment
ENV FLASK_APP=service:app
ENV PORT 8080
EXPOSE $PORT

ENV GUNICORN_BIND 0.0.0.0:$PORT
ENTRYPOINT ["gunicorn"]
CMD ["--log-level=info", "service:app"]