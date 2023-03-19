import pyautogui
import time
import datetime

class TimeRecord(object):
    def __init__(self):
        self.schedules = [0, 0, 0, 0.0]
    
    def setTime(self, hour_min=None, sec=None, milisec=None, loop_sec=None):
        if hour_min is None or hour_min=='':
            hour_min = self.schedules[0]
        if sec is None or sec=='':
            sec = self.schedules[1]
        if milisec is None or milisec=='':
            milisec = self.schedules[2]
        if loop_sec is None or loop_sec=='':
            loop_sec = self.schedules[3]

        self.schedules = [int(hour_min), int(sec), int(milisec), float(loop_sec)]

    def resetTime(self):
        self.schedules = [0, 0, 0, 0.0]

class PositionalRecord(object):
    def __init__(self):
        self.records = []
    def record(self):
        pose = pyautogui.position()
        pose_x, pose_y = pose.x, pose.y
        self.records.append([pose_x, pose_y])
    def reset(self):
        self.records = []

def main_game( pose_records,
               time_records ):

    target_time, second_delay, mili_delay, loop_delay = time_records
    loop_delay = loop_delay if loop_delay <= 1e-5 else 1e-5
    second_delay = second_delay
    mili_delay = int(mili_delay * 1000)
    loop_flag = True

    while loop_flag:
        nowtime = datetime.datetime.now()
        if nowtime.hour==(target_time//100) and nowtime.minute >= target_time%100 and \
                                                nowtime.second >= second_delay and \
                                                nowtime.microsecond >= mili_delay:    
            for x_point, y_point in pose_records:
                pyautogui.click(x_point,y_point)
                time.sleep(loop_delay)
            loop_flag = False
        else:
            print(nowtime, end='\r')

        if nowtime.hour==(target_time//100) and nowtime.minute >= (target_time%100 +1):
            loop_flag = False

    return True