class ProgressBar:
    def __init__(self,
                 title,
                 progress=0.0, #当前进度
                 run_status="进行中", #运行时状态
                 finish_status="已完成", #完成时状态
                 total=100.0, #总大小
                 unit='byte', #单位
                 sep='/',
                 chunk_size=1): #单位有关
        self.title = title
        self.total = total
        self.progress = progress
        self.chunk_size = chunk_size
        self.run_status = run_status
        self.fin_status = finish_status
        self.unit = unit
        self.seq = sep

    def __get_info(self,state):
        # 【名称】 状态 (当前进度 单位) 分割线 (总数 单位) 百分比
        _info = "【%s】%s (%.2f %s) %s (%.2f %s) %.2f%%" % (self.title,
                             state, #状态
                             self.progress / self.chunk_size,
                             self.unit,
                             self.seq,
                             self.total / self.chunk_size,
                             self.unit,
                            (self.progress / self.total )* 100)
        return _info

    def refresh(self, cur_progress):
        self.progress += cur_progress
        # if status is not None:
        end_str = "\r"
        state = self.run_status
        if self.progress >= self.total:
            end_str = '\n'
            state = self.fin_status
        print(self.__get_info(state), end=end_str)