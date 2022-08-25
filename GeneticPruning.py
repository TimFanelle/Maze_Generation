import math
import random
import stack
#import backtracking_maze as bm
import copy


class Chromo:

    def __init__(self, maze):
        self.startP = [0, 0]
        self.endP = [len(maze)-1, len(maze[0])-1]
        # self.ssP = []
        self.maze = self.resetWalls(self.reprobe(self.forceState(maze)))
        self.farPP = self.farP()[1]
        #self.revFP = self.rfar()[1]
        self.lPth = math.sqrt(math.pow((self.farPP[0]-self.startP[0]), 2) + math.pow((self.farPP[1]-self.startP[1]), 2))

    def forceState(self, mz):
        s1 = {0: 2, 1: 1, 2: 2, 3: 1}
        s2 = {0: 3, 1: 1, 2: 1, 3: 3}
        for y in range(0, len(mz)-1):  # right side
            mz[len(mz)-1][y].state = s1[mz[len(mz)-1][y].state]
            if y == len(mz)-2:
                mz[len(mz) - 1][y].state = 2
        for x in range(0, len(mz[0])-1):  # bottom
            mz[x][len(mz[0])-1].state = s2[mz[x][len(mz[0])-1].state]
            if x == len(mz[0]) - 2:
                mz[x][len(mz[0]) - 1].state = 3
        return mz

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

    def resetWalls(self, m):
        for i in m:
            for p in i:
                s = p.state
                if s == 0:
                    p.walls = [False, False]
                elif s == 1:
                    p.walls = [True, True]
                elif s == 2:
                    p.walls = [True, False]
                else:
                    p.walls = [False, True]
        return m

    def cull(self, lists):
        r = []
        for j in lists:
            r.append([math.sqrt(math.pow((j[0]-self.startP[0]), 2) + math.pow((j[1]-self.startP[1]), 2)), j])
        m = r[0]
        for x in r:
            if x[0] > m[0]:
                m = x
        return m

    def farP(self):
        oP = []
        sP = self.startP
        n = self.maze[sP[0]][sP[1]]
        if sum(n.statement) > 0:
            sP = self.selD(n.statement, n.cords)
            q = stack.Stack()
            q.push(n.cords)
            oP.append(n.cords)
        else:
            fp = [0, n.cords]
            return fp
        n = self.maze[sP[0]][sP[1]]
        while not q.isEmpty():
            if sum(n.statement) == 0:
                sP = q.pop()
                oP.append(n.cords)
                n = self.maze[sP[0]][sP[1]]
                if sum(n.statement) > 0:
                    q.push(n.cords)
            else:
                if sum(n.statement) > 1:
                    q.push(n.cords)
                sP = self.selD(n.statement, n.cords)
                oP.append(n.cords)
                try:
                    n = self.maze[sP[0]][sP[1]]
                except IndexError:
                    try:
                        sP[1] += 1
                        sP[0] -= 1
                        xo = self.maze[sP[0]][sP[1]]
                        sp[1] -= 1
                        n = self.maze[sP[0]][sP[1]]
                    except IndexError:
                        fp = self.endP
                        return fp
                        #n = self.maze[sP[0]][sP[1]]
        fp = self.cull(oP)
        return fp

    def rfar(self):
        oP = []
        sP = self.endP
        n = self.maze[sP[0]][sP[1]]
        print(n.statement)
        if sum(n.statement) > 0:
            sP = self.selD(n.statement, n.cords)
            q = stack.Stack()
            q.push(n.cords)
            oP.append(n.cords)
        else:
            fp = [0, n.cords]
            return fp
        n = self.maze[sP[0]][sP[1]]
        while not q.isEmpty():
            print(n.statement)
            if sum(n.statement) == 0:
                sP = q.pop()
                oP.append(n.cords)
                n = self.maze[sP[0]][sP[1]]
                if sum(n.statement) > 0:
                    q.push(n.cords)
            else:
                if sum(n.statement) > 1:
                    q.push(n.cords)
                sP = self.selD(n.statement, n.cords)
                oP.append(n.cords)
                try:
                    n = self.maze[sP[0]][sP[1]]
                except IndexError:
                    try:
                        sP[1] -= 1
                        n = self.maze[sP[0]][sP[1]]
                    except IndexError:
                        sP[0] -= 1
                        n = self.maze[sP[0]][sP[1]]
        fp = self.cullX(oP)
        return fp

    def cullX(self, inp):
        r = []
        for j in inp:
            r.append([math.sqrt(math.pow((j[0] - self.endP[0]), 2) + math.pow((j[1] - self.endP[1]), 2)), j])
        m = r[0]
        for x in r:
            if x[0] > m[0]:
                m = x
        return m

    def selD(self, statements, crds):
        if crds[0] >= (len(self.maze) - 1) and crds[1] >= (len(self.maze[0]) - 1):
            return [len(self.maze) - 1, len(self.maze) - 1, 1]
        y = {0: "R", 1: "D", 2: "L", 3: "U"}
        c = {"R": [crds[0]+1, crds[1], 0], "D": [crds[0], crds[1]+1, 0], "L": [crds[0]-1, crds[1], 1],
             "U": [crds[0], crds[1]-1, 1]}
        cc = {"R": 0, "D": 1, "L": 2, "U": 3}
        ot = []
        for u in range(4):
            if statements[u]:
                ot.append(y[u])
        if crds[0] < (len(self.maze)) and crds[1] < (len(self.maze[0])):
            if len(ot) > 1:
                r = ot[random.randint(0, len(ot)-1)]
            else:
                r = ot[0]
            p = cc[r]
            self.maze[crds[0]][crds[1]].statement[p] = 0
            try:
                self.maze[c[r][0]][c[r][1]].statement[p + 2] = 0
            except IndexError:
                self.maze[c[r][0]][c[r][1]].statement[p - 2] = 0
            return c[r]
        else:
            if len(ot) > 1:
                r = ot[random.randint(0, len(ot)-1)]
            else:
                r = ot[0]
            p = cc[r]
            self.maze[crds[0]][crds[1]].statement[p] = 0
            return [crds[0], crds[1], 1]


