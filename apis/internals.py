import requests
import time
from apis.music import WYYMSC_API


class WYYINC:
    def __init__(self):
        self.api = WYYMSC_API()
        self.header = {
            'Accept': '*/*',
            'Host': 'music.163.com',
            'User-Agent': 'curl/7.51.0',
            'Referer': 'http://music.163.com/',
            'Cookie': 'appver=2.0.2'
        }

    # POST - 访问网络 - 重试三次
    def requistInternet(self, url, list, count=0):
        resp = None
        try:
            index = count + 1 if count < 1 else 1
            count = index
            # print('第%d次' % count,'尝试访问:%s' % url ,'参数:', list)
            r = self.api.encrypt(list)
            data = {
                'params': r['encText'],
                'encSecKey': r['encSecKey']
            }
            resp = requests.post(url=url, headers=self.header, data=data)
            code = resp.status_code if resp is not None else -1
            if code == 200:
                # print(resp.content.decode("UTF-8"))
                return resp.json()
            raise Exception('response code:', code)
        except Exception as e:
            # print(e)
            if count <= 3:
                # print("一秒后重试...")
                time.sleep(1)
                return self.requistInternet(url, list, count)
            else:
                return None
        finally:
            if resp:
                resp.close()


    #get - 访问网络 - 重试三次
    def requistInternetByGet(self,url,count=0):
        resp = None
        try:
            index = count+1 if count<1 else 1
            count = index
            # print('第%d次' % count,'尝试访问:%s' % url ,'参数:', list)
            resp = requests.get(url=url)
            code = resp.status_code if resp is not None else -1
            if code == 200:
                # print(resp.content.decode("UTF-8"))
                return resp.json()
            raise Exception('response code:', code)
        except Exception as e:
            # print(e)
            if count <= 3:
                #print("一秒后重试...")
                time.sleep(1)
                return self.requistInternet(url, list,count)
            else:
                return None
        finally:
            if resp :
                resp.close()


    # 热门查询
    def search_hot(self, key):
        url, list = self.api.search(key)
        return self.requistInternet(url, list)
    #获取指定MV 信息
    def mvInfo(self, id):
        url,list = self.api.target_mv_info(id)
        return self.requistInternet(url, list)
    #获取指定歌曲信息
    def songsInfo(self, id):
        url, list = self.api.target_songs_info(id)
        return self.requistInternet(url, list)
    #获取指定歌曲的下载链接
    def songsLink(self, id, brs):
        url, list = self.api.target_songs_downloadlink(id,brs)
        return self.requistInternet(url, list)
    #查询单曲信息
    def search_songs(self, key, index, limit):
        url, list = self.api.search(key, 1,index,limit)
        return self.requistInternet(url, list)
    #查询MV信息
    def search_mv(self, key, index, limit):
        url, list = self.api.search(key, 1004, index, limit)
        return self.requistInternet(url, list)

    def search_sq_songs(self, key):
        url = self.api.search_sq(key)
        return self.requistInternetByGet(url)

    def sqInfo(self, id):
        url = self.api.search_sq_songid(id)
        return self.requistInternetByGet(url)

