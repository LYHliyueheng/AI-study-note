import sys
import copy
import time

start = 0
TeamNum = 0
Groupnum = 0
iterationNum = 0
EUingroups = []
TeamName = []
EUlist = []                                                       # list of European teams' name


def backtracking(assignment, csp, domain):
    global TeamNum, iterationNum, Groupnum, EUingroups, EUlist, start
    end = time.clock()
    if end - start > 150:
        return False
    if len(assignment) == TeamNum:
        return assignment
    iterationNum += 1

    isEU = 0
    team = selectvar(assignment, domain, csp)
    if EUlist.count(TeamName[team]) == 1:
        isEU = 1
    for group in orderval(team, domain, assignment, csp):
        assignment[team] = group

        if isEU == 1:
            EUingroups[group] += 1
        # if EUingroups[group] > 2:
        #     del assignment[team]
        #     EUingroups[group] -= 1
        #     continue

        # EUconstraint = False
        # for i in range(Groupnum):
        #     EUcount = 0
        #     for j in assignment:
        #         if assignment.get(j) == i and EUlist.count(TeamName[j]) == 1:
        #             EUcount += 1
        #     if EUcount > 2:
        #         EUconstraint = True
        #         break
        # if EUconstraint == True:
        #      del assignment[team]
        #      continue

        copyDomain = copy.deepcopy(domain)
        copyDomain[team] = [group]
        if AC3(csp, copyDomain, assignment):
            result = backtracking(assignment, csp, copyDomain,)
            if result:
                return result
        del assignment[team]
        if isEU == 1:
            EUingroups[group] -= 1
    return False


def selectvar(assignment, domain, csp):
    global TeamNum
    valueNum = sys.maxint
    MRV = 0
    for i in range(TeamNum):
        if len(domain[i]) <= valueNum and assignment.get(i) is None:
            if len(domain[i]) == valueNum:                                         # break tie
                num1 = 0
                num2 = 0
                for j in range(len(csp[i])):
                    if csp[i][j] > 0 and assignment.get(j) is None:
                        if csp[i][j] == 5:
                            num1 -= 0.5
                        num1 += 1
                for k in range(len(csp[MRV])):
                    if csp[MRV][k] > 0 and assignment.get(k) is None:
                        if csp[i][j] == 5:
                            num1 -= 0.5
                        num2 += 1
                if num1 > num2:
                    MRV = i
                    valueNum = len(domain[i])
            else:
                MRV = i
                valueNum = len(domain[i])
    return MRV


def orderval(team, domain, assignment, csp):
    global Groupnum, EUingroups
    if len(assignment) == 0:                          # the first variable only be assigned to the first group
        return [0]
    order = []

    connum = []                                       # be assigned to least constraining value
    for i in assignment:
        for j in range(Groupnum):
            connum.append(0)
            if assignment.get(i) == j and csp[team][i] > 0:
                connum[j] += 1
                if csp[team][i] == 5 and EUingroups[j] < 2:
                    connum[j] -= 1
    for i in domain[team]:
        order.append((i, connum[i]))

    # assigned = assignment.values()                    # be assigned to the group which has least teams
    # for i in domain[team]:
    #     order.append((i, assigned.count(i)))

    order.sort(key=lambda x:x[1])
    orders = []
    for i in range(len(order)):
        orders.append(order[i][0])
    return orders


def AC3(csp, domain, assignment):
    global TeamNum
    queue = []
    for i in range(TeamNum):
        for j in range(TeamNum):
            if csp[i][j] > 0 and len(domain[j]) == 1 and domain[i].count(domain[j][0]) == 1:
                queue.append((i, j))
    while len(queue) != 0:
        arc = queue.pop()
        if revise(csp, domain, assignment, arc):
            if len(domain[arc[0]]) == 0:                # domain become empty after revise
                return False
            if len(domain[arc[0]]) == 1:                # only right part has 1 left in domain can be revised
                for k in range(TeamNum):
                    if csp[k][arc[0]] > 0 and domain[k].count(domain[arc[0]][0]) == 1:
                        queue.append((k, arc[0]))
    return True


