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
		self.rank = self.getRank(rank)
	def getRank(self, rank):
		if self.name == "Number F0: Utopic Draco Future" or self.name == "Number F0: Utopic Future" or self.name == "Number F0: Utopic Future Slash" or self.name == "Number S0: Utopic ZEXAL":
			rank = 1
		return rank
	def getNo(self):
		no = self.name.split(":")[0].split(" ")[1]
		i = 0
		while i <= len(no) and no[i:].isnumeric() != True:
			i = i + 1
		if no[i:].isnumeric() == True:
			no = int(no[i:])
		elif self.name == "Ultimate Leo Utopia Ray" or self.name == "Ultimate Dragonic Utopia Ray":
			no = 39
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
		self.listNames()
		self.listNo()
		self.listRanks()
		self.listUniqueRanks()
	def show(self):
		for c in self.deck:
			c.show()
	def listNames(self):
		for c in self.deck:
			self.names.append(c.name)
		return self
	def listNo(self):
		for card in self.deck:
			self.no.append(card.no)
		self.no = list(set(self.no))
		return self
	def listRanks(self):
		for c in self.deck:
			self.ranks.append(c.rank)
		return self
	def listUniqueRanks(self):
		self.sranks = list(set(self.ranks))
		return self
	def addCard(self, c):
		self.deck.append(c)
		self.update()
		return self
	def removeCard(self, card):
		self.deck.pop(self.deck.index(card))#may need fixed to pass removed card to another thing
		self.update()
		return self
	def update(self):
		self.listNames()
		self.listNo()
		self.listRanks()
		self.listUniqueRanks()
		return self
	def noSort(self, bool=True):
		self.deck = sorted(self.deck, key = lambda card: card.no, reverse = bool)
		self.update()
		return self
	def less(self, num):
		lst = []
		for n in self.deck:
			if n.no <= num:
				lst.append(n)
		return Deck(lst)
	def limit(self, cards, target):
		if cards.sum() <= target:
			self = self.less(target-cards.sum())
			self.update()
			self.excludeRank(cards)
		else:
			self.deck = []
		self.noSort()
		self.update()
		return Deck(self.deck)
	def excludeRank(self, cards):
		tmp = []
		for card in self.deck:
			if card.rank not in cards.sranks:
				tmp.append(card)
		self.deck = tmp
		self.update()
		return self
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
	
	target = []
	
	tmpInput = input("Input a target or selection of target to summon with Numbers Evaille.")
	if tmpInput:
		if "," not in tmpInput and "-" not in tmpInput:
			target.append(int(tmpInput))
		if "," in str(tmpInput):
			tmpInput = tmpInput.split(",")
			#tmp = []
			for element in tmpInput:
				#tmp.append(int(element))
				target.append(int(element))
			#target = tmp
		elif "-" in str(tmpInput):
			tmpInput = tmpInput.split("-")
			if len(tmpInput) == 2:
				start, stop = tmpInput[0], tmpInput[1]
				for x in range(int(start), int(stop)+1):
					target.append(x)
			else:
				print("Error 2: range wronge")
	else:
		target = deck.no#May make this a method- annoying
	return target
def addCombos(combo, comboDict, target):
	comboDict[target] = combo
	return comboDict
def saveCombos(fcombo):
	file = open("C:\\Users\\Chris\\OneDrive\\Documents\\Programming\\Python\\YGO Numbers Evaille\\Combos.txt", "w")
	for i in fcombo:
		file.write("{}\n".format(i))
		
	file.close()
	return
def formatCombos(comboDict, totalIterations):
	fcombo = []
	fcombo.append("ctrl + f \"Target: Number X\" with X being the target for easier sorting")
	fcombo.append("Iterations: {}".format(totalIterations))
	for key in comboDict:
		counter = 1
		if len(comboDict[key]) != 0:
			fcombo.append("Target: Number {} monster Options: {}".format(key,len(comboDict[key])))
			for combo in comboDict[key]:
				fcombo.append("  Option {}:".format(counter))
				for card in combo.deck:
					fcombo.append("    Name: {} Rank: {}".format(card.name, card.rank))
				counter = counter + 1	
		else:
			fcombo.append("There are no options to summon a Number: {} monster. [Num:{}]".format(key,key))
	return fcombo
def printCombos(fcombo):
	for i in fcombo:
		print(i)
	return
def main():
	filename = "numbers.csv"
	deck = openFile(filename)
	deck = Deck(deck)
	
	iterations, totalIterations, comboDict = 0, 0, {}
	target = getTarget(deck)
	for number in target:
		comboDict, iterations = Evaille(number, deck, comboDict, iterations)
		totalIterations = iterations + totalIterations

	formattedCombos = formatCombos(comboDict, totalIterations)
	printCombos(formattedCombos)
	saveCombos(formattedCombos)
main()
