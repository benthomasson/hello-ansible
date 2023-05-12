"""
file.py

An ansible-rulebook event source plugin for loading facts from YAML files
initially.

Arguments:
    files - a list of YAML files

Example:

    - ansible.eda.file:
      files:
        - fact.yml

"""

import os
import asyncio

import yaml


async def send_facts(queue, filename):
    with open(filename) as f:
        data = yaml.safe_load(f.read())
        if data is None:
            return
        if isinstance(data, dict):
            await queue.put(data)
        else:
            if not isinstance(data, list):
                raise Exception(
                    "Unsupported facts type, expects a list of dicts found"
                    f" {type(data)}"
                )
            if not all(True if isinstance(item, dict) else False for item in data):
                raise Exception(
                    f"Unsupported facts type, expects a list of dicts found {data}"
                )
            for item in data:
                await queue.put(item)


async def main(queue, args):
    files = [os.path.abspath(f) for f in args.get("files", [])]

    if not files:
        return

    for filename in files:
        await send_facts(queue, filename)

    # Sleep forever
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), {"files": ["facts.yml"]}))
