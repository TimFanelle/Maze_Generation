import numpy as np
class sector:
    def __init__(self, x, y):
        self.down = True
        self.right = True
        self.up = True
        self.left = False
        if y == 0:
            self.up = True
        if x == 0:
            self.left = True
            self.up = True
        '''
        if y == len(inp[1])+1:
            self.down = False
        if x == len(inp[0])+1:
            self.right = False
        '''
        self.name = "C" + str(x) + "R" + str(y)
        self.row = y
        self.col = x
        self.walls = self.numWalls()
        self.ns = self.outState()

    def numWalls(self):
        return int(self.up)+int(self.down)+int(self.left)+int(self.right)

    def outState(self):
        states = {"N": 0, "DR": 1, "R": 2, "D": 3}
        k = ""
        if self.down:
            k = k + "D"
        if self.right:
            k = k + "R"
        if len(k) == 0:
            k = "N"
        return states[k]

class testingEnv:
    def __init__(self, r, c):
        self.nA = 0
        self.P = [[]]
        self.nS = len(self.P)
        self.mazze = self.aMAZEing(r, c)
        self.reset = self.mazze[:][:]
        self.step = 0
        self.states = {0: "N", 1: "DR", 2: "R", 3: "D"}


    def aMAZEing(self, r, c):
        mazz = []
        for l in range(r):
            inner = []
            for w in range(c):
                inner.append(sector(l, w))
            mazz.append(inner)
        return mazz

    def numActs(self, s):
        s = self.states[s]
        if s == "N":
            return 1, ["N"], [1], 0
        elif s == "DR":
            return 4, ["N", "DR", "R", "D"], [.1, .2, .35, .35], -.5
        elif s == "R":
            return 2, ["N", "R"], [.3, .7], 1
        elif s == "D":
            return 2, ["N", "D"], [.3,.7], 1

    def _step(self, s):
        self.P = [[]]
        p.append()
        for y in range(2**s.ns):
            na, stit, probs, rew = self.numActs(s.ns)
            P.append(0)
            for h in range(na):
                #P[y][h] = (probs,,rew,)
                h = 3
        #self.nS = len(self.P)
        '''

        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = self.status != hfo_py.IN_GAME
        return ob, reward, episode_over, {}
        '''
    def _reset(self):
        self.mazze = self.reset
        self.step = 0

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):
        pass

    def _get_reward(self):
        """ Reward is given for XY. """
        if self.status == FOOBAR:
            return 1
        elif self.status == ABC:
            return self.somestate ** 2
        else:
            return 0

    def outMaze(self):
        return self.mazze

    def outWall(self, x, y, wall):
        if wall == "RIGHT":
            self.mazze[x][y].right = False
        elif wall == "DOWN":
            self.mazze[x][y].down = False
        elif wall == "NONE":
            badabing = "badaboom"
