import urllib
import urllib.request
import urllib.parse
import recognition as r
import json

baseURL='http://pgzy.zjzs.net:8011'
loginInfo={
	'shenfenzheng': '', #身份证号码
	'mima': '' #密码
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
	print('logging out...')
	f=explorer.open(urllib.request.Request(
		url=baseURL+'/logout.aspx',
		headers=generalHeaders
	))
