from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Iterable, List, Mapping

import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = ("json", "csv", "xml")

def _ensure_parent_dir(path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

def export_json(records: List[Mapping], path: Path) -> None:
    _ensure_parent_dir(path)
    logger.debug("Writing JSON output to %s", path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

def export_csv(records: List[Mapping], path: Path) -> None:
    _ensure_parent_dir(path)
    if not records:
        logger.warning("No records to write to CSV; creating an empty file.")
        with path.open("w", encoding="utf-8", newline="") as f:
            f.write("")
        return

    fieldnames = list(records[0].keys())
    logger.debug("Writing CSV output to %s", path)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)

def export_xml(records: Iterable[Mapping], path: Path) -> None:
    _ensure_parent_dir(path)

    root = ET.Element("Shorts")
    for rec in records:
        item_el = ET.SubElement(root, "Short")
        for key, value in rec.items():
            tag = key.replace(" ", "")
            child = ET.SubElement(item_el, tag)
            child.text = str(value)

    tree = ET.ElementTree(root)
    logger.debug("Writing XML output to %s", path)
    tree.write(path, encoding="utf-8", xml_declaration=True)

def export_data(records: List[Mapping], fmt: str, path: Path) -> None:
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported export format '{fmt}'")

    logger.info("Exporting %d records as %s to %s", len(records), fmt.upper(), path)

    if fmt == "json":
        export_json(records, path)
    elif fmt == "csv":
        export_csv(records, path)
    elif fmt == "xml":
        export_xml(records, path)