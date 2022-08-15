# Author: Yoonsung Nam
# Date: 4/19/2022
# Programming Assignment 3
# Implement the different types of join functionalities. Also implement a new parsing system as the SQL file syntax has changed.

from ast import Num
import os
import os.path
import shutil	#This library is included for my drop database functionality
import sys
import fileinput	

parentDir = os.path.dirname(os.path.abspath(__file__)) #this code basically creates a general space for the directory to stay in.
currentDir = None
currentTable = None
setInput = None
delete = False		#Global variable to tell if we need to delete or not
selectOne = None
selectTwo = None
dir1 = None
dir2 = None

fs = sys.stdin.read().split('\n')
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
	global dir1
	global dir2
	len1 = []
	selectTableEm = myList[index].split()[1]										#We are parsing here to find the correct keywords: "Employee" and "Sales"
	selectTableSa = myList[index].split()[3]
	len1.append(len(myList[index]))	#we use this for comparison
	
	if selectTableSa == "Sales":
		pathToDir1 = os.path.join(parentDir, currentDir)							#We are going to create two path diretories. One for the employee and one for the sales.
		pathToDir1 = os.path.join(pathToDir1, selectTableEm)						#Now we are joining the created file in the new directory.
		pathToDir2 = os.path.join(parentDir, currentDir)
		pathToDir2 = os.path.join(pathToDir2, selectTableSa)

		dir1 = pathToDir1															#We made global variables so we can call some the path directories into the global variables to be accssed later.
		dir2 = pathToDir2

def createTable(index):
	paren = '('
	mySplit = myList[index].split()[2]
	tableSplit = mySplit.split(paren, 1)[0]
	tableInput = myList[index][myList[index].find("(") + 1: myList[index].find(";") - 1]	#This line will make sure that the file is parsed through. From the content that is to be inputed, the "(" and the ";" will be taken out.
	inputWithBar = tableInput.replace(",", " | ")											#Since the formatt needes to have a bar, the program will replace the comma with the bar.
	completeInput = inputWithBar.split()
	pathToDir = os.path.join(parentDir, currentDir)
	pathToDir = os.path.join(pathToDir, tableSplit)
	if not (os.path.exists(pathToDir)):
		tableMake = open(pathToDir, "x")													#inside the correct directory, the program will create a file and write to the file.
		tableMake = open(pathToDir, "w")
		tableMake.write(completeInput[0] + " " + completeInput[1] + completeInput[2] + completeInput[3] + " " + completeInput[4] + "\n") 														#write in the inputs into the file.
		tableMake.close()
		if tableSplit != "to":																#This if and else statement is placed here to remove a little error in the output
			print("Table " + tableSplit + " created.")
	else:
		print("!Failed to create table " + tableSplit + " because it already exists.")

def useDatabase(index):
	global currentDir 																		#global current_dir takes the local use variable
	useDir =myList[index].split()[1].replace(";", "") 										#this is the name of the directory accessed.
	checkDir = os.listdir(parentDir)
	if useDir in checkDir:
		currentDir = useDir 																#this changes my current_dir to the user input dir
		if os.path.exists(useDir) == True:	
			print("Using Database " + useDir + ".")

def createDatabase(index):
	databaseSplit = myList[index].split()[2].replace(";", "")	#The program will first find the database name in the file. Since the database name will also have a semicolon attached to it, we will have to replace that.
	path = os.path.join(parentDir, databaseSplit)				#The program join the database (directory name) to the existing directory (parentDir). This will add a new extension to the path.
	if os.path.exists(path) == False:							
		path = os.path.join(parentDir, databaseSplit)			#if the new path that includes the new directory exists, then we can actually create the path with the os.mkdir.
		os.mkdir(path)
		print("Database " + databaseSplit + " created.")
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
			print("1 new record inserted")
	else:
		print("!Failed to create table " + insertSplit + " because it already exists.")

def update(index):												#This code block is for updating the current table that will be accessed. This code will read through the sql file and will take in the name of the table.
	global currentTable 										#Then, the table name will be set to the global variable value.
	updateTable = myList[index].split()[1]
	currentTable = updateTable									#The global variable value for the name of the table is now initialized. This vale can be accessed later to tell which table is being used.

def setStuff(index): 											#With this function, we are going to read through the given SQL file to find where it says "set." Where it says "set", the code will read the value that we will be setting the value into the table to.
	global setInput												#For example, with set name 'Gizmo', we will set aside Gizmo as a global setInput variable to be used later.
	setSplit = myList[index].split()[3]
	setInput = setSplit.replace("'", "")						#This line is basically for taking away the ' in 'Gizmo'. so it will be Gizmo.
	#print("This is the setInput: " + setInput)
	# if '.' in setInput:
	# 	#Try to tell if string is a a float
	# 	float(setInput)

