FROM python:2.7.15

WORKDIR /usr/src/release-deployment-history
#RUN yum -y install python-pip
RUN pip install dash \
                dash_core_components \
                dash_html_components \
                datetime \
                pymongo \
                Flask

COPY app.py ./ \
     asap_hosts ./

ADD static ./

CMD [ "python", "./app.py" ]
