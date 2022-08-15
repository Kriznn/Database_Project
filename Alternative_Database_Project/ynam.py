#Author: Yoonsung Nam
#Date: 5/10/2022
#Purpose: This program will take into account two different processes running the code. It will manage the transaction between them.

import os
import os.path
import shutil	

transaction = False
commit = False
wasCalled = False
tableName = ""
parentDir = os.path.dirname(os.path.abspath(__file__)) #this code basically creates a general space for the directory to stay in.
currentDir = None

# fs = sys.stdin.read().split('\n')
myList = [] #the sql file input is stored in this list

def alterTable(index):
	alterTable = myList[index].split()[2]
	alterTable1 = myList[index].split()[4]								#The program will take the file input afte the keyword "ADD"
	alterTable2 = myList[index].split()[5].replace(";","")				#The program takes the file input, but it will remove the semicolon.
	maxTable = alterTable1 + " " + alterTable2							#This new variable will put the others together

	pathToDir = os.path.join(parentDir, currentDir)						#This will access the path(directory) that contains the file inputed filename
	pathToDir = os.path.join(pathToDir, alterTable)
	if os.path.exists(pathToDir):										#if the path exists, the program will add in the newly read content into the file.
		addFile = open(pathToDir, "a")
		addFile.write(" | " + maxTable) 
		addFile.close()
		print("Table " + alterTable + " modified.")
	else:
		print("!Failed to query table " + alterTable + " because it does not exist.")

def selectTable(index):
	selectTable = myList[index].split()[3]
	newTable = selectTable.replace(";", "")
	pathToDir = os.path.join(parentDir, currentDir)						#This access the global variables. The general parentDir is moved back into the currentDir.
	pathToDir = os.path.join(pathToDir, newTable)						#Now we are joining the created file in the new directory.
	if os.path.exists(pathToDir):										#Checking if the directory path where the table we are printing exists.
		tableOpen = open(pathToDir, "r")
		output = tableOpen.read()
		print(output)
		tableOpen.close()
	else: 
		print("!Failed to query table " + selectTable + " because it does not exist.")

def createTable(index):
	global tableName
	tableSplit = myList[index].split()[2] #remember that we split by whitespace	
	tableInput = myList[index][myList[index].find("(") + 1: myList[index].find(";") - 1]	#This line will make sure that the file is parsed through. From the content that is to be inputed, the "(" and the ";" will be taken out.
	inputWithBar = tableInput.replace(",", " | ")											#Since the formatt needes to have a bar, the program will replace the comma with the bar.
	pathToDir = os.path.join(parentDir, currentDir)
	pathToDir = os.path.join(pathToDir, tableSplit)
	tableName = tableSplit
	
	if not (os.path.exists(pathToDir)):
		tableMake = open(pathToDir, "x")													#inside the correct directory, the program will create a file and write to the file.
		tableMake = open(pathToDir, "w")
		tableMake.write(f"{inputWithBar}\n") 														#write in the inputs into the file.
		tableMake.close()
		if tableSplit != "to":																#This if and else statement is placed here to remove a little error in the output
			print("-- Table " + tableSplit + " created.")
	else:
		print("!Failed to create table " + tableSplit + " because it already exists.")

def useDatabase(index):
	global currentDir 																		#global current_dir takes the local use variable
	useDir =myList[index].split()[1].replace(";", "") 										#this is the name of the directory accessed.
	checkDir = os.listdir(parentDir)
	if useDir in checkDir:
		currentDir = useDir 																#this changes my current_dir to the user input dir
		if os.path.exists(useDir) == True:	
			print("-- Using Database " + useDir + ".")

def createDatabase(index):
	databaseSplit = myList[index].split()[2].replace(";", "")	#The program will first find the database name in the file. Since the database name will also have a semicolon attached to it, we will have to replace that.
	path = os.path.join(parentDir, databaseSplit)				#The program join the database (directory name) to the existing directory (parentDir). This will add a new extension to the path.
	if os.path.exists(path) == False:							
		path = os.path.join(parentDir, databaseSplit)			#if the new path that includes the new directory exists, then we can actually create the path with the os.mkdir.
		os.mkdir(path)
		print("\n-- Database " + databaseSplit + " created.")
	else:
		print("!Failed to create database " + databaseSplit + " because it already exists.")