def revise(csp, domain, assignment, arc):
    global EUlist, TeamName
    left = domain[arc[0]]
    right = domain[arc[1]]
    revised = False

    count = 0                                                   # the number of European teams in right's group
    # if len(right) >= 2:                                         # only right part has 1 left in domain can be revised
    #     return revised
    if csp[arc[0]][arc[1]] == 5:                                # the constraint caused only by both coming from Europe
        if assignment.get(arc[0]) == right[0]:
            if assignment.get(arc[1]) is None:
                if EUingroups[right[0]] <= 1:
                    return revised
            else:
                if EUingroups[right[0]] <= 2:
                    return revised
        if assignment.get(arc[0]) is None:
            if assignment.get(arc[1]) is None:
                if EUingroups[right[0]] == 0:
                    return revised
            else:
                if EUingroups[right[0]] <= 1:
                    return revised

        # for j in assignment:
        #     if assignment.get(j) == right[0] and j != arc[1] and j != arc[0]:   # other teams in the same group as right
        #         if EUlist.count(TeamName[j]) == 1:              # is a European team
        #             count += 1
        # if count == 0:                                          # no other European teams
        #     return revised

    for i in left:
        if i == right[0]:
            left.remove(i)
            revised = True
    return revised


if __name__ == '__main__':

    start = time.clock()
    finalAssignment = True
    fin = open("input6.txt", "r")                                                      # read input
    Groupnum = int(fin.readline().rstrip('\n').rstrip('\r'))
    Potnum = int(fin.readline().rstrip('\n').rstrip('\r'))
    PotCon = []
    for i in range(Potnum):
        string = fin.readline().rstrip('\n').rstrip('\r')
        Potlist = string.split(',')
        if len(Potlist) > Groupnum:                             # number of teams in each pot can't beyond group number
            finalAssignment = False
        PotCon.append(Potlist)
        listiter = iter(Potlist)
        for j in range(len(Potlist)):
            TeamName.append(listiter.next())
            TeamNum += 1

# only EU constraint : 5   both EU constraint and Pots constraint : 6
    CSP = [[0 for i in range(TeamNum)] for i in range(TeamNum)]                       # construct csp
    for i in range(Potnum):
        for j in range(len(PotCon[i])):
            if j < len(PotCon[i]) - 1:
                for k in range(j + 1, len(PotCon[i])):
                    x = TeamName.index(PotCon[i][j])
                    y = TeamName.index(PotCon[i][k])
                    CSP[x][y] += 1
                    CSP[y][x] += 1

    for i in range(6):
        string = fin.readline().rstrip('\n').rstrip('\r')
        Pos = string.find(':')
        Continentallist = string[Pos + 1:].split(',')
        if string[0:Pos] == 'UEFA':
            EUlist = copy.deepcopy(Continentallist)
            if len(Continentallist) > 2 * Groupnum:       # number of teams in UEFA can't beyond group number * 2
                finalAssignment = False
            a = 5
        else:
            if len(Continentallist) > Groupnum:       # number of teams in other continent can't beyond group number
                finalAssignment = False
            a = 1
        if Continentallist[0] != 'None':
            for j in range(len(Continentallist)):
                if j < len(Continentallist) - 1:
                    for k in range(j + 1, len(Continentallist)):
                        x = TeamName.index(Continentallist[j])
                        y = TeamName.index(Continentallist[k])
                        CSP[x][y] += a
                        CSP[y][x] += a

    fin.close()

    judgement = 'No'
    initialAssignment = {}
    initialDomain = []
    for i in range(TeamNum):
        group = []
        for j in range(Groupnum):
            group.append(j)
        initialDomain.append(group)
    for i in range(Groupnum):
        EUingroups.append(0)

    if finalAssignment is True:
        finalAssignment = backtracking(initialAssignment, CSP, initialDomain)
    if finalAssignment is not False:
        judgement = 'Yes'
        groups = []
        for i in range(Groupnum):
            group = []
            for j in finalAssignment:
                if finalAssignment.get(j) == i:
                    group.append(j)
            groups.append(group)
        for i in range(Groupnum):
            for j in range(len(groups[i])):
                groups[i][j] = TeamName[groups[i][j]]

    # print Groupnum
    # print TeamNum
    # print TeamName
    # for i in range(TeamNum):
    #     print "%d:" % (i), CSP[i]
    # print finalAssignment
    # print iterationNum
    # print EUingroups
    # print EUlist

    fout = open('output.txt', 'w')

    print >> fout, judgement
    if judgement == 'Yes':
        for i in range(Groupnum):
            if i >= len(groups):
                print >> fout, 'None'
            line = ''
            for j in groups[i]:
                line = line + j + ','
            print >> fout, line[0:len(line)-1]

    fout.close()

