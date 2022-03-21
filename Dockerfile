FROM python:latest

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY transformer.py .
CMD ["python", "-u", "transformer.py"]