import random
import time
from dataclasses import dataclass
from queue import Queue
from typing import Callable, Iterable, Iterator


@dataclass(kw_only=True)
class Brain:
    iq: int

    def is_empty(self):
        return self.iq <= 0


class Life:
    def __init__(self, brain: Brain):
        self.brain = brain

    def code(self):
        n = random.randint(3, 24)
        print(f"Coding for {n} hours...")

        self.brain.iq -= 5 * n

    def order_coffee(self):
        n = random.randint(1, 3)
        print(f"Ordering {n} coffees...")

        self.brain.iq += random.randint(-1, 1) * 20 * n

    def sleep(self):
        p = random.randint(1, 10)
        supersleep = False

        if self.brain.is_empty():
            p = 10
            supersleep = True
            print("Preprare for SUPERSLEEP!!!", end="    ")

        self.brain.iq += 10 * p

        if p < 3:
            print(f"Coding for {random.randint(1, 4)} hours before sleeping for {p} hours...")
        else:
            print(f"Sleeping for {p} hours...")

            if supersleep:
                self.brain.iq = max(50, self.brain.iq)


class EventLoop:
    def __init__(self, ips: int, hard_delay: float, repeat: bool = False):
        """
        @param ips (int): [iterations per second to run]
        @param hard_delay (float): [constant delay between operations]
        @param repeat (bool): [whether to loop tasks indefinitely or to iterate and return]
        """
        self.iteration_speed = ips
        self.iteration_time = 1 / ips
        self.intertask_delay = hard_delay
        self.loop_tasks = repeat

        self._life: Life = Life(Brain(iq=0))

        self.task_template = []

        self.queue: Queue[Callable[[Life], None]] = Queue()

    def add_tasks(self, tasks_list: Iterable[Callable]) -> None:
        self.task_template.extend(tasks_list)

    def run_next(self) -> None:
        if self.queue.qsize() == 0:
            if self.loop_tasks:
                self.init_queue()
            else:
                return

        self.queue.get()(self._life)

    def init_queue(self):
        """Re/fill queue with tasks"""
        for task in self.task_template:
            self.queue.put(task)

    def wait(self) -> None:
        time.sleep(max(self.intertask_delay, self.iteration_time))

    def run(self, life: Life) -> None:
        self._life = life
        self.init_queue()

        while True:
            self.run_next()
            self.wait()


def get_event_loop(ips: int, delay: float = 0.0, repeat: bool = True) -> EventLoop:
    iterations_per_second = ips
    intertask_delay = delay
    loop_tasks = repeat

    return EventLoop(
        iterations_per_second,
        intertask_delay,
        loop_tasks,
    )

def get_random_tasks(life: Life, n: int) -> Iterator[Callable[[Life], None]]:
    task_weights: dict[Callable[[Life], None], int] = {
        Life.code: 1,
        Life.order_coffee: 2,
        Life.sleep: 3,
    }

    tasks = []

    for task, weight in task_weights.items():
        tasks.extend([task] * weight)

    return (random.choice(tasks) for _ in range(n))

def main():
    life = Life(Brain(iq=100))

    event_loop = get_event_loop(1, 0.2, repeat=True)
    event_loop.add_tasks(get_random_tasks(life, n=1000))
    event_loop.run(life)


if __name__ == "__main__":
    main()
