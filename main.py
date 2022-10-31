from util.Parse import extract_screen, extract_time, Parse


def parse_txt(BatteryState):
    f = open(BatteryState,encoding = "utf-8")
    fileContent=f.readlines()
    f.close()
    return fileContent




if __name__ == '__main__':
    battery_txt = r"data/result.log"
    fileContent=parse_txt(battery_txt)
    parse = Parse(fileContent);
    parse.parseLines();
    mAlarm = parse.getAlarmStore()
    mJob = parse.getJobStore()
    # TODO:将alarm和job放入idle状态中更新