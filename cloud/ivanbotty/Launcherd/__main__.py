import time
import os
import json
from cloud.ivanbotty.Launcher.services.applications_service import ApplicationsService

CACHE_PATH = os.path.expanduser("~/.config/cloud.ivanbotty.Launcher/applications_cache.json")
SCAN_INTERVAL = 60  # in seconds

def main():
    service = ApplicationsService()
    while True:
        store = service.load_applications()
        apps = [model.to_dict() for model in store]
        with open(CACHE_PATH, "w") as f:
            json.dump(apps, f)
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()