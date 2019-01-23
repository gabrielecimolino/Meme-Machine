from tkinter import *

import random
import Knapsack

WIDTH = 0
HEIGHT = 0

backgroundColor = '#aacbff'
graph = None
problem = None
instance = None
root = None

grid = None
gridFitness = None
gridColors = None
memeGrid = None

gridWidth = 0
gridHeight = 0

def drawGrid():
	global grid
	global gridColors
	global gridFitness
	global graph
	global WIDTH
	global HEIGHT
	
	gridWidth = len(grid)
	gridHeight = len(grid[0])

	widthPhi = WIDTH / 1.618
	heightPhi = HEIGHT / 1.618

	gridXOffset = (WIDTH - widthPhi) / 2
	gridYOffset = (HEIGHT - heightPhi) / 2

	cellWidth = widthPhi / gridWidth
	cellHeight = heightPhi / gridHeight


	for x in range(gridWidth):
		for y in range(gridHeight):
			
			colorHex = '#%02x%02x%02x' % gridColors[x][y]
			graph.create_rectangle(x * cellWidth + gridXOffset, y * cellHeight + gridYOffset, (x + 1) * cellWidth + gridXOffset, (y + 1) * cellHeight + gridYOffset, fill=colorHex) 			
			graph.create_text(x * cellWidth + gridXOffset + (cellWidth / 2.0), y * cellHeight + gridYOffset + (cellHeight / 2.0), text=str(gridFitness[x][y]))

def nextGeneration():
	global grid
	global gridColors
	global gridFitness
	global problem
	global instance
	global gridWidth
	global gridHeight


	#print("Next generation\nGrid width: " + str(gridWidth) + ", Grid height: " + str(gridHeight))	
	newGrid = [ [ None for y in range(gridHeight) ] for x in range(gridWidth) ]
	
	fittestMember = [0, 0]
	highestFitness = 0


	for x in range(gridWidth):
		for y in range(gridHeight):
			
			gridFitness[x][y] = problem.EvaluateFitness(grid[x][y])	
			if(gridFitness[x][y] > highestFitness):
				highestFitness = gridFitness[x][y]
				fittestMember[0] = x
				fittestMember[1] = y
				#print("Fitness(" + str(x) + ", " + str(y) + "): " + str(gridFitness[x][y])) 
		
	problem.PrintSolutionInfo(instance, grid[fittestMember[0]][fittestMember[1]])
	print("Highest fitness: " + str(highestFitness))
	
	for x in range(gridWidth):
		for y in range(gridHeight):

			fittestNeighbour = [0,0]
			maxFitness = 0
			
			for xOffset in range(-1, 2):
				for yOffset in range(-1, 2):

					xIndex = x + xOffset
					yIndex = y + yOffset

					if(xIndex >= 0 and xIndex < gridWidth and yIndex >= 0 and yIndex < gridHeight):
						if(not (xOffset == 0 and yOffset == 0)):
							if(gridFitness[x + xOffset][y + yOffset] > maxFitness):
								fittestNeighbour[0] = xOffset
								fittestNeighbour[1] = yOffset
			
			#print("Fittest neighbour: " + str(fittestNeighbour))
			fittestNeighbour[0] = fittestNeighbour[0] + x
			fittestNeighbour[1] = fittestNeighbour[1] + y
			
			newGrid[x][y] = problem.Crossover(instance, grid[x][y], grid[fittestNeighbour[0]][fittestNeighbour[1]], [gridFitness[x][y], gridFitness[fittestNeighbour[0]][fittestNeighbour[1]] ])


	for x in range(gridWidth):
		for y in range(gridHeight):
			
			for it in range(10):
				problem.Mutate(instance, newGrid[x][y])

			#gridColors[x][y] = problem.SolutionColor(newGrid[x][y])
			
			grid[x][y] = newGrid[x][y]							
			problem.SolutionColors(instance, grid, gridColors)
							

