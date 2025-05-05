docker run --rm -it \
  -v certbot-etc:/etc/letsencrypt \
  -v certbot-var:/var/lib/letsencrypt \
  -p 80:80 \
  certbot/certbot certonly --standalone \
  -d *.loop.htl --agree-tos --email itp.loop.htl@gmail.com --non-interactive
