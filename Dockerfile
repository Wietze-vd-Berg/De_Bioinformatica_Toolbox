FROM python:3.10-slim

# Voeg salmon toe aan PATH
ENV PATH="/usr/local/bin:$PATH"

# Systeemafhankelijkheden
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download en installeer salmon
RUN curl -L https://github.com/COMBINE-lab/salmon/releases/download/v1.10.2/salmon-1.10.2_linux_x86_64.tar.gz | tar xz && \
    cp salmon-1.10.2_linux_x86_64/salmon /usr/local/bin/salmon && \
    chmod +x /usr/local/bin/salmon && \
    rm -rf salmon-1.10.2_linux_x86_64

# Werkdirectory
WORKDIR /app

# Installeer Python-dependencies
COPY Website/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy alle bestanden uit je project
COPY Website/ .

# Start Flask-app met gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]

