from math import *
import turtle

# CONSTANTS
WIDTH = 800
HEIGHT = 600
AXISCOLOR = "black"
TICKSIZE = 5
DELTA = 0.1
EXTREMACIRCLERAD = 5

#Global Variables
lowestGlobalMin = None
largestGlobalMax = None


#
#  Returns the screen (pixel based) coordinates of some (x, y) graph location base on configuration
#
#  Parameters:
#   xo, yo : the pixel location of the origin of the  graph
#   ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#   x, y: the graph location to change into a screen (pixel-based) location
#
#  Usage -> screenCoor(xo, yo, ratio, 1, 0)
#
#  Returns: (screenX, screenY) which is the graph location (x,y) as a pixel location in the window
#
def screenCoor(xo, yo, ratio, x, y):
    #print(((xo + ratio * x), (yo + ratio * y)))
    return (xo + ratio * x), (yo + ratio * y) #Calculate new pixel coordinates and return them.

#
#  Returns a string of the colour to use for the current expression being drawn
#  This colour is chosen based on which how many expression have previously been drawn
#  The counter starts at 0, the first or 0th expression, should be red, the second green, the third blue
#  then loops back to red, then green, then blue, again
#
#  Usage -> getColor(counter)
#
#  Parameters:
#  counter: an integer where the value is a count (starting at 0) of the expressions drawn
#
#  Returns: 0 -> "red", 1 -> "green", 2 -> "blue", 3 -> "red", 4 -> "green", etc.
#
def getColor(counter):
    if(counter%3 == 0):
        return "red"
    elif(counter%3 == 1):
        return "green"
    elif(counter%3 == 2):
        return "blue"

#
#  Draw in the window an xaxis label (text) for a point at (screenX, screenY)
#  the actual drawing points will be offset from this location as necessary
#  Ex. for (x,y) = (1,0) or x-axis tick/label spot 1, draw a tick mark and the label 1
#
#  Usage -> drawXAxisLabelTick(pointer, 1, 0, "1")
#
#  Parameters:
#  pointer: the turtle drawing object
#  screenX, screenY): the pixel screen location to drawn the label and tick mark for
#  text: the text of the label to draw
#
#  Returns: Nothing
#
def drawXAxisLabelTick(pointer, screenX, screenY, text):
    pointer.pendown()
    pointer.sety(screenY+TICKSIZE)
    pointer.write(text, align = "center")
    pointer.sety(screenY-TICKSIZE)
    pointer.sety(screenY)

#
#  Draw in the window an yaxis label (text) for a point at (screenX, screenY)
#  the actual drawing points will be offset from this location as necessary
#  Ex. for (x,y) = (0,1) or y-axis tick/label spot 1, draw a tick mark and the label 1
#
#  Usage -> drawXAxisLabelTick(pointer, 0, 1, "1")
#
#  Parameters:
#  pointer: the turtle drawing object
#  screenX, screenY): the pixel screen location to drawn the label and tick mark for
#  text: the text of the label to draw
#
#  Returns: Nothing
#
def drawYAxisLabelTick(pointer, screenX, screenY, text):
    pointer.pendown()
    pointer.setx(screenX+TICKSIZE)
    pointer.penup()
    pointer.sety(screenY-10) #This is to align text to be just beside the tick
    pointer.write(text, align = "left")
    pointer.sety(screenY) #Set the y  position back before drawing more ticks.
    pointer.pendown()
    pointer.setx(screenX-TICKSIZE)
    pointer.setx(screenX)

#
#  Draw in the window an xaxis (secondary function is to return the minimum and maximum graph locations drawn at)
#
#  Usage -> drawXAxis(pointer, xo, yo, ratio)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#
#  Returns: (xmin, xmax) where xmin is minimum x location drawn at and xmax is maximum x location drawn at
#
def drawXAxis(pointer, xo, yo, ratio):
    xmin = 0
    xmax = 0

    pointer.penup()
    pointer.goto(xo,yo)
    pointer.color("black")
    pointer.pendown()

    xPosition = 1 #This is the turtles cartesian X Position to go to on the right side.
    
    while(pointer.position()[0] < WIDTH): #Draw the X axis going right
        pointer.goto(screenCoor(xo, yo, ratio, xPosition, 0))
        drawXAxisLabelTick(pointer, pointer.position()[0], pointer.position()[1], str(xPosition))
        xmax = max(xmax,xPosition)
        xPosition += 1

    pointer.penup()
    pointer.goto(xo,yo)
    pointer.pendown()
    xPosition = -1 #This is the turtles cartesian X Position to go to on the left side.

    while(pointer.position()[0] > 0): #Draw the X axis going left
        pointer.goto(screenCoor(xo, yo, ratio, xPosition, 0))
        drawXAxisLabelTick(pointer, pointer.position()[0], pointer.position()[1], str(xPosition))
        xmin = min(xmin,xPosition)
        xPosition -= 1

    
    return xmin, xmax

