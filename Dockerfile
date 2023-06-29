FROM python:3.9

WORKDIR /PyInvestAnalyzer

COPY . .

RUN pip install --upgrade pipenv && pipenv install --system

ENV DOCKER=True

CMD ["python3", "run.py"]
