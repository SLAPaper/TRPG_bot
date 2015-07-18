import random, os

def roll(query):
    # d = 1#1d20+0
    # [times'#'][count]'d'[faces]['+'addend]' '[description]
    try:
        def f(s):
            if s.isnumeric():
                return int(s)
            else:
                return 1
        front, back = query.split('d', maxsplit=2)
        
        if '#' in front:
            times, count = map(f, front.split('#'))
        elif front.isnumeric():
            times = 1
            count = int(front)
        else:
            times = 1
            count = 1
        
        if ' ' in back:
            back2, description = back.split(maxsplit=2)
        else:
            back2 = back
            description = None
        
        if '+' in back2:
            faces, addend = map(f, back2.split('+'))
        elif back2.isnumeric():
            faces = int(back2)
            addend = 0
        else:
            faces = 20
            addend = 0
        result = []
        for i in range(times):
            dice_sum = 0
            for j in range(count):
                dice_sum += random.randrange(faces)
            dice_sum += addend
            result.append(dice_sum)
        return tuple(result)
    except:
        return (random.randrange(20) + 1,)

while True:
    query = input("请输入roll命令，形如“5#3d6+8”，如果错误会输出1d20。按Ctrl+C退出。\n")
    if len(query) == 0:
        break
    print(roll(query))
os.system("pause")