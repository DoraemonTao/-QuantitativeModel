from extractInfo import extract_screen, extract_time


def parse_txt(BatteryState):
    f = open(BatteryState,encoding = "utf-8")
    fileContent=f.readlines()
    f.close()
    return fileContent




if __name__ == '__main__':
    battery_txt = r"C:\Users\Tao\PycharmProjects\AnalyzeModule\bugreport\bugreport-PDPT00-RKQ1.200710.002-2022-09-18-09-53-22.txt"
    fileContent=parse_txt(battery_txt)
    print(extract_time(extract_screen(fileContent)))