import math
import random
import stack
import backtracking_maze as bm


class Chromo:

    def __init__(self, maze, endP=0, startP=0):
        self.maze = self.forceState(maze)
        self.maze = self.reprobe(self.maze)
        self.maze = self.resetWalls(self.maze)
        if endP is not 0:
            self.endP = endP
        else:
            self.endP = [len(maze)-1, len(maze[0])-1]
        if startP is not 0:
            self.startP = startP
        else:
            self.startP = [int(0), int(0)]
        mar = self.farPP()
        self.farP = mar[1]
        self.ssP = []  # mar[2]
        self.dist = math.sqrt(math.pow((self.endP[0]-self.farP[0]), 2) + math.pow((self.endP[1]-self.farP[1]), 2))

    def reprobe(self, m):
        for n in m:
            for ns in n:
                s = ns.state
                jj = {0: [1, 1], 1: [0, 0], 2: [0, 1], 3: [1, 0], 4: [0, 0]}  # [r,d]
                out = jj[s][:]
                ss = [0, 0]
                if ns.cords[0] > 0 and (ns.cords[0] < len(ns.strangeNeed)-1):
                    ss[0] = int(ns.strangeNeed[ns.cords[0] - 1][ns.cords[1]].state == 3 or ns.strangeNeed[ns.cords[0] - 1][ns.cords[1]].state == 0)
                if ns.cords[1] > 0 and (ns.cords[1] < len(ns.strangeNeed[0])-1):
                    ss[1] = int(ns.strangeNeed[ns.cords[0]][ns.cords[1] - 1].state == 2 or ns.strangeNeed[ns.cords[0]][ns.cords[1] - 1].state == 0)
                if (ns.cords[0] == (len(ns.strangeNeed)-1)) and (ns.cords[1] == (len(ns.strangeNeed[0])-1)):
                    ss = [0, 0]  # [l,t]
                out = out + ss[:]
                ns.statement = out
                '''
                if sum(out) > 1 and self.turnAndBurn(out):  # don't do this, it would get every turn in the whole grid, not just the ones at the start
                    self.ssP.append([ns.cords[0], ns.cords[1]])
                '''
        return m

    # This doesn't necessarily work, I need to make it something else; probably related to farPP
    def turnAndBurn(self, sts):
        if sts[0] and (sts[1] or sts[3]):
            return True
        elif sts[1] and sts[2]:
            return True
        elif sts[2] and sts[3]:
            return True
        else:
            return False

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

    def dirp(self, statements, crds):  # I'm pretty sure this is where one of our larger problems is
        if crds[0] >= (len(self.maze) - 1) and crds[1] >= (len(self.maze[0]) - 1):
            return [len(self.maze) - 1, len(self.maze) - 1, 1]
        y = {0: "R", 1: "D", 2: "L", 3: "U"}
        c = {"R": [crds[0]+1, crds[1], 0], "D": [crds[0], crds[1]+1, 0], "L": [crds[0]-1, crds[1], 1], "U": [crds[0], crds[1]-1, 1]}
        cc = {"R": 0, "D": 1, "L": 2, "U": 3}
        ot = []
        for u in range(4):
            if statements[u]:
                ot.append(y[u])
        #if len(ot) == 0:  # This isn't real code, just a pseudo-fix for now
        #    r = "D"
        if crds[0] < (len(self.maze)-1) and crds[1] < (len(self.maze[0])-1):
            if len(ot) > 1:
                r = ot[random.randint(0, len(ot)-1)]
            else:
                r = ot[0]
            p = cc[r]
            self.maze[crds[0]][crds[1]].statement[p] = 0
            try:  # make sure that c[r] will never be out of bounds
                self.maze[c[r][0]][c[r][1]].statement[p + 2] = 0
            except IndexError:
                self.maze[c[r][0]][c[r][1]].statement[p - 2] = 0
            return c[r]
        else:  # this has messed something up, somehow
            if len(ot) > 1:
                r = ot[random.randint(0, len(ot)-1)]
            else:
                r = ot[0]
            p = cc[r]
            self.maze[crds[0]][crds[1]].statement[p] = 0
            '''
            try:  # make sure that c[r] will never be out of bounds
                self.maze[c[r][0]][c[r][1]].statement[p + 2] = 0
            except IndexError:
                self.maze[c[r][0]][c[r][1]].statement[p - 2] = 0
            '''
            return [crds[0], crds[1], 1]

    '''
    def fuckDirs(self, h, mz, second=0):
        posib = []
        x = h[0]
        y = h[1]
        if not second:
            if x < len(mz) - 1:
                if (not mz[x + 1][y].visited or len(self.fuckDirs([x + 1, y], mz, 1)) > 0) and (mz[x][y].state == 3 or mz[x][y].state == 0):
                    posib.append([mz[x + 1][y].cords[0], mz[x + 1][y].cords[1], 0])  # ["RIGHT", x+1, y]
            if y < len(mz[0]) - 1:
                if (not mz[x][y + 1].visited or len(self.fuckDirs([x, y + 1], mz, 1)) > 0) and (mz[x][y].state == 2 or mz[x][y].state == 0):
                    posib.append([mz[x][y + 1].cords[0], mz[x][y + 1].cords[1], 0])  # ["DOWN", x, y+1]
            if x > 0:
                if (not mz[x - 1][y].visited or len(self.fuckDirs([x - 1, y], mz, 1)) > 0) and (mz[x - 1][y].state == 3 or mz[x - 1][y].state == 0):
                    posib.append([mz[x - 1][y].cords[0], mz[x - 1][y].cords[1], 1])  # ["LEFT", x-1, y]
            if y > 0:
                if (not mz[x][y - 1].visited or len(self.fuckDirs([x, y - 1], mz, 1)) > 0) and (mz[x][y - 1].state == 2 or mz[x][y - 1].state == 0):
                    posib.append([mz[x][y - 1].cords[0], mz[x][y - 1].cords[1], 1])  # ["UP", x, y-1]
        else:
            if x < len(mz) - 1:
                if (not mz[x + 1][y].visited) and (mz[x][y].state == 3 or mz[x][y].state == 0):
                    posib.append([mz[x + 1][y].cords[0], mz[x + 1][y].cords[1], 0])  # ["RIGHT", x+1, y]
            if y < len(mz[0]) - 1:
                if (not mz[x][y + 1].visited) and (mz[x][y].state == 2 or mz[x][y].state == 0):
                    posib.append([mz[x][y + 1].cords[0], mz[x][y + 1].cords[1], 0])  # ["DOWN", x, y+1]
            if x > 0:
                if (not mz[x - 1][y].visited) and (mz[x - 1][y].state == 3 or mz[x - 1][y].state == 0):
                    posib.append([mz[x - 1][y].cords[0], mz[x - 1][y].cords[1], 1])  # ["LEFT", x-1, y]
            if y > 0:
                if (not mz[x][y - 1].visited) and (mz[x][y - 1].state == 2 or mz[x][y - 1].state == 0):
                    posib.append([mz[x][y - 1].cords[0], mz[x][y - 1].cords[1], 1])  # ["UP", x, y-1]
        return posib
        
    def dirs(self, r, h, mz):
        x = h[0]
        y = h[1]
        if (x < len(mz) - 1) and (y < len(mz[0]) - 1) and x > 0 and y > 0:
            if not mz[x - 1][y].visited or not mz[x + 1][y].visited or not mz[x][y - 1].visited or not mz[x][y + 1].visited:
                if not mz[x - 1][y].visited:
                    r.append([x-1, y])
                    r.append(self.dirs(r, [x-1, y], mz))
                if not mz[x + 1][y].visited:
                    r.append([x + 1, y])
                    r.append(self.dirs(r, [x + 1, y], mz))
                if not mz[x][y - 1].visited:
                    r.append([x, y-1])
                    r.append(self.dirs(r, [x, y-1], mz))
                if not mz[x][y + 1].visited:
                    r.append([x, y+1])
                    r.append(self.dirs(r, [x, y+1], mz))
            else:
                r.append([0, 0])
        return r
        
    def direct(self, h, mz):
        x = h[0]
        y = h[1]
        h = mz[x][y]
        pp = []
        if h.state == 2 and y < len(mz):  # down
            if not mz[x][y+1].visited:
                pp.append([x, y + 1, 0])
                return pp
        elif h.state == 3 and x < len(mz):  # right
            if not mz[x + 1][y].visited:
                pp.append([x+1, y, 0])
                if pp is not None:
                    return pp
                else:
                    pp = [[x+1, y, 0]]
                    return pp
        elif h.state == 0:  # both
            if x < len(mz):
                if not mz[x+1][y].visited:
                    pp.append([x+1, y, 0])
            if y < len(mz):
                if not mz[x][y + 1].visited:
                    pp.append([x, y + 1, 0])
            return pp
        elif h.state == 1:
            if x > 0:
                if not mz[x-1][y].visited:
                    pp.append([x - 1, y, 1])
            if y > 0:
                if not mz[x][y - 1].visited:
                    pp.append([x, y - 1, 1])
            return pp
        else:
            return [0, 0, 0]
    '''

    #I think I'm going to just rewrite this from scratch, maybe try something different
    def farPP(self):  # need to rewrite so ssP takes in points with turns, then set pick3 to take the 3 furthest
        oP = []
        sP = self.startP
        n = self.maze[sP[0]][sP[1]]
        if sum(n.statement) > 0:
            sP = self.dirp(n.statement, n.cords)
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
                sP = self.dirp(n.statement, n.cords)
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
        fp = self.cull(oP)
        return fp

    def forceState(self, mz):
        s1 = {0: 2, 1: 1, 2: 2, 3: 1}
        s2 = {0: 3, 1: 1, 2: 1, 3: 3}
        for y in range(0, len(mz)-1):
            mz[len(mz)-1][y].state = s1[mz[len(mz)-1][y].state]
        for x in range(0, len(mz[0])-1):
            mz[x][len(mz[0])-1].state = s2[mz[x][len(mz[0])-1].state]
        return mz

    def cull(self, lists):
        r = []
        for j in lists:
            # check to make sure this line is working properly
            r.append([math.sqrt(math.pow((j[0]-self.startP[0]), 2) + math.pow((j[1]-self.startP[1]), 2)), j])
        #r[0].sort()
        m = r[0]
        for x in r:
            if x[0] > m[0]:
                m = x
        return m


