import time
import os
import json
import logging

from cloud.ivanbotty.Launcher.services.applications_service import ApplicationsService

CACHE_PATH = os.path.expanduser("~/.cache/cloud.ivanbotty.Launcher/applications_cache.json")
SCAN_INTERVAL = 60

logger = logging.getLogger(__name__)

def ensure_cache_dir_exists(path):
    """Ensure the cache directory exists."""
    cache_dir = os.path.dirname(path)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        logger.debug("Created cache directory: %s", cache_dir)

def update_cache(service):
    """Update the cache file with the list of applications."""
    try:
        store = service.load_applications()
        apps = [model.to_dict() for model in store]
        ensure_cache_dir_exists(CACHE_PATH)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2, ensure_ascii=False)
        logger.info("Cache updated with %d applications.", len(apps))
    except Exception as e:
        logger.exception("Error updating the cache: %s", e)

def main():
    """Start the periodic cache update service."""
    service = ApplicationsService()
    logger.info("Launcher cache service started. Scanning every %d seconds.", SCAN_INTERVAL)
    try:
        while True:
            update_cache(service)
            time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Service manually interrupted.")

if __name__ == "__main__":
    main()
