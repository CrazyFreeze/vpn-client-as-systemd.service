# -*- coding: utf-8 -*-
import os
import subprocess
import time
import signal
import sys
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption, load_pem_private_key
import tempfile
import configparser
import base64
import getpass

class Find_path_util:
    def __init__(self, util):
        self.util = util
        self.cmd = ["whereis", self.util, "awk", "{print $2}" ]
    
    def output(self):
        cmd = self.cmd
        t1 = subprocess.Popen(cmd[:2], stdout=subprocess.PIPE)
        t2 = subprocess.Popen(cmd[2:], stdin=t1.stdout, stdout=subprocess.PIPE)
        t1.stdout.close()
        output = t2.communicate()[0]
        return output.decode().strip()
    
    def reboot(self):
        util = self.util
        cmd = ["/bin/systemctl", "restart", util]
        try:
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
                proc.stdout.close()
        except:
            exit(1)


class Check:
    def __init__(self):
        self.resolv = '/etc/resolv.conf'

    def run(self):
        tmp = []
        with open(self.resolv, 'r') as f:
            for i in f:
                tmp.append(i)
        while True:
            time.sleep(1)
            try:
                tmp2 = []
                with open(self.resolv, 'r') as f:
                    for i in f:
                        tmp2.append(i)
                if tmp != tmp2:
                    return 0
                else:
                    continue
                        
            except:
                exit(1)


class Stop:
    def __init__(self, name, cert, key):
        self.name = name
        self.cert = cert
        self.key = key

    def __check(self, name):
        try:
            return int(subprocess.check_output(['pidof', name]))
        except:
            return 0

    def proc(self):
        number = self.__check(self.name)
        print(number)
        if number != 0:
            os.kill(number, signal.SIGTERM)
            os.unlink(self.cert)
            os.unlink(self.key)
            exit(0)
        else:
            exit(1)


class Start:
    def __init__(self, util, certificate, cert_key, username, password, servername):
        self.logfile = '/tmp/tmp_vpn.log'
        self.util = util
        self.certificate = certificate
        self.cert_key = cert_key
        self.username = username
        self.password = password
        self.servername = servername

    def run(self):
        commandline = [self.util, "--user", self.username, "--passwd-on-stdin", "--background", "--certificate={}".format(self.certificate), "--sslkey={}".format(self.cert_key), self.servername]
        try:
            with open(self.logfile, 'w') as errf:
                subprocess.Popen(commandline, stdin=subprocess.PIPE, stderr=errf).communicate(self.password.encode())
        except:
            with open(self.logfile, 'r') as log:
                line = log.readlines()
                for i in line:
                    if 'login failed.' in i.lower():
                        sys.stdout.write("Authentication error! See more --> /tmp/tmp_vpn.log")
                    else:
                        exit(1)


class Read_p12:
    def __init__(self, path, otppass):
        self.path = path
        self.otppass = otppass.encode('UTF-8')

    def read_cert(self):

        key, cert, p12 = pkcs12.load_key_and_certificates(open(self.path, 'rb').read(), self.otppass)
        
        key = key.private_bytes( encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption(),)
        
        cert = cert.public_bytes(Encoding.PEM)
        
        fd, _cert = tempfile.mkstemp()
        
        with open(_cert, "wb") as f:
            f.write(cert)
        
        fd, _key = tempfile.mkstemp()
        
        with open(_key, "wb") as f:
            f.write(key)

        return _cert, _key


class SIG_handler:
    
    def __init__(self):
        self.SIGINT = False
        self.SIGTERM = False

    def signal_handler(self, signal, frame):
        self.SIGINT = True
        self.SIGTERM = True


class Config:
    

    def __init__(self, filename):
        self.filename = filename
        
    def __dialog(self, question, def_answer="yes"):
        
        answers = {"yes": 1, "y": 1, "ye":1, "no": 0, "n": 0}

        if def_answer == None:
            t = " [y/n]"
        elif def_answer == "yes":
            t = " [Y/n]"
        elif def_answer == "no":
            t = " [y/N]"
        else:
            raise ValueError("Invalid value {}".format(def_answer))
        
        while True:

            print(question + t + ": ")

            user_answer = input().lower()

            if def_answer is not None and user_answer == '':

                return answers[def_answer]

            elif user_answer in answers:

                return answers[user_answer]

            else:
                print("Please select yes/y or no/n\n")

    
    def __inputpass(self, text):
        while True:
            pass1 = getpass.getpass(text)
            pass2 = getpass.getpass("Confirm password input: ")
            if pass1 == pass2:
                return pass1
            else:
                print("Passwords don't match! Repeat the input...")

    def __check(self, text):
        while True:
            value = str(input(text))
            dialog = self.__dialog(value)
            if dialog == 1:
                return value

    def _obfusc(self, data):
        return base64.b64encode(data.encode("UTF-8")).decode("UTF-8")

    def _deobf(self, data):
        return base64.b64decode(data.encode("UTF-8")).decode("UTF-8")

    def _set(self, object, section, key, value):
        return object.set(section, key, value)

    
    def write_config(self):

        parser = configparser.ConfigParser()
        section = ["VPN", "servername", "username", "one-time-password", "password"]
        with open(self.filename, "w") as conf:
            parser.add_section(section[0])
            self._set(parser, section[0], section[1], self._obfusc(self.__check("Input Server Address: ")))
            self._set(parser, section[0], section[2], self._obfusc(self.__check("Input Username: ")))
            self._set(parser, section[0], section[3], self._obfusc(self.__inputpass("One-time-password: ")))
            self._set(parser, section[0], section[4], self._obfusc(self.__inputpass("Password of certificate: ")))
            return parser.write(conf)

    def read_config(self):

        parser = configparser.ConfigParser()
        parser.read(self.filename)
        val_ = dict()
        for sectionName in parser.sections():
            for name, value in parser.items(sectionName):
                val_[str(name)] = self._deobf(value)
        return val_


