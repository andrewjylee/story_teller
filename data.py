import urllib2
import string
import re


class html_parser:
    def __init__(self, gameid):
        self.gameid = gameid
        self.base_url = "http://www.basketball-reference.com/boxscores/pbp/"
        self.url = self.base_url + self.gameid + ".html"
        self.html = urllib2.urlopen(self.url).read()



