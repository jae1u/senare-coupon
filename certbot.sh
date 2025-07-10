docker run -it --rm --name certbot \
    -p 80:80 \
    -v "./letsencrypt:/etc/letsencrypt" \
    certbot/certbot certonly -d snrcoupon.kro.kr --standalone -n --agree-tos
