echo "Now opening all ports needed for loop"

sudo firewall-cmd --zone=public --add-port=3000/udp --permanent
sudo firewall-cmd --zone=public --add-port=3000/tcp --permanent
sudo firewall-cmd --zone=public --add-port=5000/udp --permanent
sudo firewall-cmd --zone=public --add-port=5000/tcp --permanent
sudo firewall-cmd --zone=public --add-port=5432/udp --permanent
sudo firewall-cmd --zone=public --add-port=5432/tcp --permanent
sudo firewall-cmd --zone=public --add-port=8000/udp --permanent
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
sudo firewall-cmd --zone=public --add-port=8080/udp --permanent
sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent

echo "Successfully opend all ports needed for loop"

