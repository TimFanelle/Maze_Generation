import stack
import random
import shelve


class node:
    def __init__(self, x, y, probs=0, s=4, mz=None):
        self.cords = [x, y]
        if mz is not None:
            self.strangeNeed = mz
        else:
            self.strangeNeed = []
        self.visited = False
        self.walls = [True, True]
        self.state = s
        self.statement = []
        self.turn = self.turnNburn()
        #self.dead = bool(sum(self.statement) == 1)
        self.pl = 0
        if probs:
            self.setWallsonState(s)

    def setWallsonState(self, s):
        if s == 0:
            self.walls = [False, False]
        elif s == 1:
            self.walls = [True, True]
        elif s == 2:
            self.walls = [True, False]
        else:
            self.walls = [False, True]
        self.visited = True
        #write the code to take a grid of states and make it into back into a grid of nodes

    def setStateonWalls(self):
        if self.walls[0] and self.walls[1]:
            self.state = 1
        elif not self.walls[0] and not self.walls[1]:
            self.state = 0
        elif self.walls[0] and not self.walls[1]:
            self.state = 2
        else:
            self.state = 3

    def probe(self):
        jj = {0: [1, 1], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [0, 0]}
        out = jj[self.state][:]
        ss = [0, 0]
        if self.cords[0] > 0 and (self.cords[0] < len(self.strangeNeed)):
            ss[0] = int(self.strangeNeed[self.cords[0] - 1][self.cords[1]].state == 3 or self.strangeNeed[self.cords[0] - 1][self.cords[1]].state == 0)
        if self.cords[1] > 0 and (self.cords[1] < len(self.strangeNeed[0])):
            ss[1] = int(self.strangeNeed[self.cords[0]][self.cords[1] - 1].state == 2 or self.strangeNeed[self.cords[0]][self.cords[1] - 1].state == 0)
        out = out + ss[:]
        self.statement = out

    def restate(self):
        self.probe()
        if self.cords[0] < len(self.strangeNeed):
            self.strangeNeed[self.cords[0] + 1][self.cords[1]].probe(self.strangeNeed[self.cords[0] + 1][self.cords[1]].state)
        if self.cords[1] < len(self.strangeNeed[0]):
            self.strangeNeed[self.cords[0]][self.cords[1] + 1].probe(self.strangeNeed[self.cords[0]][self.cords[1] + 1].state)

    def addMaz(self, mz):
        self.strangeNeed = mz
        self.statement = self.probe(self.state)

    def turnNburn(self):
        u = self.statement
        if len(u) > 1:
            if u[0] and u[1]:
                return True
            elif u[1] and u[3]:
                return True
            elif u[3] and u[2]:
                return True
            elif u[2] and u[0]:
                return True
            else:
                return False
        else:
            return False


class sNode:
    def __init__(self, mzs, nod, det=0, det1=0):
        self.sStates = self.oStats(mzs, nod)
        self.state = self.detStat(nod, det, det1)

    def detStat(self, nod, det=0, det1=0):
        if det == 0:
            try:
                if nod.walls[0] and nod.walls[1]:
                    return 1
                elif nod.walls[0]:
                    return 2
                elif nod.walls[1]:
                    return 3
                else:
                    return 0
            except AttributeError:
                if nod.state is not 5:
                    return nod.state
                else:
                    print("Confusion " + str(nod.cords[0]) + " " + str(nod.cords[1]))
                #print("Nope")
        else:
            return self.probsNstuff(self.sStates, nod, det, det1)

    def oStats(self, mzs, nod):
        ss = [4, 4, len(mzs)]
        if nod.cords[0] > 0:
            ss[0] = self.detStat(mzs[nod.cords[0]-1][nod.cords[1]])
        if nod.cords[1] > 0:
            ss[1] = self.detStat(mzs[nod.cords[0]][nod.cords[1]-1])
        return ss

    def probsNstuff(self, ss, nod, det, det1):
        sel = {1: "four", 2: "spec"}
        r = shelve.open("mSavs")
        g = r[sel[det]]
        r.close()
        if det == 1:
            #g = r["four"]
            g = g[ss[2]-20]
            g = g[ss[0]]#g[ss[0]]
            g = g[ss[1]]#[ss[1]]
        else:  #det == 2
            #g = r["spec"]
            # g = r["fixbit"]
            # q = []
            if det1 == 1:
                g = g[nod.cords[0]][nod.cords[1]][ss[0]][ss[1]]
                # q = [nod.cords[0], nod.cords[1], ss[0], ss[1]]
            elif det1 == 2:
                g = g[45-(ss[2]-nod.cords[0])][nod.cords[1]][ss[0]][ss[1]]
                # q = [45-(ss[2]-nod.cords[0]), nod.cords[1], ss[0], ss[1]]
            elif det1 == 3:
                g = g[nod.cords[0]][45-(ss[2]-nod.cords[1])][ss[0]][ss[1]]
                # q = [nod.cords[0], 45-(ss[2]-nod.cords[1]), ss[0], ss[1]]
            elif det1 == 4:
                g = g[45-(ss[2]-nod.cords[0])][45-(ss[2]-nod.cords[1])][ss[0]][ss[1]]
                # q = [45-(ss[2]-nod.cords[0]), 45-(ss[2]-nod.cords[1]), ss[0], ss[1]]
            '''
            else:
                #darn man this better not happen seeing as I'm the one inputing stuff
                print("something messed up")
                #g = g[nod.cords[0]][nod.cords[1]][ss[0]][ss[1]]
            '''
        for c in range(4):
            g[c] = g[c] / g[4]
            '''
            if g[4] is not 0:
                g[c] = g[c] / g[4]
            else:
                g = [1, 1, 1, 1, 4]
                r = shelve.open("mSavs")
                r["four"][q[0]][q[1]][q[2]][q[3]] = g
                r.close()
                c = 0
                #print("div by zer")
            '''
        for c in range(1, 4):
            g[c] = g[c] + g[c - 1]
        p = (random.randint(0, 99) / 100)
        f = 0
        while g[f] < p:
            f += 1
            if f >= 4:
                f = 3
                break
        return f


