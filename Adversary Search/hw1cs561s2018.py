import sys
import copy

nodes = 1
utility = 0
depth = 0
nextmove = 0
alpha = - sys.maxint
beta = sys.maxint


class State:
    def __init__(self):
        self.state = [['0' for i in range(8)] for i in range(8)]
        self.player = None
        self.sequence = [0000]
        self.utility = 0
        self.depth = -1
        self.spass = 0
        self.cpass = 0

    def playertype(self, playertype):
        self.player = playertype

    def assign(self, row, rowstate):
        self.state[row] = rowstate

    def totalutility(self, w):
        s = 0
        c = 0
        global player
        w = w.split(',', 7)
        for i in range(8):
            for j in range(8):
                if self.state[i][j][0] == 'S':
                    s += int(self.state[i][j][1]) * int(w[7-i])
                else:
                    if self.state[i][j][0] == 'C':
                        c += int(self.state[i][j][1]) * int(w[i])

            self.utility = s - c

    def action(self, num):
        row1 = num / 1000
        col1 = num / 100 % 10
        row2 = num / 10 % 10
        col2 = num % 10
        str1 = self.state[row2][col2]
        if str1[0] == self.player[0]:                                                   # last row properties
            self.state[row2][col2] = self.player[0] + str(int(str1[1])+1)
        else:
            self.state[row2][col2] = self.state[row1][col1]
        self.state[row1][col1] = '0'
        if abs(row2 - row1) == 2:                                                      # capture
            self.state[(row1 + row2) / 2][(col1 + col2) / 2] = '0'

    def sequencelist(self):
        if self.player == 'Star':
            for i in range(8):
                for j in range(8):
                    if self.state[i][j][0] == 'S' and i != 0:
                        if j > 0 and i > 0:                                              # move left
                            if self.state[i-1][j-1] == '0':
                                self.sequence += [i * 1000 + j * 100 + (i-1) * 10 + j-1]
                            else:
                                if self.state[i-1][j-1][0] == 'S':
                                    if i-1 == 0:
                                        self.sequence += [i * 1000 + j * 100 + (i-1) * 10 + j-1]
                                else:
                                    if j-1 > 0 and i-1 > 0:
                                        if self.state[i-2][j-2] == '0':
                                            self.sequence += [i * 1000 + j * 100 + (i-2) * 10 + j-2]
                                        else:
                                            if self.state[i-2][j-2][0] == 'S':
                                                if i-2 == 0:
                                                    self.sequence += [i * 1000 + j * 100 + (i-2) * 10 + j-2]
                        if j < 7 and i > 0:                                              # move right
                            if self.state[i-1][j+1] == '0':
                                self.sequence += [i * 1000 + j * 100 + (i-1) * 10 + j+1]
                            else:
                                if self.state[i-1][j+1][0] == 'S':
                                    if i-1 == 0:
                                        self.sequence += [i * 1000 + j * 100 + (i-1) * 10 + j+1]
                                else:
                                    if j+1 < 7 and i-1 > 0:
                                        if self.state[i-2][j+2] == '0':
                                            self.sequence += [i * 1000 + j * 100 + (i-2) * 10 + j+2]
                                        else:
                                            if self.state[i-2][j+2][0] == 'S':
                                                if i-2 == 0:
                                                    self.sequence += [i * 1000 + j * 100 + (i-2) * 10 + j+2]

        if self.player == 'Circle':
            for i in range(8):
                for j in range(8):
                    if self.state[i][j][0] == 'C' and i != 7:
                        if j > 0 and i < 7:                                              # move left
                            if self.state[i+1][j-1] == '0':
                                self.sequence += [i * 1000 + j * 100 + (i+1) * 10 + j-1]
                            else:
                                if self.state[i+1][j-1][0] == 'C':
                                    if i+1 == 7:
                                        self.sequence += [i * 1000 + j * 100 + (i+1) * 10 + j-1]
                                else:
                                    if j-1 > 0 and i+1 < 7:
                                        if self.state[i+2][j-2] == '0':
                                            self.sequence += [i * 1000 + j * 100 + (i+2) * 10 + j-2]
                                        else:
                                            if self.state[i+2][j-2][0] == 'C':
                                                if i+2 == 7:
                                                    self.sequence += [i * 1000 + j * 100 + (i+2) * 10 + j-2]
                        if j < 7 and i < 7:                                              # move right
                            if self.state[i+1][j+1] == '0':
                                self.sequence += [i * 1000 + j * 100 + (i+1) * 10 + j+1]
                            else:
                                if self.state[i+1][j+1][0] == 'C':
                                    if i+1 == 7:
                                        self.sequence += [i * 1000 + j * 100 + (i+1) * 10 + j+1]
                                else:
                                    if j+1 < 7 and i+1 < 7:
                                        if self.state[i+2][j+2] == '0':
                                            self.sequence += [i * 1000 + j * 100 + (i+2) * 10 + j+2]
                                        else:
                                            if self.state[i+2][j+2][0] == 'C':
                                                if i+2 == 7:
                                                    self.sequence += [i * 1000 + j * 100 + (i+2) * 10 + j+2]