class ChromeField:

    def __init__(self):
        self.gen = []
        self.genSize = 0
        self.pullNum = 0

    def add2Gen(self, insert):
        self.gen.append(insert)
        self.genSize += 1

    def culling(self):
        h = sorted(self.gen, key=lambda b: b.lPth, reverse=True)
        randSurvN = random.randint(1, 4)
        randSurv = []
        while len(randSurv) < randSurvN:
            n = random.randint(5, self.genSize-1)
            if not randSurv.__contains__(self.gen[n]):
                randSurv.append(self.gen[n])
        self.gen = h[:5] + randSurv
        self.genSize = len(self.gen)

    def pull(self):
        j = self.gen[self.pullNum].maze
        self.pullNum += 1
        return j


class GeneShift:

    def __init__(self, StartField):
        self.Flux = [StartField, ChromeField()]
        self.CurField = 0
        self.addP = self.PointBreak()

    def PointBreak(self):
        boink = []
        l = len(self.Flux[0].gen[0].maze)-1
        for i in range((l//3)-1, -1, -1):
            for j in range((l // 3) - 1, -1, -1):
                if ((i % 2 == 0) and not (j % 2 == 0)) or (not (i % 2 == 0) and (j % 2 == 0)):
                    boink.append([l-i, l-j])
        return boink

    def PickPoints(self, inpt):
        indpt = inpt.maze
        fp = inpt.farPP
        ep = inpt.endP
        p = []
        while len(p) < 4:
            m1 = fp[0] - int((ep[0]-fp[0])*.5)
            if m1 < 0:
                m1 = 0
            m2 = fp[1] - int((ep[1]-fp[1])*.5)
            if m2 < 0:
                m2 = 0
            p1 = random.randint(m1, len(indpt)-1)
            p2 = random.randint(m2, len(indpt)-1)
            if not p.__contains__([p1, p2]):
                p.append([p1, p2])
        return p

    def merge(self):
        self.Flux[self.CurField].culling()
        GenX = self.Flux[self.CurField].gen
        flip = not self.CurField
        counter = 4
        for C in GenX:
            ps = self.PickPoints(C)
            #ps = ps + self.addP
            #else:
            for b in range(len(self.Flux[0].gen[0].maze)//5):
                ps.append(C.farPP)
            #ps.append(C.revFP)
            #ps.append([len(C.maze)-2, len(C.maze)-3])
            #ps.append([len(C.maze)-3, len(C.maze)-2])
            for m in GenX:
                if m is not C:
                    mz = copy.deepcopy(C.maze)
                    mz1 = m.maze
                    if C.farPP[0] / C.endP[0] >= .65 and C.farPP[1] / C.endP[1] >= .65:
                        counter = 2
                    for p in ps:
                        switch = mz1[p[0]][p[1]].state
                        if p == C.farPP:
                            counter = 1
                        r = random.randint(0, 32)
                        if r % counter == 0:
                            for q in range(r // counter):
                                switch = self.upState(switch)
                        mz[p[0]][p[1]].state = switch
                        meep = Chromo(copy.deepcopy(mz))
                        self.Flux[flip].add2Gen(meep)
        self.Flux[flip].gen = self.Flux[flip].gen + GenX
        self.CurField = flip

    def Pull(self):
        return self.Flux[self.CurField].pull()

    def upState(self, stat):  # takes the current state and makes it one higher or cycles around
        h = {4: 0, 0: 1, 1: 2, 2: 3, 3: 0}
        return h[stat]

    def isEnd(self):
        full = []
        for i in self.Flux[self.CurField].gen:
            #print("%s vs. %s" % (i.farPP, i.endP))
            if (int(i.farPP[0]) == int(i.endP[0])) and (int(i.farPP[1]) == int(i.endP[1])):
                i.reprobe(i.maze)
                full.append(i.maze)
        return full
