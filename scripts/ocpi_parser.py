#!/usr/bin/env python3
"""
OCPI AsciiDoc to Pydantic Parser

Parses the official OCPI specification from https://github.com/ocpi/ocpi
and generates Pydantic models and enums for py_ocpi.

Usage:
    python scripts/ocpi_parser.py --version 2.3.0 --output py_ocpi/modules
"""

import argparse
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class PropertyDef:
    """Represents a property definition from an OCPI schema."""

    name: str
    type_str: str
    cardinality: str
    description: str
    # Parsed type info
    base_type: str = ""
    max_length: Optional[int] = None
    is_list: bool = False
    is_optional: bool = False
    is_enum: bool = False
    is_class: bool = False
    reference_module: str = ""


@dataclass
class ObjectDef:
    """Represents an OCPI object definition."""

    name: str
    module: str
    anchor: str
    description: str
    properties: list[PropertyDef] = field(default_factory=list)
    is_enum: bool = False
    enum_values: list[tuple[str, str, str]] = field(
        default_factory=list
    )  # (name, value, description)


@dataclass
class ModuleDef:
    """Represents an OCPI module."""

    name: str
    identifier: str
    objects: list[ObjectDef] = field(default_factory=list)
    enums: list[ObjectDef] = field(default_factory=list)


