#!/usr/bin/env python3
"""Generate a report for a two-run OCI reproducibility pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)
    raise SystemExit(1)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_manifest_info(archive_path: Path) -> dict[str, Any]:
    try:
        with tarfile.open(archive_path, "r") as archive:
            try:
                index_member = archive.getmember("index.json")
            except KeyError as exc:
                fail(f"{archive_path} is missing index.json: {exc}")

            index_file = archive.extractfile(index_member)
            if index_file is None:
                fail(f"{archive_path} index.json could not be read")

            index_data = json.load(index_file)
    except tarfile.TarError as exc:
        fail(f"Failed to open OCI archive {archive_path}: {exc}")

    manifests = index_data.get("manifests")
    if not isinstance(manifests, list) or not manifests:
        fail(f"{archive_path} index.json must contain at least one manifest entry")

    manifest = manifests[0]
    digest = manifest.get("digest")
    if not isinstance(digest, str) or not digest.startswith("sha256:"):
        fail(f"{archive_path} manifest digest is missing or invalid")

    platform = manifest.get("platform", {})
    os_name = platform.get("os")
    architecture = platform.get("architecture")
    platform_name = (
        f"{os_name}/{architecture}"
        if isinstance(os_name, str) and isinstance(architecture, str)
        else "unknown"
    )

    annotations = manifest.get("annotations", {})
    ref_name = annotations.get("org.opencontainers.image.ref.name", "")

    return {
        "manifest_digest": digest,
        "platform": platform_name,
        "ref_name": ref_name,
    }


def write_report(
    output_dir: Path,
    image_name: str,
    first_path: Path,
    second_path: Path,
    first_info: dict[str, Any],
    second_info: dict[str, Any],
) -> tuple[Path, Path, str]:
    status = "pass" if first_info["manifest_digest"] == second_info["manifest_digest"] else "mismatch"
    output_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "schema_version": "1.0",
        "image_name": image_name,
        "status": status,
        "comparison_basis": "oci_manifest_digest",
        "runs": [
            {
                "name": "first",
                "archive": str(first_path),
                "archive_sha256": file_sha256(first_path),
                "manifest_digest": first_info["manifest_digest"],
                "platform": first_info["platform"],
                "ref_name": first_info["ref_name"],
            },
            {
                "name": "second",
                "archive": str(second_path),
                "archive_sha256": file_sha256(second_path),
                "manifest_digest": second_info["manifest_digest"],
                "platform": second_info["platform"],
                "ref_name": second_info["ref_name"],
            },
        ],
    }

    report_path = output_dir / "report.json"
    summary_path = output_dir / "summary.md"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary_lines = [
        "# Reproducibility Pilot Summary",
        "",
        f"- Image: `{image_name}`",
        f"- Status: `{status}`",
        f"- Comparison basis: `oci_manifest_digest`",
        f"- First manifest digest: `{first_info['manifest_digest']}`",
        f"- Second manifest digest: `{second_info['manifest_digest']}`",
        f"- First platform: `{first_info['platform']}`",
        f"- Second platform: `{second_info['platform']}`",
        "",
        "Interpretation:",
        (
            "- The two normalized OCI builds produced the same manifest digest."
            if status == "pass"
            else "- The two normalized OCI builds produced different manifest digests. Treat this as a reproducibility pilot failure that needs investigation before using the result as evidence."
        ),
        "",
        "Artifacts:",
        f"- `{report_path.name}`",
        f"- `{summary_path.name}`",
    ]
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    return report_path, summary_path, status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-name", required=True)
    parser.add_argument("--first-archive", required=True, type=Path)
    parser.add_argument("--second-archive", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    first_path = args.first_archive.resolve()
    second_path = args.second_archive.resolve()

    if not first_path.is_file():
        fail(f"First OCI archive does not exist: {first_path}")
    if not second_path.is_file():
        fail(f"Second OCI archive does not exist: {second_path}")

    first_info = extract_manifest_info(first_path)
    second_info = extract_manifest_info(second_path)
    report_path, summary_path, status = write_report(
        args.output_dir.resolve(),
        args.image_name,
        first_path,
        second_path,
        first_info,
        second_info,
    )

    print(f"[reproducibility-pilot] report: {report_path}")
    print(f"[reproducibility-pilot] summary: {summary_path}")
    if status != "pass":
        print("[reproducibility-pilot] mismatch detected")
        return 1
    print("[reproducibility-pilot] pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
