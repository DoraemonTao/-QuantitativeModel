from matplotlib import pyplot as plt

from alarm.Alarm import Alarm


def get_alarm_windowlength(tasks):
    window_length = []
    for task in tasks:
        if isinstance(task, Alarm):
            window_length.append(task.windowLength / 60 / 1000)
    return window_length

# 绘制不同情况下的alarm窗口
def plot_alarm_window(tasks):
    thresholds = 4000
    n_bins = 4
    left_index = 0
    window_list = []
    for i in range(3):
        window_length = get_alarm_windowlength(tasks[left_index:left_index+thresholds])
        window_list.append(window_length)
        left_index = left_index+thresholds
    fig, ax = plt.subplots()
    # 实际绘图代码与单类型直方图差异不大，只是增加了一个图例项
    # 在 ax.hist 函数中先指定图例 label 名称
    ax.hist(window_list, n_bins, histtype='bar', label=["0:4000","4000:8000","8000:12000"],range = (0.01,15))
    ax.set_title('Number of times at different time intervals')
    plt.xlabel('window length(min)')
    plt.ylabel('frequence')

    # 通过 ax.legend 函数来添加图例
    ax.legend()

    plt.show()