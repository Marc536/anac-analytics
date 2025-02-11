# Uses the official Python image
FROM python:3.9

# Defines the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install Flask dependencies
RUN pip install -r requirements.txt

# Expose port 5000 for external access
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
