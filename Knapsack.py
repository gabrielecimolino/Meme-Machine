import random
import math
import numpy
import copy

def SolutionColors(problem, grid, gridColors):
	numberOfBags = problem[0]
	numberOfItems = len(problem[2])
	gridWidth = len(grid)
	gridHeight = len(grid[0])
	numberOfSolutions = gridWidth * gridHeight
	
	solutionMatrix = numpy.matrix([ numpy.zeros(numberOfItems * numberOfBags) for x in range(numberOfSolutions) ])

	for x in range(gridWidth):
		for y in range(gridHeight):
			solution = grid[x][y]
			matrixIndex = x + (gridWidth * y)
	
			for bagIndex in range(len(solution[0])):
				for item in solution[0][bagIndex]:
					solutionMatrix[matrixIndex, item + (numberOfItems * bagIndex)] = 1
	
	#print(solutionMatrix)

	u, s, vh = numpy.linalg.svd(solutionMatrix, full_matrices=False, compute_uv=True)
	
	#print(u)
	#print(s)
	#print(vh)

	for x in range(gridWidth):
		for y in range(gridHeight):
			matrixIndex = x + (gridWidth * y)
	
			gridColors[x][y] = (int(255 * ((1 + u[matrixIndex, 0]) / 2.0 )), int(255 * ((1 + u[matrixIndex, 1]) / 2.0)), int(255 * ((1 + u[matrixIndex, 2]) / 2.0)))
			
	#print(gridColors)	

def SolutionColor(solution):
	lists = [ [], [], [] ]

	for bag in range(len(solution[0])):
		for item in solution[0][bag]:
			listIndex = bag % 3

			lists[listIndex].append(item)

	color = [1.0, 1.0, 1.0]

	for l in range(len(lists)):
		for item in lists[l]:
			color[l] = color[l] * item

		if(len(lists[l]) > 0): color[l] = color[l] / float(len(lists[l]))

	mag = math.sqrt( (color[0] * color[0] ) + (color[1] * color[1]) + (color[2] * color[2]) )
		
	color[0] = float(color[0]) / mag
	color[1] = float(color[1]) / mag
	color[2] = float(color[2]) / mag

	return (color[0] * 255, color[1] * 255, color[2] * 255)		

def PrintModuleInfo():
	print("0-1 Knapsack\n============")

def PrintProblemInfo(problem):
	PrintModuleInfo()
	print("Instance has " + str(problem[0]) + " bags")

	for i in range(len(problem[1])):
		print("Bag " + str(i + 1) + " has capacity " + str(problem[1][i]))

	print()
	print("Instance has " + str(len(problem[2])) + " items")

	for i in range(len(problem[2])):
		print("Item " + str(i + 1) + " has weight " + str(problem[2][i][0]) + " and value " + str(problem[2][i][1]))

	print()

def PrintSolutionInfo(problem, solution):
	print("Solution has " + str(len(solution[0])) + " bags")

	for i in range(len(solution[0])):

		print("Bag " + str(i + 1) + " has a weight of " + str(solution[1][i]) + "/" + str(problem[1][i])  + " and a value of " + str(solution[2][i]) + " across "  + str(len(solution[0][i])) + " items")

		for j in range(len(solution[0][i])):
			print("\tItem " + str(j + 1) + " has index " + str(solution[0][i][j] + 1) + ", weight " + str(problem[2][ solution[0][i][j] ][0]) + ", and value " + str(problem[2][ solution[0][i][j] ][1]))

	print()

def PrintMemeInfo(meme):
	print("Meme\n====")
	print("Bag " + str(meme[0] + 1))
	print("Contents: " + str(meme[1]))
	print()

def GenerateRandomProblemInstance(maxBags, maxCapacity, maxItems, maxWeight, maxValue):
	numberOfBags = random.randrange(maxBags) + 1

	capacities = []

	for i in range(numberOfBags):
		capacity = random.randrange(maxCapacity) + 1

		capacities.append(capacity)

	items = []
	numberOfItems = random.randrange(maxItems) + 1

	for i in range(numberOfItems):
		weight = random.randrange(maxWeight) + 1
		value = random.randrange(maxValue) + 1

		items.append( (weight, value) )

	return (numberOfBags, capacities, items)

def GenerateRandomProblemSolution(problem, constraints):
	numberOfBags = problem[0]
	numberOfItems = len(problem[2])
	selectionProbability = constraints[0]

	bags = [ [] for i in range(numberOfBags) ]
	bagWeights = [ 0 for i in range(numberOfBags) ]
	bagValues = [ 0 for i in range(numberOfBags) ]

	for i in range(numberOfItems):
		p = random.random()

		if(p < selectionProbability):
			bag = random.randrange(numberOfBags)
			bagCapacity = problem[1][bag]
			itemWeight = problem[2][i][0]
			itemValue = problem[2][i][1]

			if(bagWeights[bag] + itemWeight <= bagCapacity):
				bags[bag].append(i)
				bagWeights[bag] += itemWeight
				bagValues[bag] += itemValue

	return (bags, bagWeights, bagValues)

