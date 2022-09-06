# -*- coding: utf-8 -*-
import classes
import start_vpn


if __name__ == "__main__":
    classes.Config(start_vpn.configfile).write_config()
