# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    '''
    Input: none
    Output: none

        -inits all necessary items
    '''
    def __init__ ( self ):      
        self.worldMatrix = [[-1,-1,-1,-1,-1,-1,-1] for i in range(7)]
        self.row, self.col = 6,0
        self.direction = 'R'
        self.maxRow, self.maxCol = 0,6
        self.hasArrow = True
        self.wumpusKilled = False
        self.started = False
        self.clockwise = False
        self.backtracking = False
        self.grabbedGold = False
        self.turnCount = 0
        self.pastTurns = [] # used to see if we've made a 180 degree turn 
        self.pastMoves = [] # stack containing previous moves
        self.visited = {}

    '''
    Input:
        N/A

    Output:
        1 - if successful 
        -1 - if not successful 

        - updates the location internally where the agent is within the world based on direction
    '''
    # direction: u d l r (up down left right)
    def updateRowCol(self):
        #instead of checking bounds with each if statement, check at once here, then check direction
        if self.isFrontClear():
            if self.direction == 'U':
                self.row -= 1
                return 1
            if self.direction == 'D':
                self.row += 1
                return 1
            if self.direction == 'R':
                self.col += 1
                return 1
            if self.direction == 'L':
                self.col -= 1
                return 1
        return -1

    '''
    Input: 
        N/A
    Output:
        True or False

    Reports whether or not there is a wall in front of the user
    '''
    def isFrontClear(self):
        if self.direction == 'U':
            return self.row - 1 >= self.maxRow
        if self.direction == 'D':
            return self.row + 1 <= 6
        if self.direction == 'R':
            return self.col + 1 <= self.maxCol
        if self.direction == 'L':
            return self.col - 1 >= 0

    '''
    Input:
        stench, breeze, glitter(?), bump(?), scream
    Output:
        True or False
    
    Reports whether or not the spot immediately in front of the user is safe or not (does not have pit or wumpus)
    '''
    def isFrontSafe(self, stench, breeze, glitter, bump, scream):
        #no percepts
        if not stench and not breeze:
            return True

        #already marked as safe
        if self.direction == 'U' and self.worldMatrix[self.row - 1][self.col] == 'S':
            return True
        if self.direction == 'D' and self.worldMatrix[self.row + 1][self.col] == 'S':
            return True
        if self.direction == 'L' and self.worldMatrix[self.row][self.col - 1] == 'S':
            return True
        if self.direction == 'R' and self.worldMatrix[self.row][self.col + 1] == 'S':
            return True

        return False

    '''
    Input:
        Turn - either left or right

    Output:
        N/A

        - updates the direction based on the turn needed
    '''
    def updateDirection(self, turn):
        if turn == 'left':
            if (self.direction == 'U'):
                self.direction = 'L'
                return
            elif (self.direction == 'L'):
                self.direction = 'D'
                return
            elif (self.direction == 'D'):
                self.direction = 'R'
                return
            elif (self.direction == 'R'):
                self.direction = 'U'
                return
        if turn == 'right':
            if self.direction == 'U':
                self.direction = 'R'
                return
            elif self.direction == 'L':
                self.direction = 'U'
                return
            elif self.direction == 'D':
                self.direction = 'L'
                return
            elif self.direction == 'R':
                self.direction = 'D'            
                return

    '''
    Input:
        N/A
    Output:
        True or False

    Keeps track of whether we are going clockwise or counter clockwise. 
    This determines which direction to turn when front is not safe/clear
    and should help prevent getting stuck
    '''
    def updateClockwise(self):
        if self.pastTurns[-1] != "forward" and self.pastTurns[-2] != "forward":
            if self.pastTurns[-1] == self.pastTurns[-2]:
                self.clockwise = not self.clockwise
                self.pastTurns.clear()
        return self.clockwise
    
    '''
    Input:
        flag - 
                P - potentially unsafe
                D - Do not go, 100% bad
                S - Safe to go
    Output:
        N/A

    - Will update the surrounding areas with the given flag, if it's not a Safe space 
    '''
    def updateSurroundingArea(self, flag):
        if self.row - 1 >= self.maxRow:
            if (self.worldMatrix[self.row - 1][self.col] != 'S'):
                self.worldMatrix[self.row - 1][self.col] = flag
        if self.row + 1 <= 6:
            if (self.worldMatrix[self.row + 1][self.col] != 'S'):
                self.worldMatrix[self.row + 1][self.col] = flag
        if self.col - 1 >= 0:
            if (self.worldMatrix[self.row][self.col - 1] != 'S'):
                self.worldMatrix[self.row][self.col - 1] = flag
        if self.col + 1 <= self.maxCol:
            if (self.worldMatrix[self.row][self.col + 1] != 'S'):
                self.worldMatrix[self.row][self.col + 1] = flag       

    '''
    Input:
        - stench, breeze, glitter, bump, scream
            All boolean values

    Output:
        - N/A

    Will update the map based on what is given in the input. 
    '''
    def updateMap(self,stench, breeze, glitter, bump, scream):
        if (stench or breeze): #lowkey unsafe area
            self.worldMatrix[self.row][self.col] = 'S'
            self.updateSurroundingArea('P')
        else:
            self.worldMatrix[self.row][self.col] = 'S'
            self.updateSurroundingArea('S')

    '''
    Input:
        - N/a

    Output:
        -N/a

        - When we feel a bump, and we have to revert the action internally, also setting max bounds to go to
        - Only useful for setting the max bounds for the right and upper sides. 
    '''    
    def revertAction(self):
        self.worldMatrix[self.row][self.col] = -1
        if (self.direction == 'U'):
            self.maxRow = self.row -1
            self.row -= 1

        elif (self.direction == 'R'):
            self.maxCol = self.col -1
            self.col -= 1

    '''
    Input:
        - stench, breeze, glitter, bump, scream

    Output:
        - Action

    - This is the main function that will be called in order to find the best plan of action
    '''
    def getAction( self, stench, breeze, glitter, bump, scream ):
        print("past moves:", self.pastMoves, "visited", self.visited)

        stench = False if ( self.wumpusKilled ) else stench

        if glitter:
            self.grabbedGold = True
            return Agent.Action.GRAB

        if self.grabbedGold and self.turnCount < 2:
            self.turnCount += 1
            if self.clockwise:
                self.updateDirection("right")
                self.pastTurns.append("right")
                return Agent.Action.TURN_RIGHT
            else:    
                self.updateDirection("left")
                self.pastTurns.append("left")
                return Agent.Action.TURN_LEFT

        if (bump):
            self.revertAction()
        
        if len(self.pastTurns) >= 2:
            self.updateClockwise()
        
        self.updateMap(stench, breeze, glitter, bump, scream)
        
        #start of game
        if self.row == 6 and self.col == 0 and not self.started:
            
            #dip if theres a chance of a pit
            if breeze:
                return Agent.Action.CLIMB

            #wumpus shot, front clear
            if scream:
                self.started = True

                if (self.row, self.col) not in self.visited:
                    self.pastMoves.append((self.row, self.col))       
                    self.visited[(self.row, self.col)] = 1  
                self.updateRowCol()
                self.wumpusKilled = True
                self.pastTurns.append("forward")
                return Agent.Action.FORWARD

            #wumpus not shot, front still clear
            if not self.hasArrow:
                self.started = True
                if (self.row, self.col) not in self.visited:
                    self.pastMoves.append((self.row, self.col))       
                    self.visited[(self.row, self.col)] = 1 
                self.updateRowCol()
                self.pastTurns.append("forward") 
                return Agent.Action.FORWARD

            #shoot the arrow, wumpus may be in front of us
            if stench and not self.wumpusKilled:
                self.hasArrow = False
                return Agent.Action.SHOOT

        #climb out if we've returned to start
        if self.row == 6 and self.col == 0 and self.started:
            return Agent.Action.CLIMB

        if self.isFrontClear() and self.isFrontSafe(stench, breeze, glitter, bump, scream):
            if (self.row, self.col) not in self.visited:
                self.pastMoves.append((self.row, self.col))       
                self.visited[(self.row, self.col)] = 1  

            self.updateRowCol()
            self.started = True
            self.pastTurns.append("forward")   
            return Agent.Action.FORWARD
        elif self.clockwise:
            self.updateDirection("right")
            self.pastTurns.append("right")
            return Agent.Action.TURN_RIGHT
        else:    
            self.updateDirection("left")
            self.pastTurns.append("left")
            return Agent.Action.TURN_LEFT  

        
        #python3 Main.py -f ./Worlds
        #to iterate through the worlds
