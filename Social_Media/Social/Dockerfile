FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5002

# Define environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ENV DB_USER=postgres
ENV DB_NAME=cofeee
ENV HOST=host.docker.internal
ENV PASSWORD=jayant
ENV PORT=5432
ENV USER_APP_PORT=5003
ENV POST_APP_PORT=5001
ENV SOCIAL_APP_PORT=5002

# Run the application:
CMD ["python", "run.py"]