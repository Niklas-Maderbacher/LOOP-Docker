#!/bin/bash

mkdir -p ./certs

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ./certs/local.key \
  -out ./certs/local.crt \
  -subj "/C=AT/ST=Vienna/L=Vienna/O=Local Dev/CN=loop.htl"
