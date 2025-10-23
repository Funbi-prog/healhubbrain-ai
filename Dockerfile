# Start with a clean official Python image
FROM python:3.10.13-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Upgrade build tools
RUN pip install --upgrade pip setuptools wheel packaging

# Copy project files into container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose Rasa port
EXPOSE 5005

# Start Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005", "--debug"]
