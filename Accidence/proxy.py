import urllib.request

url = 'http://www.baidu.com'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

httpproxy_handler = urllib.request.ProxyHandler({'http':'122.95.9.3:8118'})
nullproxy_handler = urllib.request.ProxyHandler({})

proxyswitch = True

if proxyswitch: 
    opener = urllib.request.build_opener(httpproxy_handler)
else:
    opener = urllib.request.build_opener(nullproxy_handler)

request = urllib.request.Request(url, headers=header)

# 只有使用opener.open()方法发送请求才使用自定义的代理,
# 而urlopen()则不适用自定义代理
response = opener.open(request)

# 这么写，就是将opener应用到全局，之后所有的，不管是opener.open()
# 还是urlopen()发送请求，都将使用自定义代理
# urllib.install_opener(opener)
# response = urllib.request.urlopen(request)

print(response.read().decode('utf-8'))
