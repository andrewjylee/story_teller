import re

class Game:
    def __init__(self):#, home, away, score):

        self.home_quarterly = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        self.away_quarterly = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    def set_teams(self, home, away, score):
        self.home = home
        self.away = away
        self.score = score
        pattern = "(\d+)-(\d+)"
        match = re.search(pattern, self.score)
        self.away_score = int(match.group(1))
        self.home_score = int(match.group(2))

    def set_qtr_score(self, qtr, score):
        pattern = "(\d+)-(\d+)"
        match = re.search(pattern, score)
        self.away_quarterly[qtr] = int(match.group(1)) - sum([self.away_quarterly[x] for x in range(qtr)])
        self.home_quarterly[qtr] = int(match.group(2)) - sum([self.home_quarterly[x] for x in range(qtr)])


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
        #TODO: add quarterly info
        self.home.get_outstanding_stats()
        self.away.get_outstanding_stats()
 
