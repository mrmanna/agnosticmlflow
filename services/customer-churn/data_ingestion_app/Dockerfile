# Use the Python 3.9-slim-bullseye base to ensure we can install OpenJDK packages
FROM python:3.9-slim


WORKDIR /app
# COPY . .

# # (Optional) Remove the existing Poetry lock
# # RUN rm poetry.lock

# # Install Poetry
# RUN pip install poetry

# # Install dependencies from pyproject.toml
# RUN poetry install

# CMD ["poetry", "run", "python", "src/main.py"]
# Install dependencies before copying code to leverage Docker cache
COPY requirements-docker.txt .

# Install dependencies from requirements.txt
RUN pip install -r requirements-docker.txt

ARG CACHEBUST=1
# Copy application code after installing dependencies
COPY . .

# Command to run the application
CMD ["python", "src/main.py"]