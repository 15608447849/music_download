import os

from beans.controller import console_controller
if __name__ == '__main__':
    root_path = os.path.abspath('./res').replace("\\", "/")

    # 控制访问对象
    contro = console_controller(root_path)
    contro.loop()
        
        
        