class OCPIParser:
    """Parser for OCPI AsciiDoc specifications."""

    # Mapping of OCPI types to Python/Pydantic types
    TYPE_MAPPING = {
        "string": "str",
        "int": "int",
        "integer": "int",
        "number": "Number",
        "boolean": "bool",
        "object": "dict",
        "any": "Any",
    }

    # Types that need special handling with max_length
    CONSTRAINED_TYPES = {
        "CiString": "CiString",
        "String": "String",
        "string": "String",
    }

    # Core OCPI data types from types.asciidoc
    CORE_DATA_TYPES = {
        "DateTime": "DateTime",
        "URL": "URL",
        "DisplayText": "DisplayText",
        "Price": "Price",
        "Number": "Number",
    }

    def __init__(self, repo_path: str, version: str):
        self.repo_path = Path(repo_path)
        self.version = version
        self.modules: dict[str, ModuleDef] = {}
        self.global_enums: dict[str, ObjectDef] = {}
        self.global_classes: dict[str, tuple[str, ObjectDef]] = (
            {}
        )  # name -> (module, obj)

    def clone_repo(self, branch: str = "master") -> Path:
        """Clone the official OCPI repo to a temporary directory."""
        temp_dir = tempfile.mkdtemp(prefix="ocpi_")
        repo_url = "https://github.com/ocpi/ocpi.git"

        print(f"Cloning OCPI repo (branch: {branch})...")
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", branch, repo_url, temp_dir],
            check=True,
            capture_output=True,
        )
        return Path(temp_dir)

    def parse_all_modules(self):
        """Parse all OCPI modules from the repo."""
        # First parse types.asciidoc for core types
        types_file = self.repo_path / "types.asciidoc"
        if types_file.exists():
            self._parse_types_file(types_file)

        # Parse each module file
        module_files = [
            ("locations", "mod_locations.asciidoc"),
            ("sessions", "mod_sessions.asciidoc"),
            ("cdrs", "mod_cdrs.asciidoc"),
            ("tariffs", "mod_tariffs.asciidoc"),
            ("tokens", "mod_tokens.asciidoc"),
            ("commands", "mod_commands.asciidoc"),
            ("chargingprofiles", "mod_charging_profiles.asciidoc"),
            ("hubclientinfo", "mod_hub_client_info.asciidoc"),
            ("credentials", "credentials.asciidoc"),
            ("versions", "version_information_endpoint.asciidoc"),
        ]

        # Add payments module for 2.3.0
        if self.version.startswith("2.3"):
            module_files.append(("payments", "mod_payments.asciidoc"))

        for module_name, filename in module_files:
            filepath = self.repo_path / filename
            if filepath.exists():
                print(f"Parsing {filename}...")
                self._parse_module_file(module_name, filepath)
            else:
                print(f"Warning: {filename} not found")

    def _parse_types_file(self, filepath: Path):
        """Parse the types.asciidoc file for core type definitions."""
        content = filepath.read_text()
        # This file contains core types like DateTime, URL, etc.
        # These are already defined in py_ocpi/core/data_types.py

    def _parse_module_file(self, module_name: str, filepath: Path):
        """Parse a module file and extract object definitions."""
        content = filepath.read_text()
        module = ModuleDef(name=module_name, identifier=module_name)

        # Find all object definitions (look for ==== _Name_ Object patterns)
        object_pattern = re.compile(
            r"\[\[([^\]]+)\]\]\s*\n"  # Anchor
            r"={3,4}\s+[_*]?([A-Za-z_]+)[_*]?\s+(?:Object|object|Class|class)\s*\n"  # Title
            r"(.*?)"  # Description and content
            r"(?=\n\[\[|\n={3,4}\s+|\Z)",  # Until next section
            re.DOTALL,
        )

        for match in object_pattern.finditer(content):
            anchor, name, section_content = match.groups()
            obj = self._parse_object_section(name, anchor, section_content, module_name)
            if obj and obj.properties:
                module.objects.append(obj)
                self.global_classes[obj.name] = (module_name, obj)

        # Find all enum definitions
        enum_pattern = re.compile(
            r"\[\[([^\]]+)\]\]\s*\n"  # Anchor
            r"={3,5}\s+[_*]?([A-Za-z_]+)[_*]?\s+(?:enum|Enum)\s*\n"  # Title
            r"(.*?)"  # Content
            r"(?=\n\[\[|\n={3,5}\s+|\Z)",  # Until next section
            re.DOTALL,
        )

        for match in enum_pattern.finditer(content):
            anchor, name, section_content = match.groups()
            enum_obj = self._parse_enum_section(name, anchor, section_content)
            if enum_obj and enum_obj.enum_values:
                module.enums.append(enum_obj)
                self.global_enums[enum_obj.name] = enum_obj

        self.modules[module_name] = module

    def _parse_object_section(
        self, name: str, anchor: str, content: str, module_name: str
    ) -> Optional[ObjectDef]:
        """Parse an object section and extract properties from the table."""
        obj = ObjectDef(
            name=self._normalize_class_name(name),
            module=module_name,
            anchor=anchor,
            description="",
        )

        # Extract description (text before the table)
        desc_match = re.search(r"^(.*?)(?=\[cols=|\|===)", content, re.DOTALL)
        if desc_match:
            obj.description = desc_match.group(1).strip()[:200]

        # Find the properties table
        table_match = re.search(
            r'\[cols="[^"]*",\s*options="header"\]\s*\n\|===\s*\n'
            r"\|Property\s*\|Type\s*\|Card\.\s*\|Description\s*\n"
            r"(.*?)\n\|===",
            content,
            re.DOTALL | re.IGNORECASE,
        )

        if not table_match:
            return None

        table_content = table_match.group(1)
        obj.properties = self._parse_properties_table(table_content)

        return obj

    def _parse_properties_table(self, table_content: str) -> list[PropertyDef]:
        """Parse a properties table and extract PropertyDef objects."""
        properties = []

        # Split by row (each row starts with |)
        # Handle multi-line cells
        rows = self._split_table_rows(table_content)

        for row in rows:
            prop = self._parse_property_row(row)
            if prop:
                properties.append(prop)

        return properties

    def _split_table_rows(self, table_content: str) -> list[str]:
        """Split table content into rows, handling multi-line cells."""
        rows = []
        current_row = []
        lines = table_content.strip().split("\n")

        for line in lines:
            if line.startswith("|") and not line.startswith("|==="):
                # Count pipes to detect if this is a new row
                pipe_count = line.count("|")
                if pipe_count >= 4 and current_row:
                    # This looks like a new row, save the previous one
                    rows.append("\n".join(current_row))
                    current_row = [line]
                else:
                    current_row.append(line)
            elif current_row:
                current_row.append(line)

        if current_row:
            rows.append("\n".join(current_row))

        return rows

    def _parse_property_row(self, row: str) -> Optional[PropertyDef]:
        """Parse a single property row from the table."""
        # Clean up the row - remove anchors like [[...]]
        row = re.sub(r"\[\[[^\]]+\]\]", "", row)
        row = row.replace("\n", " ").strip()

        # Split by | but handle the complexity of nested content
        parts = self._split_table_cells(row)

        if len(parts) < 4:
            return None

        name = parts[0].strip()
        type_str = parts[1].strip()
        cardinality = parts[2].strip()
        description = parts[3].strip() if len(parts) > 3 else ""

        # Skip header rows or empty rows
        if not name or name.lower() == "property" or name == "===":
            return None

        # Clean name from any remaining artifacts
        name = re.sub(r"[^a-zA-Z0-9_]", "", name)
        if not name:
            return None

        prop = PropertyDef(
            name=self._to_snake_case(name),
            type_str=type_str,
            cardinality=cardinality,
            description=description[:200],
        )

        # Parse type information
        self._parse_type_info(prop)

        return prop

    def _split_table_cells(self, row: str) -> list[str]:
        """Split a table row into cells, handling nested content."""
        # Remove leading |
        row = row.lstrip("|")

        # Split by | but be careful with <<...>> references
        cells = []
        current = ""
        depth = 0

        for char in row:
            if char == "<":
                depth += 1
                current += char
            elif char == ">":
                depth -= 1
                current += char
            elif char == "|" and depth == 0:
                cells.append(current)
                current = ""
            else:
                current += char

        if current:
            cells.append(current)

        return cells

    def _parse_type_info(self, prop: PropertyDef):
        """Parse the type string and extract type information."""
        type_str = prop.type_str

        # Handle cardinality
        card = prop.cardinality.strip()
        if card == "?":
            prop.is_optional = True
        elif card == "*":
            prop.is_list = True
            prop.is_optional = True  # Empty list is valid
        elif card == "+":
            prop.is_list = True
            prop.is_optional = False  # Must have at least one

        # Parse type reference patterns like <<types.asciidoc#types_cistring_type,CiString>>(36)
        ref_pattern = re.compile(
            r"<<([^,>]+),([^>]+)>>(?:\((\d+)\)|\[(\d+)\])?"
        )
        ref_match = ref_pattern.search(type_str)

        if ref_match:
            ref_path, type_name, max_len1, max_len2 = ref_match.groups()
            max_len = max_len1 or max_len2
            prop.base_type = type_name.strip()

            if max_len:
                prop.max_length = int(max_len)

            # Check if it's an enum or class reference
            if "_enum" in ref_path.lower():
                prop.is_enum = True
            elif "_class" in ref_path.lower() or "_object" in ref_path.lower():
                prop.is_class = True

            # Extract module reference
            if "#" in ref_path:
                module_part = ref_path.split("#")[0]
                if module_part and module_part != "types.asciidoc":
                    prop.reference_module = module_part.replace(
                        "mod_", ""
                    ).replace(".asciidoc", "")
        else:
            # Handle simple types
            simple_type = type_str.strip()
            # Check for array notation like String[50]
            array_match = re.match(r"([A-Za-z]+)\[(\d+)\]", simple_type)
            if array_match:
                prop.base_type = array_match.group(1)
                prop.max_length = int(array_match.group(2))
            else:
                prop.base_type = simple_type

    def _parse_enum_section(
        self, name: str, anchor: str, content: str
    ) -> Optional[ObjectDef]:
        """Parse an enum section and extract values."""
        enum_obj = ObjectDef(
            name=self._normalize_class_name(name),
            module="",
            anchor=anchor,
            description="",
            is_enum=True,
        )

        # Find the enum values table
        table_match = re.search(
            r'\[cols="[^"]*",\s*options="header"\]\s*\n\|===\s*\n'
            r"\|Value\s*\|Description\s*\n"
            r"(.*?)\n\|===",
            content,
            re.DOTALL | re.IGNORECASE,
        )

        if not table_match:
            return None

        table_content = table_match.group(1)

        # Parse enum values
        for line in table_content.strip().split("\n"):
            if line.startswith("|") and not line.startswith("|==="):
                parts = line.split("|")
                if len(parts) >= 2:
                    value = parts[1].strip()
                    desc = parts[2].strip() if len(parts) > 2 else ""
                    if value and value.lower() != "value":
                        # Generate Python-friendly name
                        py_name = self._to_snake_case(value)
                        enum_obj.enum_values.append((py_name, value, desc[:100]))

        return enum_obj

    def _normalize_class_name(self, name: str) -> str:
        """Normalize a class name to PascalCase."""
        # Remove underscores and special chars, convert to PascalCase
        name = re.sub(r"[_\s]+", " ", name)
        return "".join(word.capitalize() for word in name.split())

    def _to_snake_case(self, name: str) -> str:
        """Convert a name to snake_case."""
        # Handle already snake_case
        if "_" in name and name.islower():
            return name
        # Convert CamelCase to snake_case
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def generate_pydantic_models(self, output_dir: Path):
        """Generate Pydantic model files for all parsed modules."""
        version_name = f"v_{self.version.replace('.', '_')}"

        for module_name, module in self.modules.items():
            module_dir = output_dir / module_name / version_name
            module_dir.mkdir(parents=True, exist_ok=True)

            # Generate enums.py
            enums_content = self._generate_enums_file(module)
            (module_dir / "enums.py").write_text(enums_content)

            # Generate schemas.py
            schemas_content = self._generate_schemas_file(module)
            (module_dir / "schemas.py").write_text(schemas_content)

            # Generate __init__.py
            init_content = self._generate_init_file(module)
            (module_dir / "__init__.py").write_text(init_content)

            # Create api directory
            api_dir = module_dir / "api"
            api_dir.mkdir(exist_ok=True)
            (api_dir / "__init__.py").write_text(
                f'"""API routers for {module_name} module v{self.version}."""\n'
            )

            print(f"Generated {module_name}/{version_name}/")

    def _generate_enums_file(self, module: ModuleDef) -> str:
        """Generate enums.py content for a module."""
        lines = [
            f'"""Enums for {module.name} module - OCPI {self.version}.',
            "",
            "Auto-generated from the official OCPI specification.",
            f"https://github.com/ocpi/ocpi/tree/release-{self.version}-bugfixes",
            '"""',
            "",
            "from enum import Enum",
            "",
        ]

        # Check if we should import from parent module (for shared enums)
        parent_enums_exist = (
            Path(f"py_ocpi/modules/{module.name}/enums.py").exists()
        )
        if parent_enums_exist:
            lines.append(f"from py_ocpi.modules.{module.name}.enums import *  # noqa")
            lines.append("")

        for enum_obj in module.enums:
            lines.append("")
            lines.append(f"class {enum_obj.name}(str, Enum):")
            lines.append(f'    """')
            lines.append(
                f"    https://github.com/ocpi/ocpi/blob/release-{self.version}-bugfixes/"
            )
            lines.append(f'    """')
            lines.append("")

            if not enum_obj.enum_values:
                lines.append("    pass")
            else:
                for py_name, value, desc in enum_obj.enum_values:
                    if desc:
                        lines.append(f"    # {desc}")
                    lines.append(f'    {py_name} = "{value}"')

            lines.append("")

        return "\n".join(lines)

    def _generate_schemas_file(self, module: ModuleDef) -> str:
        """Generate schemas.py content for a module."""
        lines = [
            f'"""Schemas for {module.name} module - OCPI {self.version}.',
            "",
            "Auto-generated from the official OCPI specification.",
            f"https://github.com/ocpi/ocpi/tree/release-{self.version}-bugfixes",
            '"""',
            "",
            "from typing import List, Optional",
            "",
            "from pydantic import BaseModel",
            "",
        ]

        # Collect imports
        imports = self._collect_imports(module)
        lines.extend(imports)
        lines.append("")

        # Generate classes
        for obj in module.objects:
            lines.extend(self._generate_class(obj))
            lines.append("")

        return "\n".join(lines)

    def _collect_imports(self, module: ModuleDef) -> list[str]:
        """Collect necessary imports for a module's schemas."""
        lines = []
        enum_imports = set()

        # Always import core data types
        lines.append(
            "from py_ocpi.core.data_types import ("
        )
        lines.append("    CiString,")
        lines.append("    DateTime,")
        lines.append("    DisplayText,")
        lines.append("    Number,")
        lines.append("    Price,")
        lines.append("    String,")
        lines.append("    URL,")
        lines.append(")")

        for obj in module.objects:
            for prop in obj.properties:
                # Check for enum references
                if prop.is_enum:
                    enum_imports.add(prop.base_type)

        # Add enum imports
        if enum_imports:
            version_name = f"v_{self.version.replace('.', '_')}"
            lines.append(
                f"from py_ocpi.modules.{module.name}.{version_name}.enums import ("
            )
            for e in sorted(enum_imports):
                lines.append(f"    {e},")
            lines.append(")")

        return lines

    def _generate_class(self, obj: ObjectDef) -> list[str]:
        """Generate a Pydantic class definition."""
        lines = [
            f"class {obj.name}(BaseModel):",
            f'    """',
            f"    https://github.com/ocpi/ocpi/blob/release-{self.version}-bugfixes/",
            f"    #{obj.anchor}",
            f'    """',
            "",
        ]

        if not obj.properties:
            lines.append("    pass")
            return lines

        for prop in obj.properties:
            type_annotation = self._get_type_annotation(prop)
            default = self._get_default_value(prop)

            if default:
                lines.append(f"    {prop.name}: {type_annotation} = {default}")
            else:
                lines.append(f"    {prop.name}: {type_annotation}")

        return lines

    def _get_type_annotation(self, prop: PropertyDef) -> str:
        """Get the Python type annotation for a property."""
        base = prop.base_type

        # Map to Python types
        if base.lower() in self.TYPE_MAPPING:
            base = self.TYPE_MAPPING[base.lower()]
        elif base in ["CiString", "String"]:
            if prop.max_length:
                base = f"{base}(max_length={prop.max_length})"
            else:
                base = "str"

        # Handle list types
        if prop.is_list:
            base = f"List[{base}]"

        # Handle optional types
        if prop.is_optional and not prop.is_list:
            base = f"Optional[{base}]"

        # Add type ignore comment for constrained types
        if "max_length=" in base:
            base = f"{base}  # type: ignore"

        return base

    def _get_default_value(self, prop: PropertyDef) -> str:
        """Get the default value for a property."""
        if prop.is_list:
            return "[]"
        if prop.is_optional:
            return "None"
        return ""

    def _generate_init_file(self, module: ModuleDef) -> str:
        """Generate __init__.py content for a module version."""
        return f'"""OCPI {self.version} {module.name} module."""\n'


def main():
    parser = argparse.ArgumentParser(
        description="Parse OCPI AsciiDoc specs and generate Pydantic models"
    )
    parser.add_argument(
        "--version",
        default="2.3.0",
        help="OCPI version to parse (default: 2.3.0)",
    )
    parser.add_argument(
        "--output",
        default="py_ocpi/modules",
        help="Output directory for generated files",
    )
    parser.add_argument(
        "--repo",
        help="Path to local OCPI repo (will clone if not provided)",
    )
    parser.add_argument(
        "--branch",
        help="Git branch to use (default: release-{version}-bugfixes)",
    )

    args = parser.parse_args()

    # Determine branch
    branch = args.branch or f"release-{args.version}-bugfixes"

    # Get repo path
    if args.repo:
        repo_path = Path(args.repo)
    else:
        ocpi_parser = OCPIParser("", args.version)
        repo_path = ocpi_parser.clone_repo(branch)

    # Parse and generate
    ocpi_parser = OCPIParser(str(repo_path), args.version)
    ocpi_parser.parse_all_modules()
    ocpi_parser.generate_pydantic_models(Path(args.output))

    print(f"\nGenerated OCPI {args.version} models in {args.output}/")


if __name__ == "__main__":
    main()
