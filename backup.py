# -*- coding: utf-8 -*-
import ConfigParser
import argparse
from __init__ import do


parser = argparse.ArgumentParser(description='Wrapper for backup GFI EventsManager')
parser.add_argument('-c', dest='config', action='store', default='default.ini',
                    help='wskaz plik z konfiguracja')
parser.add_argument('action', choices=['export', 'delete', 'ping'])

args = parser.parse_args()


def read_config(config_file, section):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    args = dict(config.items('main'))
    args.update(dict(config.items(section)))
    return args

params = read_config(args.config, args.action)

do(args.action, params)