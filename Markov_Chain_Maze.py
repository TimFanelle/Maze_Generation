import shelve
import tkinter as tk
from tkinter import Canvas
import GeneticPruning as CC
import copy
import random
# from PIL import Image, ImageDraw
import time
import backtracking_maze as bm


class Wall:
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy

    def setX(self, xx):
        self.x = xx

    def setY(self, yy):
        self.y = yy

    def getX(self):
        return self.x

    def getY(self):
        return self.y


def fillWalls(mzz):
    mz = []
    hor = []
    ver = []
    for y in mzz:
        for x in y:
            if x.right:
                ver.append(Wall(x.col+1, x.row))
            if x.down:
                hor.append(Wall(x.col, x.row+1))
    for y in range(len(mzz)):
        hor.append(Wall(y, 0))
    for y in range(len(mzz[0])):
        ver.append(Wall(0, y))
    '''
    p = 0
    while p < hors:
        q = 0
        while q < vers:
            hor.append(Wall(p, q))
            q += 1
        p += 1
    p = 0
    while p < vers:
        q = 0
        while q < hors:
            ver.append(Wall(q, p))
            q += 1
        p += 1
    mz.append(hor)
    mz.append(ver)
    mY = max(mz[0], key=lambda x: x.getY()).getY() + 1
    mX = max(mz[0], key=lambda x: x.getX()).getX() + 1
    for h in range(mY):
        mz[0].append(Wall(h, mY))
    for h in range(mX):
        mz[1].append(Wall(mX, h))
    '''
    mz.append(hor)
    mz.append(ver)
    return mz


def fillWallsX(inns):
    mz = []
    hor = []
    ver = []
    try:
        inn = inns.maz
    except AttributeError:
        inn = inns
    for y in range(len(inn)):
        for x in range(len(inn[y])):
            if inn[y][x].walls[0]:
                ver.append(Wall(inn[y][x].cords[0] + 1, inn[y][x].cords[1]))
            if inn[y][x].walls[1]:
                hor.append(Wall(inn[y][x].cords[0], inn[y][x].cords[1] + 1))
    for y in range(len(inn)):
        hor.append(Wall(y, 0))
    for y in range(1, len(inn[0])):
        ver.append(Wall(0, y))
    mz.append(hor)
    mz.append(ver)
    return mz


def drawGrid(mzz, cv):
    for _ in mzz[0]:
        cv.create_line(_.getX() * 15 + 3, _.getY() * 15 + 3, (_.getX() + 1) * 15 + 3, _.getY() * 15 + 3)
    for _ in mzz[1]:
        cv.create_line(_.getX() * 15 + 3, _.getY() * 15 + 3, _.getX() * 15 + 3, (_.getY() + 1) * 15 + 3)


def showMaze(mzz):
    mz = fillWalls(mzz)
    window = tk.Tk()
    window.title("Maze Representation")
    xxx = (len(mz[0])*8)
    yyy = (len(mz[1])*8)
    #siz = str(xxx) + "x" + str(yyy)
    #print(siz)
    window.geometry("350x350")
    #f = Frame()
    #f.pack(fill=tk.BOTH, expand=True)
    cv = Canvas(window, bg='green')
    cv.delete("all")
    #cv.mailbox_frame = Frame(cv, bg="green")
    #cv.create_window((0, 0), window=cv.mailbox_frame)
    drawGrid(mz, cv)
    cv.config(width=xxx, height=yyy)
    cv.pack(side=tk.LEFT, anchor=tk.NW)
    window.mainloop()


