# vpn-client-as-systemd.service
Add-on for VPN client openconnect (for Docker + Cisco Anyconnect)

At the moment it works as follows:

You must have Docker installed!
```
$> sudo -i 
#> apt install openconnect python3-venv
#> cd /opt/vpn-service
#> python3 -m venv env
#> source env/bin/activate
#> pip3 install cryptography
#> python3 configure.py
#> cp vpn-service.service /etc/systemd/system/
#> systemctl daemon-reload
#> systemctl start vpn-service.service
#> systemctl status vpn-service.service***
```
