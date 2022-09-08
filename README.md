# vpn-client-as-systemd.service
Add-on for VPN client openconnect (for Docker + Cisco Anyconnect)

At the moment it works as follows:

You must have Docker installed!
```
$> sudo -i 
#> apt install openconnect python3-venv
#> mkdir -p /opt/vpn-service/
#> cp ./start_vpn.py /opt/vpn-service/
#> cp ./classes.py /opt/vpn-service/
#> cp ./stop.py /opt/vpn-service/
#> cp ./configure.py /opt/vpn-service/
#> mkdir -p /opt/vpn-service/certs
#> mkdir -p /opt/vpn-service/client
#> cp YOUR_PATH/{SomethingYourCertName}.p12 /opt/vpn-service/certs/certificate.p12
#> cp /usr/sbin/openconnect /opt/vpn-service/client/client_by_openconnect
#> cd /opt/vpn-service
#> python3 -m venv env
#> source env/bin/activate
#> pip3 install cryptography
#> python3 configure.py
#> cp vpn-service.service /etc/systemd/system/
#> systemctl daemon-reload
#> systemctl start vpn-service.service
#> systemctl status vpn-service.service
```