#
#  Draw in the window an yaxis 
#
#  Usage -> drawYAxis(pointer, xo, yo, ratio)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#
#  Returns: Nothing
#
def drawYAxis(pointer, xo, yo, ratio):
    ymin = 0
    ymax = 0
    
    pointer.penup()
    pointer.goto(xo,yo)
    pointer.color("black")
    pointer.pendown()

    yPosition = 1 #This is the turtles cartesian Y Position to go up to.
    
    while(pointer.position()[1] < HEIGHT): #Draw the Y axis going up
        pointer.goto(screenCoor(xo, yo, ratio, 0, yPosition))
        drawYAxisLabelTick(pointer, pointer.position()[0], pointer.position()[1], str(yPosition))
        xmax = max(ymax,yPosition)
        yPosition += 1

    pointer.penup()
    pointer.goto(xo,yo)
    pointer.pendown()
    
    yPosition = -1 #This is the turtles cartesian Y Position to go down to.

    while(pointer.position()[1] > 0): #Draw The Y axis going down.
        pointer.goto(screenCoor(xo, yo, ratio, 0, yPosition))
        drawYAxisLabelTick(pointer, pointer.position()[0], pointer.position()[1], str(yPosition))
        ymin = min(ymin,yPosition)
        yPosition -= 1
        

#
#  Draw in the window the given expression (expr) between [xmin, xmax] graph locations
#
#  Usage -> drawExpr(pointer, xo, yo, ratio, xmin, xmax, expr)
#
#  Parameters:
#  pointer: the turtle drawing object
#  xo, yo : the pixel location of the origin of the  graph
#  ratio: the ratio of pixels to single step in graph (i.e 1 step is ratio amount of pixels)
#  expr: the expression to draw (assumed to be valid)
#  xmin, ymin : the range for which to draw the expression [xmin, xmax]
#
#  Returns: Nothing
#
def drawExpr(pointer, xo, yo, ratio, xmin, xmax, expr):
    global largestGlobalMax #Use the global variables largestGlobalMax and lowestGlobalMin
    global lowestGlobalMin
    x = xmin
    exprType = type(eval(expr))
    globalMax = None
    globalMin = None
    currLocalMax = None
    currLocalMin = None
    pointer.penup()
    if(exprType != complex):
            pointer.goto(screenCoor(xo, yo, ratio, x, eval(expr)))
    pointer.pendown()
    while(x<=xmax): #Loop through all values n+0.1 where xmin <= n <= xmax
        #Set up the calculation of the extrema
        nextX = x+DELTA 
        prevX = x-DELTA
        exprType = type(eval(expr))
        if(exprType != complex):
            currentCoordinates = screenCoor(xo, yo, ratio, x, eval(expr)) #Get the pixel coordinates (x,y)

            #Calculate Extrema
            nextExpr = expr.replace("x", "nextX")
            prevExpr = expr.replace("x", "prevX")
            nextY = screenCoor(xo, yo, ratio, nextX, eval(nextExpr))[1]
            prevY = screenCoor(xo, yo, ratio, prevX, eval(prevExpr))[1]

            pointer.goto(currentCoordinates[0], currentCoordinates[1])#go to and draw the function


            if(type(eval(prevExpr)) != complex):
                currLocalMax,currLocalMin = identifyExtrema(currentCoordinates, pointer, expr, nextX, nextY, prevX, prevY,x)


            #Set the global max and global min for this function
            if(globalMax != None and currLocalMax != None):#Conditional that helps get rid of NoneType errors
                if(currLocalMax[1] > globalMax[1]):
                    globalMax = currLocalMax
                globalMax = max(globalMax, currLocalMax)
            elif(currLocalMax != None):#Conditional that helps get rid of NoneType errors
                globalMax = currLocalMax
            if(globalMin != None and currLocalMin != None):#Conditional that helps get rid of NoneType errors
                if(currLocalMin[1] < globalMin[1]):
                    globalMin = currLocalMin
            elif(currLocalMin != None):#Conditional that helps get rid of NoneType errors
                globalMin = currLocalMin
        pointer.pendown()        

        #x increments through the delta
        x = nextX

        
    #Set the global max and global min for all of the functions       
    if(largestGlobalMax != None and globalMax != None):#Conditional that helps get rid of NoneType errors
        if(globalMax[1] > largestGlobalMax[1]):
            largestGlobalMax = globalMax
    elif(globalMax != None):#Conditional that helps get rid of NoneType errors
            largestGlobalMax = globalMax
    if(lowestGlobalMin != None and globalMin != None):#Conditional that helps get rid of NoneType errors
        if(globalMin[1] < lowestGlobalMin[1]):
            lowestGlobalMin = globalMin
    elif(globalMin != None):#Conditional that helps get rid of NoneType errors
        lowestGlobalMin = globalMin

    #Print the global min and max for this and all of the functions.            
    if(globalMax == None):
        print("No global max value for this function")
    else:
        print("Approx Global Max For This Function: " + "(" + str(globalMax) + ")")
    if(globalMin == None):
        print("No global min for this function")
    else:
        print("Approx Global Min For This Function: " + "(" + str(globalMin)+ ")")
        
    if(largestGlobalMax == None):
        print("No largest global max value")
    else:
        print("Largest Global Max: " + "(" + str(largestGlobalMax) + ")")
    if(lowestGlobalMin == None):
        print("No lowest global min value")
    else:
        print("Lowest Global Min: " + "(" + str(lowestGlobalMin) + ")")

    pointer.penup()
    pointer.goto(xo,yo)
