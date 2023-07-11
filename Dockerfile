FROM python:3.10

WORKDIR /PyInvestAnalyzer

COPY . .

RUN pip install --upgrade pipenv && pipenv install --system

ENV DOCKER=True

CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false"]
