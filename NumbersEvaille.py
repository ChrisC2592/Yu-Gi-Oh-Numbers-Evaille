import csv
#NOTE: Instead of brute force, try making a dynamically updated selection.
#Remove from consideration all that dont match at each step.
#On picking a card remove all other cards with matching rank and
#all cards that would match more than target.
#Require checks that the card pool and picked cards are at least 4
class Number():
	def __init__(self, name, rank):
		self.name = name
		self.no = self.getNo()
		self.rank = rank
	def getNo(self):
		no = self.name.split(":")[0].split(" ")[1]
		i = 0
		while i <= len(no) and no[i:].isnumeric() != True:
			i = i + 1
		if no[i:].isnumeric() == True:
			no = int(no[i:])
		else:
			no = "Number does not have a numeric value."
		return no
	def show(self):
		print("Name: ",self.name," Rank: ", self.rank)
		return
class Deck():
	def __init__(self, deck = []):
		self.deck = deck
		self.no, self.ranks, self.names = [], [], []
		self.names = self.listName()
		self.no = list(set(self.listNo()))
		self.ranks = self.listRank()
		self.sranks = list(set(self.ranks))
	def show(self):
		for c in self.deck:
			c.show()
	def listNo(self):
		for card in self.deck:
			self.no.append(card.no)
		return self.no
	def listRank(self):
		for c in self.deck:
			self.ranks.append(c.rank)
		return self.ranks
	def listName(self):
		for c in self.deck:
			self.names.append(c.name)
		return self.names
	def addCard(self, c):
		self.deck.append(c)
		self.update()
		return self
	def removeCard(self, card):
		self.deck.pop(self.deck.index(card))
		self.update()
		return self
	def update(self):
		self.listName()
		self.listNo()
		self.listRank()
		return self
	def less(self, num):
		lst = []
		for n in self.deck:
			if n.no < num:
				lst.append(n)
		return Deck(lst)
	def sum(self):
		sumNum = 0
		for card in self.deck:
			sumNum = sumNum + card.no
		return sumNum
def openFile(filename):
	deck = []
	with open(filename, encoding = "utf-8") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if  "Number" in row["English name (linked)"]:
				name = row["English name (linked)"].strip("[]").split("|")[0]
				rank = int(row["[[Level]]/ [[Rank]]"])
				tmpNum = Number(name,rank)
				if type(tmpNum.no) == type(int()):
					deck.append(tmpNum)
	return deck
def Evaille(target, deck, comboDict, iterations):
	deck = deck.less(target)
	validCombos = []
	iterationCount = 0
	while len(deck.deck) >= 4:
		validCombos, deck, i  = evalEvaille(target, deck, validCombos, iterations)
		iterationCount = iterationCount + i
	addCombos(validCombos, comboDict, target),
	return comboDict, iterationCount
def evalEvaille(target, deck, validCombos, i):
	c1 = deck.deck.pop(0)
	deck.update()
	for c2 in deck.deck:
		i=i+1
		if c1.no + c2.no < target and c1.rank != c2.rank:
			for c3 in deck.deck:
				i=i+1
				if c1.no + c2.no + c3.no < target and c3.rank != c1.rank and c3.rank != c2.rank:
					for c4 in deck.deck:
						i=i+1
						tmp = Deck([c1,c2,c3,c4])
						if len(tmp.sranks) == 4 and tmp.sum() == target and notDuplicate(validCombos,tmp):
							validCombos.append(tmp)	
	return validCombos, deck, i
def dumbEvaille(target, deck):
	combo = []
	tmp = []
	deck = deck.less(target)
	i = 0
	for c1 in deck.deck:
		i=i+1
		for c2 in deck.deck:
			i=i+1
			for c3 in deck.deck:
				i=i+1
				for c4 in deck.deck:
					i=i+1
					tmp = Deck([c1,c2,c3,c4])
					sumNum = int()
					for element in tmp.deck:
						sumNum = sumNum + element.no
					if len(tmp.sranks) == 4 and sumNum == target:
						if notDuplicate(combo, tmp):
							combo.append(tmp)
	return combo,i
def notDuplicate(comb, deck):
	booLst = []
	bol = True
	for lst in comb:
		for elm in lst.deck:
			for card in deck.deck:
				if elm.name == card.name:
					booLst.append(True)
	if booLst:
		bol = False
	
	return bol
def getTarget(deck):
	print("You may search multipe number at a time by seperating them with a \",\"")
	print("or \"-\" for a range")
	print("If left blank will return all valid combinations for all numbers.")
	print("WARNING: Processing all valid combinations for all numbers will take a while(~30 min for me.)")
	
	target = input("Input a target or selection of target to summon with Numbers Evaille.")

	if target:
		if "," not in target and "-" not in target:
			target = int(target)
		if "," in str(target):
			target = target.split(",")
			tmp = []
			for element in target:
				tmp.append(int(element))
			target = tmp
		elif "-" in str(target):
			target = target.split("-")
			if len(target) == 2:
				start, stop = target[0], target[1]
				target = []
				for x in range(int(start), int(stop)+1):
					target.append(x)
			else:
				print("Error 2: range wronge")
	else:
		target = deck.no	
	return target
def addCombos(combo, comboDict, target):
	comboDict[target] = combo
	return comboDict
def saveCombos(comboDict):
	file = open("C:\\Users\\Chris\\OneDrive\\Documents\\Programming\\Python\\YGO Numbers Evaille\\Combos.txt", "w")
	counter = 1
	for key in comboDict:
		file.write("Target: Number {} monster Options: {}".format(key,len(comboDict[key])))
		if len(comboDict) != 0:
			for combo in comboDict[key]:
				file.write("  Option {}:\n".format(counter))
				counter = counter + 1
				for card in combo.deck:
					file.write("    Name: {}, Rank: {}\n".format(card.name, card.rank))
			counter = 1
	file.close()
	return
def main():
	filename = "numbers.csv"
	deck = openFile(filename)
	deck = Deck(deck)
	
	iterations, totalIterations, comboDict = 0, 0, {}
	target = getTarget(deck)
	if type(target) != type(list()):
		comboDict, totalIterations = Evaille(target, deck, comboDict, iterations)
	elif type(target) == type(list()):
		for number in target:
			comboDict, iterations = Evaille(number, deck, comboDict, iterations)
			totalIterations = iterations + totalIterations
	print("ctrl + f Target: x with x being the target for easier sorting")
	print("Iterations: {}".format(totalIterations))
	for key in comboDict:
		counter = 1
		if len(comboDict[key]) != 0:
			print("Target: Number {} monster Options: {}".format(key,len(comboDict[key])))
			for combo in comboDict[key]:
				print("  Option {}:".format(counter))
				for card in combo.deck:
					print("    Name: {} Rank: {}".format(card.name, card.rank))
				counter = counter + 1	
		else:
			print("There are no options to summon a Number: {} monster. [Num:{}]".format(key,key))
	# saveCombos(comboDict)

main()