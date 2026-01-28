#!/usr/bin/env python3
"""
Utility for handling YAML frontmatter in Markdown files.
"""

import re
import yaml


def load_yaml_frontmatter(filepath):
    """
    Loads YAML frontmatter from a markdown file.
    Returns (frontmatter_dict, markdown_content).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match YAML frontmatter
    # It should start and end with --- and be at the top of the file
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_str = match.group(1)
        markdown_content = content[match.end():]
        try:
            data = yaml.safe_load(yaml_str)
            return data, markdown_content
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML in {filepath}: {exc}")
            return {}, content

    return {}, content


def dump_yaml_frontmatter(frontmatter, markdown_content):
    """
    Dumps frontmatter and markdown content into a single string.
    """
    yaml_str = yaml.dump(frontmatter, sort_keys=False)
    return f"---\n{yaml_str}---\n\n{markdown_content}"
