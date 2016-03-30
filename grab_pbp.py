import string
import re
import sys
from data import html_parser
from game import Game
from team import Team

#TODO Ejections
#TODO Get runs
#TODO quarterly player performance?


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
    #if len(sys.argv) < 2:
    #    print 'Enter game_id: YYYYMMDD0TID (note the 0 inbetween date and TeamID)'
    #    sys.exit(1)
    #gameid = sys.argv[1]

    gameid = "201603240BRK"
    html_class = html_parser(gameid)

    start = 0
    pbp_lines = html_class.pbp_html.splitlines()
    game_lines = html_class.game_html.splitlines()

    home = Team()
    away = Team()
    home.set_opponent(away)
    away.set_opponent(home)
    game = Game()

    # TODO: Better design?
    for i in range(len(pbp_lines)):
        line = pbp_lines[i]
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
            #continue

        if "<th>Time</th>" in line and start == 0:
            away.get_teamname(pbp_lines[i+1])
            home.get_teamname(pbp_lines[i+3])
            print away.team_name, "VS", home.team_name
        if "Start of 1st quarter" in line:
            start = 1
            continue
        if "End of 1st quarter" in line:
            game.set_qtr_score(1, score)
        if "End of 2nd quarter" in line:
            game.set_qtr_score(2, score)
        if "End of 3rd quarter" in line:
            game.set_qtr_score(3, score)
        if "End of 4th quarter" in line:
            # TODO: Overtime games
            game.set_qtr_score(4, score)
            print "END OF GAME"
            break

    for i in range(len(game_lines)):
        line = game_lines[i]
        if 'Lost' in line or 'Won' in line:
            away.get_streak(line)
            home.get_streak(game_lines[i+3])
            break

    # Score = away - home
    game.set_teams(home, away, score)
    game.summarize()
    print '--'
    home.print_stats()
    print '--'
    away.print_stats()
    for k, v in game.home_quarterly.iteritems():
        print k, v
    for k, v in game.away_quarterly.iteritems():
        print k, v
    


