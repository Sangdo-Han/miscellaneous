# Eventloop Callback based

import time
import typing as T
from collections import deque

class Event:
    def __init__(
        self,
        name: str,
        action: T.Callable[..., None],
        next_event: T.Optional["Event"] = None
    ) -> None:
        self.name = name
        self._action = action
        self._next_event = next_event
    
    def set_next_event(self, next_event:"Event") -> None:
        self._next_event = next_event

class EventLoop:
    def __init__(
        self    
    ) -> None:
        self._events = deque()
    
    def register_event(self, event):
        print(f"{event.name} is enrolled.")
        self._events.append(event)

    def run_forever(self) -> None:
        while True:
            try:
                event = self._events.popleft()
            except IndexError:
                continue
            self._execute_action(event)
    
    # execute action sequentially register the next event. (callbacks)
    def _execute_action(self, event) -> None:
        event._action(event)
        print(f"{event.name} is executed.")
        if event._next_event:
            self.register_event(event._next_event)

def echo_event(event: Event)->None:
    print(f"{event.name} is now being executed.")
    time.sleep(1)

if __name__ == "__main__":
    event_loop = EventLoop()

    for idx in range(2):
        main_event = Event(f"Main Event {idx}", action=echo_event)
        sub_event = Event(f"Sub Event {idx}", action=echo_event)
        main_event.set_next_event(sub_event)
        event_loop.register_event(main_event)

    event_loop.run_forever()
