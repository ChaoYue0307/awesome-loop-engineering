#!/usr/bin/env python3
"""Preview a loop contract as a readable operating plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from check_loop_contract_examples import SCHEMA_PATH, validate


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def render_contract(contract: dict[str, Any]) -> str:
    trigger = contract["trigger"]
    intake = contract["intake"]
    workspace = contract["workspace"]
    context = contract["context"]
    verification = contract["verification"]
    state = contract["state"]
    budget = contract["budget"]
    escalation = contract["escalation"]
    exit_rules = contract["exit"]

    agents = "\n".join(
        f"  - {agent['role']}: {agent['responsibility']}" for agent in contract["agents"]
    )

    return f"""# {contract['name']}

Objective:
  {contract['objective']}

Trigger:
  Type: {trigger['type']}
  Cadence or event: {trigger['cadence_or_event']}

Discover / Intake:
{bullet_list(intake['sources'])}
  Selection rule: {intake['selection_rule']}

Workspace:
  Isolation: {workspace['isolation']}
  Allowed actions:
{bullet_list(workspace['allowed_actions'])}
  Disallowed actions:
{bullet_list(workspace['disallowed_actions'])}

Context:
  Required files:
{bullet_list(context['required_files'])}
  Runtime sources:
{bullet_list(context['runtime_sources'])}

Agents:
{agents}

Verification:
  Gates:
{bullet_list(verification['gates'])}
  Receipts:
{bullet_list(verification['receipts'])}

State:
  Artifacts:
{bullet_list(state['artifacts'])}
  Update rule: {state['update_rule']}

Budget:
  Max retries: {budget['max_retries']}
  Max runtime minutes: {budget['max_runtime_minutes']}

Escalation:
  Conditions:
{bullet_list(escalation['conditions'])}
  Destination: {escalation['destination']}

Exit:
  Success: {exit_rules['success']}
  Stop without success: {exit_rules['stop_without_success']}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path, help="Path to a loop contract JSON file.")
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    errors = validate(contract, schema, str(args.contract))
    if errors:
        for error in errors:
            print(error)
        return 1

    print(render_contract(contract))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
