import cv2
import diff_match_patch as dmplib
import sys
import json
import numpy
import difflib

def recognize(filename):
	dmp=dmplib.diff_match_patch()
	with open('numSamples.json','r') as fi:
		sample=json.load(fi)

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

	def recognizeOne(imgstr,type):
		similarity={}
		for i in range(0,10):
			similarity.update({i:[]})

		tofind=sample[type]
		for i in range(0,10):
			for j in tofind[str(i)]:
				'''diffs=dmp.diff_main(j,imgstr)
				diffvalue=dmp.diff_levenshtein(diffs)
				maxLength=max(len(j),len(imgstr))
				smlrt=(1-float(diffvalue)/float(maxLength))*100
				'''
				smlrt=difflib.SequenceMatcher(None,j,imgstr).ratio()
				similarity[i].append(smlrt)
		maxvalue=0.0
		maxnum=''
		for i in range(0,10):
			for j in similarity[i]:
				if(j>maxvalue):
					maxvalue=j
					maxnum=str(i)
		return(maxnum)

	img=cv2.imread(filename)
	img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval,img_binized=cv2.threshold(img_gray,180,255,cv2.THRESH_BINARY)
	digits=[img_binized[7:31,0:14],img_binized[12:36,18:36],img_binized[7:31,39:57],img_binized[12:36,62:80]]

	stri=recognizeOne(imageArrayToString(digits[0]),'first')
	for i in range(1,4):
		stri+=recognizeOne(imageArrayToString(digits[i]),'other')
	return(stri)
