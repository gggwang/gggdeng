#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "女团组合"
    def init(self,extend=""):
        print("============{0}============".format(extend))
        pass
    def isVideoFormat(self,url):
        pass
    def manualVideoCheck(self):
        pass
    def homeContent(self,filter):
        result = {}
        cateManual = {
            "中国女团":"中国女团4K",
"日本女团":"日本女团4K",
"韩国女团":"韩国女团4K",
"SNH48":"SNH48MV合集",
"S.H.E":"S.H.EMV合集",
"Twins":"TwinsMV合集",
"火箭少女101":"火箭少女101MV合集",
"BY2":"BY2MV合集",
"S.I.N.G":"S.I.N.GMV合集",
"3unshine":"3unshineMV合集",
"蜜蜂少女队":"蜜蜂少女队MV合集",
"七朵组合":"七朵组合MV合集",
"GNZ48":"GNZ48MV合集",
"TWICE":"TWICEMV合集",
"4MINUTE":"4MINUTEMV合集",
"EXID":"EXIDMV合集",
"KARA":"KARAMV合集",
"TARA":"TARAMV合集",
"BLACKPINK":"BLACKPINKMV合集",
"LOONA":"LOONAMV合集",
"ITZY":"ITZYMV合集",
"RedVelvet":"RedVelvetMV合集",
"Everglow":"EverglowMV合集",
"Mamamoo":"MamamooMV合集",
"少女时代":"少女时代MV合集",
"S.E.S":"S.E.SMV合集",
"FIN.K.L":"FIN.K.LMV合集",
"2NE1":"2NE1MV合集",
"WonderGirls":"WonderGirlsMV合集",
"IZ*ONE":"IZ*ONEMV合集",
"Sistar":"SistarMV合集",
"Apink":"ApinkMV合集",
"AOA":"AOAMV合集",
"GFRIEND":"GFRIENDMV合集",
"f(x)":"f(x)MV合集",
"(G)I-DLE":"(G)I-DLEMV合集",
"Itzy":"ItzyMV合集",
"Oh!GG":"Oh!GGMV合集",
"GirlCrush":"GirlCrushMV合集",
"AKB48":"AKB48MV合集",
"SKE48":"SKE48MV合集",
"NMB48":"NMB48MV合集",
"JKT48":"JKT48MV合集",
"HKT48":"HKT48MV合集",
"AKB48TeamTP":"AKB48TeamTPMV合集",
"Perfume":"PerfumeMV合集",
"桃色幸运草Z":"桃色幸运草ZMV合集",
"乃木坂46乃":"乃木坂46乃MV合集",
"樱坂46":"樱坂46MV合集",
"日向坂46":"日向坂46MV合集",
"E-girls":"E-girlsMV合集",
"NiziU":"NiziUMV合集",
"BiSH":"BiSHMV合集",
"早安少女组":"早安少女组MV合集"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name':k,
                'type_id':cateManual[k]
            })
        result['class'] = classes
        if(filter):
            result['filters'] = self.config['filter']
        return result
    def homeVideoContent(self):
        result = {
            'list':[]
        }
        return result
    cookies = ''
    def getCookie(self):
        import requests
        import http.cookies
        # 这里填cookie
        raw_cookie_line = "innersign=0;buvid3=2E536ADC-CD6D-46AB-A9FF-904395151EE369713infoc;b_nut=1669016569;i-wanna-go-back=-1;b_ut=7;_uuid=761F7F106-C575-884D-6C10A-92BC10A10D10FBC68934infoc;buvid4=5B25B999-AE15-E09A-A0CC-3661981B71BF70255-122112115-JOyWSaNZfI2kZmT1KYmcQA%3D%3D;fingerprint=6d9ef93c89a567d22b6a9c4104e6cc50;buvid_fp_plain=undefined;buvid_fp=6d9ef93c89a567d22b6a9c4104e6cc50;SESSDATA=2d6f63c8%2C1684568607%2C19eb6%2Ab1;bili_jct=21d538b01566c26afc81ff68c2ac7dca;DedeUserID=3493083203242585;DedeUserID__ckMd5=7b86f3894ed7f8c0;sid=ng0uyvaz;b_lsid=97FB69A2_1869DE8E2C5;bg_view_44176=720227"
        simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.update(simple_cookie)
        return cookie_jar
    def get_dynamic(self,pg):
        result = {}
        
        url= 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page={0}'.format(pg)
        
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['items']
            for vod in vodList:
                if vod['type'] == 'DYNAMIC_TYPE_AV':
                    ivod = vod['modules']['module_dynamic']['major']['archive']
                    aid = str(ivod['aid']).strip()
                    title = ivod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                    img =  ivod['cover'].strip()
                    remark = str(ivod['duration_text']).strip()
                    videos.append({
                        "vod_id":aid,
                        "vod_name":title,
                        "vod_pic":img,
                        "vod_remarks":remark
                    })
                result['list'] = videos
                result['page'] = pg
                result['pagecount'] = 9999
                result['limit'] = 90
                result['total'] = 999999
        return result

    def get_hot(self,pg):
        result = {}
        url= 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={0}'.format(pg)
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                img =  vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id":aid,
                    "vod_name":title,
                    "vod_pic":img,
                    "vod_remarks":remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result
    def get_rank(self):
        result = {}
        url= 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                img =  vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id":aid,
                    "vod_name":title,
                    "vod_pic":img,
                    "vod_remarks":remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result
    def categoryContent(self,tid,pg,filter,extend):	
        result = {}
        if tid == "热门":
            return self.get_hot(pg=pg)
        if tid == "排行榜" :
            return self.get_rank()
        if tid == '动态':
            return self.get_dynamic(pg=pg)
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}'.format(tid,pg)
        if len(self.cookies) <= 0:
            self.getCookie()
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:			
            rspRetry = self.fetch(url,cookies=self.getCookie())
            content = rspRetry.text		
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['aid']).strip()
            title = tid + ":" + vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
            img = 'https:' + vod['pic'].strip()
            remark = str(vod['duration']).strip()
            videos.append({
                "vod_id":aid,
                "vod_name":title,
                "vod_pic":img,
                "vod_remarks":remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result
    def cleanSpace(self,str):
        return str.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
    def detailContent(self,array):
        aid = array[0]
        url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)

        rsp = self.fetch(url,headers=self.header,cookies=self.getCookie())
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        title = jo['title'].replace("<em class=\"keyword\">","").replace("</em>","")
        pic = jo['pic']
        desc = jo['desc']
        typeName = jo['tname']
        vod = {
            "vod_id":aid,
            "vod_name":title,
            "vod_pic":pic,
            "type_name":typeName,
            "vod_year":"",
            "vod_area":"bilidanmu",
            "vod_remarks":"",
            "vod_actor":jo['owner']['name'],
            "vod_director":jo['owner']['name'],
            "vod_content":desc
        }
        ja = jo['pages']
        playUrl = ''
        for tmpJo in ja:
            cid = tmpJo['cid']
            part = tmpJo['part']
            playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

        vod['vod_play_from'] = 'B站'
        vod['vod_play_url'] = playUrl

        result = {
            'list':[
                vod
            ]
        }
        return result
    def searchContent(self,key,quick):
        search = self.categoryContent(tid=key,pg=1,filter=None,extend=None)
        result = {
            'list':search['list']
        }
        return result
    def playerContent(self,flag,id,vipFlags):
        # https://www.555dianying.cc/vodplay/static/js/playerconfig.js
        result = {}

        ids = id.split("_")
        url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(ids[0],ids[1])
        rsp = self.fetch(url,cookies=self.getCookie())
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        ja = jo['durl']
        
        maxSize = -1
        position = -1
        for i in range(len(ja)):
            tmpJo = ja[i]
            if maxSize < int(tmpJo['size']):
                maxSize = int(tmpJo['size'])
                position = i

        url = ''
        if len(ja) > 0:
            if position == -1:
                position = 0
            url = ja[position]['url']

        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = {
            "Referer":"https://www.bilibili.com",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        result["contentType"] = 'video/x-flv'
        return result

    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def localProxy(self,param):
        return [200, "video/MP2T", action, ""]