def EvaluateFitness(solution):
	fitness = 0

	for i in range(len(solution[2])):
		fitness += solution[2][i]

	return fitness

def Mutate(problem, solution):
	p = random.random()
	randomItem = int(random.random() * len(problem[2]))

	if(p > 0.5):
		randomBag = int(random.random() * problem[0])
		InsertItem(problem, solution, randomItem, randomBag)
	
	else:
		RemoveItem(problem, solution, randomItem)	


def IdentifyMeme(problem, solution):
	meme = None
	numberOfBags = problem[0]
	bagGoodnessValues = [ 0 for bag in range(numberOfBags) ] 	 

	for bag in range(numberOfBags):
		bagValue = solution[2][bag]
		bagWeight = solution[1][bag]
		bagCapacity = problem[1][bag]
		bagGoodness = bagValue * (bagWeight / float(bagCapacity))

		bagGoodnessValues[bag] = bagGoodness

	bestBag = -1
	bestGoodness = -1

	for bag in range(numberOfBags):
		if(bagGoodnessValues[bag] > bestGoodness):
			bestGoodness = bagGoodnessValues[bag]
			bestBag = bag

	meme = (bestBag, solution[0][bestBag])

	return meme

def Learn(problem, solution, meme):
	fitness = EvaluateFitness(solution)
	currentFitness = fitness
	initialFitness = fitness
	bestBag = meme[0]
	bag = meme[1]
	bagCapacity = problem[1][bestBag]

	currentSolution = copy.deepcopy(solution)

	for item in bag:
		removedItem = None

		if(solution[1][bestBag] + problem[2][item][0] > bagCapacity):
			removedItem = solution[0][bestBag][int(random.random() * len(solution[0][bestBag]))]
			RemoveItem(problem, currentSolution, removedItem, bestBag)
			 
		InsertItem(problem, currentSolution, item, bestBag)

		currentFitness = EvaluateFitness(currentSolution)

		if(currentFitness >= fitness):
			if(removedItem != None): RemoveItem(problem, solution, removedItem, bestBag)
			InsertItem(problem, solution, item, bestBag)
			fitness = currentFitness
		else:
			currentSolution = copy.deepcopy(solution)

	if(fitness < initialFitness): "Knapsack::Learn ~ Error: Returned a member with lower fitness"

def InsertItem(problem, solution, item, bagNumber=None):
	for bag	in range(problem[0]):
		if(item in solution[0][bag]):
			RemoveItem(problem, solution, item, bag)

	itemWeight = problem[2][item][0]
	itemValue = problem[2][item][1]

	if(solution[1][bagNumber] + itemWeight < problem[1][bagNumber]):
		solution[0][bagNumber].append(item)
		solution[1][bagNumber] += itemWeight
		solution[2][bagNumber] += itemValue

def RemoveItem(problem, solution, item, bagNumber=None):
	if(bagNumber == None):
		for bag in range(problem[0]):
			if(item in solution[0][bag]):
				bagNumber = bag
	
	if(bagNumber != None and item in solution[0][bagNumber]):
		itemWeight = problem[2][item][0]
		itemValue = problem[2][item][1]	
	
		solution[0][bagNumber].remove(item)
		solution[1][bagNumber] -= itemWeight
		solution[2][bagNumber] -= itemValue
			

def Crossover(problem, father, mother, constraints):
	if(constraints[0] + constraints[1] > 0):
		fatherFitness = constraints[0] / float(constraints[0] + constraints[1])
		motherFitness = constraints[1] / float(constraints[0] + constraints[1])
	else:
		fatherFitness = 1
		motherFitness = 0

	#print("Father fitness: " + str(fatherFitness))
	#print("Mother fitness: " + str(motherFitness))

	child1 = None

	childBags = [ [] for bag in range(problem[0]) ]
	childBagWeights = [ 0 for bag in range(problem[0]) ]
	childBagValues = [ 0 for bag in range(problem[0]) ]

	child1 = (childBags, childBagWeights, childBagValues)	
		
	childBags = [ [] for bag in range(problem[0]) ]
	childBagWeights = [ 0 for bag in range(problem[0]) ]
	childBagValues = [ 0 for bag in range(problem[0]) ]

	child2 = (childBags, childBagWeights, childBagValues)	
	
	for bag in range(problem[0]):
		p = random.random()

		if(p < fatherFitness):
			for item in father[0][bag]:
				InsertItem(problem, child1, item, bag)
			for item in mother[0][bag]:
				InsertItem(problem, child2, item, bag)

		else:
			for item in father[0][bag]:
				InsertItem(problem, child2, item, bag)
			for item in mother[0][bag]:
				InsertItem(problem, child1, item, bag)	

		#for item in father[0][bag]:
			#p = random.random()

			#if(p < fatherFitness):
			#	InsertItem(problem, child, item, bag)

		#for item in mother[0][bag]:
		#	p = random.random()
	
		#	if(p < motherFitness):
		#		InsertItem(problem, child, item, bag)


	child = None
	child1Fitness = EvaluateFitness(child1)
	child2Fitness = EvaluateFitness(child2)

	if(child2Fitness > child1Fitness): child = child2
	else: child = child1
	
	return child				
