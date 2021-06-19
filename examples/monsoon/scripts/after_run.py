import time# noinspection PyUnusedLocal
import subprocess

def send_command(cmd):
    proc = subprocess.Popen(["adb", "shell",  cmd], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate() 
    print("Jaaa returned")
    out = out.decode('ascii')
    print(out)
    if err:
        err = err.decode("ascii")
        print(err)
    time.sleep(5)

def execute_thing():
    # proc = subprocess.Popen(["sh", "/home/omar/Desktop/swipe.sh"], shell=True, 
    #     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print("using shell")
    # out, err = proc.communicate() 
    # out = out.decode('ascii')
    subprocess.call("sh /home/omar/Desktop/swipe.sh", shell=True)
    # if err:
    #     err = err.decode("ascii")
    #     print(err)
    time.sleep(2)

def main(device, *args, **kwargs):

    # subprocess.call("adb shell sendevent /dev/input/event2 1 116 1", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event2 0 0 0", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event2 1 116 0", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event2 0 0 0", shell=True)

    # """
    # /dev/input/event2: 0001 0074 00000001
    # /dev/input/event2: 0000 0000 00000000
    # /dev/input/event2: 0001 0074 00000000
    # /dev/input/event2: 0000 0000 00000000


    # """
    # time.sleep(2)
    # print("Wakeup")
    # subprocess.call("adb shell sendevent /dev/input/event2 1 116 1", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event3 0 0 1", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event0 0 0 1", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event2 0 0 0", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event2 1 116 0", shell=True)
    # subprocess.call("adb shell sendevent /dev/input/event2 0 0 0", shell=True)
    print("Sleep")
    time.sleep(2)
    subprocess.call("adb -s 01ca4c64db5d1014  shell input keyevent KEYCODE_SLEEP", shell=True)
    time.sleep(2)
    print("wakeup")
    subprocess.call("adb -s 01ca4c64db5d1014  shell input keyevent KEYCODE_WAKEUP", shell=True)
    time.sleep(2)
    print("Swipe first time")
    subprocess.call("adb -s 01ca4c64db5d1014 shell input touchscreen swipe 530 1420 530 0", shell=True)
    time.sleep(2)
    print("swipe second time")
    subprocess.call("adb -s 01ca4c64db5d1014 shell input touchscreen swipe 530 1420 530 0", shell=True)
    time.sleep(2)
    print("Input code")
    subprocess.call("adb -s 01ca4c64db5d1014 shell input text 0000", shell=True)
    
    print("Press okay")
    subprocess.call("adb -s 01ca4c64db5d1014 shell input keyevent 66", shell=True)

    time.sleep(2)

    # while True:
    #     print("Sleep")

    #     device.shell("sendevent /dev/input/event2 1 116 1")
    #     device.shell("sendevent /dev/input/event2 0 0 0")
    #     device.shell("sendevent /dev/input/event2 1 116 0")
    #     device.shell("sendevent /dev/input/event2 0 0 0")

    #     """
    # /dev/input/event2: 0001 0074 00000001
    # /dev/input/event2: 0000 0000 00000000
    # /dev/input/event2: 0001 0074 00000000
    # /dev/input/event2: 0000 0000 00000000


    #     """
    #     time.sleep(2)
    #     print("Wakeup")
    #     device.shell("sendevent /dev/input/event2 1 116 1")
    #     device.shell("sendevent /dev/input/event3 0 0 1")
    #     device.shell("sendevent /dev/input/event0 0 0 1")
    #     device.shell("sendevent /dev/input/event2 0 0 0")
    #     device.shell("sendevent /dev/input/event2 1 116 0")
    #     device.shell("sendevent /dev/input/event2 0 0 0")
    #     time.sleep(2)
    #     print("Swipe")
    #     execute_thing()
    #     time.sleep(2)
    #     print("Enter code")
    #     device.shell("input text 0000")
    #     time.sleep(2)
    #     print("Press okay")
    #     device.shell("input keyevent 66")
    #     time.sleep(2)
