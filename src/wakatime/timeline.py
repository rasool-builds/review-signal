from src.wakatime.collect_activity import get_heartbeats


def get_file_events(day: str, file_name: str):
    data = get_heartbeats(day)
    heartbeats = data.get("data", [])

    events = []

    for heartbeat in heartbeats:
        entity = heartbeat.get("entity", "").replace("\\", "/").lower()

        if entity.endswith(file_name.lower()):
            events.append(heartbeat)

    events.sort(key=lambda heartbeat: heartbeat["time"])

    return events
if __name__ == "__main__":
    events = get_file_events(
        "2026-09-10",
        "src/experiment/process_test.py",
    )

    print(f"Events found: {len(events)}")

    previous_time = None
    first_time = events[0]["time"] if events else None

    for i, event in enumerate(events, start=1):
        print(f"\n--- EVENT {i} ---")
        print("Time:", event["time"])

        if previous_time is not None:
            gap = event["time"] - previous_time
            print("Seconds since previous event:", round(gap, 2))

        previous_time = event["time"]

        print("Write:", event.get("is_write"))
        print("Human changes:", event.get("human_line_changes"))
        print("Category:", event.get("category"))

    if first_time is not None and events:
        total_window = events[-1]["time"] - first_time
        print("\nTotal process window:", round(total_window, 2), "seconds")