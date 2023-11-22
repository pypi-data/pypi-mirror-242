#!/usr/bin/env python3

import argparse
import asyncio
import os
import shlex
import sys
from asyncio.subprocess import PIPE, create_subprocess_exec
from contextlib import suppress


class Display:
    def __init__(self, size=None, pos=None, white=False, parent_did=0, own_did=1):
        self.display_process = None
        self.process = None
        self.size = size or (1024, 768)
        self.pos = pos or (100, 100)
        self.white = white
        self.parent_did = parent_did
        self.own_did = own_did

    def __str__(self):
        return f"Display({self.parent_did}=>{self.own_did})"

    @staticmethod
    async def handle_lines(stream, prefix: str) -> None:
        async for line in (raw_line.decode().rstrip("\n") async for raw_line in stream):
            print(f"{prefix}: {line}")

    async def __aenter__(self, *args):
        assert not self.display_process
        self.display_process = await create_subprocess_exec(
            *shlex.split(
                f"Xephyr {'-wr' if self.white else ''} -screen"
                f" {self.size[0]}x{self.size[1]}"
                f"+{self.pos[0]}+{self.pos[1]}"
                f" :{self.own_did}"
            ),
            env={"DISPLAY": f":{self.parent_did}"},
            stdout=PIPE,
            stderr=PIPE,
        )
        asyncio.create_task(self.handle_lines(self.display_process.stdout, prefix="Xephyr std"))
        asyncio.create_task(self.handle_lines(self.display_process.stderr, prefix="Xephyr err"))
        await asyncio.sleep(0.05)
        return self

    async def __aexit__(self, *args):
        with suppress(ProcessLookupError):
            self.display_process.terminate()
            await self.display_process.wait()

    async def execute(self, command, prefix):
        assert not self.process
        self.process = await create_subprocess_exec(
            *command,
            env={"DISPLAY": f":{self.own_did}"},
            stdout=PIPE,
            stderr=PIPE,
        )
        asyncio.create_task(self.handle_lines(self.process.stdout, prefix=prefix))
        asyncio.create_task(self.handle_lines(self.process.stderr, prefix=prefix))
        return self.process.wait()

    def Display(self, size=None, pos=None, white=False, parent_did=0, own_did=1):
        return Display(size, pos, white, parent_did, own_did)


async def amain():
    async with Display(white=True) as main_display:
        async with (
            main_display.Display(
                size=(300, 300), pos=(100, 100), parent_did=1, own_did=2
            ) as sub_display1,
            main_display.Display(
                size=(300, 300), pos=(400, 400), parent_did=1, own_did=3
            ) as sub_display2,
        ):
            await asyncio.gather(
                await sub_display1.execute(sys.argv[1:], "p1"),
                await sub_display2.execute(sys.argv[1:], "p2"),
            )


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
