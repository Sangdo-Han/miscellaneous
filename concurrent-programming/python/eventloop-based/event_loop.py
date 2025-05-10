
import time
import typing as T
from collections import deque
from utils import Timer

class Event:
    def __init__(
        self,
        name:str,
        action:T.Callable[..., None],
        next_event:T.Optional["Event"] = None,
    ) -> None:
        self._name = name
        self._action = action
        self._next_event = next_event
    
    def execute_action(self, event_loop) -> None:
        self._action(self)
        if self._next_event:
            event_loop.register_event(self._next_event)

class EventLoop:
    def __init__(self):
        self.event_queue : deque[Event] = deque()
    
    def register_event(self, new_event:Event):
        self.event_queue.append(new_event)
    
    def run(self):
        while True:
            try:
                event = self.event_queue.popleft()
            except IndexError:
                continue
            event.execute_action(self)

def knock(event):
    print(event._name)
    time.sleep(1)

def who(event):
    print(event._name)
    time.sleep(1)


if __name__ == "__main__":
    event_loop = EventLoop()

    for idx in range(2):
        replying = Event(f"Who's there? {idx}", who)
        knocking = Event(f"Knock Knock {idx}", knock, replying)
        event_loop.register_event(knocking)
    
    event_loop.run()