"""
json_post.py  Send http post to url with json data


"""


from ansible_rulebook.action.plugin import Control, Metadata, Helper

import aiohttp


async def main(metadata: Metadata, control: Control, **action_args) -> None:
    helper = Helper(metadata, control, "say")
    uri = action_args.get("uri")
    data = action_args.get("data", {})
    # Send http post to url

    async with aiohttp.ClientSession() as session:
        async with session.post(uri, json=data) as resp:
            print(resp.status)
            print(await resp.json())

    await helper.send_default_status()


if __name__ == "__main__":
    import asyncio
    from unittest.mock import MagicMock

    metadata = MagicMock()
    control = MagicMock()
    control.queue = asyncio.Queue()

    asyncio.run(
        main(
            metadata, control, uri="http://localhost:8000/path", data={"name": "test"}
        )
    )

    print(control.queue.get_nowait())
