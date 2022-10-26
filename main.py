from util.Parse import extract_screen, extract_time


def parse_txt(BatteryState):
    f = open(BatteryState,encoding = "utf-8")
    fileContent=f.readlines()
    f.close()
    return fileContent




if __name__ == '__main__':
    battery_txt = r"data/result.txt"
    fileContent=parse_txt(battery_txt)
    print(extract_time(extract_screen(fileContent)))