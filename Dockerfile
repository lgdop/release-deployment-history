FROM python:2.7.15

WORKDIR /usr/src/release-deployment-history

ENV https_proxy=http://172.23.29.155:3128
ENV http_proxy=http://172.23.29.155:3128
ENV PATH /usr/src/release-deployment-history:$PATH
#RUN yum -y install python-pip
RUN pip install dash \
                dash_core_components \
                dash_html_components \
                datetime \
                pymongo \
                flask \
                gunicorn \
                dash-renderer \
                plotly \
                python-dotenv \
		pandas
COPY . .
EXPOSE 3005

CMD [ "gunicorn", "--bind", "0.0.0.0:3005", "index:server" ]
