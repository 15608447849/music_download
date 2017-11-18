import os
import re
from apis.internals import WYYINC
from sys import stdin
from beans.download import downloadTask

class console_controller:
    def __init__(self,res_dirs):

        if not os.path.exists(res_dirs):
            os.mkdir(res_dirs)
        self.res_dirs = res_dirs
        self.minc = WYYINC()
        self.TF = '='*15
        self.TR = '\n>>'
        self.actions ={
            '0': lambda :self._search_hot(self.input_key()),
            '1': lambda :self._search_songs(self.input_key()),
            '2': lambda :self._search_mv(self.input_key()),
            '3': lambda :self._search_sq(self.input_key()),
            'b':lambda :os._exit(0),
            'c':lambda :os.system('cls'),
            'mv':self.mvs,
            'sg':self.songs,
            'sq':self.sq
        }

    # 等待控制台输入
    def _input(self):
        return stdin.readline().strip('\n')

    def input_key(self):
        print("#请输入关键字", end=self.TR)
        return self._input()

    #热门搜索
    def _search_hot(self,value):
        json = self.minc.search_hot(key=value)
        if json :
            order = json['result']['order']
            for it in order:
                its = json['result'][it]
                if it in {'mvs','songs'}:
                    print('(%s) :' % it)
                    for its_it in its:
                        print('\t', 'id:', its_it['id'], '\t','info:', its_it['name'],end='\t')
                        if 'artists' in its_it:
                            artists = its_it['artists']
                            stem = ''
                            for sit in artists:
                                stem+=sit['name']+'/'
                            stem=stem[:len(stem)-1]
                            print(stem,end='\t')
                        if 'alia' in its_it:
                            print(its_it['alia'][0],end='\t')
                        if 'artisName' in its_it:
                            print(its_it['artisName'],end='\t')
                        if 'briefDesc' in its_it:
                            print(its_it['briefDesc'],end='\t')
                        print()
            print("\n")
        else:
            print('获取服务器信息失败.')


    #单曲查询
    def _search_songs(self, key):
        #初始化数据
        index = 0
        limit = 100
        json = self.minc.search_songs(key,index,limit)
        if json is not None and json['code'] == 200:
            count = json['result']['songCount']
            songs = json['result']['songs']
            list = []
            list.append(songs)
            if(count>limit):
                i = count % limit
                sunIndex = int(count / limit)
                if i > 0:
                    sunIndex+=1
                index = 1
                while(index<sunIndex):
                    json = self.minc.search_songs(key, index, limit)
                    if json is not None and json['code'] == 200:
                        songs = json['result']['songs']
                        list.append(songs)
                    index+=1
            map={}
            info = 'songs id:%s,\tmvs id :%s,\t%s,\t%s,\t%s'
            for songs in list:
                for it in songs:
                    privilege = it['privilege']
                    if privilege['pl'] == 0:
                        continue
                    name = it['name']
                    id = it['id']
                    mv = it['mv']
                    al = ' '
                    if 'al' in it:
                        al = it['al']['name']
                    ar_str = ' '
                    if 'ar' in it:
                        ar = it['ar']
                        for s in ar:
                            ar_str += s['name']+'/'
                        ar_str = ar_str[:len(ar_str)-1]
                    if id not in map:
                        map[id] = info % (str(id), str(mv), name, ar_str, al)

                for id in map:
                    print(map[id])
        print("\n")

    #MV查询
    def _search_mv(self, key):
        index = 0
        limit = 15
        json = self.minc.search_mv(key, index, limit)
        if json is not None and json['code'] == 200:
            count = json['result']['mvCount']
            mvs = json['result']['mvs']
            list = []
            list.append(mvs)
            if (count > limit):
                i = count % limit
                sunIndex = int(count / limit)
                if i > 0:
                    sunIndex += 1
                index = 1
                while (index < sunIndex):
                    json = self.minc.search_mv(key, index, limit)
                    if json is not None and json['code'] == 200:
                        mvs = json['result']['mvs']
                        list.append(mvs)
                    index += 1

            info = 'mvs id :%s,\t%s,\t%s,\t%s'
            map={}
            for mvs in list:
                for it in mvs:
                    name = it['name']
                    briefDesc = it['briefDesc']
                    id = it['id']
                    artists = it['artists']
                    artists_str=''
                    for s in  artists:
                        artists_str+=s["name"]+'/'
                    artists_str = artists_str[:len(artists_str)-1]
                    if id not in map:
                        map[id] = info % (str(id),name,artists_str,briefDesc)

            for id in map:
                print(map[id])
        print("\n")

    #无损音乐查询
    def _search_sq(self, key):
        json = self.minc.search_sq_songs(key)
        if json is not None and 'data' in json:
            data = json['data']
            if 'song' in data:
                song = data['song']
                info = 'sq id:%s,\t%s,\t%s'
                for it in song:
                    songid = it['songid']
                    songname = it['songname']
                    artistname = it['artistname']
                    json = self.minc.sqInfo(songid)
                    if json is not None and json['errorCode'] == 22000:
                        songList = json['data']['songList']
                        for it in songList:
                            format = it['format']
                            showLink = it['showLink']
                            if format is not '' and showLink is not '':
                                print(info % (songid,songname,artistname))
        print("\n")

    #下载MV
    def mvs(self,id):
        json = self.minc.mvInfo(id)
        if json is not None and json["code"] == 200:
            mv_urls = json['data']['brs']
            mv_name = json['data']['name']
            print(mv_name, '\t', json['data']['artistName'], '\t', json['data']['desc'])
            for it in mv_urls:
                # print(" %s - %s " % (it, mv_urls[it]))
                print("p\t%s " % (it))
            print("#请选择(输入p),返回(b)", end=self.TR)
            value = self._input()
            if value == 'b':
                return False
            url = mv_urls[value]
            file_name = mv_name + '-' + value + 'p.mp4'
            path = self.res_dirs + '/mv'
            print("#指定下载目录,直接回车使用默认目录[%s] , 返回(b)" % path, end=self.TR)
            value = self._input()
            if value == 'b':
                return
            if len(value) > 0:
                path = value
            downloadTask(path, file_name, url)
        else:
            print('获取服务器信息失败.')
    #下载单曲
    def songs(self,id):
        json = self.minc.songsInfo(id)
        if json is not None and json["code"] == 200:
            songs_info = json['songs'][0]
            privileges_info = json['privileges'][0]

            urls = {}
            self._songsDownloadLink(id, privileges_info['maxbr'], urls)
            if 'h' in songs_info:
                self._songsDownloadLink(id, songs_info['h']['br'], urls)
            if 'm' in songs_info:
                self._songsDownloadLink(id, songs_info['m']['br'], urls)
            if 'l' in songs_info:
                self._songsDownloadLink(id, songs_info['l']['br'], urls)
            if (len(urls) == 0):
                print("无法获取下载连接.")
                return
            name = songs_info["name"]
            ar = songs_info['ar']
            ar_str = ''
            for it in ar:
                ar_str += it['name']+'/'
            ar_str = ar_str[:len(ar_str)-1]
            al = songs_info['al']['name']
            print('单曲下载: <%s>\t歌手:%s\t专辑:%s ' % (name, ar_str, al))
            for it in urls:
                # print("br value : %s - %s" % (it,urls[it]))
                print("br:\t %s " % (it))

            print("#请选择(输入br),返回(b)", end=self.TR)
            value = self._input()
            if value == 'b':
                return
            url = urls[int(value)]
            file_name = name + '-(' + value + ').mp3'
            path = self.res_dirs + '/music'
            print("#指定下载目录,直接回车使用默认目录[%s] , 返回(b)" % path, end=self.TR)
            value = self._input()
            if value == 'b':
                return
            if len(value) > 0:
                path = value
            downloadTask(path, file_name, url)
        else:
            print('获取服务器信息失败.')
    #单曲下载链接
    def _songsDownloadLink(self, id, brs,urls):
       json = self.minc.songsLink(id,brs)
       if json is not None and json["code"] == 200:
            br = json['data'][0]['br']
            url = json['data'][0]['url']
            if  br not in urls and br>0:
                 urls[br] = url
    #下载无损音乐
    def sq(self,id):
            json = self.minc.sqInfo(id)
            if json is not None and json['errorCode'] == 22000:
                songList = json['data']['songList']
                for it in songList:
                    format = it['format']
                    showLink = it['showLink']
                    if format is '' and showLink is '':
                        print('无法获取指定无损音乐下载地址.')
                        return
                    songName  = it['songName']
                    path = self.res_dirs + '/sqmusic'
                    print("准备下载无损音乐 - %s , %s" %( songName,it['artistName']))
                    print("#指定下载目录,直接回车使用默认目录[%s] , 返回(b)" % path, end=self.TR)
                    value = self._input()
                    if value == 'b':
                        return
                    if len(value) > 0:
                        path = value
                    downloadTask(path, songName+'.'+format, showLink)
            else:
                print('获取服务器信息失败.')


    #循环控制台
    def loop(self):
        while True:
            try:

                print(self.TF,'选项',self.TF)
                print("\t0\t模糊查询\n"
                      "\t1\t单曲查询\n"
                      "\t2\tMV查询\n"
                      "\t3\t无损音乐查询\n"
                      "\tb\t退出\n"
                      "\tc\t清屏\n"
                      "\tsg 'id'\t下载指定单曲\n"
                      "\tmv 'id'\t下载指定MV\n"
                      "\tsq 'id'\t下载指定无损音乐\n",end=self.TR)
                command = self._input()
                self.option(command)

            except Exception as e:
                print(e)

    def option(self,command):
        value = re.sub('\s+', '#', command)
        arr = value.split('#')
        if len(arr) >=1 and arr[0] in self.actions:
            func = self.actions[arr[0]]
            if len(arr)==2:
                func(arr[1])
            else:
                func()