class ChromeField:

    def __init__(self):
        self.generation = []
        self.genNum = 0
        self.genSize = 0
        self.pullNum = 0
        self.genX = []

    def add2Gen(self, insert):
        self.generation.append(insert)
        self.genSize += 1

    def culling(self, nomNum):  # look into this method for order of list
        h = sorted(self.generation, key=lambda n: n.dist)
        self.generation = h[:nomNum]
        self.genSize = len(self.generation)

    def merge(self, mai):  # will take main and merge the faulty cells with that of the matching cells in the/
        # other mazes within the generation
        # This apparently isn't doing anything and I don't know why
        main = self.generation[mai]
        mP = self.pick3(main.ssP)
        cop = self.quick2D(len(main.maze))
        for i in range(self.genSize):
            if i is not mai:
                sain = self.generation[i]
                for j in range(len(cop)):
                    for y in range(len(cop)):
                        si = sain.maze[j][y].state
                        r = random.randint(0, 30)
                        if r % 9 == 0:
                            for p in range(r // 9):
                                si = self.upState(si)
                        if self.checkBeck(mP, [j, y]):
                            cop[j][y] = bm.node(j, y, s=si)
                        else:
                            cop[j][y] = bm.node(j, y, s=si)
                for p in cop:
                    for h in p:
                        h.addMaz(cop)
                self.genX.append(Chromo(cop))

        '''
        cop = [r[:] for r in main.maze]
        for i in range(self.genSize):
            if i is not mai:
                sain = self.generation[i]
                for pair in mP:
                    s = sain.maze[pair[0]][pair[1]].state
                    r = random.randint(0, 30)
                    if r % 9 == 0:
                        for p in range(r//9):
                            s = self.upState(s)
                    cop[pair[0]][pair[1]].state = s
                    #cop[pair[0]][pair[1]].restate()
                self.genX.append(Chromo(cop))
        '''

    def quick2D(self, leng):
        r = list()
        for i in range(leng):
            r.append([])
            for u in range(leng):
                r[i].append(0)
        return r

    def checkBeck(self, points, coords):
        for p in points:
            if coords[0] == p[0] and coords[1] == p[1]:
                return True
        return False

    def pick3(self, inn):
        if len(inn) > 3:
            t = []
            while len(t) < 3:
                e = random.randint(0, len(inn)-1)
                if not t.__contains__(e):
                    t.append(inn[e])
            return t
        else:
            return inn

    def newGen(self):
        for i in range(self.genSize):
            self.merge(i)
        self.generation = self.genX
        self.genSize = len(self.generation)
        self.genX = []
        self.genNum += 1

    def pull(self):
        #will return a maze from current generation
        j = self.generation[self.pullNum].maze
        print(self.generation[self.pullNum].farP)
        self.pullNum += 1
        return j

    def upState(self, stat):  # takes the current state and makes it one higher or cycles around
        h = {4: 0, 0: 1, 1: 2, 2: 3, 3: 0}
        return h[stat]
