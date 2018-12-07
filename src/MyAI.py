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
        self.justShot = False
        self.wumpusKilled = False
        self.started = False
        self.clockwise = False
        self.backtracking = False
        self.stuck = False
        self.justGrabbedGold = False
        self.hasGold = False
        self.turnCount = 0
        self.pastTurns = [] # used to see if we've made a 180 degree turn 
        self.locations = [(6,0)] # stack containing previous spots
        self.visited = {(6,0): 1}
        self.findSurrounding = False

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
                self.backtracking = True
                if not self.hasGold:
                    self.findSurrounding = True
                if self.justGrabbedGold:
                    self.justGrabbedGold = False
                self.stuck = True
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

    def printMap(self):
        for row in self.worldMatrix:
            print(row)

    '''
    Input:
        - N/a

    Output:
        -N/a

        - When we feel a bump, and we have to revert the action internally, also setting max bounds to go to
        - Only useful for setting the max bounds for the right and upper sides. 
    '''    
    def revertAction(self):
        #print("revert")
        self.locations.pop()
        self.visited.pop((self.row, self.col))
        
        self.worldMatrix[self.row][self.col] = -1
        if (self.direction == 'U'):
            self.maxRow = self.row + 1
            self.row += 1

        elif (self.direction == 'R'):
            self.maxCol = self.col -1
            self.col -= 1
    
    '''
    Input:
        - row, col

    Output:
        - True or False

    - Will check to see if the provided (row, col) is valid to move to (we haven't already visited it, and is known to be safe)
    '''

    def isValid(self, row, col):
        return (row, col) not in self.visited and self.worldMatrix[row][col] == 'S' and (row, col) != (self.row, self.col)

    '''
    Input:
        - row, col

    Output:
        - List of valid (x, y) coords

    - Will check to see if the provided (row, col) have valid "child nodes"/spots around them. For use in DFS.
    '''
    def checkSurrounding(self, rowCol):
        #valid = []
        row = rowCol[0]
        col = rowCol[1]
        if row != 6:
            if self.isValid(row + 1, col):
                return (row + 1, col)
        if row != self.maxRow:
            if self.isValid(row - 1, col):
                return (row - 1, col)
        if col != 0:
            if self.isValid(row, col - 1):
                return (row, col - 1)
        if col != self.maxCol:
            if self.isValid(row, col + 1):
                return (row, col + 1)

        return (-1,-1)

    '''
    Input:
        - n/a

    Output:
        - True or Flase

    - Checks to make sure at least two moves have been made. If so, we can safely see if the agent has made a 180 degree turn
    '''
    def checkForTurnAround(self):
        return len(self.pastTurns) >= 2
    
    '''
    Input:
        - percepts

    Output:
        - Action

    - Actions to be taken in the starting square of the game. Can likely be generalized for regular use, 
    - so we may not need this in the future
    '''
    def startOfGameAction(self, stench, breeze, glitter, bump, scream):            
            #dip if theres a chance of a pit
            if breeze:
                return Agent.Action.CLIMB

            #wumpus shot, front clear
            if scream:
                self.started = True     
                self.updateRowCol()
                self.wumpusKilled = True
                self.pastTurns.append("forward")
                return Agent.Action.FORWARD

            #shoot the arrow, wumpus may be in front of us
            if stench and not self.wumpusKilled and self.hasArrow:
                self.hasArrow = False
                return Agent.Action.SHOOT

            self.started = True
            self.updateRowCol()
            self.pastTurns.append("forward") 
            return Agent.Action.FORWARD

    '''
    Input:
        - N/A

    Output:
        - Action

    - Finds alternate locations are the most recently visited location on the stack (the one before your current spot) 
    - and moves the agent back one spot. From here, the agent should start exploring the child/alternate spots on the
    - locations stack
    '''

    def backtrack(self):
        #print("in backtrack()")

        if self.stuck:
            #print("getting unstuck")
            self.locations.pop()
            self.updateRowCol()
            self.pastTurns.append("forward")
            self.stuck = False
            return Agent.Action.FORWARD


        if (self.row, self.col) != self.locations[-1]:
            #print("catchup")
            return self.goTo(self.locations[-1])

        if self.findSurrounding:
            #print("searching for locations around ", self.locations[-1])
            validLocation = self.checkSurrounding(self.locations[-1])
            if validLocation != (-1, -1):
                #print("location found, ", validLocation)
                self.findSurrounding = False
                self.locations.append(validLocation)
                self.backtracking = False
            else:
                self.locations.pop()
        else:
            self.locations.pop()
        if len(self.locations) > 0:
            #print("backtracking to ", self.locations[-1])
            return self.goTo(self.locations[-1])
        else:
            return Agent.Action.CLIMB





    def isNotVisited(self):
        if self.direction == 'U': 
            return (self.row - 1, self.col) not in self.visited
        if self.direction == 'D':
            return (self.row + 1, self.col) not in self.visited
        if self.direction == 'L':
            return (self.row, self.col - 1) not in self.visited
        if self.direction == 'R':
            return (self.row, self.col + 1) not in self.visited

    '''
    Input:
        - percepts

    Output:
        - Action

    - Will move the agent forwards if possible, or turn him right or left 
    '''

    def move(self, stench, breeze, glitter, bump, scream):

        if self.isFrontClear() and self.isFrontSafe(stench, breeze, glitter, bump, scream) and self.isNotVisited() and not self.justGrabbedGold:     
            #self.addLocation()
            self.updateRowCol()
            #self.started = True
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

    '''
    Input:
        - location

    Output:
        - Action

    - Backtracks the stack
    '''

    def goTo(self, location):
        if self.row - location[0] == 1:
            if self.direction == 'L':
                self.updateDirection("right")
                self.pastTurns.append("right")
                return Agent.Action.TURN_RIGHT
            elif self.direction == 'R':
                self.updateDirection("left")
                self.pastTurns.append("left")
                return Agent.Action.TURN_LEFT

        if self.row - location[0] == -1:
            if self.direction == 'L':
                self.updateDirection("left")
                self.pastTurns.append("left")
                return Agent.Action.TURN_LEFT
            elif self.direction == 'R':
                self.updateDirection("right")
                self.pastTurns.append("right")
                return Agent.Action.TURN_RIGHT

        if self.col - location[1] == 1:
            if self.direction == 'D':
                self.updateDirection("right")
                self.pastTurns.append("right")
                return Agent.Action.TURN_RIGHT
            elif self.direction == 'U':
                self.updateDirection("left")
                self.pastTurns.append("left")
                return Agent.Action.TURN_LEFT

        if self.col - location[1] == -1:
            if self.direction == 'D':
                self.updateDirection("left")
                self.pastTurns.append("left")
                return Agent.Action.TURN_LEFT
            elif self.direction == 'U':
                self.updateDirection("right")
                self.pastTurns.append("right")
                return Agent.Action.TURN_RIGHT

        #print("GOTO FORWARD")
        self.updateRowCol()
        self.pastTurns.append("forward")
        return Agent.Action.FORWARD

    '''
    Input:
        - N/A
    Output:
        - N/A

    - Adds current location to stack and visited, if not already in either
    '''

    def addLocation(self):
        if (self.row, self.col) not in self.visited:
            self.visited[(self.row, self.col)] = 1 
            #print("added ", self.row, ", ", self.col, "to visited") 
            if (self.row, self.col) != self.locations[-1]:
                self.locations.append((self.row, self.col))
                #print("added ", self.row, ", ", self.col, "to locations") 

    '''
    Input:
        - stench, breeze, glitter, bump, scream

    Output:
        - Action

    - This is the main function that will be called in order to find the best plan of action
    '''
    def getAction( self, stench, breeze, glitter, bump, scream ):
        try:
            '''if self.justShot:
                self.justShot = False
                return self.handleShot(stench, breeze, glitter, bump, scream)'''

            #self.printMap()
            
            stench = False if ( self.wumpusKilled ) else stench

            self.addLocation()

            #print("past locations:", self.locations, "visited", self.visited)
            #print("row: ", self.row, "col: ", self.col)

            if (bump):
                self.revertAction()
            
            if self.checkForTurnAround():
                self.updateClockwise()

            #print("clockwise:", self.clockwise)
            #print("backtracking:", self.backtracking)
            #print("looking for surrounding spots:", self.findSurrounding)

            self.updateMap(stench, breeze, glitter, bump, scream)  

            if glitter:
                self.justGrabbedGold = True
                self.hasGold = True
                #self.backtracking = True
                #self.locations.pop()
                return Agent.Action.GRAB

            if self.row == 6 and self.col == 0 and self.hasGold:
                return Agent.Action.CLIMB

            if not self.started and breeze:
                return Agent.Action.CLIMB

            #start of game
            if self.row == 6 and self.col == 0 and not self.started:
                return self.startOfGameAction(stench, breeze, glitter, bump, scream)

            #climb out if we've returned to start and no moves are left
            if self.row == 6 and self.col == 0 and len(self.locations) == 0:
                return Agent.Action.CLIMB

            if self.backtracking:
                return self.backtrack()

            #movement logic
            #print("moving, getAction")
            if not self.started:
                self.started = True
            return self.move(stench, breeze, glitter, bump, scream)
        
        except Exception as e :
            print(e)
    
        #python3 Main.py -f ./Worlds
        #to iterate through the worlds
        

        '''def handleShot(self, stench, breeze, glitter, bump, scream):
        if scream:
            self.wumpusKilled = True

        if not self.started:
            self.started = True
        
        if breeze:
            return self.move(stench, breeze, glitter, bump, scream)
        else:
            self.updateRowCol()
            self.pastTurns.append("forward")
            return Agent.Action.FORWARD'''

        #code for shooting wumpus anywhere on map. didn't seem to help and only affects a small portion of the map,
        #so I'll leave it down here for now. 
        '''if stench and not self.wumpusKilled and self.hasArrow and self.isFrontClear() and not self.hasGold:
            self.hasArrow = False
            self.justShot = True
            return Agent.Action.SHOOT'''

