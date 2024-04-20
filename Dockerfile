FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src

ENTRYPOINT ["python", "src/main.py"]