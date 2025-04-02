FROM continuumio/miniconda3

# Werkdirectory
WORKDIR /app

# Installeer salmon via conda
RUN conda install -c bioconda -c conda-forge salmon=1.10.2

# Controleer of salmon bestaat en werkt
RUN echo "✅ Check salmon install:" && which salmon && salmon --version

# Voeg environment path toe zodat salmon beschikbaar is
ENV PATH="/opt/conda/bin:$PATH"

# Install Python dependencies
COPY Website/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY Website/ .

# Start Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]

