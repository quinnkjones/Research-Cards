
FROM python:3.12
#set the working directory in the container
WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

#these two lines set up a virtual environment I found this is necessary for djangorestframework to work properly in docker
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (as per compose file)
EXPOSE 8000

