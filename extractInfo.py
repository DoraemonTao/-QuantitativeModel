import re




# 提取屏幕状态
def extract_screen(lines):
    ScreenContentPattern = re.compile('(-screen )|( \+screen )')
    battery_histories = []
    flag = False
    for line in lines:

        if ('DUMP OF SERVICE batterystats:' in line):
            flag = True
        if (flag):
            content = None
            content = ScreenContentPattern.search(line)
            if (content):
                battery_histories.append(line)

    return battery_histories


# 根据内容提取出时间
def extract_time(screen_contents):
    OnScreenStatePattern = re.compile(' \+screen ')
    OffScreenStatePattern = re.compile(' \-screen ')
    TimePattern = re.compile(' \+\d+h\d+m\d+s\d+ms')

    # 记录着休眠时间段
    screen_state = []
    off_screen_time = 0

    #  取每行内容
    for content in screen_contents:
        screen_flag = None
        screen_flag = OnScreenStatePattern.search(content)
        if (screen_flag):
            # 第一次的是亮屏状态
            OnScreenTime = TimePattern.search(content).group(0)
        else:
            off_screen_time = TimePattern.search(content).group(0)

        if (screen_flag):
            screen_state.append([off_screen_time, OnScreenTime])



    return screen_state


# 提取出idle状态的
def extract_idle(lines):
    IdleContentPattern = re.compile('device_idle=')
    # 记录着idle时间段
    idle_histories = []
    flag = False
    for line in lines:

        if ('DUMP OF SERVICE batterystats:' in line):
            flag = True
        if (flag):
            content = None
            content = IdleContentPattern.search(line)
            if (content):
                idle_histories.append(line)

    return idle_histories

def extract_idle(idle_contents):
    OnIdleStatePattern = re.compile('device_idle=full')
    TimePattern = re.compile(' \+\d+h\d+m\d+s\d+ms')

    # 记录着休眠时间段
    idle_state = []
    off_idle_time = 0

    #  取每行内容
    for content in idle_contents:
        idle_flag = None
        idle_flag = OnIdleStatePattern.search(content)
        if (idle_flag):
            OnIdleTime = TimePattern.search(content).group(0)
        else:
            off_idle_time = TimePattern.search(content).group(0)

        if (idle_flag):
            idle_state.append([OnIdleTime,off_idle_time])

    return idle_state


def extra_alarm(lines):
