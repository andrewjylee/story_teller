import urllib2
import string
import re

" Fix last line? "
"J. McRae makes 3-pt shot from 22 ft (assist by T. Thompson)+395-104 "

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
    print ''
    " Get score out first "
    #match = re.search('">(.+?)</td>', line)

    #score = ''
    #if match:
    #    score = match.group(1)
    #line = re.sub(score, '', line)

    match = re.search("^.*(\d+)\-(\d+).*$", line)
    #regex = re.compile("^.*[0-9]+\-[0-9]+.*$")
    #if regex.match(line):
    #    print 'here'
    score = ''
    if match:
        print 'here'
        score = match.group(1)

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
    
 
    score = ''
    ret = re.sub('&nbsp;', '', ret)
    return score, ret

html = urllib2.urlopen("http://www.basketball-reference.com/boxscores/pbp/201603240BRK.html").read()
start = 0
lines = html.splitlines()
for i in range(len(lines)):
    line = lines[i]
    if start:
        if filter(line):
            possession = line
            side = which_team(possession)
            if side == 1:
                print clean_up(line)
            elif side == 2:
                print clean_up(line)
            else:
                print 'should never be here?'
        continue

    if "Start of 1st quarter" in line:
        start = 1
        continue
    if "End of 4th quarter" in line:
        print "END OF GAME"
        break


