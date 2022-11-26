from util.Constant import *
from alarm.AlarmManager import *

# 延长alarm的周期
def delivery_time_delay(alarms):
    for alarm in alarms:
        if alarm.repeatInterval != 0 and alarm.repeatInterval > alarm.windowLength:
            if alarm.mMaxWhenElapsed < alarm.mWhenElapsed + alarm.repeatInterval * DELAY_PERCENTAGE:
                alarm.mMaxWhenElapsed = alarm.mWhenElapsed + alarm.repeatInterval * DELAY_PERCENTAGE
        if alarm.windowLength != 0 and alarm.flags != FLAG_IDLE_UNTIL:
            if alarm.mPolicyWhenElapsed[0] < alarm.enqueueTime + alarm.windowLength * 1.28:
                alarm.setPolicyElapsed(0,alarm.enqueueTime + alarm.windowLength * 1.28)




