import argparse, sys, time, requests
from azure.identity import DefaultAzureCredential

ap = argparse.ArgumentParser()
ap.add_argument("--ws"); ap.add_argument("--ds")
a = ap.parse_args()
tok = DefaultAzureCredential().get_token("https://analysis.windows.net/powerbi/api/.default").token
h = {"Authorization": f"Bearer {tok}"}
url = f"https://api.powerbi.com/v1.0/myorg/groups/{a.ws}/datasets/{a.ds}/refreshes"

requests.post(url, headers=h, json={"type": "full"}).raise_for_status()
for _ in range(120):                        # max. 60 minutes
    time.sleep(30)
    status = requests.get(url + "?$top=1", headers=h).json()["value"][0]["status"]
    print("Refresh:", status)               # "Unknown" = still running
    if status == "Completed":
        sys.exit(0)
    if status in ("Failed", "Cancelled", "Disabled"):
        sys.exit(f"Refresh {status}")
sys.exit("Refresh timeout")
