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

#hasArrow = True
#wumpusKilled = False

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
    '''
    Input: N/a

    Output:
        worldMatrix

        -Prints out the matrix
    '''
    def printMap(self):
        for row in self.worldMatrix:
            print(row)


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
            return self.col -1 >= 0

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

        #if scream and not breeze:
        #    return True


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
        print("update mpa")
        if (stench or breeze): #lowkey unsafe area
            print('breeze')
            self.worldMatrix[self.row][self.col] = 'S'
            self.updateSurroundingArea('P')
        else:
            print("got to this safe area")
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
        print('in revert')
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
        stench = False if ( self.wumpusKilled ) else stench

        self.updateMap(stench, breeze, glitter, bump, scream)
        print("update map called")
        self.printMap()
        print('row: ', self.row, 'col: ', self.col)
        print('direction: ', self.direction)
        print("Front safe?: ", self.isFrontSafe(stench, breeze, glitter, bump, scream))
        #starting spot
        if self.row == 6 and self.col == 0:
            if breeze:
                print("breeze: ", breeze)
                return Agent.Action.CLIMB

            if scream:
                stench = False if ( self.wumpusKilled ) else stench
                self.updateMap(stench, breeze, glitter, bump, scream)
                print("scream: ", scream)
                self.updateRowCol()
                self.wumpusKilled = True

                return Agent.Action.FORWARD
    
            if stench and not self.wumpusKilled:
                print("stench: ", stench)
                self.hasArrow = False
                return Agent.Action.SHOOT

        '''
        trying to make scream and stench more general, instead of specific to start state
        if scream:
            #stench = False if ( self.wumpusKilled ) else stench
            self.updateMap(stench, breeze, glitter, bump, scream)
            print("scream: ", scream)
            self.updateRowCol()
            self.wumpusKilled = True

            return Agent.Action.FORWARD

        if stench and not self.wumpusKilled:
            print("stench: ", stench)
            if self.isFrontClear() and not self.isFrontSafe():
                self.hasArrow = False
                return Agent.Action.SHOOT
            else:
                return Agent.Action.TURN_LEFT'''

        if self.isFrontClear():
            return Agent.Action.FORWARD

        
        '''
        if (bump):
            print('REVERT')
            self.revertAction()
        print ( "Press 'w' to Move Forward  'a' to 'Turn Left' 'd' to 'Turn Right'" )
        
        #Get Input
        userInput = input ( 'Please input: ' ).strip()
        while not userInput:
            userInput = input().strip()
        
        # Return Action Associated with Input
        if userInput[0] == 'w':
            self.updateRowCol()
            return Agent.Action.FORWARD
            
        if userInput[0] == 'a':
            self.updateDirection('left')
            return Agent.Action.TURN_LEFT
            
        if userInput[0] == 'd':
            self.updateDirection('right')
            return Agent.Action.TURN_RIGHT
            
        if userInput[0] == 's':
            return Agent.Action.SHOOT
            
        if userInput[0] == 'g':
            return Agent.Action.GRAB
        return Agent.Action.CLIMB'''




        #python3 Main.py -f ./Worlds
        #to iterate through the worlds
