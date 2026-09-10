import subprocess
from datetime import datetime, timezone

from src.wakatime.collect_activity import get_heartbeats


def get_commit_info(commit_hash: str):
    timestamp = subprocess.check_output(
        ["git", "show", "-s", "--format=%ct", commit_hash],
        text=True,
    ).strip()

    files = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash],
        text=True,
    ).splitlines()

    return int(timestamp), files


def match_commit(commit_hash: str, day: str):
    commit_time, changed_files = get_commit_info(commit_hash)

    data = get_heartbeats(day)
    heartbeats = data.get("data", [])

    print(f"\nCommit: {commit_hash}")
    print(
        "Commit time:",
        datetime.fromtimestamp(commit_time, tz=timezone.utc).isoformat(),
    )
    print("Changed files:", changed_files)

    print("\nMatching WakaTime activity:")

    matches = []

    for heartbeat in heartbeats:
        entity = heartbeat.get("entity", "")

        # Convert Windows path to a Git-style relative path
        entity_normalized = entity.replace("\\", "/").lower()

        for file in changed_files:
            file_normalized = file.replace("\\", "/").lower()

            if entity_normalized.endswith(file_normalized):
                difference = commit_time - heartbeat["time"]

                # Activity occurring before the commit
                if 0 <= difference <= 3600:
                    matches.append((heartbeat, difference))

    if not matches:
        print("No matching activity found.")
        return

    for heartbeat, difference in matches:
        print("\n--- MATCH ---")
        print("File:", heartbeat["entity"])
        print("Category:", heartbeat.get("category"))
        print("Is write:", heartbeat.get("is_write"))
        print("Human changes:", heartbeat.get("human_line_changes"))
        print("Seconds before commit:", round(difference, 3))


if __name__ == "__main__":
    match_commit(
        "0f4a19e08571a6b222fda1a45d8b0a296981c84f",
        "2026-09-10",
    )