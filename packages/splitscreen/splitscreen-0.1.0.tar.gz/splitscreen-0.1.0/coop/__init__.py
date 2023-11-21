#!/usr/bin/env python3

#from pyvirtualdisplay import Display
import os
import asyncio
from asyncio.subprocess import PIPE, create_subprocess_exec
import shlex
from contextlib import asynccontextmanager


async def handle_lines(stream, prefix:str)->None:
    async for line in (
        raw_line.decode().rstrip("\n")
        async for raw_line in stream
    ):
        print(f"{prefix}: {line}")


class Display:
    def __init__(self, size=None, pos=None, white=False):
        self.process = None
        self.size = size or (1024, 768)
        self.pos = pos or (100, 100)
        self.white = white

    async def __aenter__(self, *args):
        self.process = await create_subprocess_exec(
            *shlex.split(
                f"Xephyr {'-wr' if self.white else ''} -screen"
                f" {self.size[0]}x{self.size[1]}"
                f"+{self.pos[0]}+{self.pos[1]}"
                f" :1"), stdout=PIPE, stderr=PIPE)
        asyncio.create_task(handle_lines(self.process.stdout, prefix=f"Xephyr std"))
        asyncio.create_task(handle_lines(self.process.stderr, prefix=f"Xephyr err"))
        return self

    async def __aexit__(self, *args):
        self.process.terminate()
        await self.process.wait()

    def SubDisplay(self):
        ...

    async def execute(self, command):
        ...
    
@asynccontextmanager
async def execute(command:str, prefix:str, pos):
    env_display = os.environ["DISPLAY"]
    with Display():
        print(prefix, os.environ["DISPLAY"])
        #d.__enter__()
        print(prefix, 1)
        process = await create_subprocess_exec(*shlex.split(command), stdout=PIPE, stderr=PIPE)
        print(prefix, 2)
        await asyncio.sleep(1)
        os.environ["DISPLAY"] = env_display
        yield asyncio.gather(
            handle_lines(process.stdout, prefix=f"{prefix} std"),
            handle_lines(process.stderr, prefix=f"{prefix} err"),
            process.wait(),
        )
        print(prefix, 3)
    print(prefix, 4)


async def amain():
    async with Display(white=True) as main_display:
        await asyncio.sleep(2)
        #with main_display.SubDisplay() as sub_display1, main_display.SubDisplay() as sub_display2:
        #    await asyncio.gather(
        #        sub_display1.execute("glxgears", "p1"),
        #        sub_display2.execute("glxgears", "p2"),
        #    )


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
