FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything inside backend/ into the container
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI from the correct app path
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
