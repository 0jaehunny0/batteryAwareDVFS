import subprocess
from time import sleep
import os
import random


little_available_frequencies = [300000, 574000, 738000, 930000, 1098000, 1197000, 1328000, 1401000, 1598000, 1704000, 1803000]
mid_available_frequencies = [400000, 553000, 696000, 799000, 910000, 1024000, 1197000, 1328000, 1491000, 1663000, 1836000, 1999000, 2130000, 2253000]
big_available_frequencies = [500000, 851000, 984000, 1106000, 1277000, 1426000, 1582000, 1745000, 1826000, 2048000, 2188000, 2252000, 2401000, 2507000, 2630000, 2704000, 2802000]

little_min_freq = 300000
mid_min_freq = 400000
big_min_freq = 500000

little_max_freq = 1803000
mid_max_freq = 2253000
big_max_freq = 2802000 

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1

    return path


# set root
msg = 'adb root'
subprocess.run(msg.split(), stdout=subprocess.PIPE)


# set brightness
msg = 'adb shell settings put system screen_brightness 158'
subprocess.run(msg.split(), stdout=subprocess.PIPE)


# set battery level
""" set limit """
targetBatteryLevel = 70
msg = 'adb shell "echo '+str(targetBatteryLevel)+' > /sys/devices/platform/google,charger/charge_stop_level"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" check limit """
msg = 'adb shell cat /sys/devices/platform/google,charger/charge_stop_level'
result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
check = int(result.stdout.decode('utf-8'))
print(check)


# checking battery level
""" check current level """
msg = 'adb shell cat /sys/devices/platform/google,battery/power_supply/battery/capacity'
result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
level = int(result.stdout.decode('utf-8'))
print(level)

### when battery reaches its targer level
## if level == targetBatteryLevel:


# turn off charging
""" turn off usb charging """
msg = 'adb shell dumpsys battery set usb 0'
subprocess.run(msg.split(), stdout=subprocess.PIPE)


# turn on heater
""" check screen and unlock screen """
msg = 'adb shell dumpsys input_method | grep mInteractive=true'
result = subprocess.run(msg.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
if len(result) < 1:
    """ unlock screen """
    msg = 'adb shell input keyevent 82'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)
    sleep(0.5)
a,b = 500+random.randint(0,50), 1200+random.randint(0,100)
c,d = 500+random.randint(0,50), 400+random.randint(0,100)
msg = 'adb shell input touchscreen swipe '+str(a)+' '+str(b)+' '+str(c)+' '+str(d)
subprocess.run(msg.split(), stdout=subprocess.PIPE)
msg = 'adb shell input touchscreen swipe '+str(a)+' '+str(b)+' '+str(c)+' '+str(d)
subprocess.run(msg.split(), stdout=subprocess.PIPE)
""" start application"""
msg = 'adb shell am start -n com.sqzsoft.freeheater/com.sqzsoft.freeheater.ActivityMain'
subprocess.run(msg.split(), stdout=subprocess.PIPE)
sleep(1)
""" touch start button """
msg = 'adb shell input tap 290 2085'
subprocess.run(msg.split(), stdout=subprocess.PIPE)

# set governor
""" little """
msg = 'adb shell "echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" mid """
msg = 'adb shell "echo performance > /sys/devices/system/cpu/cpufreq/policy4/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" big """
msg = 'adb shell "echo performance > /sys/devices/system/cpu/cpufreq/policy6/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()


# set frequency
""" little """
msg = 'adb shell "echo 1197000 > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1197000 > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" mid """
msg = 'adb shell "echo 1197000 > /sys/devices/system/cpu/cpufreq/policy4/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1197000 > /sys/devices/system/cpu/cpufreq/policy4/scaling_max_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" big """
msg = 'adb shell "echo 1277000 > /sys/devices/system/cpu/cpufreq/policy6/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1277000 > /sys/devices/system/cpu/cpufreq/policy6/scaling_max_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()


# turn off cores
""" big """
msg = 'adb shell "echo 0 > /sys/devices/system/cpu/cpu6/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 0 > /sys/devices/system/cpu/cpu7/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

# logging start
""" waiting for settling """
sleep(10)
""" read a file"""
with open('logger/perfetto.txt') as f:
    msg = f.read()
result = subprocess.Popen(msg, shell=True, stderr=subprocess.PIPE).stderr.read()
""" wait for logging """
sleep(1)
print(result)

# logging result copy
""" name the new file """
fileName = str(uniquify("trace"))
""" copy """
msg = 'adb pull /data/misc/perfetto-traces/trace '+fileName
subprocess.run(msg.split(), stdout=subprocess.PIPE)
print(fileName)


# turn on cores
""" little """
# msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu0/online"'
# subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu1/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu2/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu3/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" mid """
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu4/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu5/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" big """
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu6/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu7/online"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()


# unset freqeuncy
""" little """
msg = 'adb shell "echo '+str(little_min_freq)+' > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo '+str(little_max_freq)+' > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" mid """
msg = 'adb shell "echo '+str(mid_min_freq)+' > /sys/devices/system/cpu/cpufreq/policy4/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo '+str(mid_max_freq)+' > /sys/devices/system/cpu/cpufreq/policy4/scaling_max_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" big """
msg = 'adb shell "echo '+str(big_min_freq)+' > /sys/devices/system/cpu/cpufreq/policy6/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
msg = 'adb shell "echo '+str(big_max_freq)+' > /sys/devices/system/cpu/cpufreq/policy6/scaling_max_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

# unset governor
""" little """
msg = 'adb shell "echo schedutil > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" mid """
msg = 'adb shell "echo schedutil > /sys/devices/system/cpu/cpufreq/policy4/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
""" big """
msg = 'adb shell "echo schedutil > /sys/devices/system/cpu/cpufreq/policy6/scaling_min_freq"'
subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

# turn off heater
""" touch stop button """
msg = 'adb shell input tap 790 2085'
subprocess.run(msg.split(), stdout=subprocess.PIPE)


# turn on charging
""" turn on usb charging """
msg = 'adb shell dumpsys battery set usb 1'
subprocess.run(msg.split(), stdout=subprocess.PIPE)


# lock screen
""" lock screen """
msg = 'adb shell input keyevent 26'
subprocess.run(msg.split(), stdout=subprocess.PIPE)
sleep(0.5)