import csv

import pandas as pd
import ast

# input_file = '../data/batterystats.csv'
input_file = 'data/batterystats.csv'
output_file = 'data/op.csv'
dict_uid = {}
stop_item = ['vers', 'uid', 'apk', 'wua', 'st', 'wl', 'awl', 'sy', 'jb', 'jbc', 'jbd', 'wr', 'pwi']


def hardware_component():
    df_h = data_frame
    # print(df_h)
    output = {}

    for index, row in df_h.iterrows():
        if not str(row[1]).isdigit():
            continue
        if int(row[1]) < 1000:
            continue
        if row[3] in stop_item:
            continue
        if row[1] in output.keys():
            if row[3] not in output[row[1]]:
                output[row[1]].append(row[3])
        else:
            output[row[1]] = [row[3]]

    dataframe = pd.DataFrame({'uid': list(output.keys()), 'hardware component': list(output.values())})
    dataframe.to_csv(output_file, sep=',', index=False)
    return output


def hc_query(u1, u2):
    df_q = pd.read_csv(output_file, header=0, lineterminator='\n')
    df1, df2 = df_q[df_q['uid'] == u1], df_q[df_q['uid'] == u2]
    temp_lst1, temp_lst2 = list(df1['hardware component']), list(df2['hardware component'])
    lst1, lst2 = [], []
    for item in temp_lst1:
        lst1 = ast.literal_eval(item)
    for item in temp_lst2:
        lst2 = ast.literal_eval(item)
    lst3 = set(lst1 + lst2)  # 15
    len1 = len(lst3)  # 15
    len2 = len(lst1) + len(lst2) - len1  # 9
    return len2 / len1

def get_hardware_similarity(lst1, lst2):

    lst3 = set(lst1 + lst2)  # 15
    len1 = len(lst3)  # 15
    len2 = len(lst1) + len(lst2) - len1  # 9
    if len1 == 0:
        return 0
    return len2 / len1


# 得到组件信息信息
def get_uid_hardware():
    return hardware_set

if __name__ == '__main__':
    col_names = [i for i in range(0, 120)]
    data_frame = pd.read_csv('../data/batterystats.csv', header=None, names=col_names, lineterminator="\n",encoding="UTF16")
    output_file = '../data/op.csv'
    hardware_component()
    print(hc_query(1020, 1000))


col_names = [i for i in range(0, 120)]
data_frame = pd.read_csv(input_file, header=None, names=col_names, lineterminator="\n",encoding="UTF16")
hardware_set = hardware_component()

