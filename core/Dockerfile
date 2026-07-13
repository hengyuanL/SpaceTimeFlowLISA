FROM python:3.12-slim

RUN pip install pandas numpy scipy

WORKDIR /app
COPY . .

CMD ["python", "SpaceTimeFlowLISA_main.py"]
