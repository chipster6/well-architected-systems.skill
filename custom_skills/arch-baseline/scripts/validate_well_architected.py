#!/usr/bin/env python3
"""
Validate Well-Architected Adherence Plan
Ensures the baseline document meets all requirements for the baseline gate.
"""

import sys
import os
import re
import yaml
import json
from pathlib import Path


def load_yaml_frontmatter(file_path):
    """Load and parse YAML frontmatter from a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split frontmatter and content
        if not content.startswith("---\n"):
            print("ERROR: File must start with YAML frontmatter (---)")
            return None, None

        parts = content.split("---\n", 2)
        if len(parts) < 3:
            print("ERROR: Invalid YAML frontmatter format")
            return None, None

        frontmatter_str = parts[1]
        markdown_content = parts[2]

        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_str)
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML frontmatter: {e}")
            return None, None

        return frontmatter, markdown_content

    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None, None
    except Exception as e:
        print(f"ERROR: Failed to read file: {e}")
        return None, None


def validate_frontmatter(frontmatter):
    """Validate frontmatter against schema and business rules."""
    errors = []

    # Required fields
    required_fields = [
        "doc_id",
        "doc_type",
        "status",
        "phase",
        "provider",
        "framework_name",
        "framework_version",
        "owner",
        "review_cadence",
        "last_reviewed",
        "next_review_due",
        "related_docs",
        "evidence_log",
    ]

    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Validate provider is not TBD
    if frontmatter.get("provider") == "tbd":
        errors.append("Provider cannot be 'tbd' - must be 'aws', 'azure', or 'gcp'")

    # Validate no TBD values
    for key, value in frontmatter.items():
        if value == "TBD":
            errors.append(f"Field '{key}' cannot be 'TBD'")

    # Validate doc_type
    if frontmatter.get("doc_type") != "well_architected_adherence_plan":
        errors.append("doc_type must be 'well_architected_adherence_plan'")

    # Validate phase
    if frontmatter.get("phase") != "baseline":
        errors.append("phase must be 'baseline'")

    # Validate status
    valid_statuses = ["draft", "approved", "superseded"]
    if frontmatter.get("status") not in valid_statuses:
        errors.append(f"status must be one of: {valid_statuses}")

    return errors


def validate_required_headings(markdown_content):
    """Validate that required headings exist in the markdown content."""
    errors = []

    required_headings = [
        "# Well-Architected Adherence Plan",
        "## 1. Purpose",
        "## 2. Framework Selection",
        "## 3. Definitions",
        "## 4. Pillar-to-Documentation Mapping",
        "## 5. Baseline Requirements",
        "## 6. Review Procedure",
        "## 7. Evidence and Audit Rules",
        "## 8. Exception / Waiver Process",
        "## 9. Acceptance Criteria",
        "## 10. Change Log",
    ]

    for heading in required_headings:
        if heading not in markdown_content:
            errors.append(f"Missing required heading: {heading}")

    return errors


def validate_pillar_table(markdown_content):
    """Validate that the pillar mapping table exists and has content."""
    errors = []

    # Look for the pillar table in section 4
    section4_match = re.search(
        r"## 4\. Pillar-to-Documentation Mapping.*?## 5\.", markdown_content, re.DOTALL
    )
    if not section4_match:
        errors.append("Could not find section 4 content")
        return errors

    section4_content = section4_match.group(0)

    # Check for table marker
    if "|---" not in section4_content:
        errors.append("Pillar mapping table not found or malformed")
        return errors

    # Extract table rows
    table_lines = [
        line.strip() for line in section4_content.split("\n") if line.startswith("|")
    ]

    if len(table_lines) < 2:  # Header + divider + at least one data row
        errors.append("Pillar mapping table must have at least one pillar row")
        return errors

    # Check for placeholder rows
    data_rows = table_lines[2:]  # Skip header and divider
    for row in data_rows:
        if "{{" in row or "TBD" in row or "tbd" in row:
            errors.append(f"Pillar table contains placeholders: {row}")

    # Check for non-empty pillar column (first column after |)
    for row in data_rows:
        cells = [
            cell.strip() for cell in row.split("|")[1:-1]
        ]  # Remove empty first/last
        if not cells or not cells[0] or "{{" in cells[0]:
            errors.append(f"Pillar table has empty pillar name: {row}")

    return errors


def validate_no_placeholders(content):
    """Validate that no placeholders remain in the document."""
    errors = []

    # Check for various placeholder patterns
    placeholder_patterns = [
        r"\{\{[^}]+\}\}",  # {{placeholder}}
        r"TBD",  # TBD
        r"tbd",  # tbd (case insensitive)
        r"{{[^}]+}}",  # malformed {{placeholder
    ]

    full_content = content  # Include frontmatter and markdown

    for pattern in placeholder_patterns:
        if re.search(pattern, full_content, re.IGNORECASE):
            matches = re.findall(pattern, full_content, re.IGNORECASE)
            for match in matches:
                # Skip legitimate patterns like provider enums in description
                if pattern == r"TBD" and "aws|azure|gcp|tbd" in full_content:
                    continue
                errors.append(f"Document contains placeholder: {match}")

    return errors


def main():
    """Main validation function."""
    if len(sys.argv) != 2:
        print("Usage: python validate_well_architected.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Load document
    frontmatter, markdown_content = load_yaml_frontmatter(file_path)
    if frontmatter is None:
        sys.exit(1)

    all_errors = []

    # Validate frontmatter
    frontmatter_errors = validate_frontmatter(frontmatter)
    all_errors.extend(frontmatter_errors)

    # Validate required headings
    heading_errors = validate_required_headings(markdown_content)
    all_errors.extend(heading_errors)

    # Validate pillar table
    pillar_errors = validate_pillar_table(markdown_content)
    all_errors.extend(pillar_errors)

    # Validate no placeholders
    placeholder_errors = validate_no_placeholders(str(frontmatter) + markdown_content)
    all_errors.extend(placeholder_errors)

    # Report results
    if all_errors:
        print(f"VALIDATION FAILED for {file_path}")
        print("\nErrors found:")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED for {file_path}")
        sys.exit(0)


if __name__ == "__main__":
    main()
