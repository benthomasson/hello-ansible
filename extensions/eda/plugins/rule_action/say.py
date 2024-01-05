import subprocess

from ansible_rulebook.action.control import Control
from ansible_rulebook.action.helper import Helper
from ansible_rulebook.action.metadata import Metadata


async def main(metadata: Metadata, control: Control, **action_args) -> None:
    helper = Helper(metadata, control, "say")
    text = action_args.get("text", None)
    try:
        subprocess.run(["say", "--", text])
    except KeyboardInterrupt:
        pass
    await helper.send_default_status()
