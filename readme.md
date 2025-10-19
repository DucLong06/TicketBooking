sudo certbot certonly --webroot -w /var/www/html -d booking.duongcam.art -d www.booking.duongcam.art


docker volume inspect ticketbooking_frontend_build 2>/dev/null | grep Mountpoint
docker volume inspect ticketbooking_static_volume_prod 2>/dev/null | grep Mountpoint
docker volume inspect ticketbooking_media_volume_prod 2>/dev/null | grep Mountpoint

sudo chmod 755 /var/lib/docker
sudo chmod 755 /var/lib/docker/volumes