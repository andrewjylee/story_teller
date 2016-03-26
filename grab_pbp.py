import urllib2
import string
import re
from data import html_parser

class Team:
    def __init__(self):
        self.players = dict()
        

    def print_stats(self):
        for k in self.players.keys():
            print k, self.players[k]

    def add_points(self, player, points):
        if points == "2-pt":
            points = 2
        elif points == "3-pt":
            points = 3
        elif points == "free throw":
            points = 1
        else:
            print "should never be here"

        if player in self.players.keys():
            self.players[player] += points
        else:
            self.players[player] = points

    def score_tracker(self, line):
        pattern = "^(\d+-\d+)\s\+?\d?[A-Z]\.\s(\w+)\smakes\s(\d-pt|free throw).*$"
        match = re.search(pattern, line)

        if match:
            game_score = match.group(1)
            player = match.group(2)
            points = match.group(3)
            self.add_points(player, points)

    def stats_tracker(self, line):
        if 'makes' in line:
            self.score_tracker(line)




def filter_tr(line):
    # Return tr_tag if line == <tr> or </tr>
    if line == "</tr>" or line == "<tr>":
        return 1
    return 0

def filter_time(line):
    # Return 1 if line == time line
    pattern = "^.*([0-9]|[0-1][0-9]):[0-5][0-9].*$"
    regex = re.compile(pattern)
    if regex.match(line):
        return 1
    return 0

def filter_possessions(line):
    pattern = "<td>&nbsp;</td><td>&nbsp;</td>"
    if pattern not in line:
        return 0
    return 1

def filter(line):
    tr_tag = filter_tr(line)
    if tr_tag == 0:
        if filter_time(line) == 0:
            if filter_possessions(line):
                return line
    return None


def which_team(line):
    # Return 0 if neither, 1 if left, 2 if right
    pattern = "<td>&nbsp;</td><td>&nbsp;</td>"
    index = line.index(pattern)
    if index == 0:
        return 1
    elif index > 0:
        return 2
    else:
        return 0

       
def clean_up(line):
    " Get score out first "
    match = re.search('^.*>(\d+-\d+)</td>.*$', line)

    score = ''
    if match:
        score = match.group(1)
    line = re.sub(score, '', line)

    inbetween = 0
    ret = ""
    for i in range(len(line)):
        char = line[i]
        if char == ">":
            inbetween = 0
            continue
        if char == "<":
            inbetween = 1
            continue
        if inbetween:
            continue
        ret += char
    
    ret = re.sub('&nbsp;', '', ret)
    return score, ret



def get_winner(score):
    pattern = "(\d+)-(\d+)"
    match = re.search(pattern, score)
    home_score = match.group(1)
    away_score = match.group(2)
    if home_score > away_score:
        print "Home team won!"
    else:
        print "Away team won!"

        

def summarize(score, home, away):
    get_winner(score)


if __name__ == "__main__":

    # TODO: make url out of user input of date and team
    gameid = "201603240BRK"
    html_class = html_parser(gameid)

    start = 0
    lines = html_class.html.splitlines()

    home = Team()
    away = Team()

    for i in range(len(lines)):
        line = lines[i]
        if start:
            if filter(line):
                possession = line
                side = which_team(possession)
                if side == 1:
                    score, summary = clean_up(line)
                    home.stats_tracker(score + " " + summary)

                elif side == 2:
                    score, summary = clean_up(line)
                    away.stats_tracker(score + " " + summary)
                else:
                    print 'should never be here?'
            continue

        # TODO: quarter-granularity?
        if "Start of 1st quarter" in line:
            start = 1
            continue
        # TODO: Overtime games
        if "End of 4th quarter" in line:
            print "END OF GAME"
            break


    summarize(score, home, away)
    print '--'
    home.print_stats()
    print '--'
    away.print_stats()


