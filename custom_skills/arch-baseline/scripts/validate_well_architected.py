#!/usr/bin/env python3
"""
Validate Well-Architected Adherence Plan
Ensures the baseline document meets all requirements for the baseline gate.
"""

import sys
import re
from pathlib import Path


def parse_frontmatter_lines(lines):
    """Parse a minimal subset of YAML used in the adherence plan frontmatter."""
    data = {}
    current_list_key = None

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            if current_list_key is None:
                raise ValueError("List item encountered without an active key")
            item = stripped[2:].strip()
            data.setdefault(current_list_key, []).append(item)
            continue

        current_list_key = None
        if ":" not in raw_line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if "#" in value:
            value = value.split("#", 1)[0].strip()

        if not key:
            raise ValueError("Frontmatter key cannot be empty")

        if value == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = value

    return data


def load_yaml_frontmatter(file_path):
    """Load and parse YAML frontmatter from a markdown file without external deps."""
    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None, None
    except Exception as exc:
        print(f"ERROR: Failed to read file: {exc}")
        return None, None

    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        print("ERROR: File must start with YAML frontmatter delimited by '---'")
        return None, None

    frontmatter_lines = []
    closing_index = None

    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = idx
            break
        frontmatter_lines.append(line.rstrip("\r\n"))

    if closing_index is None:
        print("ERROR: Closing '---' for frontmatter not found")
        return None, None

    markdown_content = "".join(lines[closing_index + 1 :])

    try:
        frontmatter = parse_frontmatter_lines(frontmatter_lines)
    except ValueError as exc:
        print(f"ERROR: Invalid YAML frontmatter: {exc}")
        return None, None

    return frontmatter, markdown_content


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

    # Validate provider
    # This repository supports a template-mode adherence plan where the provider is not yet chosen.
    # In template-mode, provider must be "unselected". Post-decision plans must be one of aws/azure/gcp.
    valid_providers = ["aws", "azure", "gcp", "unselected"]
    if frontmatter.get("provider") not in valid_providers:
        errors.append(f"provider must be one of: {valid_providers}")

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


def validate_required_headings(markdown_content, provider: str):
    """Validate that required headings exist in the markdown content."""
    errors = []

    # The adherence plan has two supported shapes:
    # - Template-mode (provider = unselected): focuses on selection procedure and how provider mapping is materialized.
    # - Post-decision (provider in aws/azure/gcp): focuses on explicit pillar mapping table for the selected provider.
    if provider == "unselected":
        required_headings = [
            "# Well-Architected Adherence Plan",
            "## 1. Purpose",
            "## 2. Provider Selection Procedure",
            "## 3. Provider Packs",
            "## 4. Materializing Pillar Mapping Post-Decision",
            "## 5. Baseline Requirements (Provider-Agnostic)",
            "## 6. Review Procedure",
            "## 7. Evidence and Audit Rules",
            "## 8. Exception / Waiver Process",
            "## 9. Acceptance Criteria",
            "## 10. Change Log",
        ]
    else:
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
        # Ensure template-mode-only sections are not accidentally present after provider selection.
        if "## 2. Provider Selection Procedure" in markdown_content:
            errors.append("Template-mode sections present but provider is selected (provider must be 'unselected' for template-mode)")

    for heading in required_headings:
        if heading not in markdown_content:
            errors.append(f"Missing required heading: {heading}")

    return errors


def validate_pillar_table(markdown_content, provider: str):
    """Validate that the pillar mapping table exists and has content."""
    errors = []

    # Template-mode adherence plans do not include a pillar table; pillar mapping is materialized from provider packs
    # after the provider decision.
    if provider == "unselected":
        return errors

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

    provider = frontmatter.get("provider", "")
    if not isinstance(provider, str):
        provider = ""

    # Validate required headings
    heading_errors = validate_required_headings(markdown_content, provider)
    all_errors.extend(heading_errors)

    # Validate pillar table
    pillar_errors = validate_pillar_table(markdown_content, provider)
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
