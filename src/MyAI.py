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
        self.maxRow, self.maxCol = 7,7

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
        if self.direction == 'U' and self.row - 1 > -1 :
            self.row -= 1
            return 1
        if self.direction == 'D' and self.row + 1 < self.maxRow:
            self.row += 1
            return 1
        if self.direction == 'R' and self.col + 1 < self.maxCol:
            self.col += 1
            return 1
        if self.direction == 'L' and self.col - 1 > -1:
            self.col -= 1
            return 1
        return -1

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
        if self.row - 1 > -1:
            if (self.worldMatrix[self.row - 1][self.col] != 'S'):
                self.worldMatrix[self.row - 1][self.col] = flag
        if self.row + 1 < self.maxRow:
            if (self.worldMatrix[self.row + 1][self.col] != 'S'):
                self.worldMatrix[self.row + 1][self.col] = flag
        if self.col - 1 > -1:
            if (self.worldMatrix[self.row][self.col - 1] != 'S'):
                self.worldMatrix[self.row][self.col - 1] = flag
        if self.col + 1 < self.maxCol:
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
        self.worldMatrix[self.row][self.col] = 'S'

    '''
    Input:
        - N/a

    Output:
        -N/a

    - When we feel a bump, and we have to revert the action, also setting max bounds to go to
    '''    
    def revertAction(self):
        if (self.direction == 'U'):
            self.row -= 1
        elif (self.direction == 'L'):
            self.col 
        elif (self.direction == 'D'):
            self.direction = 'R'
            return
        elif (self.direction == 'R'):
            self.direction = 'U'
            return

    '''
    Input:
        - stench, breeze, glitter, bump, scream

    Output:
        - Action

    - This is the main function that will be called in order to find the best plan of action
    '''
    def getAction( self, stench, breeze, glitter, bump, scream ):
        print("stench: ", stench)
        print("breeze: ", breeze)
        print("bump: ", bump)
        self.updateMap(stench, breeze, glitter, bump, scream)
        self.printMap()
        print('row: ', self.row, 'col: ', self.col)
        print('direction: ', self.direction)



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
        return Agent.Action.CLIMB




        #python3 Main.py -f ./Worlds
        #to iterate through the worlds