import re

class Team:
    def __init__(self):
        # TODO: Get team names
        #self.team_name = name
        self.players = dict()

    def set_opponent(self, opponent):
        self.opponent = opponent

    def get_teamname(self, name_line):
        pattern = "^\<th\>(\w+)\<\/th\>.*$"
        match = re.search(pattern, name_line)
        self.team_name = match.group(1)

       
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
            pattern = "^(\d+-\d+)\s\+?\d?([A-Z]\.\s\w+-?\w+)\smakes\s(\d-pt|free throw).*$"
        else:
            pattern = "^(\d+-\d+)\s\+?\d?([A-Z]\.\s\w+-?\w+)\smisses\s(\d-pt|free throw).*$"
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
        pattern = "^.*rebound by ([A-Z]\.\s\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'rebounds', 1)
        else:
            if 'rebound by Team' not in line:
                print line
                print 'rebound error'
                sys.exit()

    def assist_tracker(self, line):
        pattern = "^.*\(assist by ([A-Z]\.\s\w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'assists', 1)
        else:
            print line
            print 'assist error'
            sys.exit()

    def turnover_tracker(self, line):
        pattern = "^.*Turnover by ([A-Z]\. \w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'turnovers', 1)
        else:
            if 'Turnover by Team' not in line:
                print line
                print 'turnover error'
                sys.exit()

    def steal_tracker(self, line):
        pattern = "^.*steal by ([A-Z]\. \w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'steals', 1)
        else:
            print line
            print 'steal error'
            sys.exit()

    def block_tracker(self, line):
        pattern = "^.*\(block by ([A-Z]\. \w+-?\w+).*$"
        match = re.search(pattern, line)

        if match:
            self.update_stats(match.group(1), 'blocks', 1)
        else:
            print line
            print 'block error'
            sys.exit()

    def foul_tracker(self, line):
        # flag = 1: defensive, 0: offensive
        pattern = "^.*foul by ([A-Z]\. \w+-?\w+).*$"

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
        # Triple Doubles
        # Double Doubles
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

            if v['FGA'] > 12 and v['FG']/float(v['FGA']) > 0.7:
                print k, " made ", v['FG'], " out of ", v['FGA'], " shots"
            if v['3PA'] >= 9 and v['3P']/float(v['3PA']) >= 0.5:
                print k, " made ", v['3P'], " out of ", v['3PA'], " shots"

                
    def get_streak(self, line):
        if "Won" in line:
            won = 1
            pattern = "^.*\(Won (\d+)\).*$"
        elif "Lost" in line:
            won = 0
            pattern = "^.*\(Lost (\d+)\).*$"
        else:
            'Shouldnt be here, error in get_streak'
            sys.exit(0)

        match = re.match(pattern, line)
        self.streak = int(match.group(1))
        if won == 0:
            self.streak = -1 * self.streak

        print self.team_name, "is on a ", self.streak, "winning streak"

 
