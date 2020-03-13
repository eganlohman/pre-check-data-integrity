FROM python:3.8

WORKDIR /concordance
COPY concordance/ ./
COPY requirements.txt requirements.txt

# install concordance python package
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# set entrypoint
ENTRYPOINT ["python", "/concordance/concordance.py"]
