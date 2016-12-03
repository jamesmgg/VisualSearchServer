FROM gcr.io/tensorflow/tensorflow:latest
MAINTAINER Akshay Bhat <akshayubhat@gmail.com>

RUN add-apt-repository ppa:kirillshkrogalev/ffmpeg-next && \
    apt-get update && apt-get install -y protobuf-compiler \
    python-scipy \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    ffmpeg && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
                          fabric \
                          django \
                          jinja \
                          jinja2 \
                          djangorestframework \
                          markdown \
                          django-filter \
                          raven \
                          fabric \
                          awscli \
                          nearpy \
                          flask \
                          ipython \
                          jupyter \
                          psycopg2 \
                          requests \
                          plyvel \
                          boto3 \
                          protobuf \
                          humanize
USER root
RUN git clone https://github.com/akshayubhat/VisualSearchServer /root/VS
WORKDIR "/root/VS"
RUN fab test
EXPOSE 8888 8000
