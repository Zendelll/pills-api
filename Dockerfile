FROM nginx/unit:1.29.0-python3.11

COPY ./nginx/config.json /docker-entrypoint.d/config.json

RUN mkdir app

COPY . ./app

RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r /app/requirements.txt                               \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

EXPOSE 80