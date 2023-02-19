import argparse
import time
import datetime
import pyautogui
import sys

def main(x_point,
         y_point,
         target_time,
         second_delay,
         mili_delay,
         loop_delay):
    x_point = x_point
    y_point = y_point
    second_delay = second_delay
    mili_delay = int(mili_delay * 100000)
    target_time = target_time
    mark_time = datetime.datetime.now()
    loop_flag = True
    while loop_flag:
        time.sleep(loop_delay)
        nowtime = datetime.datetime.now()
        if nowtime.hour==(target_time//100) and nowtime.minute >= target_time%100 and \
                                                nowtime.second >= second_delay and \
                                                nowtime.microsecond >= mili_delay:    
            pyautogui.click(x_point,y_point)
            loop_flag = False
        else:
            print(nowtime, end='\r')

        if nowtime.hour==(target_time//100) and nowtime.minute >= (target_time%100 +1):
            loop_flag = False

    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--x_point', type=int, default=500)
    parser.add_argument('-y', '--y_point', type=int, default=500)
    parser.add_argument('-t', '--target_time', type=int, default=2219)
    parser.add_argument('-sd', '--second_delay', type=int, default=0)
    parser.add_argument('-md', '--mili_delay', type=int, default=1)
    parser.add_argument('-ld', '--loop_delay', type=float, default=0.0)
    args = parser.parse_args()
    main(args.x_point, args.y_point,
         args.target_time, args.second_delay,
         args.micro_delay, args.loop_delay)