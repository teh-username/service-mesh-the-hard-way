#! /bin/sh

while true; do cat resp.http | nc -l 8080; done
