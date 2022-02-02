import asyncio
import threading
from asyncio import sleep, current_task
from dataclasses import dataclass
from datetime import datetime
from random import random


def ts():
    return datetime.now().timestamp()


def task_name():
    return current_task().get_name()


def thread_name():
    return threading.current_thread().name


def log(msg):
    current_time = datetime.now().strftime("%H:%M:%S.%f")
    print(f"[{current_time[:-3]}]\t{msg}")


@dataclass
class Pos:
    x: float
    y: float


@dataclass
class Altitude:
    h: float


async def update_gps(d: Pos):
    log("starting gps... ")
    while True:
        # normalnie tu byśmy napisali d.x = await gpd.get_current_position()
        d.x = random()
        d.y = random()
        await sleep(0.5)


async def update_altimeter(a: Altitude):
    log("calculating height...")
    while True:
        a.h = random()
        await sleep(0.5)


async def stabilize_drone(d: Pos, a: Altitude):
    log("drone stabilization initiated")
    while True:
        log(f"stabilizing... at: x={d.x},{d.y}")
        log(f"keeping altitude at: h={a.h}")
        await sleep(0.01)


async def main_foo():
    st = ts()
    log(f"start -- na wątku {thread_name()}")
    d = Pos(0, 0)
    a = Altitude(0)
    asyncio.create_task(update_gps(d))
    asyncio.create_task(update_altimeter(a))
    asyncio.create_task(stabilize_drone(d, a))
    log(f"main -- done after {ts() - st:.3f}s")
    await sleep(2)


asyncio.run(main_foo())
