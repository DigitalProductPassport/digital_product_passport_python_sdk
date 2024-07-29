FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install nicegui web3 solidity-python-sdk

EXPOSE 8080

CMD ["python", "main.py"]
