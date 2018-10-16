import csv
import json
import sys
import ast

def getcols(line,parent=''):
	headers=[]
	# print(parent)
	for key,val in line.items():
		if(isinstance(val,str) and val.startswith('{')):
			val=ast.literal_eval(val)
		if(isinstance(val,dict)):
			if(parent!=''):
				headers.extend(getcols(val,parent+'.'+key))
			else:
				headers.extend(getcols(val,key))
		else:
			if(parent!=''):
				headers.append(parent+'.'+key)
			elif(val!=None):
				headers.append(key)
	return(headers)

def getNestedElements(line,column):
	if('.' not in column):
		if(column not in line):
			return(None)
		return(line[column])
	else:
		parent,child=column.split('.',1)
		try:
			if(parent not in line):
				return(None)
			if(line[parent]==None):
				return(None)
		except KeyError:
			print("KeyError")
			
		else:
			#if(isinstance(line[parent],str) and line[[parent].startswith('{')]):
			if(isinstance(line[parent],str) and line[parent].startswith('{')):
				return(getNestedElements(ast.literal_eval(line[parent]),child))
			else:
				return(getNestedElements(line[parent],child))

def flatten(line,columns):
	record=[]
	for i in columns:
		ele=getNestedElements(line,i)
		if(ele==None):
			record.append('')
		else:
			record.append(ele)
	return(record)


def convert_to_csv(jsonfile):
	print(jsonfile)
	csvfile=open(jsonfile[0:jsonfile.index('.')+1]+"csv",'w')
	writer=csv.writer(csvfile,delimiter=',')
	with open(jsonfile,'r') as file:
		headers=set()
		for line in file:
			headers.update(getcols(json.loads(line)))
		print(headers)
		writer.writerow(headers)
		file.seek(0,0)
		for line in file:
			l=flatten(json.loads(line),headers)
			writer.writerow(l)
	csvfile.close()

jsonfile=sys.argv[1]
convert_to_csv(jsonfile)