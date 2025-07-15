# Use a specific Python version slim base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Optional: if you don't need PDF processing in frontend, skip this block
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code
COPY . .

# Expose the port Cloud Run expects
EXPOSE 8080

# Run the Streamlit app on $PORT from Cloud Run
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0


