from datetime import datetime, timedelta
import re
import pandas as pd
df = pd.read_csv('DailyReport.csv', skiprows=5)		#Deltes the data we don't need, also for confidentiality sakes I changed the name of the actual report to DailyReort

'''
Due to the nature of the the reports, it will save the with the same name followed by the number, this makes it so you dont have to change the name of the file
Because of windows, if file have same name it will just put a number to diff
serialNumberOfCSV = 0
with open('Serial.txt', 'r') as r:
	serialNumberOfCSV = r.read()
	
with open('Serial.txt','w') as r:
	no = int(serialNumberOfCSV) + 1
	r.write(str(no))
'''
today = datetime.today()
d1 = today.strftime("%d %b %Y")
yesterday = today - timedelta(days = 1)
yesterday = yesterday.strftime("%d %b %Y")
df = df.drop(columns = ['Response ID','Download Status'])						#annoying columns that block info while testing
df = df.loc[~(df['Timestamp'].str.contains('^'+yesterday+'[a-z]*', flags = re.I, regex = True) & df['Timestamp'].str.endswith('AM'))] #Removes all the morning shifts from yesterday
df = df.sort_values('Ambulance Base', ascending = True)

class Shift:
	questions = ['under a Health Risk Warning, Leave of Absence or MC?','Experiencing symptoms', 'Living with someone with covid and has gotten positive ART']
	def __init__(self, type, nric, discrep, health, ARTStatus):
		self.type = type
		self.nric = nric
		self.discrep = discrep
		self.health = health
		self.ARTStatus = ARTStatus

	def checkHealth(self): 														#'Asks' the shift if there's any issue with the heath decleration, if so it will return which part is not cleared.
		string = ""
		clear = True
		multiple = False
		try:
			for x in range(3):
				if self.health[x] == "Yes" or self.health[x] == "ART Positive":
					clear = False
					if multiple == False:
						string += "shift has said yes for " + self.questions[x]
					else:
						string += ", " + self.questions[x]
			if clear == True:
				string = "all clear"
			return string
		except:
			return 'et'

	def getMaskedNric(self, index):										#Masks their ID number
		nric_current = self.nric[index]
		maskedNric = nric_current[0]+nric_current[5:8]
		return maskedNric

	def checkART_Status(self):											#Checks the ART test status for the shifts team, will return either all clear or the masked id of who has not done it
		indexOfNotDoneART = []
		outputStr_forNRIC = ""
		for x in range(3):
			if(self.ARTStatus[x].lower() != "yes"):						#If any of the art status is no, then take down the index (parallel arrays)
				indexOfNotDoneART.append(x)
		if len(indexOfNotDoneART) != 0:									#If there are any art not done then get me all masked id's that have not done it
			for y in range(len(indexOfNotDoneART)):
				outputStr_forNRIC += " " + getMaskedNric(indexOfNotDoneART[y])
			return outputStr_forNRIC + " not done"
		else:
			return "All done"

class base:
	baseLevelDiscrep = "nil"
	baseLevelHpIssue = "No"
	def __init__(self, name):
		self.name = name 
		self.attendance = [0,0,0]
		self.morning_shift = Shift("n/a",["et"],"nil",["et"],['et'])
		self.night_shift = Shift("n/a",["et"],"nil",["et"],['et'])

	def add_shift(self, shift):
		self.attendance[0] += 1
		if shift.type == "Morning Shift":
			self.morning_shift = shift
			self.attendance[1] += 1
		elif shift.type == "Night Shift":
			self.night_shift = shift
			self.attendance[2] += 1

	def getHP(self):
		hp =[self.morning_shift.health,self.night_shift.health]
		return hp
		
	def getNric(self):
		nric = [self.morning_shift.nric,self.night_shift.nric]
		return nric

	def getART(self):
		ARTStatusShifts = [self.morning_shift.ARTStatus,self.night_shift.ARTStatus]
		return nric

	def getShifts(self):
		shifts = [self.morning_shift, self.night_shift]
		return shifts

def writeRpt():
	with open('newTxt.txt','w') as f:
		f.writelines('Ambulance Sitrep Daily report for: ' + d1)
	writeComplete()

def writeHp(base, shiftno): 														#function which returns a str to reperesent the total health decleration for a base(Honestly could have just put this in the base class zzz)
	shift = ["morning", "night"]
	if shiftno == 2: 																#flagged, both shifts submitted
		tempListShifts = base.getShifts()
		listHP = [tempListShifts[0].checkHealth(), tempListShifts[1].checkHealth()]
		for x in range(2):
			if listHP[x] != "all clear":
				return listHP[x]
		return "all clear for both shifts"
	else:
		temp = base.getShifts()
		singleHP = temp[shiftno].checkHealth()
		if singleHP != "all clear":
			return singleHP
		else:
			return ("all clear" + " for " + shift[shiftno]+" shift")
	
