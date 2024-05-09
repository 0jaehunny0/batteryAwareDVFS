import subprocess
from time import sleep
import os
import random
import numpy as np
import pickle

little_available_frequencies = [300000, 574000, 738000, 930000, 1098000, 1197000, 1328000, 1401000, 1598000, 1704000, 1803000]
mid_available_frequencies = [400000, 553000, 696000, 799000, 910000, 1024000, 1197000, 1328000, 1491000, 1663000, 1836000, 1999000, 2130000, 2253000]
big_available_frequencies = [500000, 851000, 984000, 1106000, 1277000, 1426000, 1582000, 1745000, 1826000, 2048000, 2188000, 2252000, 2401000, 2507000, 2630000, 2704000, 2802000]

little_min_freq = 300000
mid_min_freq = 400000
big_min_freq = 500000

little_max_freq = 1803000
mid_max_freq = 2253000
big_max_freq = 2802000 

trial = 2

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1
    return path

def set_root(): 
    msg = 'adb root'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)

def set_brightness(level):
    msg = 'adb shell settings put system screen_brightness '+str(level)
    subprocess.run(msg.split(), stdout=subprocess.PIPE)

def set_limit_battery_level(level):
    msg = 'adb shell "echo '+str(level)+' > /sys/devices/platform/google,charger/charge_stop_level"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

def get_limit_battery_level():
    msg = 'adb shell cat /sys/devices/platform/google,charger/charge_stop_level'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
    return int(result.stdout.decode('utf-8'))
    
def get_battery_level():
    msg = 'adb shell cat /sys/devices/platform/google,battery/power_supply/battery/capacity'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
    return int(result.stdout.decode('utf-8'))

def turn_off_usb_charging():
    msg = 'adb shell dumpsys battery set usb 0'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)

def turn_on_usb_charging():
    msg = 'adb shell dumpsys battery set usb 1'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)

def turn_on_screen():
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

def turn_off_screen():
    """ check screen and lock screen """
    msg = 'adb shell dumpsys input_method | grep mInteractive=true'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
    if len(result) > 1:
        """ lock screen """
        msg = 'adb shell input keyevent 26'
        subprocess.run(msg.split(), stdout=subprocess.PIPE)
        sleep(0.5)

def turn_on_heater(level):
    """ start application"""
    msg = 'adb shell am start -n com.sqzsoft.freeheater/com.sqzsoft.freeheater.ActivityMain'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)
    sleep(0.5)
    """ touch heating degree button """
    if level == 'low':
        msg = 'adb shell input tap 80 1835'
        subprocess.run(msg.split(), stdout=subprocess.PIPE)
    elif level == 'medium':
        msg = 'adb shell input tap 400 1835'
        subprocess.run(msg.split(), stdout=subprocess.PIPE)
    else:
        msg = 'adb shell input tap 765 1835'
        subprocess.run(msg.split(), stdout=subprocess.PIPE)
    sleep(0.5)
    """ touch start button """
    msg = 'adb shell input tap 290 2085'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)

def turn_off_heater():
    """ touch stop button """
    msg = 'adb shell input tap 790 2085'
    subprocess.run(msg.split(), stdout=subprocess.PIPE)    

def set_governor(governor):
    """ little """
    msg = 'adb shell "echo '+governor+' > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    """ mid """
    msg = 'adb shell "echo '+governor+' > /sys/devices/system/cpu/cpufreq/policy4/scaling_governor"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    """ big """
    msg = 'adb shell "echo '+governor+' > /sys/devices/system/cpu/cpufreq/policy6/scaling_governor"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

