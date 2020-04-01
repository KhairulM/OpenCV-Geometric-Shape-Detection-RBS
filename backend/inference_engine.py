from image_processing import processImage
import cv2 as cv
from sys import argv


class InferenceEngine:
	def __init__(self):
		self.sides = 0
		self.angles = 0
		self.vertices = 0
		self.conflictSet = {}
		self.factOrdering = []
		self.facts = []
		self.rules = dict()
		self.ruleOrderer = []
		self.rulePrio = [ "factRecency", "ruleOrdering","specificity"]
		
	def createRule(self,rule,action):
		self.rules[rule] = action
		self.ruleOrderer.append(rule)
	
	def addFacts(self, action):
		self.facts.append(action)
	
	def constructConflictSet(self):
		self.conflictSet = dict()
		p = []
		for i in range(0, len(self.facts)):
			p.append(self.facts[i])
		for i in self.rules:
			for j in self.facts:
				exec(j)
			try:
				if eval(i):
					self.conflictSet[i] = self.rules[i]
			except NameError:
				pass
	
	def resolveByRecency(self):
		recencyList = dict()
		mostRecent = -1
		toReturn = dict()
		
		for i in self.conflictSet:
			processedRule = i.replace(" ", "")
			processedRule = processedRule.replace("or", "and")
			processedRule = processedRule.replace("not", "and")
			processedRule = processedRule.split("and")
			
			for j in range(0,len(processedRule)):
				for k in range(0,len(self.facts)):
					str = self.facts[k].replace(" ", "")
					str = str.split("=")
					procRule = processedRule[j].replace("!=", "==")
					procRule = procRule.replace(">=", "==")
					procRule = procRule.replace("<=", "==")
					procRule = procRule.replace("<", "==")
					procRule = procRule.replace(">", "==")
					procRule = procRule.split("==")
		
					if (procRule[0] == str[0] and i not in recencyList):
						recencyList[i] = []
						recencyList[i].append(k)
					elif (processedRule[j] in recencyList):
						recencyList[i].append(k)
		x = ""
		for i in recencyList:
			if (recencyList[i][len(recencyList[i])-1] > mostRecent):
				mostRecent = recencyList[i][len(recencyList[i])-1]
		for i in recencyList:
			if (recencyList[i][len(recencyList[i])-1] == mostRecent):
				toReturn[i] = self.conflictSet[i]
				x = i
				
		if (len(toReturn) > 1):
			return toReturn, 0
		else:
			return toReturn,x
		
	def resolveByRuleOrder(self):
		smallest = 9999999
		l = {}
		toReturn = ""
		for i in self.conflictSet:
			for j in range(0, len(self.ruleOrderer)):
				if (i == self.ruleOrderer[j]):
					if j < smallest:
						smallest = j
						toReturn = i
		l[toReturn] = self.conflictSet[toReturn]
		return l,toReturn
	
	def resolveBySpecificity(self):
		longestRule = -1
		toReturn = {}
		for i in self.conflictSet:
			processedRule = i.replace(" ", "")
			processedRule = processedRule.replace("or", "and")
			processedRule = processedRule.replace("not", "and")
			processedRule = processedRule.split("and")
			if (len(processedRule) > longestRule):
				longestRule = len(processedRule)
		x = ""
		for i in self.conflictSet:
			processedRule = i.replace(" ", "")
			processedRule = processedRule.replace("or", "and")
			processedRule = processedRule.replace("not", "and")
			processedRule = processedRule.split("and")

			if (len(processedRule) == longestRule):
				toReturn[i] = self.conflictSet[i]
				x = i
		if (len(toReturn) > 1):
			return toReturn
		else:
			return toReturn,x
	
	def conflictResolution(self):
		ruleTemp = []
		res = []
		key = ""
		for i in range(0, len(self.rulePrio)):
			ruleTemp.append(self.rulePrio[i])
		while (len(self.conflictSet) != 1):
			for i in range(0,len(ruleTemp)):
				if (ruleTemp[i] == "specificity"):
					try:
						self.conflictSet, key = self.resolveBySpecificity()
						break
					except ValueError:
						pass
					try:
						self.conflictSet = self.resolveBySpecificity()
						break
					except ValueError:
						pass
					break
				if (ruleTemp[i] == "factRecency"):
					
					try:
						self.conflictSet, key = self.resolveByRecency()
						break
					except ValueError:
						pass
					try:
						self.conflictSet = self.resolveByRecency()
						break
					except ValueError:
						pass

					break
				if (ruleTemp[i] == "ruleOrdering"):
					
					try:
						self.conflictSet, key = self.resolveByRuleOrder()
						break
					except ValueError:
						pass
					try:
						self.conflictSet = self.resolveByRuleOrder()
						break
					except ValueError:
						pass
					break
			if (self.conflictSet == None):
				return []
			ruleTemp.pop(0)
		if (len(self.conflictSet) == 1):
			i = self.conflictSet
			pairs = zip(i.keys(), i.values())
			q = list(pairs)
			self.facts.append(q[0][1])
			
			print("\t* ", q[0][0], "->", self.rules[q[0][0]])
			del self.rules[q[0][0]]
			
	def infer(self):
		self.constructConflictSet()
		self.conflictResolution()
		while (len(self.conflictSet) != 0):
			self.constructConflictSet()
			if (len(self.conflictSet) > 0):
				self.conflictResolution()
		return self.facts

	def clearFacts(self):
		self.facts = []
		self.conflictSet = {}
		self.factOrdering = []
		self.facts = []
		self.ruleOrderer = []
		self.rulePrio = [ "factRecency", "ruleOrdering","specificity"]

	def printFacts(self):
		print(self.facts)

	def printRules(self):
		print(self.rules)
		
