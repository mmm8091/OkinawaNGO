from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from research_publication import (
    compile_publication_snapshot,
    verify_publication_channel,
)


def default_channel_path(profile: str) -> Path:
    """Keep every release profile on its own channel by default."""

    return Path("outputs/publication_channels_v1") / f"{profile}.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile the method-gated static data snapshot used by the explorer."
    )
    parser.add_argument(
        "--profile",
        default=os.environ.get("PUBLICATION_PROFILE", "client_preview"),
        choices=("reviewed", "client_preview", "internal"),
    )
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/publication_releases_v1"),
        help="Immutable release-store root",
    )
    parser.add_argument(
        "--channel-file",
        type=Path,
        default=None,
        help=(
            "Channel pointer updated after a successful build "
            "(default: outputs/publication_channels_v1/<profile>.json)"
        ),
    )
    args = parser.parse_args()
    project_root = PROJECT_ROOT
    output = args.output
    if not output.is_absolute():
        output = project_root / output
    selected_channel = args.channel_file or default_channel_path(args.profile)
    if args.verify_only:
        channel_file = selected_channel
        if not channel_file.is_absolute():
            channel_file = project_root / channel_file
        output_report = verify_publication_channel(
            project_root,
            channel_file,
            expected_profile=args.profile,
        )
    else:
        channel_file = selected_channel
        if not channel_file.is_absolute():
            channel_file = project_root / channel_file
        report = compile_publication_snapshot(
            project_root,
            output,
            profile=args.profile,
            channel_file=channel_file,
        )
        output_report = {
            "release_id": report["release_id"],
            "profile": report["release_profile"],
            "data_build_id": report["data_build_id"],
            "validation": report["validation"],
        }
    print(json.dumps(output_report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
