# Task 5

FROM scratch
ADD centos-7-x86_64-docker.tar.xz /

LABEL org.label-schema.schema-version="1.0" \
    org.label-schema.name="CentOS Base Image" \
    org.label-schema.vendor="CentOS" \
    org.label-schema.license="GPLv2" \
    org.label-schema.build-date="20190305"

RUN yum update -y
RUN yum install -y yum-utils wget curl vim jq git
RUN wget https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN ls -lrt *.rpm
RUN yum install -y ius-release.rpm


# Install Java JDK
RUN yum install -y java-1.8.0-openjdk
RUN echo "Java version and location"
RUN java -version
RUN which java

# Install Python3.6 and pip
RUN yum install -y python36u
RUN yum install -y python36u-pip
RUN pip3.6 install --upgrade pip
RUN python3.6 -V
RUN pip3.6 -V

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1


COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN touch guinicorn_access.log 
RUN touch guinicorn_error.log

# Installing Dependencies
RUN pip3.6 install -r requirements.txt
RUN pip3.6 install gunicorn
EXPOSE 5001

CMD ["sh", "/app/start_app.sh" ]
