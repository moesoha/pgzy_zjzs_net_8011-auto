# 浙江省高校招生考试信息管理系统自动脚本

详细介绍请看BLOG.md

很遗憾，本仓库中的验证码识别方法仅能用于浙江省高校招生考试信息管理系统的登录验证码。但是希望文中的识别思路能给你带来灵感。

文件解释：
  - `splitDigits.py`是根据`captchaExamples`文件夹中包含的`*.jpg`分离出每一位数字然后建立识别库的。
  - `recognize.py`通过使用`$ recognize.py captcha.jpg`命令可以输出captcha.jpg的识别结果。
  - `recognition.py`识别方法。在别的py中通过`import recognition as r`然后`r.recognize(filename)`可以识别filename这个图片文件中的数字。
  - `login.py`仅登录登出，登录信息在代码中的`loginInfo`变量内。
  - `getScore.py`登录获取成绩们并登出，登录信息在代码中的`loginInfo`变量内。。
  - `numSamples.json`数字样本数据库。
  - `testCaptcha`文件夹，存放着10张用于测试的验证码，不放入样本库。
  - `captchaExamples`文件夹，存放着用于样本识别的验证码。
