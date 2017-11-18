import os
from contextlib import closing

import re
import requests
from beans.progress import ProgressBar

class downloadTask:
    def string_filter(self,str_v):
        # r1 = u'[’!"#$%&\'*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^`{|}~]+'
        r1 = u'[#?*:"<>|，。?★、…【】《》？“”‘’！]+'
        r2 = u'[\\\\\/]+'
        # r2 = u'\s+'
        str_v = re.sub(r1, ' ', str_v)  # 过滤内容中的各种标点符号
        str_v = re.sub(r2, '_', str_v)  # 过滤内容中的各种标点符号
        # str_v = re.sub(r2, '_', str_v)  # 过滤内容中的各种标点符号
        return str_v.rstrip()

    def __init__(self,path,file_name,url,chunk_size = 1024,):

        path = path.replace('\\','/')
        file_name =self.string_filter(file_name)
        if not path.endswith('/') :
            path  = path +'/'
        if not os.path.exists(path):
            os.mkdir(path)
        print("连接数据中,请等待...")
        with closing(requests.get(url, stream=True)) as response:
            content_size = int(response.headers['content-length'])  #内容体总大小
            progress = ProgressBar(file_name,
                                   total=content_size,
                                   unit="Mb",
                                   chunk_size=1024*1024,
                                   run_status="正在下载",
                                   finish_status="下载完成")
            with open(path+file_name, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(len(data))
