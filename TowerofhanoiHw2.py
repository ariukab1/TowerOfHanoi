
"""
Ariunbold Batsaikhan HW2
"""

import sys
import os


from copy import deepcopy
from copy import copy




class stack:
    def __init__(self):
        self.p = []

    def push(self, t):
        if (self.pushable(t)):
            self.p.append(t)
            return True
        else:
            return False

    def pop(self):
        return self.p.pop()

    def top(self):
        if self.p:
            return self.p[-1]

    def remove(self):
        self.p.pop(0)

    def isEmpty(self):
        return (len(self.p) == 0)

    def printStack(self):
        print(
        self.p)

    def isFull(self):
        return (len(self.p) >= 5)

    def pushable(self, t):
        if (self.isFull()):
            return False
        else:
            return self.isEmpty() or t < self.top()

    def size(self):
        return len(self.p)

    def equal(self, s):
        return self.p == s.p





class towers:
    def __init__(self):

        self.P = stack()
        self.Q = stack()
        self.R = stack()
        self.stacks = [self.P, self.Q, self.R]
        self.allMoves = ((0, 1), (0, 2), (1, 0), (1, 2),(2, 0), (2, 1))
        self.path = []
        self.validMoves = []
        self.lastMove = ()
        self.steps = 0
        self.setup()

    def setup(self):
        for x in range(5, 0, -1):
            self.R.push(x)
        self.generateMoves()

    def generateMoves(self):
        moves = list(self.allMoves)


        for move in self.allMoves:
            fromStack = self.stacks[move[0]]
            toStack = self.stacks[move[1]]
            # if there is anything on the stack
            if fromStack.top():
                # if this move is not valid
                if not toStack.pushable(fromStack.top()):
                    # remove it from the list of valid moves
                    moves.remove(move)
            else:
                moves.remove(move)


        if self.lastMove in moves:
            # to prevent back and forth
            moves.remove(self.lastMove)
        self.validMoves = moves

    def printValidMoves(self):
        print(
        self.validMoves)

    def move(self, t):
        if t in self.validMoves:
            fromStack = self.stacks[t[0]]
            toStack = self.stacks[t[1]]
            if fromStack.top():
                toStack.push(fromStack.pop())
            self.lastMove = t
            self.generateMoves()
            self.steps += 1
            self.path.append(t)

    def firstmove(self):
        fromstack = None
        tostack = None
        for stack in self.stacks:
            if stack.top() == 1:
                fromstack = self.stacks.index(stack)
                tostack = fromstack - 1
                if tostack == -1:
                    tostack = 2

        self.move((fromstack, tostack))

    def moveValid(self):
        # after first move there will be only one proper next move.

        self.firstmove()
        self.toString()


        self.generateMoves()
        moves = self.validMoves

        # remove all moves that involve moving the 1 disk
        theonestack = None
        for stack in self.stacks:
            if stack.top() == 1:
                theonestack = self.stacks.index(stack)

        removeAll = [(theonestack, 0), (theonestack, 1), (theonestack, 2)]
        r = removeAll

        for move in r:
            if move[0] == move[1]:
                removeAll.remove(move)

        for move in removeAll:
            if move in self.validMoves:
                moves.remove(move)

        if (len(moves) > 1):
            print(
            "error")
        elif self.validMoves:
            self.move(self.validMoves[0])

    def strategySolve(self):
        while (not self.solved()):
            self.moveValid()

    def reset(self):
        for stack in self.stacks:
            for x in range(stack.size()):
                stack.remove()

    def solved(self):
        return self.stacks[0].size() == 5

    def toString(self):
        for stack in self.stacks:
            print(
            "Tower: %d" % self.stacks.index(stack))
            stack.printStack()

    def equal(self, t):
        return self.P.equal(t.P) and self.Q.equal(t.Q) and self.R.equal(t.R)




def pchildren(children, open_states, closed):
    for child in children[:]:
        if open_states:
            for state in open_states:
                if child.equal(state):
                    children.remove(child)
        if closed:
            for state in closed:
                if child.equal(state):
                    children.remove(child)
    return children


def depth_first_search():

    start = towers()
    print(
    "Initial state:")
    start.toString()

    open_states = [start]
    closed = list()
    while open_states:
        X = open_states.pop()
        if X.solved():
            return X
        else:
            moves = X.validMoves
            children = []
            for move in moves:
                Y = deepcopy(X)
                Y.move(move)
                children.append(Y)
            closed.append(X)
            children = pchildren(children, open_states, closed)
            open_states.extend(children)


def main():
    solved = depth_first_search()
    print(
    "Goal State:")
    solved.toString()
    print(
    "Path is found. It took %d steps!" % solved.steps)

    userstring = input("Do you wanna know about steps? Yes or No")
    print("")
    if userstring == "Yes":
        print(solved.path)


if __name__ == '__main__':
    main()
