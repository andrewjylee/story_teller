import urllib2
import string
import re
import sys
from data import html_parser

#TODO Ejections
#TODO Get runs

class Team:
    def __init__(self):
        # TODO: Fix player names to include first name initial, 
        # in case some players have the same last name
        # TODO: Get team names
        #self.team_name = name
        self.players = dict()

    def set_opponent(self, opponent):
        self.opponent = opponent
        
    def add_player(self, player):
        self.players[player] = {'points': 0, 'FGA': 0, 'FG': 0, 'FTA': 0, 'FT': 0, '3P': 0, '3PA': 0, 'rebounds': 0, 'assists': 0, 'steals': 0, 'blocks': 0, 'turnovers': 0, 'fouls': 0}

    def update_stats(self, player, stat_type, increment_value):
        if player in self.players.keys():
            self.players[player][stat_type] += increment_value
        else:
            self.add_player(player)
            self.players[player][stat_type] = increment_value
        

    def print_stats(self):
        print 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS'
        for k in self.players.keys():
            if self.players[k]['FGA']:
                FGP = self.players[k]['FG']/float(self.players[k]['FGA'])
            else:
                FGP = 'N/A'
            if self.players[k]['3PA']:
                TPP = self.players[k]['3P']/float(self.players[k]['3PA'])
            else:
                TPP = 'N/A'
            if self.players[k]['FTA']:
                FTP = self.players[k]['FT']/float(self.players[k]['FTA'])
            else:
                FTP = 'N/A'
            print k, self.players[k]['FG'], self.players[k]['FGA'], FGP, \
            self.players[k]['3P'], self.players[k]['3PA'], TPP, \
            self.players[k]['FT'], self.players[k]['FTA'], FTP, \
            self.players[k]['rebounds'], self.players[k]['assists'], self.players[k]['steals'], self.players[k]['blocks'], \
            self.players[k]['turnovers'], self.players[k]['fouls'], self.players[k]['points']

    def score_tracker(self, line, flag):
        # Flag 1 = make, 0 = miss
        if flag:
            pattern = "^(\d+-\d+)\s\+?\d?[A-Z]\.\s(\w+-?\w+)\smakes\s(\d-pt|free throw).*$"
        else:
            pattern = "^(\d+-\d+)\s\+?\d?[A-Z]\.\s(\w+-?\w+)\smisses\s(\d-pt|free throw).*$"
        match = re.search(pattern, line)

        if match:
            player = match.group(2)
            points = match.group(3)
            if points == "2-pt":
                points = 2
                self.update_stats(player, 'FGA', 1)
                if flag:
                    self.update_stats(player, 'FG', 1)
            elif points == "3-pt":
                points = 3
                self.update_stats(player, 'FGA', 1)
                self.update_stats(player, '3PA', 1)
                if flag:
                    self.update_stats(player, 'FG', 1)
                    self.update_stats(player, '3P', 1)
            elif points == "free throw":
                points = 1
                self.update_stats(player, 'FTA', 1)
                if flag:
                    self.update_stats(player, 'FT', 1)
            else:
                print "should never be here"
                print 'score_tracker error'
                print line
                sys.exit()

            if flag:
                self.update_stats(player, 'points', points)
        else:
            print line
            print 'score error'
            sys.exit()

    def rebound_tracker(self, line):
        # TODO split defensive and offensive rebounds?
        pattern = "^.*rebound by [A-Z]\.\s(\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'rebounds', 1)
        else:
            if 'rebound by Team' not in line:
                print line
                print 'rebound error'
                sys.exit()

    def assist_tracker(self, line):
        pattern = "^.*\(assist by [A-Z]\.\s(\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'assists', 1)
        else:
            print line
            print 'assist error'
            sys.exit()

    def turnover_tracker(self, line):
        pattern = "^.*Turnover by [A-Z]\. (\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'turnovers', 1)
        else:
            if 'Turnover by Team' not in line:
                print line
                print 'turnover error'
                sys.exit()

    def steal_tracker(self, line):
        pattern = "^.*steal by [A-Z]\. (\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'steals', 1)
        else:
            print line
            print 'steal error'
            sys.exit()

    def block_tracker(self, line):
        pattern = "^.*\(block by [A-Z]\. (\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'blocks', 1)
        else:
            print line
            print 'block error'
            sys.exit()

    def foul_tracker(self, line):
        # flag = 1: defensive, 0: offensive
        pattern = "^.*foul by [A-Z]\. (\w+-?\w+).*$"

        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'fouls', 1)
        else:
            print line
            print 'foul error'
            sys.exit()

    def stats_tracker(self, line):
        if 'makes' in line:
            self.score_tracker(line, 1)
        if 'misses' in line:
            self.score_tracker(line, 0)
        if 'rebound' in line:
            self.rebound_tracker(line)
        if 'assist' in line:
            self.assist_tracker(line)
        if 'block' in line:
            self.opponent.block_tracker(line)
        if 'Turnover' in line:
            self.turnover_tracker(line)
            if 'steal' in line:
                self.opponent.steal_tracker(line)
        if 'foul' in line and 'Turnover' not in line:
            if 'drawn by' in line:
                self.opponent.foul_tracker(line)
            else:
                self.foul_tracker(line)
            


    def get_outstanding_stats(self):
        """
        # Score >= 20
        # Rebound >= 14
        # Assists >= 10
        Steals >= 5
        # Blocks >= 5
        # Turnovers > 5
        # Fouls > 5
        # Double Doubles
        # Triple Doubles
        # TODO:
        # FG% > 0.7? && FGA > 12 ? 
        # 3P% >= 0.5 && 3PA >= 9 ?
        """
        for k, v in self.players.iteritems():
            if v['points'] >= 20:
                print k, " had ", v['points'], " points"
            if v['rebounds'] >= 14:
                print k, " had ", v['rebounds'], " rebounds"
            if v['assists'] >= 10:
                print k, " had ", v['assists'], " assists"
            if v['steals'] >= 5:
                print k, " had ", v['steals'], " steals"
            if v['blocks'] >= 5:
                print k, " had ", v['blocks'], " blocks"
            if v['turnovers'] > 5:
                print k, " had ", v['turnovers'], " turnovers"
            if v['fouls'] > 5:
                print k, " fouled out with ", v['fouls'], " fouls"

            if v['points'] >= 10 and v['rebounds'] >= 10 and v['assists'] >= 10:
                print k, " had a triple double with ", v['points'], " points, ", v['rebounds'], " rebounds, and ", v['assists'], " assists"

            elif v['points'] >= 10 and v['rebounds'] >= 10:
                print k, " had a double double with ", v['points'], " points and ", v['rebounds'], " rebounds"
            elif v['points'] >= 10 and v['assists'] >= 10:
                print k, " had a double double with ", v['points'], " points and ", v['assists'], " assists"
            elif v['assists'] >= 10 and v['rebounds'] >= 10:
                print k, " had a double double with ", v['rebounds'], " rebounds and ", v['assists'], " assists"

                


                
            