if __name__ == "__main__":
	imgFilePath = argv[1]
	detectedShapes = processImage(imgFilePath, True)

	for shape in detectedShapes['shapes']:
		nbSisi = shape['vertices']
		angles = shape['angles']

		engine = InferenceEngine()
		print("\nActivated Rules : ")

		""" Menambahkan rules-rules ke dalam inference engine """
		engine.createRule("sisi == 3", "segitiga_sembarang = True")
		engine.createRule("sisi == 3 and ada_sudut_tumpul", "segitiga_tumpul = True")
		engine.createRule("sisi == 3 and semua_sudut_lancip", "segitiga_lancip = True")
		engine.createRule("sisi == 3 and ada_sudut_siku" ,"segitiga_siku = True")
		engine.createRule("sisi == 3 and pasang_sisi_sama == 1", "segitiga_sama_kaki = True")
		engine.createRule("sisi == 3 and pasang_sisi_sama == 2", "segitiga_sama_kaki = True")
		engine.createRule("segitiga_siku and segitiga_sama_kaki", "segitiga_siku_sama_kaki = True")
		engine.createRule("sisi == 3 and pasang_sisi_sama == 3", "segitiga_sama_sisi = True")
		engine.createRule("segitiga_sama_kaki and segitiga_tumpul", "segitiga_tumpul_sama_kaki = True")
		engine.createRule("segitiga_sama_kaki and segitiga_lancip", "segitiga_lancpi_sama_kaki = True")
		engine.createRule("sisi == 4", "segiempat_sembarang = True")
		engine.createRule("sisi == 4 and bersifat_trapesium", "trapesium = True")
		engine.createRule("trapesium and rata_kanan", "trapesium_rata_kanan = True")
		engine.createRule("trapesium and rata_kiri", "trapesium_rata_kiri = True")
		engine.createRule("trapesium and pasang_sisi_sama == 1", "trapesium_sama_kaki = True")
		engine.createRule("sisi == 4 and pasang_sisi_sama == 6 and semua_sudut_siku", "segiempat_beraturan = True")
		engine.createRule("sisi == 4 and pasang_sisi_sama == 2 and tidak_ada_sudut_siku", "jajar_genjang = True")
		engine.createRule("sisi == 4 and pasang_sisi_sama == 6 and tidak_ada_sudut_siku", "jajar_genjang = True")
		engine.createRule("bersifat_layang and pasang_sisi_sama == 2", "layang_layang = True")
		engine.createRule("sisi == 5", "segilima_sembarang = True")
		engine.createRule("sisi == 5 and jumlah_sisi_sama == 10", "segilima_sama_sisi = True")
		engine.createRule("sisi == 6", "segienam_sembarang = True")
		engine.createRule("sisi == 6 and jumlah_sisi_sama == 15", "segienam_sama_sisi = True")

		deltaLength = 5
		deltaAngle = 2
		pasang_sisi_sama = 0
		adaSudutTumpul = False
		adaSudutSiku = False
		semuaSudutLancip = False
		counterSudutLancip = 0
		counterSudutTumpul = 0
		counterSudutSiku = 0
		
		""" Menambahkan fakta-fakta """
		engine.addFacts("sisi = " + str(nbSisi))

		""" Cek sudut """
		for angle in angles:
			if angle < 90 - deltaAngle:
				counterSudutLancip += 1
			elif angle > 90 + deltaAngle:
				counterSudutTumpul += 1
			else:
				counterSudutSiku += 1

		if counterSudutLancip == nbSisi:
			semuaSudutLancip = True
			engine.addFacts("semua_sudut_lancip = True")

		if counterSudutSiku > 0:
			adaSudutSiku = True
			engine.addFacts("ada_sudut_siku = True")
			if counterSudutSiku == nbSisi:
				engine.addFacts("semua_sudut_siku = True")
		else:
			engine.addFacts("tidak_ada_sudut_siku = True")

		if counterSudutTumpul > 0:
			adaSudutTumpul = True
			engine.addFacts("ada_sudut_tumpul = True")

		""" Cek jumlah sisi yang sama """
		""" Menghitung jumlah pasangan sisi yang sama """
		for i in range(shape['vertices']):
				for j in range(i+1, shape['vertices']):
					if abs(shape['sides'][i] - shape['sides'][j]) <= deltaLength:
						pasang_sisi_sama += 1	
		engine.addFacts("pasang_sisi_sama = " + str(pasang_sisi_sama))

		""" Cek Trapesium """
		adaSejajar = False
		foundSum180 = False
		foundPair90 = False
		pair = ()
		for i in range(nbSisi-1):
			for j in range(i, nbSisi):
				if angles[i] + angles[j] >= 180 - deltaAngle*2 and angles[i] + angles[j] <= 180 + deltaAngle*2 and not foundSum180:
					foundSum180 = True
					pair = (i, j)
					if pasang_sisi_sama <= 1:
						engine.addFacts("bersifat_trapesium = True")
				if (angles[i] >= 90 - deltaAngle and angles[i] <= 90 + deltaAngle) and (angles[j] >= 90 - deltaAngle and angles[j] <= 90 + deltaAngle) and not foundPair90:
					foundPair90 = True
					engine.addFacts("rata_kanan = True")

			if foundSum180 and foundPair90:
				break
					
		""" Cek Layang """
		foundSameAngle = False
		arrTemp = angles
		for i in range(len(arrTemp)-1):
			for j in range(i+1, len(arrTemp)):
				if arrTemp[i] >= arrTemp[j] - deltaAngle and arrTemp[i] <= arrTemp[j] + deltaAngle:
					foundSameAngle = True
					engine.addFacts("bersifat_layang = True")
					break
			if foundSameAngle:
				break
		
		""" Execute inference engine """
		res = engine.infer()
		print("Result : ", res, "\n")
	
	cv.waitKey(0)
	cv.destroyAllWindows()