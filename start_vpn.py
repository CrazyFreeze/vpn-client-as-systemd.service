# -*- coding: utf-8 -*-
import classes
import signal
import time


configfile = "/opt/vpn-service/properties.ini"
certfile = "/opt/vpn-service/certs/certificate.p12"
clientfile = "/opt/vpn-service/client/client_by_openconnect"



if __name__ == "__main__":
    
    config = classes.Config(configfile).read_config()
    certificate, private_key = classes.Read_p12(certfile, config["one-time-password"]).read_cert()

    classes.Start(clientfile, certificate, private_key, config["username"], config["password"], config["servername"]).run()

    handler = classes.SIG_handler()
    signal.signal(signal.SIGINT, handler.signal_handler)
    
    while True:
        time.sleep(1)
        if handler.SIGINT:
            classes.Stop("client_by_openconnect", certificate, private_key).proc()
            exit("STOP")
