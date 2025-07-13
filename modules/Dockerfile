# Author: Pavlo Nykolyn
# version of the python interpreter
ARG image_version=
# slim images may be used
ARG use_slim
ARG token=${image_version:+:${image_version}}
ARG image_type=${use_slim:+-slim}
FROM python${token}${image_type}
# the time 
ENV TZ=Europe/Rome
COPY . /modules
# will be used to set the environment variables used to generate the configuration for the uwsgi server
ARG listening_port=
ARG wsgi_file=
ARG application_instance=
ARG num_threads=1
ARG num_processes=1
EXPOSE ${listening_port}/tcp
# set of enviornment variables
ENV MODEM_API_LISTENING_PORT=${listening_port}
ENV MODEM_API_WSGI_FILE=${wsgi_file}
ENV MODEM_API_APPLICATION_INSTANCE=${application_instance}
ENV MODEM_API_NUM_THREADS=${num_threads}
ENV MODEM_API_NUM_PROCESSES=${num_processes}
# installing a set of dependencies for the application
ARG proxy_socket=
WORKDIR /modules
# updating the time zone of the container
RUN ln --force --symbolic --no-dereference /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone
# Python 3 packages
ARG requirement_file_name="requirements_api.txt"
RUN pip3 install ${proxy:+--proxy ${proxy_socket}} --requirement ${requirement_file_name}
# running the production server
ENTRYPOINT ["/bin/sh", "-c", "./init_server.sh"]