def showMazeX(inn):
    mz = fillWallsX(inn)
    window = tk.Tk()
    window.title("Maze Representation")
    xxx = (len(mz[0]) * 8)
    yyy = (len(mz[1]) * 8)
    # siz = str(xxx) + "x" + str(yyy)
    # print(siz)
    window.geometry("800x800")
    # f = Frame()
    # f.pack(fill=tk.BOTH, expand=True)
    cv = Canvas(window, bg='green')
    cv.delete("all")
    # cv.mailbox_frame = Frame(cv, bg="green")
    # cv.create_window((0, 0), window=cv.mailbox_frame)
    drawGrid(mz, cv)
    cv.config(width=xxx, height=yyy)
    cv.pack(side=tk.LEFT, anchor=tk.NW)
    window.mainloop()


def itam(mzz):
    baseX = 0
    baseY = 0
    endX = len(mzz)
    #endY = len(mzz[0])
    #X = 0
    #Y = 0
    #while baseX is not endX and baseY is not endY:
    for rr in range(0, endX, -1):
        for y in range(rr, -1, -1):
            r = mzz[baseX-y][baseY].right
            d = mzz[baseX-y][baseY].down
            r1 = mzz[baseX][baseY-y].right
            d1 = mzz[baseX][baseY-y].down
        baseX = rr
        baseY = rr
    return mzz


def m2s(mz):
    mzz = []
    mz = mz.maz
    for x in range(len(mz)):
        mzz.append([])
        for y in range(len(mz[x])):
            mzz[x].append(bm.sNode(mz, mz[x][y]))
    return mzz


def s2m(siz, c):
    mz = []
    if c == 4:
        m = mFmla(siz)
    else:
        m = fMa(siz)
    for x in range(len(m)):
        mz.append([])
        for y in range(len(m[x])):
            mz[x].append(bm.node(x, y, 1, m[x][y].state, mz=m))
    for x in mz:
        for y in x:
            y.addMaz(mz)
    return mz


def checkerB(s, f, j=0):
    qq = {4: probin, 6: probinX, 5: probeXY}
    if not j:
        for h in range(0, s):
            if h % 2 == 0:
                for p in range(0, s, 2):
                    jf = bm.maze(s, p, h)
                    k = m2s(jf)
                    qq[f](k)
            else:
                for p in range(1, s, 2):
                    jf = bm.maze(s, p, h)
                    k = m2s(jf)
                    qq[f](k)
    else:
        for h in range(0, s):
            if h % 2 is not 0:
                for p in range(0, s, 2):
                    jf = bm.maze(s, p, h)
                    k = m2s(jf)
                    qq[f](k)
            else:
                for p in range(1, s, 2):
                    jf = bm.maze(s, p, h)
                    k = m2s(jf)
                    qq[f](k)


def probin(statss):
    #takes 2d array of states and fills in the 4d array of possibilites
    #insert code to take in the 2d States and get probabilities of states from those surrounding it
    r = shelve.open("mSavs")
    w = r["four"]
    for h in range(len(statss)):
        for e in range(len(statss[h])):
            p = statss[h][e]
            lt = p.sStates[0]
            tp = p.sStates[1]
            #y = w[len(statss)-20][lt][tp][p.state]
            w[len(statss)-20][lt][tp][p.state] +=1  #w[len(statss)-20][lt][tp][p.state] + 1
            w[len(statss) - 20][lt][tp][4] +=1  #int(w[len(statss) - 20][lt][tp][4]) + 1
    r["four"] = w
    r.close()


def probinX(statss):
    #takes 2d array of states and fills in the 6d array of possibilities
    # insert code to take in the 2d States and get probabilities of states from those surrounding it and location
    far = len(statss)
    r = shelve.open("mSavs")
    j = r["six"]
    w = j[far-20]
    for x in range(far):
        for y in range(far):
            p = statss[x][y]
            lt = p.sStates[0]
            tp = p.sStates[1]
            w[x][y][lt][tp][p.state] += 1
            w[x][y][lt][tp][4] += 1
    j[far-20] = w
    r["six"] = j
    r.close()


