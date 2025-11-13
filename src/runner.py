import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

from extractors.youtube_parser import YouTubeShortsParser
from outputs.exporters import export_data, SUPPORTED_FORMATS

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
CONFIG_DIR = SRC_DIR / "config"
DEFAULT_CONFIG_FILE = CONFIG_DIR / "settings.example.json"

def configure_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def load_settings(config_path: Path | None) -> Dict[str, Any]:
    logger = logging.getLogger("runner.config")

    if config_path is None:
        if DEFAULT_CONFIG_FILE.exists():
            config_path = DEFAULT_CONFIG_FILE
        else:
            logger.warning(
                "No config file provided and default settings.example.json not found. "
                "Falling back to internal defaults."
            )
            return {
                "hashtag": "amazing",
                "max_items": 50,
                "output": {
                    "format": "json",
                    "path": "data/shorts_output.json",
                },
                "network": {
                    "timeout": 15,
                    "user_agent": (
                        "Mozilla/5.0 (compatible; BitbashScraper/1.0; "
                        "+https://bitbash.dev)"
                    ),
                },
            }

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info("Loaded configuration from %s", config_path)
        return data
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load config from %s: %s", config_path, exc)
        raise SystemExit(1) from exc

def resolve_output_path(path_str: str | None) -> Path:
    if not path_str:
        return ROOT_DIR / "data" / "shorts_output.json"

    path = Path(path_str)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="YouTube Hashtag Shorts Scraper - Bitbash demo runner"
    )
    parser.add_argument(
        "--hashtag",
        type=str,
        help="Hashtag to search (without # sign, e.g., 'travel').",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        help="Maximum number of shorts to retrieve.",
    )
    parser.add_argument(
        "--format",
        choices=SUPPORTED_FORMATS,
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path.",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to JSON config file (defaults to src/config/settings.example.json).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (use -vv for debug logging).",
    )
    return parser.parse_args()

def merge_cli_with_config(
    cfg: Dict[str, Any], args: argparse.Namespace
) -> Dict[str, Any]:
    out_cfg = dict(cfg)

    if args.hashtag:
        out_cfg["hashtag"] = args.hashtag

    if args.max_items is not None:
        out_cfg["max_items"] = max(1, int(args.max_items))

    output_cfg = dict(out_cfg.get("output", {}))
    if args.format:
        output_cfg["format"] = args.format
    if args.output:
        output_cfg["path"] = args.output

    if "format" not in output_cfg:
        output_cfg["format"] = "json"
    if "path" not in output_cfg:
        output_cfg["path"] = "data/shorts_output.json"

    out_cfg["output"] = output_cfg

    if "network" not in out_cfg:
        out_cfg["network"] = {}
    if "timeout" not in out_cfg["network"]:
        out_cfg["network"]["timeout"] = 15
    if "user_agent" not in out_cfg["network"]:
        out_cfg["network"]["user_agent"] = (
            "Mozilla/5.0 (compatible; BitbashScraper/1.0; +https://bitbash.dev)"
        )

    return out_cfg

def run() -> None:
    args = parse_args()
    configure_logging(args.verbose)

    logger = logging.getLogger("runner")

    config_path = Path(args.config) if args.config else None
    settings = load_settings(config_path)
    settings = merge_cli_with_config(settings, args)

    hashtag = settings.get("hashtag")
    if not hashtag:
        logger.error("No hashtag provided. Use --hashtag or set it in the config file.")
        raise SystemExit(1)

    max_items = int(settings.get("max_items", 50))
    network_cfg = settings.get("network", {})
    output_cfg = settings.get("output", {})

    output_format = output_cfg.get("format", "json").lower()
    if output_format not in SUPPORTED_FORMATS:
        logger.error(
            "Unsupported output format '%s'. Supported formats: %s",
            output_format,
            ", ".join(SUPPORTED_FORMATS),
        )
        raise SystemExit(1)

    output_path = resolve_output_path(output_cfg.get("path"))

    logger.info(
        "Starting scrape for hashtag '#%s' (max_items=%d, format=%s)",
        hashtag,
        max_items,
        output_format,
    )

    parser = YouTubeShortsParser(
        timeout=network_cfg.get("timeout", 15),
        user_agent=network_cfg.get("user_agent"),
    )

    try:
        records = parser.search_shorts(hashtag=hashtag, max_items=max_items)
    except Exception as exc:  # noqa: BLE001
        logger.error("Scraping failed: %s", exc, exc_info=args.verbose >= 2)
        raise SystemExit(1) from exc

    if not records:
        logger.warning("No shorts found for hashtag '#%s'.", hashtag)
    else:
        logger.info("Collected %d records.", len(records))

    dict_records: List[Dict[str, Any]] = [r.to_dict() for r in records]

    try:
        export_data(dict_records, output_format, output_path)
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to export data: %s", exc, exc_info=args.verbose >= 2)
        raise SystemExit(1) from exc

    logger.info("Finished. Output written to %s", output_path)
    print(f"Scraped {len(dict_records)} shorts for '#{hashtag}' -> {output_path}")

if __name__ == "__main__":
    # Ensure project root is on sys.path so imports work when run directly.
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    run()