import cv2
import os
import os.path
import re
import json

def imageArrayToString(img):
	string=''
	for j in img:
		for k in j:
			t=k
			if(t==255):
				t=0
			else:
				t=1
			string+=str(t)
		string+="\n"
	return(string)

fileList=[]
dictionary={'first':{},'other':{}}

for i in range(0,10):
	dictionary['first'].update({i:[]})
	dictionary['other'].update({i:[]})

rootDir='./captchaExamples'
for filename in os.listdir(rootDir):
	if os.path.isfile(os.path.join(rootDir,filename)):
		if os.path.splitext(filename)[1]=='.jpg':
			print('found CAPTCHA example: '+os.path.join(rootDir,filename))
			fileList.append(os.path.join(rootDir,filename))

for filename in fileList:
	img=cv2.imread(filename)
	thisid=re.search(r'\d\d\d\d',filename,re.M|re.I)
	thisid=thisid.group(0)
	img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval,img_binized=cv2.threshold(img_gray,180,255,cv2.THRESH_BINARY)
	#digits=[img_binized[7:24,0:14],img_binized[12:24,18:18],img_binized[7:24,39:18],img_binized[12:24,62:18]]
	digits=[img_binized[7:31,0:14],img_binized[12:36,18:36],img_binized[7:31,39:57],img_binized[12:36,62:80]]
	#for i in range(0,3):
	#	cv2.imshow('['+str(i)+'] '+thisid[i]+' - #'+thisid,digits[i])
	'''print(digits[0])
	print(digits[1])
	print(digits[2])
	print(digits[3])'''

	for i in range(0,4):
		string=imageArrayToString(digits[i])
		if(i==0):
			dictionary['first'][int(thisid[i])].append(string)
		else:
			dictionary['other'][int(thisid[i])].append(string)

for i in range(0,10):
	if(len(dictionary['first'][i])==0):
		print('first.'+str(i)+' missing')
	else:
		print('first.'+str(i)+' has '+str(len(dictionary['first'][i]))+' sample(s)')
	if(len(dictionary['other'][i])==0):
		print('other.'+str(i)+' missing')
	else:
		print('other.'+str(i)+' has '+str(len(dictionary['other'][i]))+' sample(s)')

	dictionary['first'][i]=list(set(dictionary['first'][i]))
	dictionary['other'][i]=list(set(dictionary['other'][i]))

#print(json.dumps(dictionary))
#print(dictionary)
with open('numSamples.json','w') as fi:
	json.dump(dictionary,fi)