def probeXY(statss):
    far = len(statss)
    r = shelve.open("mSavs")
    j = r["spec"]
    for x in range(far):
        for y in range(far):
            p = statss[x][y]
            lt = p.sStates[0]
            tp = p.sStates[1]
            j[x][y][lt][tp][p.state] += 1
            j[x][y][lt][tp][4] += 1
    r["spec"] = j
    r.close()


def mFmla(lmno):
    mzz = []
    for x in range(lmno):
        mzz.append([])
        for y in range(lmno):
            mzz[x].append(0)
    #write altering motion
    '''
    x, y, ending = 0, 0, 1
    mzz[x][y] = bm.sNode(mzz, bm.node(x, y), True)
    while 1:
        try:
            while x < ending and y < ending:
                # altering
                # write designation of state based on left and top cell states
                mzz[ending][y] = bm.sNode(mzz, bm.node(ending, y), True)
                mzz[x][ending] = bm.sNode(mzz, bm.node(x, ending), True)
                x += 1
                y += 1
            mzz[x][y] = bm.sNode(mzz, bm.node(x, y), True)
        except IndexError:
            break
        ending += 1
        x, y = 0, 0
    baseX = 0
    baseY = 0
    endX = len(mzz)
    # endY = len(mzz[0])
    # X = 0
    # Y = 0
    # while baseX is not endX and baseY is not endY:
    for rr in range(endX, -1, -1):
        for y in range(rr, -1, -1):
            r = mzz[baseX - y][baseY].right
            d = mzz[baseX - y][baseY].down
            r1 = mzz[baseX][baseY - y].right
            d1 = mzz[baseX][baseY - y].down
        baseX = rr
        baseY = rr
    '''
    end = len(mzz)
    check = 0
    while check < end:
        for m in range(check, -1, -1):
            mzz[check][check-m] = bm.sNode(mzz, bm.node(check, check-m), 1)
            mzz[check-m][check] = bm.sNode(mzz, bm.node(check-m, check), 1)
        check += 1
    return mzz


