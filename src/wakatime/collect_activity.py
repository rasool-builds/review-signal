import requests
from datetime import date

from src.config import WAKATIME_API_KEY


WAKATIME_API = "https://api.wakatime.com/api/v1"


def get_heartbeats(day: str):
    url = f"{WAKATIME_API}/users/current/heartbeats"

    response = requests.get(
        url,
        params={
            "api_key": WAKATIME_API_KEY,
            "date": day,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    today = date.today()
    print("Requesting WakaTime activity for:", today)
    data = get_heartbeats(today.isoformat())
    heartbeats = data.get("data", [])
    print("Heartbeats returned:", len(heartbeats))

    if heartbeats:
        for i, heartbeat in enumerate(heartbeats, start=1):
            print(f"\n--- HEARTBEAT {i} ---")
            print(heartbeat)
    else:
        print("No heartbeat data found for this date.")