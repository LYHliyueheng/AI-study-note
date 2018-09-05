import numpy as np
import sys
import time


if __name__ == '__main__':
    starttime = time.time()
    fin = open("input.txt", "r")
    size = fin.readline().rstrip('\n').split(',')
    rows = int(size[0])
    cols = int(size[1])
    walls = int(fin.readline().rstrip('\n'))
    walllist = []
    for i in range(walls):
        walllist.append(fin.readline().rstrip('\n').split(','))
    terminals = int(fin.readline().rstrip('\n'))
    terminallist = []
    for i in range(terminals):
        terminallist.append(fin.readline().rstrip('\n').split(','))
    transmod = fin.readline().rstrip('\n').split(',')
    pwalk = float(transmod[0])
    prun = float(transmod[1])
    rewards = fin.readline().rstrip('\n').split(',')
    rwalk = float(rewards[0])
    rrun = float(rewards[1])
    gamma = float(fin.readline().rstrip('\n'))

    fin.close()

    tl = []
    wl = []

    grid = np.zeros((rows, cols))

    for i in terminallist:                                          # set utility of terminals
        grid[rows - int(i[0]), int(i[1]) - 1] = float(i[2])
        tl.append((rows - int(i[0])) * cols + int(i[1]) - 1)
    for i in walllist:                                              # set utility of walls: -maxint
        grid[rows - int(i[0]), int(i[1]) - 1] = -sys.maxint
        wl.append((rows - int(i[0])) * cols + int(i[1]) - 1)

    # transmat = np.zeros((8, 8), dtype=np.float64)
    # transmat[0, 0] = transmat[1, 1] = transmat[2, 2] = transmat[3, 3] = pwalk
    # transmat[4, 4] = transmat[5, 5] = transmat[6, 6] = transmat[7, 7] = prun
    # transmat[2, 0] = transmat[3, 0] = transmat[2, 1] = transmat[3, 1] = transmat[0, 2] = transmat[1, 2] = transmat[
    #     0, 3] = transmat[1, 3] = 0.5 * (1 - pwalk)
    # transmat[6, 4] = transmat[7, 4] = transmat[6, 5] = transmat[7, 5] = transmat[4, 6] = transmat[5, 6] = transmat[
    #     4, 7] = transmat[5, 7] = 0.5 * (1 - prun)

    # statemat = np.empty((rows*cols, 8), object)
    # for i in range(rows*cols):
    #     statemat[i] = np.array(Nextstate(rows, cols, grid, i))

    iteration = 0
    Boolean = 0

    while Boolean == 0:

        walkup = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            if i == 0:
                walkup[i] = grid[0]
            else:
                walkup[i] = grid[i - 1]
        for i in wl:
            if i / cols != rows - 1:
                walkup[i / cols + 1, i % cols] = grid[i / cols + 1, i % cols]

        walkdown = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            if i == rows - 1:
                walkdown[i] = grid[rows - 1]
            else:
                walkdown[i] = grid[i + 1]
        for i in wl:
            if i / cols != 0:
                walkdown[i / cols - 1, i % cols] = grid[i / cols - 1, i % cols]

        walkleft = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            l = list(grid[i][:cols - 1])
            l.insert(0, grid[i][0])
            walkleft[i] = np.array(l)
        for i in wl:
            if i % cols != cols - 1:
                walkleft[i / cols, i % cols + 1] = grid[i / cols, i % cols + 1]

        walkright = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            l = list(grid[i][1:])
            l.append(grid[i][cols - 1])
            walkright[i] = np.array(l)
        for i in wl:
            if i % cols != 0:
                walkright[i / cols, i % cols - 1] = grid[i / cols, i % cols - 1]

        runup = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            if i == 0:
                runup[i] = grid[0]
            elif i == 1:
                runup[i] = grid[1]
            else:
                runup[i] = grid[i - 2]
        for i in wl:
            if i / cols != rows - 1:
                if i / cols == rows - 2:
                    runup[i / cols + 1, i % cols] = grid[i / cols + 1, i % cols]
                else:
                    runup[i / cols + 1, i % cols] = grid[i / cols + 1, i % cols]
                    runup[i / cols + 2, i % cols] = grid[i / cols + 2, i % cols]

        rundown = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            if i == rows - 1:
                rundown[i] = grid[rows - 1]
            elif i == rows - 2:
                rundown[i] = grid[rows - 2]
            else:
                rundown[i] = grid[i + 2]
        for i in wl:
            if i / cols != 0:
                if i / cols == 1:
                    rundown[i / cols - 1, i % cols] = grid[i / cols - 1, i % cols]
                else:
                    rundown[i / cols - 1, i % cols] = grid[i / cols - 1, i % cols]
                    rundown[i / cols - 2, i % cols] = grid[i / cols - 2, i % cols]

        runleft = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            l = list(grid[i][:cols - 2])
            l.insert(0, grid[i][1])
            l.insert(0, grid[i][0])
            runleft[i] = np.array(l)
        for i in wl:
            if i % cols != cols - 1:
                if i % cols == cols - 2:
                    runleft[i / cols, i % cols + 1] = grid[i / cols, i % cols + 1]
                else:
                    runleft[i / cols, i % cols + 1] = grid[i / cols, i % cols + 1]
                    runleft[i / cols, i % cols + 2] = grid[i / cols, i % cols + 2]

        runright = np.empty((rows, cols), dtype=np.float64)
        for i in range(rows):
            l = list(grid[i][2:])
            l.append(grid[i][cols - 2])
            l.append(grid[i][cols - 1])
            runright[i] = np.array(l)
        for i in wl:
            if i % cols != 0:
                if i % cols == 1:
                    runright[i / cols, i % cols - 1] = grid[i / cols, i % cols - 1]
                else:
                    runright[i / cols, i % cols - 1] = grid[i / cols, i % cols - 1]
                    runright[i / cols, i % cols - 2] = grid[i / cols, i % cols - 2]

        actionlist = [walkup, walkdown, walkleft, walkright, runup, rundown, runleft, runright]

        a = []
        b = []
        c = np.zeros((8, rows*cols))

        for i in range(0, 4):
            a.append(actionlist[i] * gamma + rwalk)
        for i in range(4, 8):
            a.append(actionlist[i] * gamma + rrun)

        b.append(a[0] * pwalk + a[2] * 0.5 * (1 - pwalk) + a[3] * 0.5 * (1 - pwalk))
        b.append(a[1] * pwalk + a[2] * 0.5 * (1 - pwalk) + a[3] * 0.5 * (1 - pwalk))
        b.append(a[2] * pwalk + a[0] * 0.5 * (1 - pwalk) + a[1] * 0.5 * (1 - pwalk))
        b.append(a[3] * pwalk + a[0] * 0.5 * (1 - pwalk) + a[1] * 0.5 * (1 - pwalk))
        b.append(a[4] * prun + a[6] * 0.5 * (1 - prun) + a[7] * 0.5 * (1 - prun))
        b.append(a[5] * prun + a[6] * 0.5 * (1 - prun) + a[7] * 0.5 * (1 - prun))
        b.append(a[6] * prun + a[4] * 0.5 * (1 - prun) + a[5] * 0.5 * (1 - prun))
        b.append(a[7] * prun + a[4] * 0.5 * (1 - prun) + a[5] * 0.5 * (1 - prun))

        for i in range(8):
            c[i] = np.reshape(b[i], (1, rows*cols))

        d = c.max(axis=0)
        e = np.reshape(d, (rows, cols))
        for i in wl:
            e[i/cols, i%cols] = grid[i/cols, i%cols]
        for i in tl:
            e[i/cols, i%cols] = grid[i/cols, i%cols]
        if (e == grid).all():
            Boolean = 1
        # if iteration == 1:
        #     break
        grid = np.array(e)
        iteration += 1

        # if time.time()-starttime > 5:
        #     break
    walkup = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        if i == 0:
            walkup[i] = grid[0]
        else:
            walkup[i] = grid[i - 1]
    for i in wl:
        if i / cols != rows - 1:
            walkup[i / cols + 1, i % cols] = grid[i / cols + 1, i % cols]

    walkdown = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        if i == rows - 1:
            walkdown[i] = grid[rows - 1]
        else:
            walkdown[i] = grid[i + 1]
    for i in wl:
        if i / cols != 0:
            walkdown[i / cols - 1, i % cols] = grid[i / cols - 1, i % cols]

    walkleft = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        l = list(grid[i][:cols - 1])
        l.insert(0, grid[i][0])
        walkleft[i] = np.array(l)
    for i in wl:
        if i % cols != cols - 1:
            walkleft[i / cols, i % cols + 1] = grid[i / cols, i % cols + 1]

    walkright = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        l = list(grid[i][1:])
        l.append(grid[i][cols - 1])
        walkright[i] = np.array(l)
    for i in wl:
        if i % cols != 0:
            walkright[i / cols, i % cols - 1] = grid[i / cols, i % cols - 1]

    runup = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        if i == 0:
            runup[i] = grid[0]
        elif i == 1:
            runup[i] = grid[1]
        else:
            runup[i] = grid[i - 2]
    for i in wl:
        if i / cols != rows - 1:
            if i / cols == rows - 2:
                runup[i / cols + 1, i % cols] = grid[i / cols + 1, i % cols]
            else:
                runup[i / cols + 1, i % cols] = grid[i / cols + 1, i % cols]
                runup[i / cols + 2, i % cols] = grid[i / cols + 2, i % cols]

    rundown = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        if i == rows - 1:
            rundown[i] = grid[rows - 1]
        elif i == rows - 2:
            rundown[i] = grid[rows - 2]
        else:
            rundown[i] = grid[i + 2]
    for i in wl:
        if i / cols != 0:
            if i / cols == 1:
                rundown[i / cols - 1, i % cols] = grid[i / cols - 1, i % cols]
            else:
                rundown[i / cols - 1, i % cols] = grid[i / cols - 1, i % cols]
                rundown[i / cols - 2, i % cols] = grid[i / cols - 2, i % cols]

    runleft = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        l = list(grid[i][:cols - 2])
        l.insert(0, grid[i][1])
        l.insert(0, grid[i][0])
        runleft[i] = np.array(l)
    for i in wl:
        if i % cols != cols - 1:
            if i % cols == cols - 2:
                runleft[i / cols, i % cols + 1] = grid[i / cols, i % cols + 1]
            else:
                runleft[i / cols, i % cols + 1] = grid[i / cols, i % cols + 1]
                runleft[i / cols, i % cols + 2] = grid[i / cols, i % cols + 2]

    runright = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        l = list(grid[i][2:])
        l.append(grid[i][cols - 2])
        l.append(grid[i][cols - 1])
        runright[i] = np.array(l)
    for i in wl:
        if i % cols != 0:
            if i % cols == 1:
                runright[i / cols, i % cols - 1] = grid[i / cols, i % cols - 1]
            else:
                runright[i / cols, i % cols - 1] = grid[i / cols, i % cols - 1]
                runright[i / cols, i % cols - 2] = grid[i / cols, i % cols - 2]

    actionlist = [walkup, walkdown, walkleft, walkright, runup, rundown, runleft, runright]
    a = []
    b = []
    c = np.zeros((8, rows * cols), dtype=np.float64)

    for i in range(0, 4):
        a.append(actionlist[i] * gamma + rwalk)
    for i in range(4, 8):
        a.append(actionlist[i] * gamma + rrun)

    b.append(a[0] * pwalk + a[2] * 0.5 * (1 - pwalk) + a[3] * 0.5 * (1 - pwalk))
    b.append(a[1] * pwalk + a[2] * 0.5 * (1 - pwalk) + a[3] * 0.5 * (1 - pwalk))
    b.append(a[2] * pwalk + a[0] * 0.5 * (1 - pwalk) + a[1] * 0.5 * (1 - pwalk))
    b.append(a[3] * pwalk + a[0] * 0.5 * (1 - pwalk) + a[1] * 0.5 * (1 - pwalk))
    b.append(a[4] * prun + a[6] * 0.5 * (1 - prun) + a[7] * 0.5 * (1 - prun))
    b.append(a[5] * prun + a[6] * 0.5 * (1 - prun) + a[7] * 0.5 * (1 - prun))
    b.append(a[6] * prun + a[4] * 0.5 * (1 - prun) + a[5] * 0.5 * (1 - prun))
    b.append(a[7] * prun + a[4] * 0.5 * (1 - prun) + a[5] * 0.5 * (1 - prun))

    for i in range(8):
        c[i] = np.reshape(b[i], (1, rows * cols))

    d = c.argmax(axis=0)
    # iteration = 0
    # count = 1
    # cigma = 0.1
    # changed = []
    # #if True:
    # while count > 0:
    #     a = statemat * gamma              # gamma * utility
    #     b = a[:, 0:4] + rwalk             # + R(s,a)
    #     c = a[:, 4:8] + rrun
    #     d = np.concatenate((b, c), axis=1)
    #     e = d.dot(transmat)
    #     f = e.max(axis=1)
    #     count = 0
    #
    #     if iteration > 10 and len(changed) < rows*cols/10:
    #         ll = Changed(changed, tl, wl, rows, cols)
    #     changed = []
    #     for i in ll:
    #         if abs(f[i] - grid[i / cols, i % cols].val)>cigma:
    #         #if f[i] != grid[i/cols, i%cols].val:
    #             grid[i/cols, i%cols].val = f[i]
    #             count +=1
    #             changed.append(i)
    #     iteration += 1
    #
    # # for i in range(rows*cols):
    # #     for j in range(8):
    # #         statemat[i, j] = statemat[i, j].val
    #
    # # tempmat = np.zeros((rows * cols, 8), np.float64)
    # # for i in range(rows * cols):
    # #     for j in range(8):
    # #         tempmat[i, j] = statemat[i, j].val
    # a = statemat * gamma  # gamma * utility
    # b = a[:, 0:4] + rwalk  # + R(s,a)
    # c = a[:, 4:8] + rrun
    # d = np.concatenate((b, c), axis=1)
    # e = d.dot(transmat)
    # h = e.argmax(axis=1)
    # # g = statemat.dot(transmat)
    # # h = g.argmax(axis=1)
    #
    action = ["Walk Up", "Walk Down", "Walk Left", "Walk Right", "Run Up", "Run Down", "Run Left", "Run Right"]

    fout = open('output.txt', 'w')
    for i in range(rows):
        line = ''
        for j in range(cols):
            if tl.count(i*cols + j)==1:
                line = line + "Exit,"
            elif wl.count(i*cols + j) ==1:
                line = line + "None,"
            else:
                line = line + action[d[i*cols + j]] + ','
        print >> fout, line[0:len(line) - 1]

    # print grid
    # print rows
    # print cols
    # print walllist
    # print terminallist
    # print pwalk
    # print prun
    # print rwalk
    # print rrun
    # print gamma
    # print walkup
    # print walkdown
    #
    # print walkleft
    # print walkright

    # print ll
    # print count
    # print d
    #print iteration
    # print a
    # print d
    # print e
    # print f
    #print h

    #print g
    # print a[0]
    # print b[0]
    # print c[0]
    # print d
    # print iteration
    #
    #
    # print grid
    # print e
    #
    #
    #
    # print time.time()-starttime

