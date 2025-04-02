FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install salmon (v1.10.2 als voorbeeld)
RUN curl -L https://github.com/COMBINE-lab/salmon/releases/download/v1.10.2/salmon-1.10.2_linux_x86_64.tar.gz | tar xz && \
    mv salmon-1.10.2_linux_x86_64/salmon /usr/local/bin && \
    rm -rf salmon-1.10.2_linux_x86_64

# Set work directory
WORKDIR /app

# Copy dependencies & install
COPY Website/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY Website/ .

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
