FROM python

RUN mkdir home/Portal
WORKDIR home/Portal
COPY . .

RUN apt-get update && \
        apt-get upgrade --assume-yes &&\
        apt-get install --assume-yes python3-pip &&\
        apt-get install --assume-yes redis &&\
        apt-get install --assume-yes screen &&\
        apt-get install nano &&\
        pip install -r requirements.txt &&\
        chmod +x autorun.sh

CMD ["sh", "/home/Portal/autorun.sh"]