class maze:
    def __init__(self, s, sX=0, sY=0, caterwalling=0):
        self.maz = self.buildMaze(self.fillMaze(s, caterwalling), sX, sY)
        self.fullState()
        self.maz = self.reprobe(self.maz)

    def __len__(self):
        return len(self.maz)

    def fillMaze(self, siz, caterwalling):
        mz = []#[[0]*siz]*siz
        for x in range(siz):
            mz.append([])
            for y in range(siz):
                mz[x].append(node(x, y))
        if not caterwalling:
            mz[siz-1][siz-1].walls[0] = False
        return mz

    def buildMaze(self, mz, sX, sY):
        q = stack.Stack()
        n = mz[sX][sY]  # changed to add the ability to select a starting point
        n.visited = True
        p = self.getDirs(n, mz)
        nx = self.wallin(n, p, mz)
        q.push(mz[n.cords[0]][n.cords[1]])
        n = mz[nx[0]][nx[1]]
        while not q.isEmpty():
            n.visited = True
            p = self.getDirs(n, mz)
            if len(p) > 0:
                nx = self.wallin(n, p, mz)
                q.push(n)
                n = mz[nx[0]][nx[1]]
            else:
                n = q.pop()
        return mz

    def getDirs(self, h, mz):
        posib = []
        x = h.cords[0]
        y = h.cords[1]
        if x > 0:
            if not mz[x-1][y].visited:
                posib.append("LEFT")#["LEFT", x-1, y]
        if y > 0:
            if not mz[x][y-1].visited:
                posib.append("UP")#["UP", x, y-1]
        if x < len(mz)-1:
            if not mz[x+1][y].visited:
                posib.append("RIGHT")#["RIGHT", x+1, y]
        if y < len(mz[0])-1:
            if not mz[x][y+1].visited:
                posib.append("DOWN")#["DOWN", x, y+1]
        return posib

    def wallin(self, nn, pp, mz):
        o = random.randint(0, len(pp)-1)
        dir = pp[o]
        xn = nn.cords[0]
        yn = nn.cords[1]
        if dir == "LEFT":
            nn = mz[xn-1][yn]
            nn.walls[0] = False
            xn -= 1
        elif dir == "RIGHT":
            nn.walls[0] = False
            xn += 1
        elif dir == "DOWN":
            nn.walls[1] = False
            yn += 1
        else:
            nn = mz[xn][yn-1]
            nn.walls[1] = False
            yn -= 1
        return [xn, yn]

    def fullState(self):
        for i in self.maz:
            for p in i:
                p.setStateonWalls()

    def reprobe(self, m):
        for n in m:
            for ns in n:
                s = ns.state
                jj = {0: [1, 1], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [0, 0]}  # [r,d]
                out = jj[s][:]
                if (ns.cords[0] == (len(m)-1)) and (ns.cords[1] == (len(m[0])-1)):
                    out = [0, 0]  # [r,d]
                ss = [0, 0]
                if ns.cords[0] > 0 and (ns.cords[0] < len(m)-1):
                    ss[0] = int(m[ns.cords[0] - 1][ns.cords[1]].state == 3 or m[ns.cords[0] - 1][ns.cords[1]].state == 0)
                if ns.cords[1] > 0 and (ns.cords[1] < len(m[0])-1):
                    ss[1] = int(m[ns.cords[0]][ns.cords[1] - 1].state == 2 or m[ns.cords[0]][ns.cords[1] - 1].state == 0)
                out = out + ss[:]
                ns.statement = out
                ns.turn = ns.turnNburn()
        return m
