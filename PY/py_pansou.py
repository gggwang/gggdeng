#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import requests

class Spider(Spider):
	def getDependence(self):
		return ['py_ali']
	def getName(self):
		return "py_pansou"
	def init(self,extend):
		self.ali = extend[0]
		print("============py_pansou============")
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		return result
	def homeVideoContent(self):
		result = {}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		return result

	def detailContent(self,array):
		tid = array[0]
		pattern = '(https:\\/\\/www.aliyundrive.com\\/s\\/[^\\\"]+)'
		url = self.regStr(tid,pattern)
		if len(url) > 0:
			return self.ali.detailContent(array)
		header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
			'Referer': 'https://www.alipansou.com/s/' +tid
		}
		rsp = requests.get('https://www.alipansou.com/cv/'+tid, allow_redirects=False, headers=header)
		url = self.regStr(reg=r'href=\"(.*)\"', src=rsp.text)
		if len(url) == 0:
			return ""
		url = url.replace('\\','')
		newArray = [url]
		print(newArray)
		return self.ali.detailContent(newArray)

	def searchContent(self,key,quick):
		map = {
			'7':'文件夹',
			'1':'视频'
		}
		ja = []
		for tKey in map.keys():
			url = "https://www.alipansou.com/search?k={0}&t={1}".format(key,tKey)
			rsp = self.fetch(url)
			root = self.html(self.cleanText(rsp.text))
			aList = root.xpath("//van-row/a")
			for a in aList:
				title = ''
				divList = a.xpath('.//template/div')
				t = divList[0].xpath('string(.)')
				t = self.cleanText(t).strip()
				title = title + t
				remark = divList[1].xpath('string(.)')
				remark = self.cleanText(remark).replace('\xa0\xa0','').strip().split(' ')[1]
				if key in title:
					pic = 'https://www.alipansou.com'+ self.xpText(a,'.//van-card/@thumb')
					jo = {
						'vod_id': self.regStr(a.xpath('@href')[0],'/s/(.*)'),
						'vod_name': '{0}[{1}]'.format(title,remark),
						'vod_pic': pic
					}
					ja.append(jo)
		result = {
			'list':ja
		}
		return result

	def playerContent(self,flag,id,vipFlags):
		return self.ali.playerContent(flag,id,vipFlags)

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]