class Game:
    def __init__(self, home, away, score):
        self.home = home
        self.away = away
        self.score = score
        pattern = "(\d+)-(\d+)"
        match = re.search(pattern, self.score)
        self.away_score = int(match.group(1))
        self.home_score = int(match.group(2))

    def get_winner(self):
        print self.away_score, self.home_score
        if self.home_score > self.away_score:
            print "Home team won!"
        else:
            print "Away team won!"


        if abs(self.home_score - self.away_score) <= 3:
            print "It was a really close game! Down to the wire"
        elif abs(self.home_score - self.away_score) < 9:
            print "It was a close game!"
        elif abs(self.home_score - self.away_score) < 15:
            print "Normal win"
        else:
            print "Blow out by ", abs(self.home_score - self.away_score), " points"

    def summarize(self):
        self.get_winner()
        self.home.get_outstanding_stats()
        self.away.get_outstanding_stats()
 



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



       



if __name__ == "__main__":

    # TODO: make url out of user input of date and team
    #gameid = sys.argv[1]
    gameid = "201603240BRK"
    html_class = html_parser(gameid)

    start = 0
    lines = html_class.html.splitlines()

    home = Team()
    away = Team()
    home.set_opponent(away)
    away.set_opponent(home)

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
                #print score, summary
            continue

        # TODO: quarter-granularity?
        if "Start of 1st quarter" in line:
            start = 1
            continue
        # TODO: Overtime games
        if "End of 4th quarter" in line:
            print "END OF GAME"
            break


    # Score = away - home
    game = Game(home, away, score)
    game.summarize()
    print '--'
    home.print_stats()
    print '--'
    away.print_stats()


