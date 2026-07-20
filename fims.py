import argparse
import hashlib
import json
from pathlib import Path


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_snapshot(root: Path) -> dict[str, str]:
    root = root.resolve()
    snapshot: dict[str, str] = {}
    for file_path in sorted(path for path in root.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(root).as_posix()
        snapshot[relative_path] = _hash_file(file_path)
    return snapshot


def save_baseline(root: Path, baseline_path: Path) -> None:
    snapshot = build_snapshot(root)
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")


def load_baseline(baseline_path: Path) -> dict[str, str]:
    return json.loads(baseline_path.read_text(encoding="utf-8"))


def compare_snapshot(root: Path, baseline_path: Path) -> dict[str, list[str]]:
    baseline = load_baseline(baseline_path)
    current = build_snapshot(root)
    baseline_keys = set(baseline)
    current_keys = set(current)

    added = sorted(current_keys - baseline_keys)
    removed = sorted(baseline_keys - current_keys)
    modified = sorted(path for path in baseline_keys & current_keys if baseline[path] != current[path])

    return {"added": added, "removed": removed, "modified": modified}


def _print_changes(changes: dict[str, list[str]]) -> None:
    for category in ("added", "removed", "modified"):
        items = changes[category]
        if items:
            print(f"{category}:")
            for item in items:
                print(f"  - {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="File Integrity Management System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create baseline file hashes")
    init_parser.add_argument("path", type=Path, help="Directory to monitor")
    init_parser.add_argument("--baseline", required=True, type=Path, help="Path to baseline JSON file")

    scan_parser = subparsers.add_parser("scan", help="Compare current files against baseline")
    scan_parser.add_argument("path", type=Path, help="Directory to monitor")
    scan_parser.add_argument("--baseline", required=True, type=Path, help="Path to baseline JSON file")

    args = parser.parse_args()

    if args.command == "init":
        save_baseline(args.path, args.baseline)
        print(f"Baseline created at {args.baseline}")
        return 0

    changes = compare_snapshot(args.path, args.baseline)
    has_changes = any(changes.values())
    if has_changes:
        _print_changes(changes)
        return 1

    print("No integrity changes detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
