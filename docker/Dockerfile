# Use Alpine-based Python image
FROM python:3.9-alpine

# Copy the source code into the container.
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application with automatic reload
CMD ["uvicorn", "main:app", "--reload","--host", "${HOST}", "--port", "${PORT}"]