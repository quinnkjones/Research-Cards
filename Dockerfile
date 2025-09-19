
FROM python:3.12

WORKDIR /app

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
# some ls debugging
RUN ls -la /app
RUN ls -la /app/research_cards_django
# Expose port (as per compose file)
EXPOSE 8000

