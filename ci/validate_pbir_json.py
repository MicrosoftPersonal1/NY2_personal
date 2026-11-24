"""Validate PBIR JSON files with local schema-like required-key checks."""
import json
import pathlib
import sys

REQUIRED_KEYS = {
    "report.json": ["$schema", "themeCollection", "settings"],
    "version.json": ["$schema", "version"],
    "pages.json": ["$schema", "pageOrder", "activePageName"],
    "page.json": ["$schema", "name", "displayName", "height", "width"],
    "visual.json": ["$schema", "name", "position", "visual"],
}


def schema_kind(path: pathlib.Path) -> str:
    name = path.name
    if name in REQUIRED_KEYS:
        return name
    return ""


def validate_file(path: pathlib.Path):
    errors = []
    try:
        with path.open(encoding="utf-8") as f:
            doc = json.load(f)
    except Exception as ex:
        return [f"{path}: invalid JSON -> {ex}"]
    kind = schema_kind(path)
    if not kind:
        return []
    for key in REQUIRED_KEYS[kind]:
        if key not in doc:
            errors.append(f"{path}: missing required key '{key}'")
    schema_value = doc.get("$schema")
    if not isinstance(schema_value, str) or "json-schemas/fabric/item/report" not in schema_value:
        errors.append(f"{path}: invalid $schema value '{schema_value}'")
    if kind == "pages.json" and not isinstance(doc.get("pageOrder"), list):
        errors.append(f"{path}: pageOrder must be a list")
    if kind == "visual.json":
        visual = doc.get("visual")
        if not isinstance(visual, dict) or not visual.get("visualType"):
            errors.append(f"{path}: visual.visualType is required")
    return errors


def main():
    files = sorted(pathlib.Path("workspace").glob("**/*.Report/definition/**/*.json"))
    if not files:
        print("No PBIR report JSON files found under workspace/.")
        return 1
    all_errors = []
    for file_path in files:
        all_errors.extend(validate_file(file_path))
    if all_errors:
        print("PBIR validation failed:")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print(f"PBIR validation passed ({len(files)} files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
