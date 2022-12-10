import csv

import pandas as pd
import ast

# input_file = '../data/batterystats.csv'
input_file = 'data/batterystats.csv'
output_file = 'data/op.csv'
dict_uid = {}
stop_item = ['vers', 'uid', 'apk', 'wua', 'st', 'wl', 'awl', 'sy', 'jb', 'jbc', 'jbd', 'wr', 'pwi', 'rpm', 'fg', 'fgs',
             'jbd', 'kwl', 'wr', 'ua', 'lv', 'hsp', 'h', 'sgc', 'dcc', 'wsc', 'wssc', 'wsgc', 'pws', 'dsd', 'csd', 'gcf'
             , 'ctf', 'bt', 'dc', 'm', 'gn', 'br', 'sgt', 'sst', 'dst', 'wst', 'wwst', 'wsgt', 'dtr', 'ctr', 'wmc', 'nt'
            , 'wmct']
# stop_item = []
time_dict = {'pr': [5, 6], 'cpu': [4, 5], 'sr': [5], 'vib': [4], 'gwfl': [4], 'wfl': [12], 'gwfcd': [4], 'wfcd': [4],
             'gble': [4], 'ble': [4], 'blem': [4], 'gmcd': [4], 'mcd': [4], 'fla': [4], 'cam': [4], 'vid': [4], 'aud': [4]}


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
    dataframe.to_csv('test2_op.csv', sep=',', index=False)
    return output


def hc_query(u1, u2):
    df_q = pd.read_csv('test2_op.csv', header=0, lineterminator='\n')
    df1, df2 = df_q[df_q['uid'] == u1], df_q[df_q['uid'] == u2]
    temp_lst1, temp_lst2 = list(df1['hardware component']), list(df2['hardware component'])
    lst1, lst2 = [], []
    for item in temp_lst1:
        lst1 = ast.literal_eval(item)
    for item in temp_lst2:
        lst2 = ast.literal_eval(item)
    print(lst1)
    print(lst2)
    lst3 = set(lst1 + lst2)  # 15
    len1 = len(lst3)  # 15
    len2 = len(lst1) + len(lst2) - len1  # 9
    return len2 / len1


def hc_query_prime(lst1, lst2):
    lst3 = set(lst1 + lst2)  # 15
    len1 = len(lst3)  # 15
    len2 = len(lst1) + len(lst2) - len1  # 9
    return len2 / len1


def hardware_component_plus():
    df_h = data_frame
    # print(df_h)
    output = {}  # {cpu:{1000:2304, 10024:4901}, wifi:[]..... hardware:[uid,time]}
    hardware = {}
    for index, row in df_h.iterrows():
        if not str(row[1]).isdigit():
            continue
        if int(row[1]) < 1000:
            continue
        if row[3] in stop_item:
            continue
        time = 0
        for item in time_dict[row[3]]:
            # print(item)
            time += int(row[item])
            if time == 0:
                time = 1
        tmp_list = [row[3], time]

        if row[1] in output.keys():
            if row[3] not in hardware[row[1]]:
                output[row[1]].append(tmp_list)
                hardware[row[1]].append(row[3])
            else:
                for item in output[row[1]]:
                    if item[0] == row[3]:
                        item[1] += time
        else:
            output[row[1]] = [tmp_list]
            hardware[row[1]] = [row[3]]

    dataframe = pd.DataFrame({'uid': list(output.keys()), 'hardware component': list(output.values())})
    dataframe.to_csv(output_file, sep=',', index=False)
    return output


def hc_query_plus(u1, u2):
    df_q = pd.read_csv(output_file, header=0, lineterminator='\n')
    df1, df2 = df_q[df_q['uid'] == u1], df_q[df_q['uid'] == u2]
    temp_lst1, temp_lst2 = list(df1['hardware component']), list(df2['hardware component'])
    lst1, lst2 = [], []

    for item in temp_lst1:
        lst1 = ast.literal_eval(item)
    for item in temp_lst2:
        lst2 = ast.literal_eval(item)
    # print(lst1)
    # print(lst2)
    lst1 = dict(lst1)
    lst2 = dict(lst2)
    time1, time2 = 0, 0
    for item in lst1.values():
        time1 += item
    for item in lst2.values():
        time2 += item
    total_hardware = set(list(lst1.keys()) + list(lst2.keys()))

    for item in lst1.keys():
        lst1[item] /= time1
    for item in lst2.keys():
        lst2[item] /= time2
    dist = 0.0
    for item in total_hardware:
        if item in lst1.keys() and item in lst2.keys():
            dist += (lst1[item] - lst2[item])**2
        elif item in lst1.keys():
            dist += lst1[item]**2
        else:
            dist += lst2[item]**2
    return 1/dist


def hc_query_plus_prime(lst1, lst2):
    lst1 = dict(lst1)
    lst2 = dict(lst2)
    time1, time2 = 0, 0
    for item in lst1.values():
        time1 += item
    for item in lst2.values():
        time2 += item
    total_hardware = set(list(lst1.keys()) + list(lst2.keys()))

    for item in lst1.keys():
        lst1[item] /= time1
    for item in lst2.keys():
        lst2[item] /= time2
    dist = 0.0
    for item in total_hardware:
        if item in lst1.keys() and item in lst2.keys():
            dist += (lst1[item] - lst2[item])**2
        elif item in lst1.keys():
            dist += lst1[item]**2
        else:
            dist += lst2[item]**2
    if dist == 0:
        return 0
    return 1/dist

# 得到组件信息信息
def get_uid_hardware():
    return hardware_set

def get_uid_hardware_time_set():
    return  hardware_time_set

if __name__ == '__main__':
    col_names = [i for i in range(0, 120)]
    data_frame = pd.read_csv('../data/batterystats.csv', header=None, names=col_names, lineterminator="\n",encoding="UTF16")
    output_file = '../data/op.csv'
    hardware_set = hardware_component()
    hardware_time_set = hardware_component_plus()
    get_uid_hardware_time_set()

    print(hc_query_plus(10102, 1000))

    test_l1 = [['wfcd', 0], ['cpu', 7179], ['pr', 1390]]
    test_l2 = [['mcd', 0], ['wfl', 27040], ['wfcd', 0], ['vid', 510], ['sr', 14827794], ['cpu', 8911423],
               ['pr', 8957580]]

    print(hc_query_plus_prime(test_l1, test_l2))

    test_l3 = ['wfcd', 'cpu', 'pr']
    test_l4 = ['mcd', 'wfl', 'wfcd', 'vid', 'sr', 'cpu', 'pr']
    print(hc_query(10102, 1000))
    print(hc_query_prime(test_l3, test_l4))


col_names = [i for i in range(0, 120)]
data_frame = pd.read_csv(input_file, header=None, names=col_names, lineterminator="\n",encoding="UTF16")
hardware_set = hardware_component()
hardware_time_set = hardware_component_plus()
get_uid_hardware_time_set()
