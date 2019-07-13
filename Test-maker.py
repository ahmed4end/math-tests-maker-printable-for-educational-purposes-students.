from fuzzywuzzy import process,fuzz
def myfunc(x,y):
	return(fuzz.token_sort_ratio(str(x),str(y)))
#the pupose is to group people that refer to the same entity
liste_positions=[]
for i in range(len(df.index)):
	for j in range(i+1,len(df.index)):
		if myfunc((liste_fnln[i]),(liste_fnln[j]))>=90 : #compare client name if they are similar
			if(j not in liste_positions ):
				df.UCID.loc[i]=i
				df.UCID.loc[j]=i
				df.proche=liste_fnln[j]
				df.score=myfunc((liste_fnln[i]),(liste_fnln[j]))
				liste_positions.append(j)