# Author: Pavlo Nykolyn
# creates a .ini file that will be used by uwsgi to run a request server;
# the following environment variables are expected to be defined
# - MODEM_API_LISTENING_PORT -> listening port;
# - MODEM_API_WSGI_FILE -> wsgi file (the extension is mandatory);
# - MODEM_API_APPLICATION_INSTANCE -> application instance;
# - MODEM_API_NUM_THREADS -> number of threads;
# - MODEM_API_NUM_PROCESSES -> number of processes

ini_file='server.ini'

impress ()
{
   # the first positional argument should be a prefix, indicating the message type
   # the second positional argument is the message itself
   echo "--- $(date) --- ${1} ${2}"
}

if [ ! -f "${ini_file}" ]
then
   # checking the port number
   port=$(echo ${MODEM_API_LISTENING_PORT} | sed -n '/^[1-9][0-9]*$/p')
   if [ -z ${port} ]
   then
      impress '[ERR]' "${MODEM_API_LISTENING_PORT} is not a positive number"
      exit 1
   fi
   if [ ${port} -gt 65535 ]
   then
      impress '[ERR]' "${port} exceeds 65535"
      exit 1
   fi
   # is the wsgi file a valid one?
   wsgi_file="${MODEM_API_WSGI_FILE}"
   if [ ! -f "${wsgi_file}" ]
   then
      impress '[ERR]' "${wsgi_file} either is not a regular file or does not exist within ${PWD}"
      exit 1
   fi

   application_instance=${MODEM_API_APPLICATION_INSTANCE}
   # checking both amounts of allocated threads and processes
   num_threads=$(echo ${MODEM_API_NUM_THREADS} | sed -n '/^[1-9][0-9]*$/p')
   if [ -z ${num_threads} ]
   then
      impress '[ERR]' "${MODEM_API_NUM_THREADS} is not a positive number"
      exit 1
   fi
   num_processes=$(echo ${MODEM_API_NUM_PROCESSES} | sed -n '/^[1-9][0-9]*$/p')
   if [ -z ${num_processes} ]
   then
      impress '[ERR]' "${MODEM_API_NUM_PROCESSES} is not a positive number"
      exit 1
   fi
   # creating the .ini file (only if it does not exist)
   echo '[uwsgi]' > "${ini_file}"
   echo "   master=true" >> "${ini_file}"
   echo "   http=:${port}" >> "${ini_file}"
   echo "   wsgi-file=${wsgi_file}" >> "${ini_file}"
   echo "   callable=${application_instance}" >> "${ini_file}"
   echo "   processes=${num_processes}" >> "${ini_file}"
   echo "   threads=${num_threads}" >> "${ini_file}"

   impress '[INF]' '.ini file content:'
   cat "${ini_file}"
fi
# running uwsgi with the provided file
uwsgi --ini "${ini_file}"