def fMa(siz):
    mzz = []
    for x in range(siz):
        mzz.append([])
        for y in range(siz):
            mzz[x].append(0)
    end = len(mzz)
    check = 0
    while check < end:  #sectors 2 & 3 seem like they are shifted off, absolutely no idea why
        for m in range(check, -1, -1):
            # I have to adjust in bm, so yeah, go fix that fucker
            # maybe another variable input that gives the size of the maze and then maze side that does the comp.s
            if m <= end//2:
                mzz[check][check-m] = bm.sNode(mzz, bm.node(check, check-m, mz=mzz), 2, 1)
                mzz[check-m][check] = bm.sNode(mzz, bm.node(check-m, check, mz=mzz), 2, 1)
            else:
                if m >= (end//2)+1:
                    mzz[check][check - m] = bm.sNode(mzz, bm.node(check, check - m, mz=mzz), 2, 4)
                    mzz[check - m][check] = bm.sNode(mzz, bm.node(check - m, check, mz=mzz), 2, 4)
                else:
                    mzz[check][check - m] = bm.sNode(mzz, bm.node(check, check - m, mz=mzz), 2, 2) #movement in y
                    mzz[check - m][check] = bm.sNode(mzz, bm.node(check - m, check, mz=mzz), 2, 3) #movement in x
        check += 1
    return mzz


def rStateMaz(siz):
    r = list()
    for i in range(siz):
        r.append([])
        for u in range(siz):
            r[i].append(bm.node(i, u, 1, random.randint(0, 3)))
    return r


def logProbMazBuild(siz):
    mzz = []
    for x in range(siz):
        mzz.append([])
        for y in range(siz):
            mzz[x].append(0)
    end = len(mzz)
    end0 = len(mzz[0])
    r = shelve.open("mSavs")
    g = r["spec"]
    r.close()
    for x in range(end):
        for y in range(end0):
            if x <= end // 2 and y <= end0//2:
                #mzz[x][y] = bm.sNode(mzz, bm.node(x, y, mz=mzz), 2, 1)
                quad = 1
            elif x <= end // 2 and y > end0//2:
                #mzz[x][y] = bm.sNode(mzz, bm.node(x, y, mz=mzz), 2, 3)
                quad = 3
            elif x > end // 2 and y <= end0//2:
                #mzz[x][y] = bm.sNode(mzz, bm.node(x, y, mz=mzz), 2, 2)
                quad = 2
            else:
                #mzz[x][y] = bm.sNode(mzz, bm.node(x, y, mz=mzz), 2, 4)
                quad = 4

            ss = [4, 4, end]
            try:
                ss[0] = mzz[x-1][y].state
            except (IndexError, AttributeError):
                ss[0] = 4
            try:
                ss[1] = mzz[x][y-1].state
            except (IndexError, AttributeError):
                ss[1] = 4

            if quad == 1:
                qq = g[x][y][ss[0]][ss[1]]
            elif quad == 2:
                qq = g[45 - (ss[2] - x)][y][ss[0]][ss[1]]
            elif quad == 3:
                qq = g[x][45 - (ss[2] - y)][ss[0]][ss[1]]
            elif quad == 4:
                qq = g[45 - (ss[2] - x)][45 - (ss[2] - y)][ss[0]][ss[1]]
            for c in range(4):
                qq[c] = qq[c] / qq[4]
            for c in range(1, 4):
                qq[c] = qq[c] + qq[c - 1]
            p = (random.randint(0, 99) / 100)
            f = 0
            while qq[f] < p:
                f += 1
                if f >= 4:
                    f = 3
                    break
            finStat = f
            mzz[x][y] = bm.node(x, y, 1, s=finStat, mz=mzz)
    return mzz


def mazCompl(maz):
    # some things (will take a maze as input and output the complexity)
    def pdir(nodee, d="a"):  # make sure this is working right
        y = {0: "R", 1: "D", 2: "L", 3: "U"}
        #c = {"R": [crds[0]+1, crds[1], 0], "D": [crds[0], crds[1]+1, 1], "L": [crds[0]-1, crds[1], 2],
        #     "U": [crds[0], crds[1]-1, 3]}
        cc = {"R": 0, "D": 1, "L": 2, "U": 3}
        if d is not "a" and d is not 0:
            d = cc[d]
            try:
                d += 2
                t = y[d]
            except KeyError:
                d -= 4
            nodee.statement[d] = 0
        if sum(nodee.statement) == 0:
            return 0
        elif sum(nodee.statement) == 1:
            for i in range(4):
                if nodee.statement[i]:
                    outy = y[i]
        else:
            ot = []
            for u in range(4):
                if nodee.statement[u]:
                    ot.append(y[u])
            outy = ot[random.randint(0, len(ot)-1)]
        return outy

    import stack
    dd = {"R": [1, 0], "D": [0, 1], "L": [-1, 0], "U": [0, -1]}
    hall = []  # list of all hallways and their associated number
    t = []  # list of hallways involved in the solution
    e = [len(maz)-1, len(maz[0])-1]
    curD = 0  # the current path being looked at
    cur = maz[0][0]
    cur.probe()
    sta = stack.Stack()
    sta.push(cur)
    dir = pdir(cur)
    while not sta.isEmpty():
        if dir is not 0:
            mid = dd[dir]
            x = cur.cords[0] + mid[0]
            y = cur.cords[1] + mid[1]
            if x <= e[0] and y <= e[1]:
                cur = maz[x][y]
                curD += 1
                if cur.cords[0] == e[0] and cur.cords[1] == e[1]:
                    t.append(curD)
                    dir = pdir(cur, dir)
                    cur.pl = curD
                if cur.turn and sum(cur.statement) >= 1:
                    sta.push(cur)
                    dir = pdir(cur, dir)
                    cur.pl = curD
                    print(cur.cords)
                elif sum(cur.statement) < 1:
                    hall.append(curD)
                    cur = sta.pop()
                    curD = cur.pl
                    '''
                    if sum(cur.statement) == 1:
                        sta.push(cur)
                        dir = pdir(cur, dir)
                    '''
            else:
                hall.append(curD)
                cur = sta.pop()
                curD = cur.pl
                dir = pdir(cur, dir)
        else:
            #hall.append(curD)
            cur = sta.pop()
            curD = cur.pl
            #dir = pdir(cur, dir)
    return [t, hall]



'''
jf = bm.maze(80)
showMazeX(jf)
jj = bm.maze(150)
showMazeX(jj)

for r in range(20000):
    jf = bm.maze(30)  #only run with N in [20,45]
    k = m2s(jf)
    if r == 1000000:
        apple = 2
    probin(k)

m = s2m(30)
showMazeX(m)  
'''
# has shown that I'm going to need to use the 6D, I take that back, not necessarily, I just fucked up something over in sNode but I've fixed it
# code filling the 6D
'''
for r in range(200):
    jf = bm.maze(30)  #only run with N in [20,45]
    k = m2s(jf)
    if r == 10000000:
        apple = 2
    probinX(k)
'''
'''
for r in range(100):
    jf = bm.maze(45)  #only run with N == 45
    k = m2s(jf)
    if r == 80:
        apple = 2
    probeXY(k)
'''
'''
m = s2m(30, 4)
showMazeX(m)
'''
'''
m = s2m(15, 5)
showMazeX(m)
'''
'''
for y in range(8):
    checkerB(45, 5, 1)
    checkerB(45, 5)#runs through about 1019 mazes each time it runs
'''
'''
#m = s2m(20, 5)
r = shelve.open("mSavs")
#r["tMaz"] = m
m = r["tMaz"]
r.close()
p = chromo.Chromo(m)
print(p.farP)
showMazeX(m)
'''
'''
pp = []
j = 0
qq = time.time()
for i in range(30):
    #m = s2m(40, 5)
    m = logProbMazBuild(20)
    pp.append(m)
    j += 1
    print(j)
qi = time.time()
print("%i Seconds" % (qi-qq))
r = shelve.open("mSavs")
r["tMaz4"] = pp
r.close()
#'''
'''
#r = shelve.open("mSavs")
#q = r["tMaz"]
#r.close()
#q = []
#for w in range(30):
#    q.append(copy.deepcopy(rStateMaz(30)))
q = []
for w in range(10):
    q.append(logProbMazBuild(20))
qq = time.time()
p = CC.ChromeField()
for i in q:
    h = CC.Chromo(i)
    p.add2Gen(h)
qu = time.time()
FF = CC.GeneShift(p)
out = True
a = 0
outed = []
qp = time.time()
while out:
    print("gen %i" % a)
    FF.merge()
    outed = FF.isEnd()
    out = (len(outed) < 1)
    a += 1
#FF.Flux[FF.CurField].culling()
#u = FF.Flux[FF.CurField].gen
print("After %i generation(s), there were %i mazes created." % (a, len(outed)))
qy = time.time()
print("%f sec to build Gen0 mazes, %f sec to convert, %f sec to complete all merges and output mazes, avg time per: %f" % (qu-qq, qp-qu, qy-qp, ((qu-qq)+(qp-qu)+(qy-qp))/len(outed)))
for r in outed:
    #k = FF.Pull()
    #print(r.farPP)
    #print(r.revFP)
    #print(mazCompl(r))
    showMazeX(r)
#'''
'''
y = []
for t in range(12):
    qq = time.time()
    j = bm.maze(45)
    qu = time.time()
    y.append(j)
    print(qu - qq)
#j.maz = j.reprobe(j.maz)
#print(mazCompl(j.maz))
#for j in y:
#    showMazeX(j)
'''
y = []
for i in range(1, 5):
    j = bm.maze(i*5)
    showMazeX(j)
