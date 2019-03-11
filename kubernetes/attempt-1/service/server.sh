#! /bin/sh

while true; do envsubst < resp.http | nc -l 8080; done