def whereStuff(index, check: bool):
	ID_Array_EM = []	#this now holds all the values from the employee file
	ID_Array_SA = []	#this holds all the values from the sales file
	em = []				#this holds all the values of the ID from the employee file
	sa = []				#this holds all the values of the ID from the sales file
	n, i, myIndex = 0, 0, 0
	myI = 1
	myI2 = 1


	if str(myList[index]) != "-- All done.":
		while i != 2:
			whereSplitEm = myList[index].split()[1]					#We are parsing here to check if the return myList[index] value has the E.id value
			whereSplitSa = myList[index].split()[3]					#We are parsing here to check if the retur myList[index] value has the S.employeeID inside of it.
			whereSplitSaNew = whereSplitSa.replace(";", "")

			i+=1
		f = open(dir1, 'r')						#We open up the dir1 file to read it. The dir1 should have the employee path. Thus file will have the info from the emplyee file
		file = f.read().split("\n")
		f= open(dir2, 'r')						#Same logic goes for the dir2 file. Thus file2 will have the info from the sales file in it.
		file2 = f.read().split("\n")			
		f.close()
			
		for i in file:							
			whereID = i.split("|")	
			ID_Array_EM.append(whereID)			#The ID_Array_EM array will hold all of the split whereID values.
			em.append(whereID[0])

		for i in file2:
			whereID = i.split("|")
			ID_Array_SA.append(whereID)			#The Id_Array_SA array will hold all of the split values from file2
			sa.append(whereID[0])

		if whereSplitEm == "E.id" and whereSplitSaNew == "S.employeeID" and check == False:			#Logic to inititate everything else.	We have the check statement to see if there was the keyword "outer"

			print(str(ID_Array_EM[n][n]) + "|" + str(ID_Array_EM[n][1]) + "|" + str(ID_Array_SA[n][n]) + "|" + str(ID_Array_SA[n][1]))		#Prints out the basic header titles.

			while n != (len(file) - 1):
				if str(ID_Array_EM[myI2][0]) == str(ID_Array_SA[myI][0]):			#If the IDs inside of the EM array are in the SA array, then we can print out the file values to the terminal.
					print(file[myI2] + "|" + file2[myI])
					myI+=1
				else:		
					myI2+=1
				n+=1
		else:		#In this case, there was the keyword "outer". So we will be printing everything. 
			#We can place the outer join return here.
			print(str(ID_Array_EM[n][n]) + "|" + str(ID_Array_EM[n][1]) + "|" + str(ID_Array_SA[n][n]) + "|" + str(ID_Array_SA[n][1]))
			while n != (len(file) - 1):
				if str(ID_Array_EM[myI2][0]) == str(ID_Array_SA[myI][0]):		#Same logic as above
					print(file[myI2] + "|" + file2[myI])
					myI+=1
				else:		
					myI2+=1
				n+=1
			if str(em[3]) not in sa:											#This part is the logic used to print the final value that was not printed before.
				print(file[3] + "||")		


	
	
def deleteFrom(index):												#This function basically find the word delete as the SQL file is parsed through.
	global currentTable 											#The table that we are deleting from will be specified and we will also set the global variable for delete as True.
	global delete
	deleteTable = myList[index].split()[2]
	finalDelete = deleteTable.capitalize()
	currentTable = finalDelete
	delete = True

def selectMultiple(index):											#This function is used specifically for when we are selecting multiple things.
	global selectOne												
	global selectTwo												
	pathToDir = os.path.join(parentDir, currentDir)				
	pathToDir = os.path.join(pathToDir, currentTable)
	multipleSelect = myList[index].split()
	stringSelect = ''.join(str(item) for item in multipleSelect[1])
	stringSelect2 = ''.join(str(item) for item in multipleSelect[2])		#From the SQL file, this function is going to read and store the things that we are trying to select. For example, it will be "name" and "price in this case"
	realSelect = stringSelect.replace(",", "")
	#multipleSelect[2] is the price.
	selectOne = realSelect											#We set global variables selectOne and selectTwo to be the value that we read from the SQL file. It will be name and price.
	selectTwo = multipleSelect[2]									

def myMain():
	print("-- Expected output --")
	count = 0
	
	for index in range(len(fs)):								#This for loop will loop through the "fs" which is the variable that reads through the entire input file.

		myList.append(fs[index])								#myList is declared globally as an empty list. However, as the program loops through the fs and appends each element of the fs into the myList.
																#From here on out, we will use myList to check for keywords such as "CREATE DATABASE" etc.
	for index in range(len(myList)):								
		if "DROP TABLE" in myList[index].upper():				#When we loop through the myList (Which has the contents from the sqlfile) if we find certain keywords, we will call the functions associated to them.
			dropTable(index)									#For instance, since we found "DROP TABLE" keyword from the myList, we will call the dropTable function.
		elif "ALTER TABLE" in myList[index].upper():
			alterTable(index)
		elif "select" in myList[index]:
			selectTable(index + 1)	
		elif "CREATE TABLE" in myList[index].upper():
			createTable(index)
		elif "DROP DATABASE" in myList[index].upper():
			dropDatabase(index)
		elif "USE" in myList[index].upper():
			useDatabase(index)
		elif "insert into" in myList[index]:
			insertToTable(index)
		elif "CREATE DATABASE" in myList[index].upper():
			createDatabase(index)
		elif "update" in myList[index]:
			update(index)
			count += 1
			print(str(count) + " new record modified.")			#This code is here to count how many times it is being modified.
		elif "set" in myList[index]:							
			setStuff(index)
		elif "where" in myList[index]:
			whereStuff(index, False)
		elif "delete from" in myList[index]:
			deleteFrom(index)
		elif "inner join" in myList[index]:
			whereStuff(index + 1, False)							#Since there was no "outer" in the read keyword, we will be passing in "False" as the argument type.
		elif "outer join" in myList[index]:							
			whereStuff(index + 1, True)
		# elif "select" in myList[index]:							#This select is only for the selecting multiple values. 
		# 	selectMultiple(index)
		
	print("-- All done --")
	

myMain()

