FROM python:3.8-slim

LABEL maintainer="bakduo"

RUN apt-get update && apt-get install -y software-properties-common snmp && apt-add-repository non-free && apt-add-repository contrib && apt-get update && apt-get install -y snmp-mibs-downloader && cd /tmp/ && pip install -U pip && mkdir /home/usample && useradd --home-dir /home/usample usample && mkdir -p /home/usample/.snmp/mibs/ && chown -R usample:usample /home/usample

ENV PROJECT_DIR /home/usample

WORKDIR ${PROJECT_DIR}

USER usample

COPY --chown=usample:usample mibs ${PROJECT_DIR}/mibs

COPY --chown=usample:usample Pipfile* ${PROJECT_DIR}/

RUN export PATH=$PATH:/home/usample/.local/bin && pip install pipenv && pipenv lock --keep-outdated --requirements > /tmp/requirements.txt && mv /home/usample/mibs/* /home/usample/.snmp/mibs/

RUN pip install -r /tmp/requirements.txt

COPY . ${PROJECT_DIR}/

VOLUME ["/home/usample/app/config","/home/usample/.snmp/mibs"]

EXPOSE 5000

CMD  python run.py