#
#  Setup of turtle screen before we draw
#  DO NOT CHANGE THIS FUNCTION
#
#  Returns: Nothing
#
def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer.hideturtle()
    screen.delay(delay=0)
    return pointer

#
#  Main function that attempts to graph a number of expressions entered by the user
#  The user is also able to designate the origin of the chart to be drawn, as well as the ratio of pixels to steps (shared by both x and y axes)
#  The window size is always 800 width by 600 height in pixels
#  DO NOT CHANGE THIS FUNCTION
#
#  Returns: Nothing
#
def main():
    #Setup window
    pointer = setup()

    #Get input from user
    xo, yo = eval(input("Enter pixel coordinates of origin: "))
    ratio = int(input("Enter ratio of pixels per step: "))

    #Set color and draw axes (store discovered visible xmin/xmax to use in drawing expressions)
    pointer.color(AXISCOLOR)
    xmin, xmax = drawXAxis(pointer, xo, yo, ratio)
    drawYAxis(pointer, xo, yo, ratio)

    #Loop and draw experssions until empty string "" is entered, change expression colour based on how many expressions have been drawn
    expr = input("Enter an arithmetic expression: ")
    counter = 0
    while expr != "":
        pointer.color(getColor(counter))
        drawExpr(pointer, xo, yo, ratio, xmin, xmax, expr)
        expr = input("Enter an arithmetic expression: ")
        counter += 1
#
#   Function that tests if a given point is a local extrema and circles it and prints it to console
#   Function updates the global variable largestGlobalMaximum and lowestGlobalMinimum accordingly
#
#   Parameters:
#   point:  The point that is being tested for a local minimum
#   pointer:The turtle drawing object
#   Expr:   The expression that is being tested
#   nextX:  The next X value of the function(in cartesian plane coordinates)
#   nextY:  The next Y value of the function(in pixels)
#   prevX:  The previous X value of the function(in cartesian plane coordinates)
#   prevY:  The previous Y value of the function(in pixels)
#   x:      The current x value of the function(in cartesian plane coordinates)
#
#   Returns: Nothing
#
#TODO: test why its taking the last max value
def identifyExtrema(point, pointer, expr, nextX, nextY, prevX, prevY, x):
    color = pointer.pencolor()
    pixelY = point[1]
    localMax = None
    localMin = None
    if(prevY > pixelY < nextY):  #Tests for a local minimum and circles it if True
        pointer.color("orange")
        pointer.penup()
        pointer.sety(pixelY-EXTREMACIRCLERAD)
        pointer.pendown()
        pointer.circle(EXTREMACIRCLERAD)
        pointer.penup()
        pointer.sety(pointer.position()[1]+EXTREMACIRCLERAD)
        pointer.pendown()
        pointer.color(color)
        if(localMin != None): #Conditional that helps get rid of NoneType errors
            if(pixelY < localMin[1]): #If the current y coordinate is less than the current local min
                localMin = (round(x,5),round(eval(expr),5))#Round the values to be a little more precise as oppose to massive scientific notation numbers
        else:
            localMin = (round(x,5),round(eval(expr),5))#Round the values to be a little more precise as oppose to massive scientific notation numbers
    elif(prevY < pixelY > nextY): #Tests for a local maximum and circles it if True
        pointer.color("purple")
        pointer.penup()
        pointer.sety(pixelY-EXTREMACIRCLERAD)
        pointer.pendown()
        pointer.circle(EXTREMACIRCLERAD)
        pointer.penup()
        pointer.sety(pointer.position()[1]+EXTREMACIRCLERAD)
        pointer.pendown()
        pointer.color(color)
        if(localMax != None):#Conditional that helps get rid of NoneType errors
            if(pixelY > localMax[1]): #If the current y coordinate is greater than the current local max
                 localMax = (round(x,5),round(eval(expr),5))#Round the values to be a little more precise as oppose to massive scientific notation numbers
        else:
            localMax = (round(x,5),round(eval(expr),5))#Round the values to be a little more precise as oppose to massive scientific notation numbers
    #TODO TEST IF THE MAX/MIN is outside the grid.
       #print((localMin,localMax))
    return localMax, localMin
       
#Run the program
main()
