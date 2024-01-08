import subprocess

from ansible_rulebook.action.plugin import Control, Metadata, Helper


async def main(metadata: Metadata, control: Control, **action_args) -> None:
    helper = Helper(metadata, control, "say")
    text = action_args.get("text", None)
    try:
        subprocess.run(["say", "--", text])
    except KeyboardInterrupt:
        pass
    await helper.send_default_status()
