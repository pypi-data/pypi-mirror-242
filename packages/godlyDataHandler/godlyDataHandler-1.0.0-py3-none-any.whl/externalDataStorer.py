import csv, os

currDirr = os.getcwd()
directory = "outputData"
path = os.path.join(currDirr, directory)

try:
	os.makedirs(path)
except FileExistsError:
	pass
os.chdir(path)


def storeArray(arrayName, array, arrayDimension):
	with open(arrayName+'.csv', 'w') as csvfile:
		csvwriter = csv.writer(csvfile)
		if arrayDimension==1:
			csvwriter.writerow(array)
			return
		elif arrayDimension==2:
			csvwriter.writerows(array)
			return
		raise ValueError("Invalid arrayDimension: it should be 1 or 2")

def readArray(arrayName):
	try:
		with open(arrayName+'.csv', 'r') as csvfile:
			csvFile = csv.reader(csvfile)
			arr = [elem for elem in csvFile]
			return arr
	except FileNotFoundError:
		raise NameError("Array does not exist.")

def deleteArray(arrayName):
	os.remove(arrayName)
