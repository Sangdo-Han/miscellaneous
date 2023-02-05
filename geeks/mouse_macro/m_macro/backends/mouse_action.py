import pyautogui

class TimeRecord(object):
    def __init__(self, coords, actions, timings):
        """
        Args:
            coords : list
                nested lists (dim 2), coordinates
            actions : list
                list of Natural Numbers for Number of clicks
            timings:  list 
                list of times (microsecond delays, default to 0.0)
        """
        self.schedules = zip(coords, actions, timings)
    def setTime(self, hour, min, sec, milisec, microsec):
        pass

    def resetTime(self):
        """
        """
        pass

class PositionalRecord(object):
    def __init__(self):
        self.records = []
    def record(self):
        pose = pyautogui.position()
        pose_x, pose_y = pose.x, pose.y
        self.records.append([pose_x, pose_y])
    def reset(self):
        self.record = []

class MainGame(object):
    def __init__(self, timeRec, poseRec):
        pass