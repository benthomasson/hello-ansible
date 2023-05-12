import subprocess
from typing import List, Dict
import uuid
from ansible_rulebook.util import run_at
from ansible_rulebook.builtin import _get_events

SUCCESSFUL = "successful"


async def main(
    event_log,
    inventory: str,
    hosts: List,
    variables: Dict,
    project_data_file: str,
    source_ruleset_name: str,
    source_ruleset_uuid: str,
    source_rule_name: str,
    source_rule_uuid: str,
    rule_run_at: str,
    text: str,
):
    try:
        subprocess.run(["say", "--", text])
    except KeyboardInterrupt:
        pass
    await event_log.put(
        dict(
            type="Action",
            action="say",
            action_uuid=str(uuid.uuid4()),
            ruleset=source_ruleset_name,
            ruleset_uuid=source_ruleset_uuid,
            rule=source_rule_name,
            rule_uuid=source_rule_uuid,
            activation_id="???",
            run_at=run_at(),
            status=SUCCESSFUL,
            matching_events=_get_events(variables),
            rule_run_at=rule_run_at,
        )
    )
