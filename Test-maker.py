from PIL import Image , ImageDraw , ImageFont
import os, re
import PIL


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
					"9":"٩"}
		self.A4 = 2480, 3508
		self.img = Image.new(mode = 'RGB' , size = self.A4 , color = "white")    
		self.draw = ImageDraw.Draw(self.img)
		self.fnt = ImageFont.truetype(os.path.join(os.getcwd()+ "\\ar.ttf") , 130)

		self.replace = lambda dict, text: re.sub("|".join(map(re.escape, dict.keys())),
		 	     lambda m: dict[m.string[m.start():m.end()]],
		         text)
		self.descend = 0

	def Core(self,filename , rows, columns):
		#filename: the name file that we would extract the math equations from.
		#Core : is the core function that make all this beautiful thing works and produce actual tests. 

		#warning if the columns are not readable.
		if columns > len(self.crack(filename)):
			print("WARNING: We recommend you to use less that 15 columns to make the test more readable.")
			print("RECOMMENDATION: We recommend you to use: "+str(len(self.crack(filename))+1)+" columns & 3 rows.")

		for i, c in enumerate(self.NumberOfLines_Positions(self.A4, rows)):
			for j, r in enumerate(self.NumberOfQuestionsInLine_Positions(self.A4, columns)[::-1]):


				self.descend = 0   #this part is for the steps that help make the math readable 
				try:
					for e, b in enumerate(self.crack(filename)[i][j]):   
						self.recognizer(b, r, c, isend = True if b == self.crack(filename)[i][j][-1] else False)
				except:
					print("this index doesn't exist: "+"("+ str(i)+","+str(j) +")"+ ", or you didn't command more than :" + str(len(self.crack(filename))))

		self.img.save("aa.png")

	def recognizer(self, piece, r, c, extra_sapcing=20,isend=False, equal_sign= True):
		#piece : the math piece or part that would be recognzied as a math function during the process. 
		#r     : the number of rows. 
		#c     : the number if columns. 
		#extra_sapcing : space left between all equation parts that helps make the equation more readable. 

		if "/" in piece:
			self.Fraction((r- self.descend , c), *piece.split("/"))
			self.descend += self.Fraction((r, c), "5", "5", disable_drawing=True)[0] + extra_sapcing
		if "+" in piece or "-"in piece:
			self.mathOperator((r-self.descend , c ), piece)       
			self.descend += self.mathOperator((r, c), piece, disable_drawing=True)[0] +extra_sapcing

		if piece.isdigit():
			self.numeral((r-self.descend , c), piece)
			#print(self.numeral((r, c), piece, disable_drawing= True, not_numerals=True)[0])
			self.descend += self.numeral((r, c), piece, disable_drawing= True)[0] + extra_sapcing
		
		if equal_sign and isend:
			self.mathOperator((r-self.descend, c), "=")

	def crack(self, filename, max_rows_in_the_test=30):# 
		# filename: the name file that we would extract the math equations from.

		res = [[] for _ in range(max_rows_in_the_test)]
		with open(filename + ".txt", "r") as file:
			for i, l in enumerate([g.replace("\n", "") for g in file.readlines()]):
				for j in [f for f in l.split(" ") if f != ""]:
					res[i].append(re.findall(r"([0-9]+/[0-9]+|[+-]|[0-9]+)", j))
		return [i for i in res if i != []]

	def NumberOfLines_Positions(self, size, n, head=400, tail=400, margin=50): # this func produce vertical coordinates of question.
		#size   : size of the paper.
		#n      : number of lines.
		#head   : empty space for the heading .
		#tail   : empty space at bottom of paper.
		#margin : space left from the right side to avoid the edge. 
		return [i for i in range(head, (size[1]-tail), (size[1]-tail)//n)]
	
	def NumberOfQuestionsInLine_Positions(self, size, n, marginR=200, marginL=200, mode="expand"): # this func produce horizontal coordinates of question.
		#size   : size of the paper.
		#n      : number of lines.
		#marginR: margin right.
		#marginL: margin left.
		#mode   : "expand" or "sequence" 

		return [i for i in range(marginR, (size[0]), (size[0]-marginL-marginR)//(n))][1:]
	def fixTextSize(self, position, text, not_numerals=False): 
		#position : the position of the text that you want to fix the text to fit to it.
		#text     : the text targeted to be fixed. 
		#font     : a PILLOW object of the font used by default>> fnt = ImageFon.... ect.
		size = self.draw.textsize(text=text, font= self.fnt)
	
		dict = {"__": (0, int(0.93*size[1])),   
		 		"+": (0, int(0.732*size[1])), #0.53
		 		"-": (0, int(0.72*size[1])),
		 		"=": (0, int(0.72*size[1]))}
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
		self.draw.text(self.fixTextSize(pos, num, not_numerals), text=self.replace(self.nums, num)[::-1], fill="black", font=self.fnt )

	def Fraction(self, pos, n, d, margin_from_fractoion_center= 70, disable_drawing=False):
		#pos : the position of the fraction. 
		#n   : the numerator of the fraction.
		#d   : the dominator of the fraction.
		#margin_from_fractoion_center : the distance the numerator and dominator away from the center of the fraction


		### the Center setup & drawing ###
		


		centerSize = self.draw.textsize(text="__", font= self.fnt)

		if disable_drawing:return centerSize                  # when using this func for only dimentions of "__"

		fracCenter = self.draw.text(self.fixTextSize(pos, "__", self.fnt), text="__", fill="black", font=self.fnt ) 

		### the numerator & dominator setup and drawing ####
		
		nSize = self.draw.textsize(text=n, font= self.fnt)
		dSize = self.draw.textsize(text=d, font= self.fnt)
		npos = self.fixTextSize(pos, n, self.fnt)
		dpos = self.fixTextSize(pos, d, self.fnt)
		nFixedPosition = (npos[0] + nSize[0]//2 - centerSize[0]//2), (npos[1]-margin_from_fractoion_center)
		dFixedPosition = (dpos[0] + dSize[0]//2 - centerSize[0]//2), (dpos[1]+margin_from_fractoion_center-35)
		self.draw.text(nFixedPosition, text=self.replace(self.nums, n), fill="black", font=self.fnt )
		self.draw.text(dFixedPosition, text=self.replace(self.nums, d), fill="black", font=self.fnt )
		return centerSize              #adjust

Paper().Core("math", 10, 2)

os.startfile(f"aa.png")
