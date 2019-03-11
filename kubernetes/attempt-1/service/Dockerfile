FROM byrnedo/alpine-curl
RUN apk add --update --no-cache netcat-openbsd gettext

COPY ./server.sh server.sh
COPY ./resp.http resp.http
RUN chmod a+x server.sh

ENTRYPOINT ["./server.sh"]