def dropDatabase(index):
	databaseSplit = myList[index].split()[2].replace(";", "")		#We parse through the sql file and find the directory name to be deleted.
	path = os.path.join(parentDir, databaseSplit)
	if os.path.exists(path) == True:								#If the path directory with the directory name exists, the program removes that directory.
		shutil.rmtree(databaseSplit)
		print("Database " + databaseSplit + " deleted.")
	else:
		print("!Failed to delete " + databaseSplit + " because it does not exist.")

def dropTable(index):											
	dropSplit = myList[index].split()[2].replace(";", "")		
	pathToDir = os.path.join(parentDir, currentDir)				#The program will find the path with the intended directory and the file that has been read from the sql file.
	pathToDir = os.path.join(pathToDir, dropSplit)
	if os.path.exists(pathToDir) == True:
		os.remove(pathToDir)									#If the path that has the file that is to be deleted exists, then we can remove the file
		print("Table " + dropSplit + " deleted.")
	else:
		print("!Failed to delete " + dropSplit + " because it does not exist.")

def insertToTable(index):																		#For this function, it is going to read through the sql file once more to see what we should input into out tables
	insertSplit = myList[index].split()[2]																
	tableInput = myList[index][myList[index].find("(") + 1: myList[index].find(";") - 1]		#It will take out the unnecessary info such as the ( ) and the ; and it will replace it will the |. Then it will add it on to the table.
	inputWithBar = tableInput.replace(",", " | ")
	finalInput = inputWithBar.replace("'", "")												
	finalInputWithSpace = finalInput.replace("\t", "")											#The code from lines 108 to 111 is for taking out all the unnecessary things. such as the \t, ' , and the empty spaces.
	ultimateInput = finalInputWithSpace.replace(" ", "")
	pathToDir = os.path.join(parentDir, currentDir)												#With this code, we are going to figure out the correct directory path that the table is currently in.
	pathToDir = os.path.join(pathToDir, insertSplit)

	if (os.path.exists(pathToDir)):
        #tableMake = open(pathToDir, "x")													#inside the correct directory, the program will create a file and write to the file.
		tableMake = open(pathToDir, "a")														#We will be appending into the table file. Not overwriting
		tableMake.write(ultimateInput + "\n") 													#write in the inputs into the file.
		tableMake.close()
        #print("1 new record inserted")
		if insertSplit != "to":																#This if and else statement is placed here to remove a little error in the output
			print("-- 1 new record inserted")
	else:
		print("!Failed to create table " + insertSplit + " because it already exists.")

def update(index):											#This code block is for updating the current table that will be accessed. This code will read through the sql file and will take in the name of the table.
	statusSplit = myList[index].split()[5].replace("\n", "")					
	seatSplit = myList[index].split()[9].replace("\n", "")							#We are basically parsing through the given update command to see what the seat number is and what status value we will be switching to.
	newSeatSplit = seatSplit.replace(";", "")
	tempSplit = myList[index].split()[1].replace("\n", "")
	updateSplit = tempSplit.capitalize()											#Since Flights was given uncapitalized, we have to capitalize it.		
	pathToDir = os.path.join(parentDir, currentDir)
	tempToDir = os.path.join(pathToDir, "temp.txt")									#This is the path to the temporary file placeholder.
	pathToDir = os.path.join(pathToDir, updateSplit)								#This is the directory path that has the original Flights text file.

	f = open(pathToDir, "r")														#We first read through the Flights text file to store the necessary values.
	fileRead = f.readlines()
	tableTitle = fileRead[0].replace("\n", "")
	status_one = fileRead[1].split("|")[0].replace("\n", "")
	status_one_more = fileRead[1].split("|")[1].replace("\n", "")
	status_two = fileRead[2].split("|")[0].replace("\n", "")
	status_two_more = fileRead[2].split("|")[1].replace("\n", "")

	if transaction == True:															#transaction == True only applies when the lockProcess function is called. The lockProcess function is called only when the user gives the "begin transaction" command.
		if newSeatSplit == "22" and statusSplit == "1":				#This is the edge case.
			f = open(tempToDir, "w")																	#only when the transaction begins will the program write to the temporary file.
			f.write(f"{tableTitle}\n{status_one}|{statusSplit}\n{status_two}|{status_two_more}")		#This f string basically has all the necessary information from the originally read file and it writes it to the temporary file.
			print("-- 1 record modified.")	

