import argparse
from fabric_cicd import FabricWorkspace, publish_all_items

ap = argparse.ArgumentParser()
ap.add_argument("--env", required=True)
a = ap.parse_args()
WORKSPACES = {"TEST": "<test-workspace-id>", "PROD": "<prod-workspace-id>"}

ws = FabricWorkspace(
    workspace_id=WORKSPACES[a.env],
    environment=a.env,                  # parameter.yml swaps connections per environment
    repository_directory="workspace",
    item_type_in_scope=["SemanticModel", "Report"],
)
publish_all_items(ws)
