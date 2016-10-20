import urllib
import urllib.request
import urllib.parse
import recognition as r
import json
import re

baseURL='http://pgzy.zjzs.net:8011'
loginInfo={
	'shenfenzheng': '', #身份证号码
	'mima': '' #密码
}

datasplithelper={
	'xuekao':[
		'chinese',
		'math',
		'english',
		'politics',
		'history',
		'geography',
		'physics',
		'chemistry',
		'biology',
		'technology',
		'technologyInformation',
		'technologyGeneral',
		'comprehensive'
	],
	'xuankao':[
		'politics',
		'history',
		'geography',
		'physics',
		'chemistry',
		'biology',
		'technology'
	],
}
generalHeaders={
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4',
	'Cache-Control': 'no-cache',
	'Connection': 'keep-alive',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Host': 'pgzy.zjzs.net:8011',
	'Origin': 'http://pgzy.zjzs.net:8011',
	'Pragma': 'no-cache',
	'Referer': 'http://pgzy.zjzs.net:8011/login.htm',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest'
}

cookies=urllib.request.HTTPCookieProcessor()
explorer=urllib.request.build_opener(cookies)

print('loading /login.htm...')
f=explorer.open(urllib.request.Request(
	url=baseURL+'/login.htm',
	headers=generalHeaders
))
print();

captchaFailed=True
loggedIn=False
while captchaFailed:
	print('getting CAPTCHA...')
	f=explorer.open(urllib.request.Request(
		url=baseURL+'/INC/VerifyCode.aspx',
		headers=generalHeaders
	))
	captchabin=f.read()
	myfile=open('./tmp.jpg','wb')
	myfile.write(captchabin)
	myfile.flush()
	myfile.close()

	print('recognizing CAPTCHA...')
	captcha=r.recognize('./tmp.jpg')
	print('CAPTCHA was recognized: '+captcha)

	print('trying to login...')
	logindata={
		'title': 'login',
		'yzm': captcha
	}
	logindata.update(loginInfo)
	f=explorer.open(urllib.request.Request(
		url=baseURL+'/ashx/ajaxHandler.ashx',
		headers=generalHeaders,
		data=bytes(urllib.parse.urlencode(logindata),encoding='utf-8')
	))

	rtn=json.loads(str(f.read(),encoding='utf-8'))
	if(rtn['status']=='failed'):
		if(rtn['des']=='验证码输入错误！'):
			print('CAPTCHA is wrong, try again!')
			print('--------------------------------')
		else:
			print('login failed: '+rtn['des'])
			captchaFailed=False
	else:
		print('logged in!')
		loggedIn=True
		captchaFailed=False
print();

if loggedIn:
	history={
		'xuekao':[],
		'xuankao':[]
	}
	final={
		'xuekao':{},
		'xuankao':{}
	}

	print('getting historic scores...')
	f=explorer.open(urllib.request.Request(
		url=baseURL+'/xklscj.aspx',
		headers=generalHeaders
	))
	rtn=str(f.read(),encoding='utf-8')

	print('parsing html...')
	rtn=rtn.replace('<td class="tdright"></td>','<td class="tdright">empty</td>')
	if(rtn.find('没有查询到学业考试成绩')==(-1)):
		xuekao=re.search(r'考试年月(.*)高考选考历史成绩查询',rtn,re.M|re.I|re.S)
		xuekao=xuekao.group(1)
		historicalXueKao=re.findall(r'<tr><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td></tr>',xuekao,re.M|re.I)
		for i in historicalXueKao:
			tmp={
				'time': i[0]
			}
			for j in range(1,14):
				if(i[j]!='empty'):
					tmp.update({
						datasplithelper['xuekao'][j-1]: i[j]
					})
			history['xuekao'].append(tmp)
	if(rtn.find('没有查询到高考选考成绩')==(-1)):
		xuankao=re.search(r'高考选考历史成绩查询(.*)</table>',rtn,re.M|re.I|re.S)
		xuankao=xuankao.group(1)
		historicalXuanKao=re.findall(r'<tr><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td></tr>',xuankao,re.M|re.I)
		for i in historicalXuanKao:
			tmp={
				'time': i[0]
			}
			for j in range(1,8):
				if(i[j]!='empty'):
					tmp.update({
						datasplithelper['xuankao'][j-1]: i[j]
					})
			history['xuankao'].append(tmp)

	print('getting final score...')
	f=explorer.open(urllib.request.Request(
		url=baseURL+'/xkzzcj.aspx',
		headers=generalHeaders
	))
	rtn=str(f.read(),encoding='utf-8')

	print('parsing html...')
	rtn=rtn.replace('<td class="tdright"></td>','<td class="tdright">empty</td>')
	if(rtn.find('没有查询到学业考试成绩')==(-1)):
		xuekao=re.search(r'<body>(.*)高考选考最终成绩查询',rtn,re.M|re.I|re.S)
		xuekao=xuekao.group(1)
		finallyXueKao=re.findall(r'<tr><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td></tr>',xuekao,re.M|re.I)
		for i in finallyXueKao:
			tmp={}
			for j in range(1,14):
				if(i[j]!='empty'):
					tmp.update({
						datasplithelper['xuekao'][j-1]: i[j]
					})
			final['xuekao'].update(tmp)
	if(rtn.find('没有查询到高考选考成绩')==(-1)):
		xuankao=re.search(r'高考选考最终成绩查询(.*)</table>',rtn,re.M|re.I|re.S)
		xuankao=xuankao.group(1)
		finallyXuanKao=re.findall(r'<tr><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td><td class="tdright">(.+?)</td></tr>',xuankao,re.M|re.I)
		for i in finallyXuanKao:
			tmp={}
			for j in range(1,8):
				if(i[j]!='empty'):
					tmp.update({
						datasplithelper['xuankao'][j-1]: i[j]
					})
			final['xuankao'].update(tmp)
	print(' - historic score(s): '+json.dumps(history));
	print(' - final score: '+json.dumps(final));

	print();

	print('logging out...')
	f=explorer.open(urllib.request.Request(
		url=baseURL+'/logout.aspx',
		headers=generalHeaders
	))