def Exchange():
	global grid
	global gridFitness
	global memeGrid
	global problem
	global instance
	global gridWidth
	global gridHeight
	
	fitnessList = []
	totalFitness = 0

	newMemeGrid = [ [ None for x in range(gridWidth) ] for y in range(gridHeight) ]

	for x in range(gridWidth):
		for y in range(gridHeight):
			totalFitness += gridFitness[x][y]
			fitnessList.append((x, y, gridFitness[x][y]))
			newMemeGrid[x][y] = problem.IdentifyMeme(instance, grid[x][y])

	#fitnessList.sort(key=(lambda x: x[2]))
	for i in range(gridWidth * gridHeight):
		randomSelection = int(random.random() * totalFitness)
		foundSelection = False

		for j in range(len(fitnessList)):
			randomSelection -= fitnessList[j][2]
			if(randomSelection <= 0 and not foundSelection):
				foundSelection = True
				
				for xOffset in range(-1, 2):
					for yOffset in range(-1, 2):
						p = random.random()

						if(p < 0.5):

							if(fitnessList[j][0] + xOffset >= 0 and fitnessList[j][0] + xOffset < gridWidth and fitnessList[j][1] + yOffset >= 0 and fitnessList[j][1] + yOffset < gridHeight):
								
								#print("Member (" + str(fitnessList[j][0]) + ", " + str(fitnessList[j][1]) + ") is sharing with member (" + str(fitnessList[j][0] + xOffset) + ", " + str(fitnessList[j][1] + yOffset) + ")")
								problem.Learn(instance, grid[fitnessList[j][0] + xOffset][fitnessList[j][1] + yOffset], newMemeGrid[fitnessList[j][0]][fitnessList[j][1]])
						
	for x in range(gridWidth):
		for y in range(gridHeight):

			gridFitness[x][y] = problem.EvaluateFitness(grid[x][y])
	
	problem.SolutionColors(instance, grid, gridColors)


def update():
	global graph

	graph.delete(ALL)
	
	drawGrid()
	graph.update()
	graph.after(1, update)

def quit():
	global root

	root.destroy()	

def main():
	global root
	global graph
	global WIDTH
	global HEIGHT
	global grid
	global gridColors
	global gridFitness
	global gridWidth
	global gridHeight
	global problem
	global instance	

	gridWidth = 10
	gridHeight = 10

	grid = [ [ None for y in range(gridHeight) ]  for x in range(gridWidth) ]
	gridFitness = [ [ 0 for y in range(gridHeight) ] for x in range(gridWidth) ]
	gridColors = [ [ (0.0, 0.0, 0.0) for y in range(gridHeight) ] for x in range(gridWidth) ]

	root = Tk()
	root.overrideredirect(True)
	root.attributes("-topmost", True)

	WIDTH = root.winfo_screenwidth() / 2
	HEIGHT = root.winfo_screenheight() - (root.winfo_screenheight() / 10)

	root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, WIDTH, (root.winfo_screenheight() - HEIGHT) / 2))

	root.bind_all('<Escape>', lambda event: event.widget.quit())

	frame = Frame(root, height=(HEIGHT / 10))
	frame.pack()

	quitButton = Button(frame, text="Quit", bg='red', command=quit)
	quitButton.pack(side=LEFT) 

	nextButton = Button(frame, text="Next Generation", command=nextGeneration)
	nextButton.pack(side=LEFT)	

	exchangeButton = Button(frame, text="Exchange", command=Exchange)
	exchangeButton.pack(side=LEFT)

	graph = Canvas(root, width=WIDTH, height=HEIGHT, background=backgroundColor)
	graph.after(50, update)
	graph.pack()

	problem = Knapsack
	instance = problem.GenerateRandomProblemInstance(10, 50, 1000, 10, 10)
	problem.PrintProblemInfo(instance)
	
	for x in range(gridWidth):
		for y in range(gridHeight):
			grid[x][y] = problem.GenerateRandomProblemSolution(instance, [0.5])
			#gridColors[x][y] = problem.SolutionColor(grid[x][y]) 
	
	problem.SolutionColors(instance, grid, gridColors)

	mainloop()

if __name__ == "__main__":
    main()
