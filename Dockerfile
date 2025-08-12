FROM continuumio/miniconda3:4.12.0
RUN apt update && apt upgrade -y
RUN apt-get update
RUN apt-get install -y curl unzip

RUN mkdir /repository

COPY ./environment.yml /
RUN conda env create -f /environment.yml

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
