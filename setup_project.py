"""
Project setup and configuration.
Run this after reorganization to verify everything works.
"""

import os
import sys
import json
from pathlib import Path

def check_structure():
    """Verify directory structure is correct."""
    required_dirs = ['data', 'results', 'docs', 'examples', 'tests']
    optional_dirs = ['src']
    
    print("Checking directory structure...")
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/ exists")
        else:
            print(f"  ✗ {dir_name}/ missing")
            os.makedirs(dir_name, exist_ok=True)
            print(f"    Created {dir_name}/")
    
    for dir_name in optional_dirs:
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/ exists (optional)")


def check_data_files():
    """Verify required data files exist."""
    data_dir = 'data'
    required_files = ['attribute_entity.json', 'numbered_entity.json']
    
    print("\nChecking data files...")
    for filename in required_files:
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            print(f"  ✓ {path} exists")
        else:
            # Check root directory
            if os.path.exists(filename):
                print(f"  → {filename} found in root, should be in data/")
            else:
                print(f"  ✗ {filename} missing")


def check_puzzle_files():
    """Check for generated puzzle files."""
    locations = [
        'zebra_puzzles_gurobi_100.json',
        'data/zebra_puzzles_gurobi_100.json',
        'data/generated/zebra_puzzles_gurobi_100.json'
    ]
    
    print("\nChecking for puzzle files...")
    found = False
    for loc in locations:
        if os.path.exists(loc):
            print(f"  ✓ Found: {loc}")
            try:
                with open(loc, 'r', encoding='utf-8') as f:
                    puzzles = json.load(f)
                print(f"    Contains {len(puzzles)} puzzles")
                found = True
            except Exception as e:
                print(f"    Error reading: {e}")
    
    if not found:
        print("  ⚠ No puzzle files found. Run generation script first.")


def check_imports():
    """Test if key modules can be imported."""
    print("\nChecking imports...")
    
    modules_to_test = [
        ('prompt_formatting', 'Prompt formatter'),
        ('test_llm_on_puzzles', 'LLM tester'),
        ('analyze_puzzles', 'Puzzle analyzer'),
    ]
    
    for module, description in modules_to_test:
        try:
            __import__(module)
            print(f"  ✓ {description} ({module})")
        except ImportError as e:
            print(f"  ✗ {description} ({module}): {e}")


def create_config():
    """Create a config file with paths."""
    config = {
        "data_dir": "data",
        "results_dir": "results",
        "docs_dir": "docs",
        "examples_dir": "examples",
        "attribute_file": "data/attribute_entity.json",
        "numbered_file": "data/numbered_entity.json",
        "default_puzzle_file": "data/generated/zebra_puzzles_gurobi_100.json"
    }
    
    config_file = "config.json"
    print(f"\nCreating {config_file}...")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f"  ✓ {config_file} created")


def print_summary():
    """Print setup summary."""
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nProject Structure:")
    print("  data/        - Input data (attribute_entity.json, etc.)")
    print("  results/     - Test outputs and results")
    print("  docs/        - Documentation")
    print("  examples/    - Example scripts")
    print("  tests/       - Unit tests")
    print("\nKey Files:")
    print("  zebra_abs_pro.py            - Core puzzle generator")
    print("  generate_100_with_gurobi.py - Batch generation")
    print("  test_llm_on_puzzles.py      - LLM testing")
    print("  example_llm_test.py         - Simple test example")
    print("\nNext Steps:")
    print("  1. Generate puzzles: python generate_100_with_gurobi.py")
    print("  2. Test LLM: python example_llm_test.py")
    print("  3. Analyze results: python analyze_puzzles.py")
    print()


def main():
    print("Zebra Puzzle Project Setup")
    print("="*60)
    print()
    
    check_structure()
    check_data_files()
    check_puzzle_files()
    check_imports()
    create_config()
    print_summary()


if __name__ == '__main__':
    main()