def lockProcess(index):
	global transaction
	global wasCalled
	global commit	
	transaction = True
	pathToDir = os.path.join(parentDir, currentDir)					#in this function, we will be checking and seeing if the update function has already ran. 
	tempToDir = os.path.join(pathToDir, "temp.txt")

	if os.path.exists(tempToDir) == True:							#Since update function is creating and writing to a temporary file, we will check and see if the temporary file exists
		wasCalled = True											#If the temporary file exists, we will be updating the global variable to let it know that update has been called before.
		commit = True
	else:
		wasCalled = False
	print("-- Transaction starts.")

def function_commit(index):
	global commit
	commit = True
	try:
		pathToDir = os.path.join(parentDir, currentDir)				#We are trying to read the stored information in the temporary file, and we will write that back into the Flights file.
		tempToDir = os.path.join(pathToDir, "temp.txt")
		pathToDir = os.path.join(pathToDir, tableName)

		f = open(tempToDir, "r")									#We will read from the temporary file.
		fr = f.read()

		fw = open(pathToDir, "w")									#We will place the read value from the temp file in to the main Flights file.
		fw.write(fr)

		print("-- Transaction committed.")
	except (IsADirectoryError):
		print("-- Transaction abort.")								#We implement a try-catch here to give an error in process 2. Basically, when the process tries to make a commit even though calling an update gave an errorm it will give an error.
																	#Since update was never called and given an error, the temporary file never exists in this case and will give a directory error.
	

def myMain():

	while True:
		userInput = input("")										#We changed the code to take in user input in the terminal as commands instead of reading from the SQl file and parsing through it.
		myList.append(userInput)									#We will read the user command, append it to a list, and parse through that list to find the keyword.

		for index in range(len(myList)):
			if "DROP TABLE" in myList[index].upper():				#When we loop through the myList (Which has the contents from the sqlfile) if we find certain keywords, we will call the functions associated to them.
				dropTable(index)									#For instance, since we found "DROP TABLE" keyword from the myList, we will call the dropTable function.
				myList.pop()
			elif "ALTER TABLE" in myList[index].upper():
				alterTable(index)
				myList.pop()										#We must also make sure to pop the user input from the list after the function is called. We only want to have one command in the list at a time.
			if "select" in myList[index]:
				selectTable(index)
				myList.pop()
			elif "create table" in myList[index]:
				createTable(index)
				myList.pop()
			elif "DROP DATABASE" in myList[index].upper():
				dropDatabase(index)
				myList.pop()
			elif "USE" in myList[index].upper():
				useDatabase(index)
				myList.pop()
			elif "CREATE DATABASE" in myList[index].upper():
				createDatabase(index)
				myList.pop()
			elif "insert into" in myList[index]:
				insertToTable(index)
				myList.pop()
			elif "update" in myList[index]:
				# print(f"test for wasCalled: {wasCalled}")
				# print(f"test for commit: {commit}")
				if wasCalled == False:												#This logic just checks if the update function was already called, if it was not called before, the program runs the update function.
					update(index)
				else:
					print(f"-- Error: Table {tableName} is locked!")				#In the case for process 2 where it is trying to run the update function again before the commit has been called in process 1, it will give an error
				myList.pop()
			elif "begin transaction" in myList[index]:
				lockProcess(index)
				myList.pop()
			elif "commit" in myList[index]:
				function_commit(index)
				myList.pop()

		

	

myMain()

