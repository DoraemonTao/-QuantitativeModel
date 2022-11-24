# Alarm相关的配置文件

FLAG_STANDLONE = 1<<0
FLAG_WAKE_FROM_IDLE = 1<<1
FLAG_ALLOW_WHILE_IDLE = 1 << 2
FLAG_ALLOW_WHILE_IDLE_UNRESTRICTED= 1<<3
FLAG_IDLE_UNTIL = 1<<4

# Flag for alarms: Used to provide backwards compatibility for apps with targetSdkVersion less
FLAG_ALLOW_WHILE_IDLE_COMPAT = 1 << 5;

# Index for Alarm Policy
# Nowadays we only import idle policy
REQUESTER_POLICY_INDEX = 0
DEVICE_IDLE_POLICY_INDEX = 1

if __name__ == '__main__':
    print(FLAG_IDLE_UNTIL)