def set_frequency(little_min, little_max, mid_min, mid_max, big_min, big_max):
    """ little """
    msg = 'adb shell "echo '+str(little_min)+' > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(little_max)+' > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    """ mid """
    msg = 'adb shell "echo '+str(mid_min)+' > /sys/devices/system/cpu/cpufreq/policy4/scaling_min_freq"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(mid_max)+' > /sys/devices/system/cpu/cpufreq/policy4/scaling_max_freq"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    """ big """
    msg = 'adb shell "echo '+str(big_min)+' > /sys/devices/system/cpu/cpufreq/policy6/scaling_min_freq"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(big_max)+' > /sys/devices/system/cpu/cpufreq/policy6/scaling_max_freq"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

def unset_frequency():
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

def set_cores(cpu0, cpu1, cpu2, cpu3, cpu4, cpu5, cpu6, cpu7):
    # msg = 'adb shell "echo 1 > /sys/devices/system/cpu/cpu0/online"'
    # subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(cpu1)+' > /sys/devices/system/cpu/cpu1/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(cpu2)+' > /sys/devices/system/cpu/cpu2/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(cpu3)+' > /sys/devices/system/cpu/cpu3/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    """ mid """
    msg = 'adb shell "echo '+str(cpu4)+' > /sys/devices/system/cpu/cpu4/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(cpu5)+' > /sys/devices/system/cpu/cpu5/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    """ big """
    msg = 'adb shell "echo '+str(cpu6)+' > /sys/devices/system/cpu/cpu6/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = 'adb shell "echo '+str(cpu7)+' > /sys/devices/system/cpu/cpu7/online"'
    subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE).stdout.read()

def start_logging():
    """ waiting for settling """
    sleep(10)
    """ read the perfetto script file"""
    with open('logger/perfetto.txt') as f:
        msg = f.read()
    result = subprocess.Popen(msg, shell=True, stderr=subprocess.PIPE).stderr.read()
    sleep(1)
    print(result)

def file_name_generator(battery_level, core, freq, onoff):
    prop = "trace_" + str(battery_level) + "_" + core + "_" + str(freq) + "_" + onoff
    fileName = str(uniquify(prop))
    return fileName

def copy_log(fileName):
    msg = 'adb pull /data/misc/perfetto-traces/trace '+fileName
    subprocess.run(msg.split(), stdout=subprocess.PIPE)
    print(fileName)

def get_battery_voltage():
    msg = 'adb shell cat /sys/class/power_supply/battery/voltage_now'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
    voltage_now = int(result.stdout.decode('utf-8'))
    msg = 'adb shell cat /sys/class/power_supply/battery/voltage_avg'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
    voltage_avg = int(result.stdout.decode('utf-8'))
    return [voltage_now, voltage_avg]

def get_battery_resistance():
    msg = 'adb shell cat /sys/class/power_supply/battery/resistance'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
    resistance = int(result.stdout.decode('utf-8'))
    msg = 'adb shell cat /sys/class/power_supply/battery/resistance_avg'
    result = subprocess.run(msg.split(), stdout=subprocess.PIPE)
    resistance_avg = int(result.stdout.decode('utf-8'))
    return [resistance, resistance_avg]


def save_pickle(fileName, value):
    with open(fileName+'.pkl', 'wb') as f:
    	pickle.dump(value, f, protocol=pickle.HIGHEST_PROTOCOL)

def tester(target_freq, core, targetBatteryLevel):
    while True:
        battery_level = get_battery_level()
        print(battery_level)

        if battery_level > targetBatteryLevel:
            turn_off_usb_charging()
            turn_on_screen()
            turn_on_heater("medium")
            print("battery_level > targetBatteryLevel")
        elif battery_level < targetBatteryLevel:
            turn_on_usb_charging()
            turn_on_screen()
            turn_off_heater()
            turn_off_screen()
            print("battery_level < targetBatteryLevel")
        if battery_level == targetBatteryLevel:
            break
        sleep(30)

    """ fully unplug usb charging """
    set_limit_battery_level(targetBatteryLevel-4)

    """ first try: turn on core """
    turn_on_screen()
    turn_on_heater("high")
    turn_off_usb_charging()
    if core == "little":
        set_frequency(target_freq, target_freq, mid_min_freq, mid_min_freq, big_min_freq, big_min_freq)
    elif core == "mid":
        set_frequency(little_min_freq, little_min_freq, target_freq, target_freq, big_min_freq, big_min_freq)
    elif core == "big":
        set_frequency(little_min_freq, little_min_freq, mid_min_freq, mid_min_freq, target_freq, target_freq)
    else:
        print("ERR")
    # set_governor("schedutil")
    set_cores(1,1,1,1,1,1,1,1)
    sleep(10)
    voltage1 = get_battery_voltage()
    start_logging()
    fileName = file_name_generator(battery_level, core, target_freq, "ON")
    copy_log(fileName)
    voltage2 = get_battery_voltage()
    save_pickle(fileName, [voltage1, voltage2])
    set_cores(1,1,1,1,1,1,1,1)
    unset_frequency()
    turn_off_heater()
    turn_off_screen()

    """ second try: turn off core """
    turn_on_screen()
    turn_on_heater("high")
    turn_off_usb_charging()
    if core == "little":
        set_frequency(target_freq, target_freq, mid_min_freq, mid_min_freq, big_min_freq, big_min_freq)
    elif core == "mid":
        set_frequency(little_min_freq, little_min_freq, target_freq, target_freq, big_min_freq, big_min_freq)
    elif core == "big":
        set_frequency(little_min_freq, little_min_freq, mid_min_freq, mid_min_freq, target_freq, target_freq)
    else:
        print("ERR")
    # set_governor("schedutil")
    if core == "little":
        set_cores(0,0,0,0,1,1,1,1)
    elif core == "mid":
        set_cores(1,1,1,1,0,0,1,1)
    elif core == "big":
        set_cores(1,1,1,1,1,1,0,0)
    else:
        print("ERR")
    sleep(10)
    start_logging()
    voltage1 = get_battery_voltage()
    fileName = file_name_generator(battery_level, core, target_freq, "OFF")
    copy_log(fileName)
    voltage2 = get_battery_voltage()
    save_pickle(fileName, [voltage1, voltage2])
    set_cores(1,1,1,1,1,1,1,1)
    unset_frequency()
    turn_off_heater()
    turn_off_screen()

    set_limit_battery_level(targetBatteryLevel)

set_root()

set_brightness(158)

# for targetBatteryLevel in np.arange(5,101,5)[::-1]:
for targetBatteryLevel in [90, 95,100][::-1]:
    set_limit_battery_level(targetBatteryLevel)
    limit_battery_level = get_limit_battery_level()
    print(limit_battery_level)

    for i in range(trial):
        for little_freq in little_available_frequencies:
            tester(little_freq, "little", targetBatteryLevel)
        for mid_freq in mid_available_frequencies:
            tester(mid_freq, "mid", targetBatteryLevel)
        for big_freq in big_available_frequencies:
            tester(big_freq, "big", targetBatteryLevel)