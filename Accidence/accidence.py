import urllib.request
import urllib.parse
import http.cookiejar
import webbrowser
from bs4 import BeautifulSoup

# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# rqs = opener.open('https://sso.kedacom.com:8443/CasServer/login?service=https://oa.kedacom.com/portal/j_spring_cas_security_check')
# # html = rqs.read().decode('utf-8')

# soup = BeautifulSoup(rqs.read(), 'xml')
# for item in soup.form.find_all('input'):
#     if item.get('name') == 'lt':
#         lt = item.get('value')
#     if item.get('name') == 'execution':
#         execution = item.get('value')

# action = soup.form.get('action')

# print(soup.form)
# print()
# print(lt, execution, action)

# a = {}
# for item in cookie:
#     a[item.name] = item.value

# print(a)


# if 0:
#     filename = 'cookie.txt'
#     cookie = http.cookiejar.MozillaCookieJar(filename)
#     handler = urllib.request.HTTPCookieProcessor(cookie)
#     opener = urllib.request.build_opener(handler)
#     rqs = opener.open('https://sso.kedacom.com:8443/CasServer/login')
#     cookie.save(ignore_discard=True, ignore_expires=True)

#     for item in cookie:
#         print(item.name + "=" + item.value)

#     print()
#     print(cookie)

# # rqs = urllib.request.urlopen('https://sso.kedacom.com')
# # html = rqs.read().decode('utf-8')
# # print(html)

# cookie = http.cookiejar.MozillaCookieJar()
# cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

# print(cookie)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('https://sso.kedacom.com')
# print(response.read().decode('utf-8'))


# webbrowser.open('http:www.baidu.com')

# post={
#     'username': 'username',
#     'password': 'PASSWORD',
#     'vcode': '',
#     'rememberMetest': 'true',
#     'lt': 'LT-931901-WM4c4yRoohhu2JDVIf2vHmhrPqntcN',
#     'execution': 'e6s1',
#     '_eventId': 'submit',
#     'loginType': 'web',
#     'kdmoaAccount':'nice',
#     'submit':''
# }
# postData = urllib.parse.urlencode(post)
# print(postData)

import os
import sys
import re

print(os.path.abspath(__file__))
print(os.getcwd())

target = os.path.dirname(os.path.abspath(__file__))
os.chdir(target)
f = open('return.txt', 'rb')
try:
    ret = f.read().decode('utf-8')

    # pattern = re.compile(r'badgeNumber\s?=\s?\"(\w+)\"', re.M)
    pattern = re.compile(r'isOrder\s?=\s?(\d+)', re.M)
    match = pattern.match(ret)
    print(match)
    if match:
        print('search...')
        print(match.group(1))

except Exception as e:
    print(e)
finally:
    f.close()

# with open('return.txt', 'r', encoding='utf-8') as f:
#     ret = f.read()
#     print(ret)
#     # print(re.search('overDeadTime', ret))
#     # pattern = re.compile(r'var\s(\w+)\s?=(\d)')
#     a = 'var overDeadTime =1;//1表示已经超过了时间'
#     pattern = re.compile(r'var\s(\w+)')
#     match = pattern.match(ret)
#     print()
#     print(match)
#     if match:
#         print(int(match.group(1)))
    # print(ret)

# a = '''//外部传入的值 isOrder,orderInfo.userEmail//
#         var overDeadTime =1;//1表示已经超过了时间'''
# pattern = re.compile(r'.+var\s(\w+)\s?=(\d+)', re.X)
# match = pattern.match(a)
# print(match)
# if match:
#     print('match...')
#     print(match.group(1), match.group(2))

# match = pattern.search(a, re.M)
# print(match)
# if match:
#     print('search...')
#     print(match.group(1), match.group(2))