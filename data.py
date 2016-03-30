import urllib2
import string
import re


class html_parser:
    def __init__(self, gameid):
        self.gameid = gameid
        self.base_url = "http://www.basketball-reference.com/boxscores/"
        self.pbp_url = self.base_url + "pbp/" + self.gameid + ".html"
        self.game_url = self.base_url + self.gameid + ".html"
        self.pbp_html = urllib2.urlopen(self.pbp_url).read()
        self.game_html = urllib2.urlopen(self.game_url).read()



