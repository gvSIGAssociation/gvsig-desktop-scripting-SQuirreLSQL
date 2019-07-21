# encoding: utf-8

from gvsig import *

from addons.SQuirreLSQL import squirrelsql

def main(*args):
  script.registerDataFolder("squirrelsql")

  squirrelsql.selfRegister()
