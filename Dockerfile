FROM python:2.7.15

WORKDIR /usr/src/release-deployment-history

ENV PATH /usr/src/release-deployment-history:$PATH
#RUN yum -y install python-pip
RUN pip install dash \
                dash_core_components \
                dash_html_components \
                datetime \
                pymongo \
                Flask \
                gunicorn

COPY . .

CMD [ "gunicorn", "--bind", "0.0.0.0:3005", "wsgi:server" ]
