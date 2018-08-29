import subprocess
from subprocess import PIPE, Popen
import sublime
import sublime_plugin
import threading

oz_proc = None

class SubOz(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.process = None

    def run(self):
        self.process = Popen(['ozengine', 'x-oz://system/OPI.ozf'], stdout=PIPE, stderr=PIPE)
        print("ozengine pid : %s", self.process.pid)
        while self.running:
            output = self.process.stdout.readline()
            outerr= self.process.stderr.readline()
            if output == '' and outerr == '' and self.process.poll() is not None:
                running = False
            else:
                print(output.decode('utf-8'))
                print(outerr.decode('utf-8'))

class OzRunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global oz_proc
        oz_proc = SubOz()
        oz_proc.start()