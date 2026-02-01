"""
Simple example demonstrating how to test LLM on a single puzzle.
"""

import sys
import os
import json

# Setup paths - add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_llm_on_puzzles import format_puzzle_as_prompt, test_single_puzzle

# Try to import from util, fallback to mock from test module
try:
    from util.query_seek import query as query_seek
except ModuleNotFoundError:
    from test_llm_on_puzzles import query_seek


def example_single_puzzle():
    """Example: Test LLM on first puzzle from dataset."""
    
    # Try multiple possible locations for puzzle file
    puzzle_files = [
        '../data/generated/zebra_puzzles_gurobi_100.json',
        'data/generated/zebra_puzzles_gurobi_100.json',
        '../zebra_puzzles_gurobi_100.json',
        'zebra_puzzles_gurobi_100.json'
    ]
    
    puzzles = None
    puzzle_file_used = None
    
    for puzzle_file in puzzle_files:
        if os.path.exists(puzzle_file):
            try:
                with open(puzzle_file, 'r', encoding='utf-8') as f:
                    puzzles = json.load(f)
                puzzle_file_used = puzzle_file
                break
            except Exception as e:
                print(f"Error loading {puzzle_file}: {e}")
                continue
    
    if puzzles is None:
        print("ERROR: Could not find puzzle file. Tried:")
        for pf in puzzle_files:
            print(f"  - {pf}")
        return
    
    # Get first puzzle
    puzzle = puzzles[0]
    
    print("="*70)
    print("EXAMPLE: Testing LLM on a Single Puzzle")
    print("="*70)
    
    # Show the prompt that will be sent to the LLM
    prompt = format_puzzle_as_prompt(puzzle)
    print("\n1. PROMPT TO BE SENT TO LLM:")
    print("-"*70)
    print(prompt)
    print("-"*70)
    
    # Test the puzzle
    print("\n2. SENDING TO LLM AND EVALUATING...\n")
    result = test_single_puzzle(puzzle, verbose=True)
    
    # Show summary
    print("\n3. SUMMARY:")
    print("-"*70)
    if result['success']:
        print(f"[OK] LLM responded successfully")
        print(f"[INFO] Correct: {result['evaluation']['correct']}")
        print(f"[INFO] Accuracy: {result['evaluation']['accuracy']:.1%}")
    else:
        print(f"[ERROR] Error: {result.get('error', 'Unknown error')}")
    print("-"*70)


def example_custom_prompt():
    """Example: Manually create a prompt and query the LLM."""
    
    print("\n" + "="*70)
    print("EXAMPLE: Custom Prompt to LLM")
    print("="*70)
    
    # Create a simple custom prompt
    prompt = """
# Logic Puzzle

Solve the following logic puzzle:

There are 3 people: Alice, Bob, and Charlie.
Each has a different favorite color: Red, Blue, or Green.
Each has a different age: 20, 25, or 30.

Clues:
1. Alice is not 20 years old.
2. The person who likes Blue is 25 years old.
3. Bob likes Red.
4. Charlie is 30 years old.

Question: What is each person's age and favorite color?

Provide your answer in this format:
Alice: age=[age], color=[color]
Bob: age=[age], color=[color]
Charlie: age=[age], color=[color]
"""
    
    print("\nPrompt:")
    print("-"*70)
    print(prompt)
    print("-"*70)
    
    # Query LLM
    print("\nQuerying LLM...")
    response = query_seek(prompt)
    
    print("\nLLM Response:")
    print("-"*70)
    print(response)
    print("-"*70)


if __name__ == '__main__':
    # Run first example
    example_single_puzzle()
    
    # Optionally run second example
    # example_custom_prompt()