def writeComplete():
	cmplt = ["\n\nAmbulance Sitrep Completed: "]														#Writes down, shifts submitted, health decleration status and any issues per base								
	hpLines = ["\n\nAmbulance Healh Decleration: "]													#done in a single function as it can be leveraged to do multiple 'calculations' for a single iteration of looping for
	discrep = ["\n\nAmbulance Discrepencies: "]														#each base and determining which shift has submitted
	ART = ["\n\nAmbulance ART(3 Days) Status: (Morning shift is Today, Night shift was yesterday)"]
	string = ""
	toStrForHP = "n/a"
	names = ["morning","night"]
	for i in range(6):
		onlyOneSubmission = 0
		shift_indicator = 1
		Art_Status_base = ["n/a","n/a"]
		if baseEntry[i].attendance[0] == 2: 									#If there are both shift submissions for the base in question
			string = "Yes" 														#Flagged, yes both submitted
			toStrForHP = writeHp(baseEntry[i], 2) 								#Finds out the str for the base for health decleration. Returns all clear or not clear because...
			Art_Status_base[0] = baseEntry[i].morning_shift.checkART_Status()	#Simply gets the art status for both shifts
			Art_Status_base[1] = baseEntry[i].night_shift.checkART_Status()
		
		elif baseEntry[i].attendance[0] == 1:
			if(baseEntry[i].attendance[1] == 1): 							#does the attendance for morning shift = 1?
				onlyOneSubmission = 1 								#no submisson for night when morning has 1 vice versa, if morning not submitted then onlyOnesub would b 0...
				shift_indicator = 0  								#Way of flagging which shift by index is the submitted one for health declare
			shift_current = baseEntry[i].getShifts()						#Gets art status for the current shift in question
			Art_Status_base[shift_indicator] = shift_current[shift_indicator].checkART_Status()
			string = "No submisson for "+ names[onlyOneSubmission] + " shift" 			#Flagged, no submission for X shift
			toStrForHP = writeHp(baseEntry[i], shift_indicator) 					#Finds out the string for the base in question for health, for only the shift in question

		else: 																	#No submissions for any shift
			string = "No submission for both shifts"
			toStrForHP = 'n/a'													#Adding what I want to write per line, for each cat
		ART.append(baseEntry[i].name+": \n" + "    morning shift: " + Art_Status_base[0] +"\n    night shift: " + Art_Status_base[1])
		discrep.append(baseEntry[i].name +": "+ baseEntry[i].baseLevelDiscrep)	#Discrep is determined when making the new shift thus its been calcualted already
		hpLines.append(baseEntry[i].name +": " + toStrForHP)
		cmplt.append(baseEntry[i].name+": " + string)

	#Writing to a text file.
	with open('newTxt.txt','a') as f:
		f.writelines('\n'.join(cmplt))
		f.writelines('\n'.join(hpLines))
		f.writelines('\n'.join(discrep))
		f.writelines('\n'.join(ART))

#Chunk of code which from pandas, creates shift objects from the data
baseEntry = []
baseNames = ["Base 1","Base 2","Base 3","Base 4","Base 5","Base 6"]
for i in range(6):
	tempClassObj = base(baseNames[i])
	baseEntry.append(tempClassObj)
const = 0
for i in range(df.index.size):	
	try:
		if (df.iloc[const,1] == df.iloc[const+1,1]) & (df.iloc[const,2] == df.iloc[const+1,2]):	#If the base name same and shift same of the next index then its a dup
			df = df.drop(df.index[const])
			df = df.reset_index(drop = True)
		else:																					#If not a dup
			for i in range(6):
				if df.iloc[const,1] == baseEntry[i].name:
					new_Shift = Shift(df.iloc[const,2],[df.iloc[const,3],df.iloc[const,5],df.iloc[const,7]], df.iloc[const,14], [df.iloc[const,-5],df.iloc[const,-6],df.iloc[const,-7]],[df.iloc[const,4],df.iloc[const,6],df.iloc[const,8]])
					baseEntry[i].add_shift(new_Shift)
					try:
						if(df.iloc[const,14].lower() != "nil"):
							baseEntry[i].baseLevelDiscrep = df.iloc[const,14]
					except:
						pass			
			const += 1												#need to use this rather than i because if a index is dropped the array closes and becomes smaller and you miss an index	
	except:															#need to copy the same code over because by nature of that loop it will not iterate through the last index			
		for i in reversed(range(6)):								#thus the code copied here in reality is just another iteration of the above chunk just for the last index
			if df.iloc[df.index.size-1,1] == baseEntry[i].name:
				new_Shift = Shift(df.iloc[df.index.size-1,2],[df.iloc[df.index.size-1,3],df.iloc[df.index.size-1,5],df.iloc[df.index.size-1,7]], df.iloc[df.index.size-1,14], [df.iloc[df.index.size-1,-5],df.iloc[df.index.size-1,-6],df.iloc[df.index.size-1,-7]],[df.iloc[df.index.size-1,4],df.iloc[df.index.size-1,6],df.iloc[df.index.size-1,8]])
				baseEntry[i].add_shift(new_Shift)
				print(const, ": " ,new_Shift.health)
				if(df.iloc[df.index.size-1,14].lower() != "nil"):
					baseEntry[i].baseLevelDiscrep = df.iloc[df.index.size-1,14]

for i in range(6):
	print(baseEntry[i].name)
	print(baseEntry[i].morning_shift.type)
	print(baseEntry[i].night_shift.type)
	print(baseEntry[i].attendance)
	print("disc: " ,baseEntry[i].getHP())
	
writeRpt()

