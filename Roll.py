import os
from bot_utility import roll

while True:
    query = input("请输入roll命令，形如“5#3d6+8”，如果错误会输出1d20。直接回车退出。\n")
    if len(query) == 0:
        break
    print(roll(query))
os.system("pause")