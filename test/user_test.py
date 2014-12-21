import sys
import unittest

from flask import Flask
from flaskext.script import Command, Manager, InvalidCommand, Option

class SimpleCommand(Command):
    "simple command"

    def run(self):
        print "OK"

