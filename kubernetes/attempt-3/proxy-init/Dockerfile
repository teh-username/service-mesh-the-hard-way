FROM alpine:3.8

RUN apk add --update --no-cache iptables
COPY ./iptables.sh iptables.sh

RUN chmod a+x iptables.sh

CMD ["./iptables.sh"]