def MINIMAX(state):
    global utility
    if state.player == 'Star':
        utility = Star(state)
    else:
        utility = Circle(state)


def ALPHABETA(state):
    global utility
    if state.player == 'Star':
        utility = Star(state)
    else:
        utility = Circle(state)


def Star(state):
    global depth, nodes, weight, nextmove, algorithm, alpha, beta
    state.player = 'Star'
    state.sequence = [0000]
    state.depth += 1

    if state.spass == 1 and state.cpass == 1:
        state.totalutility(weight)
        return state.utility

    if state.depth == depth:
        state.totalutility(weight)
        return state.utility

    v = - sys.maxint

    state.sequencelist()
    actionnum = len(state.sequence) - 1
    if actionnum == 0:                                   # no action
        snum = 0
        for i in range(8):
            for j in range(8):
                if state.state[i][j][0] == 'S':
                    snum += 1
        if snum == 0:                                    # no more pieces on the board
            state.totalutility(weight)
            return state.utility
        else:
            nodes += 1                                    # pass
            state.spass = 1
            if state.depth == 0:
                nextmove = 9999
            v = max(v, Circle(state))
            if algorithm == 'ALPHABETA':
                if v >= beta:
                    return v
                alpha = max(alpha, v)

    else:
        state.spass = 0
        if state.depth == 0:                             # find next move
            u = []
            for i in range(1, actionnum + 1):
                nodes += 1
                newstate = copy.deepcopy(state)
                newstate.action(state.sequence[i])
                u.append(Circle(newstate))
                nextmove = state.sequence[u.index(max(u)) + 1]
                v = max(v, max(u))
                if algorithm == 'ALPHABETA':
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
        else:
            for i in range(1, actionnum + 1):
                nodes += 1
                newstate = copy.deepcopy(state)
                newstate.action(state.sequence[i])
                v = max(v, Circle(newstate))
                if algorithm == 'ALPHABETA':
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
    return v


def Circle(state):
    global depth, nodes, weight, nextmove, algorithm, alpha, beta
    state.player = 'Circle'
    state.sequence = [0000]
    state.depth += 1

    if state.spass == 1 and state.cpass == 1:
        state.totalutility(weight)
        return state.utility

    if state.depth == depth:
        state.totalutility(weight)
        return state.utility

    v = sys.maxint

    state.sequencelist()
    actionnum = len(state.sequence) - 1
    if actionnum == 0:                                   # no action
        cnum = 0
        for i in range(8):
            for j in range(8):
                if state.state[i][j][0] == 'C':
                    cnum += 1
        if cnum == 0:                                    # no more pieces on the board
            state.totalutility(weight)
            return state.utility
        else:
            nodes += 1                                   # pass
            state.cpass = 1
            if state.depth == 0:
                nextmove = 9999
            v = min (v, Star(state))
            if algorithm == 'ALPHABETA':
                if v <= alpha:
                    return v
                beta = min(beta, v)
    else:
        state.cpass = 0
        if state.depth == 0:                             # find next move
            u = []
            for i in range(1, actionnum + 1):
                nodes += 1
                newstate = copy.deepcopy(state)
                newstate.action(state.sequence[i])
                u.append(Star(newstate))
                nextmove = state.sequence[u.index(min(u)) + 1]
                v = min(v, min(u))
                if algorithm == 'ALPHABETA':
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
        else:
            for i in range(1, actionnum + 1):
                nodes += 1
                newstate = copy.deepcopy(state)
                newstate.action(state.sequence[i])
                v = min(v, Star(newstate))
                if algorithm == 'ALPHABETA':
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
    return v


if __name__ == '__main__':
    initialstate = State()

    fin = open("input.txt", "r")                               # read input
    player = fin.readline().rstrip('\n')
    initialstate.player = player
    algorithm = fin.readline().rstrip('\n')
    depth = int(fin.readline().rstrip('\n'))
    for i in range(8):
        string = fin.readline().rstrip('\n')
        initialstate.assign(i, string.split(','))
    weight = fin.readline().rstrip('\n')

    fin.close()

    startstate = copy.deepcopy(initialstate)
    if algorithm == 'MINIMAX':
        MINIMAX(startstate)
    else:
        ALPHABETA(startstate)

    if nextmove == 9999:                                         # get next move
        move = 'pass'
    else:
        move = chr(9 - nextmove / 1000 - 1 + 64 ) + str(nextmove / 100 %10 + 1) + '-' \
        + chr(9 - nextmove / 10 % 10 - 1 + 64 ) + str(nextmove %10 + 1)

    myopicstate = copy.deepcopy(initialstate)                  # count myopic_utility
    if nextmove != 9999:
        myopicstate.action(nextmove)
    myopicstate.totalutility(weight)
    myopic_utility = myopicstate.utility
    if player == 'Circle':
        myopic_utility = - myopic_utility

    if player == 'Circle':
        utility = - utility

    fout = open('output.txt', 'w')

    print >> fout, move
    print >> fout, myopic_utility
    print >> fout, utility
    print >> fout, nodes

    fout.close()




