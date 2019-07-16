from PIL import Image , ImageDraw , ImageFont #6.1.0
import os, sys, re, time
from random import randint,choice
from tqdm import tqdm


s = time.time()
class Paper():
	def __init__(self):
		self.nums ={"0":"٠",
					"1":"١",
					"2":"٢",
					"3":"٣",
					"4":"٤",
					"5":"٥",
					"6":"٦",
					"7":"٧",
					"8":"٨",
					"9":"٩",
					"*":"×"}
		self.ranges ={#!WARNING : when using 0 in the range below it may causes Zero division error that will lead that some question will be removed automatically.
					"d": (2,50), 
					"c": (2,30),
					"b": (2,20),
					"a": (2,10),}
		self.A4 = 2480, 3508
		self.img = Image.new(mode = 'RGB' , size = self.A4 , color = "white")    
		self.draw = ImageDraw.Draw(self.img)
		self.fnt = ImageFont.truetype(os.path.join(os.getcwd()+ "\\ar.ttf") , 130)
		self.smallfnt = ImageFont.truetype(os.path.join(os.getcwd()+ "\\ar.ttf") , 75)

		self.replace = lambda dict, text: re.sub("|".join(map(re.escape, dict.keys())),
		 	     lambda m: dict[m.string[m.start():m.end()]],
		         text)
		self.replaceV2 = lambda dict, text: re.sub("|".join(map(re.escape, dict.keys())),
			 	     lambda m: str(self.rando(*dict[m.string[m.start():m.end()]])),
			         text)

		self.memory = [9999,9999] # this variable is for the function: self.rando() :"D
		self.numbering = 1
		self.health = []
		self.anti_conflict = 0

		


		################## RandomMathModel() AREA #########################################
		self.o = ["a","b","c","d"]
		self.op = ["+", "-", "*"]
		self.modelregex = f"({choice(self.o)}{choice(self.op)}{choice(self.o)})/({choice(self.o)}{choice(self.op)}{choice(self.o)}){choice(self.op)}{choice(self.o)}"
		####################################################################################

		# BORDER HERE .
		self.draw.rectangle([(30,30), (self.A4[0]-30, self.A4[1]-30)], outline="rgb(150, 150, 150)", width=5)
	def Core(self,filename , rows, columns, progressBar= True):
		#filename: the name file that we would extract the math equations from.
		#Core : is the core function that make all this beautiful thing works and produce actual tests. 

		#warning if the columns are not readable.
		if columns > len(self.crack(filename)):
			print("WARNING: We recommend you to use less that 15 columns to make the test more readable.")
			print("RECOMMENDATION: We recommend you to use: "+str(len(self.crack(filename))+1)+" columns & 3 rows.")
		############## progress bar ###############
		total = (rows-1)*columns
		pbar = tqdm(total= 60)
		############################################
		for i, c in enumerate(self.NumberOfLines_Positions(self.A4, rows)):
			for j, r in enumerate(self.NumberOfQuestionsInLine_Positions(self.A4, columns)[::-1]):


				self.descend = 0   #this part is for the steps that help make the math readable 

				########################################### PAINTING AREA #########################################################
				
			########################################### NUMBERING AREA #########################################################
				self.draw.text(self.fixTextSize((r+85, c+25), "+"), text=self.replace(self.nums, f"({str(self.numbering)})"), fill="rgb(64, 64, 64)", font=self.smallfnt )
				self.numbering += 1
			####################################################################################################################
				pbar.update(total/60*100)

				try:

					freeze = self.DomesticREngine(self.crack(filename)[i][j])
					for e, b in enumerate(freeze):   
						self.recognizer(b, r, c, isend = True if e == len(list(enumerate(freeze)))-1 else False)

				except:
					print("this index doesn't exist: "+"("+ str(i)+","+str(j) +")"+ ", or you didn't command more than :" + str(len(self.crack(filename))))
			pbar.close()
				
		health = int(sum([1 for i in self.health if i < 10])/len(self.health)*100)
		print("\nhealth:".ljust(10), str(health).rjust(5)+"%")
				###################################################################################################################

		self.img.save("aa.png")
	def DomesticREngine(self, cracked, integer_values= True, answers_min_limit=0, answers_max_limit = 50):
		#DomesticREngine: "D"omestic "R"adom "E"ngine
		#cracked        : the list that contains the equstion parts. 
		#################### conditions ##################################
		#integer_values : the term guarantees that the answers will be simple integers
		#ansers_range_limit : that makes all answers less than this value.
		self.anti_conflict = 0
		while True:

			############ Back up genrator in case the equation has problem ##########
			if self.anti_conflict != 0:
				cracked = self.anti_conflict
				time.sleep(0.5)
			#########################################################################

			
			while True:
				self.anti_conflict += 1
				sample = eval(self.replaceV2(self.ranges, str(cracked)))
				eq = eval("".join(sample))
				if all([eq == int(eq), eq >= answers_min_limit, eq <= answers_max_limit]):
					self.health.append(eq)
					self.anti_conflict = 0
					return sample
				if self.anti_conflict > 50000:break

		return eval(self.replaceV2(ranges, str(cracked)))
	def rando(self, s,e): #this function is the same random.randint however it's eveb better it can't return the same num twice in row.
			
			while True:
				n = randint(s, e)
				if n != self.memory[-1] and n!= self.memory[-2]:
					self.memory.append(n)
					return n
	def recognizer(self, piece, r, c, extra_sapcing=20,isend=False, equal_sign= True):
		#piece : the math piece or part that would be recognzied as a math function during the process. 
		#r     : the number of rows. 
		#c     : the number if columns. 
		#extra_sapcing : space left between all equation parts that helps make the equation more readable. 

		if "/" in piece and "(" in piece:                    #(n+n) / (n-n)
			piece ="("+"".join([re.findall("[0-9]+|[+\-*]", piece.split("/")[0])][0][::-1])+")"+"/"+"("+"".join([re.findall("[0-9]+|[+\-*]", piece.split("/")[1])][0][::-1])+")"
			self.Fraction((r- self.descend-30 , c), *piece.split("/"), centerLength=3)
			self.descend += self.Fraction((r, c), "5", "5", disable_drawing=True)[0]*3/1.6 + extra_sapcing
		elif "/" in piece:                    #n / n  
			self.Fraction((r- self.descend , c), *piece.split("/"))
			self.descend += self.Fraction((r, c), "5", "5", disable_drawing=True)[0] + extra_sapcing
		elif "+" in piece or "-"in piece or "*" in piece:     # n + n
			if "*"in piece:pass
			self.mathOperator((r-self.descend , c ), self.replace(self.nums, piece))       
			self.descend += self.mathOperator((r, c), piece, disable_drawing=True)[0] +extra_sapcing
		elif piece.isdigit():                 #n
			self.numeral((r-self.descend , c), piece)
			self.descend += self.numeral((r, c), piece, disable_drawing= True)[0] + extra_sapcing	
		if equal_sign and isend:
			self.mathOperator((r-self.descend, c), "=")
	def crack(self, filename, max_rows_in_the_test=30):# 
		# filename: the name file that we would extract the math equations from.

		res = [[] for _ in range(max_rows_in_the_test)]
		with open(filename + ".txt", "r") as file:
			for i, l in enumerate([g.replace("\n", "") for g in file.readlines()]):
				for j in [f for f in l.split(" ") if f != ""]:
					#res[i].append(re.findall(r"([0-9]+/[0-9]+|[+-]|[0-9]+)", j))      #disabled while random exists.
					res[i].append(re.findall(r"\([0-9abcd+\-*]+\)/\([0-9abcd+\-*]+\)|\([0-9abcd+\-*]+\)/[0-9abcd]+|[0-9abcd]+/\([0-9abcd+\-*]+\)|[0-9abcd]+/[0-9abcd]+|[+*-]|[0-9abcd]+", j))
		return [i for i in res if i != []]
	def NumberOfLines_Positions(self, size, n, head= 400, tail=400, margin=50): # this func produce vertical coordinates of question.
		#size   : size of the paper.
		#n      : number of lines.
		#head   : empty space for the heading .
		#tail   : empty space at bottom of paper.
		#margin : space left from the right side to avoid the edge. 
		return [i for i in range(head, (size[1]-tail), (size[1]-tail)//n)]
	def NumberOfQuestionsInLine_Positions(self, size, n, marginR=0, marginL=300, mode="expand"): # this func produce horizontal coordinates of question.
		#NOTE   : this function needs update. 
		#size   : size of the paper.
		#n      : number of lines.
		#marginR: margin right.
		#marginL: margin left.

		return [i for i in range(marginR, (size[0]), (size[0]-marginL-marginR)//(n))][1:]
	def fixTextSize(self, position, text, not_numerals=False): 
		#position : the position of the text that you want to fix the text to fit to it.
		#text     : the text targeted to be fixed. 
		#font     : a PILLOW object of the font used by default>> fnt = ImageFon.... ect.
		size = self.draw.textsize(text=text, font= self.fnt)
		
		#if text[0] == "_":text="__" #spectial case for the center sign of all fraction to reduce the number of conditions in the below dict.
		dict = {"__": (0, int(0.93*size[1])),   
		 		"+": (0, int(0.732*size[1])), #0.53
		 		"-": (0, int(0.72*size[1])),
		 		"=": (0, int(0.72*size[1])),
		 		"×": (-10, int(0.732*size[1])),
		 		"___":(-15, int(0.93*size[1]))}
		if text not in dict:
			if not_numerals: return position[0]-size[0], position[1] - int(size[1]*0.41) 
			#print("PROBLEM: " + text +" is not fixed, go add fixing instructions in the >>fixTextSize()<< function !"  )
			return position[0]-size[0], position[1] - int(size[1]*0.6)
		return position[0]-dict[text][0]-size[0],position[1] - dict[text][1]
	def mathOperator(self, pos, operator, disable_drawing=False):
		if disable_drawing:return self.draw.textsize(text= operator, font= self.fnt)
		self.draw.text(self.fixTextSize(pos, operator, self.fnt), text=operator, fill="black", font=self.fnt )
		return self.draw.textsize(text= operator, font= self.fnt) #adjust
	def numeral(self,pos ,num, disable_drawing= False, not_numerals=False):
		if disable_drawing: return self.draw.textsize(text= num, font= self.fnt)
		self.draw.text(self.fixTextSize(pos, num, not_numerals), text=self.replace(self.nums, num), fill="black", font=self.fnt )
	def Fraction(self, pos, n, d, centerLength=2, margin_from_fractoion_center= 70, disable_drawing=False):
		#pos : the position of the fraction. 
		#n   : the numerator of the fraction.
		#d   : the dominator of the fraction.
		#margin_from_fractoion_center : the distance the numerator and dominator away from the center of the fraction


		### the Center setup & drawing ###

		centerSize = self.draw.textsize(text="_"*centerLength, font= self.fnt)

		if disable_drawing:return centerSize                  # when using this func for only dimentions of "__"

		self.draw.text(self.fixTextSize(pos, "_"*centerLength, self.fnt), text="_"*centerLength, fill="black", font=self.fnt ) 

		### the numerator & dominator setup and drawing ####
		
		nSize = self.draw.textsize(text=n, font= self.fnt)
		dSize = self.draw.textsize(text=d, font= self.fnt)
		npos = self.fixTextSize(pos, n, self.fnt)
		dpos = self.fixTextSize(pos, d, self.fnt)
		nFixedPosition = (npos[0] + nSize[0]//2 - centerSize[0]//2), (npos[1]-margin_from_fractoion_center)
		dFixedPosition = (dpos[0] + dSize[0]//2 - centerSize[0]//2), (dpos[1]+margin_from_fractoion_center-35)
		self.draw.text(nFixedPosition, text=self.replace(self.nums, n), fill="black", font=self.fnt )
		self.draw.text(dFixedPosition, text=self.replace(self.nums, d), fill="black", font=self.fnt )
	def RandomMathModel(self, filename, rows, columns):
		#WARNING: make sure some of the operations you generate can  follows the conditions [answers_min_limit, eq <= answers_max_limit]
		with open(filename+".txt", "w") as file:
			for i in range(rows):
				for j in range(columns):
					#the line below the the imporant one: use it to write the regex of equstion per line.
					#file.write(f"({choice(self.o)}{choice(self.op)}{choice(self.o)})/({choice(self.o)}{choice(self.op)}{choice(self.o)})")
					file.write(self.modelregex)
					#file.write(f"{choice(self.o)}/{choice(self.o)}")
					file.write("  ")
				file.write("\n")

Paper().RandomMathModel("math123" , 15, 3)

Paper().Core("math123", 12, 3)

os.startfile(f"aa.png")


e = time.time()
print("time  :".ljust(10) + (str(round(e-s, 2))+"s").rjust(7))
time.sleep(60)


