from util.Constant import *
from alarm.AlarmManager import *

# 延长alarm的周期
def delivery_time_delay(alarms):
    for alarm in alarms:
        if alarm.repeatInterval != 0 and alarm.repeatInterval > alarm.windowLength:
            if alarm.mMaxWhenElapsed < alarm.mWhenElapsed + alarm.repeatInterval * DELAY_PERCENTAGE:
                alarm.mMaxWhenElapsed = alarm.mWhenElapsed + alarm.repeatInterval * DELAY_PERCENTAGE
        if alarm.windowLength != 0 :
            if alarm.mMaxWhenElapsed < alarm.getWhenElapsed() + alarm.windowLength * 1:
                alarm.mMaxWhenElapsed = alarm.getWhenElapsed() + alarm.windowLength * 1




