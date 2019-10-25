import urllib
import urllib.request
import urllib.parse
import http.cookiejar
from bs4 import BeautifulSoup
import re
import json


class KDoa:
    def __init__(self):
        self.hostUrl = "https://sso.kedacom.com:8443"
        self.paramUrl = "/CasServer/login?service=https://oa.kedacom.com/portal/j_spring_cas_security_check"
        self.dinnerUrl = "https://oa.kedacom.com/kmoa/mealOrder/dinnerToday.do"
        self.dinnerOrderUrl = "https://oa.kedacom.com/kmoa/mealOrder/orderOrCancel.do"
        self.userName = ""
        self.password = ""
        self.fullName = ""
        self.badgeNumber = ""
        self.isOrder = 0
        self.overDeadTime = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }

        self.cookie = http.cookiejar.CookieJar()
        self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler)
        response = self.opener.open(self.hostUrl + self.paramUrl)

        soup = BeautifulSoup(response.read(), "lxml")
        self.lt = soup.select("input[name='lt']")[0].get("value")
        self.execution = soup.select("input[name='execution']")[0].get("value")

        self.actionUrl = soup.form.get("action")

        self.loginPost = {
            "username": self.userName,
            "password": self.password,
            "rememberMetest": True,
            "_eventId": "submit",
            "loginType": "web",
            "kdmoaAccount": "nice",
            "lt": self.lt,
            "execution": self.execution,
            "vcode": "",
            "submit": "",
        }

        self.dinnerPost = {
            "clientType": "PC",
            "userEmail": self.userName,
            "badgeNumber": self.badgeNumber,
            "fullname": self.fullName,
            "isOrder": self.isOrder,
        }

    def login(self):
        url = self.hostUrl + self.actionUrl
        post = urllib.parse.urlencode(self.loginPost).encode(encoding="utf-8")
        request = urllib.request.Request(url, post, headers=self.headers)
        response = self.opener.open(request)
        content = response.read().decode("utf-8")

    def dinner(self):
        request = urllib.request.Request(self.dinnerUrl, headers=self.headers)
        response = self.opener.open(request)

        soup = BeautifulSoup(response.read(), "lxml")
        for item in soup.find_all("script"):
            if item.string:
                ret = item.string

        pattern = re.compile(r"overDeadTime\s?=\s?(\d+)", re.M)
        match = pattern.match(ret)
        if match:
            self.overDeadTime = int(match.group(1))

        pattern = re.compile(r"isOrder\s?=\s?(\d+)", re.M)
        match = pattern.search(ret)
        if match:
            self.isOrder = int(match.group(1))

        pattern = re.compile(r"badgeNumber\s?=\s?\"(\w+)\"", re.M)
        match = pattern.search(ret)
        if match:
            self.badgeNumber = str(match.group(1))

        if self.overDeadTime:
            if self.isOrder:
                print("不可取消...")
            else:
                print("不可预订...")
            return

        if self.isOrder:
            print("晚餐已经预约,是否要取消预约?")
            self.isOrder = 0
        else:
            print("晚餐尚未预约,是否要进行预约?")
            self.isOrder = 1

        self.dinnerPost["badgeNumber"] = self.badgeNumber
        self.dinnerPost["isOrder"] = self.isOrder

        post = urllib.parse.urlencode(self.dinnerPost).encode(encoding="utf-8")
        request = urllib.request.Request(
            self.dinnerOrderUrl, post, headers=self.headers
        )
        response = self.opener.open(request)
        content = json.loads(response.read().decode("utf-8"))

        if content:
            self.isOrder = int(content["info"]["isOrder"])

        if self.isOrder:
            print("晚餐已成功预约...")
        else:
            print("晚餐已取消预约...")


if __name__ == "__main__":
    oa = KDoa()
    oa.login()
    oa.dinner()

