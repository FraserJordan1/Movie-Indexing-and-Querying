FROM python:3.10-slim

WORKDIR /usr/src/assignment_7
COPY . .
RUN pip install --no-cache-dir pytest

CMD ["pytest"]