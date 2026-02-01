"""
Test LLMs on generated zebra puzzles.

This script loads puzzles from JSON, formats them as natural language prompts,
sends them to an LLM via query_seek, and evaluates the responses.
"""

import sys
import os
import json
import re
from datetime import datetime

# Setup paths - add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import from util, fallback to local implementation
try:
    from util.query_seek import query as query_seek
except ModuleNotFoundError:
    # Fallback: Mock query function for testing
    def query_seek(prompt):
        print("[WARNING] Using mock query_seek - util module not found")
        print("[INFO] Install util module or implement query_seek for actual LLM testing")
        return "MOCK RESPONSE - Replace with actual LLM integration"


def format_puzzle_as_prompt(puzzle):
    """
    Convert a puzzle JSON object into a natural language prompt for LLM testing.
    
    Returns a string that asks the LLM to solve the puzzle.
    """
    prompt_parts = []
    
    # Title
    prompt_parts.append("# Zebra Puzzle\n")
    
    # Setup section
    prompt_parts.append("## Puzzle Setup\n")
    prompt_parts.append(f"There are {puzzle['num_persons']} persons, each with different attributes.\n")
    prompt_parts.append("\nThe dimensions and possible values are:\n")
    
    for dim_name, entities in zip(puzzle['dimensions'], puzzle['entities']):
        entities_str = ", ".join(str(e) for e in entities)
        prompt_parts.append(f"- **{dim_name}**: {entities_str}\n")
    
    # Clues section
    prompt_parts.append(f"\n## Clues\n")
    prompt_parts.append(f"Use the following {puzzle['num_clues']} clues to determine the complete assignment:\n\n")
    
    for i, clue in enumerate(puzzle['clues'], 1):
        prompt_parts.append(f"{i}. {clue}\n")
    
    # Question section
    prompt_parts.append("\n## Question\n")
    prompt_parts.append("Based on the clues above, determine the complete solution.\n")
    prompt_parts.append("For each dimension, provide the sequence of values corresponding to each person.\n\n")
    
    # Format instructions
    prompt_parts.append("## Output Format\n")
    prompt_parts.append("Please provide your answer in the following format:\n\n")
    
    for dim_name in puzzle['dimensions']:
        prompt_parts.append(f"{dim_name}: [value1, value2, ...]\n")
    
    prompt_parts.append("\nProvide ONLY the solution in this exact format, no additional explanation.\n")
    
    return "".join(prompt_parts)


def parse_llm_response(response, puzzle):
    """
    Parse the LLM's response and extract the solution.
    
    Returns a dict mapping dimension names to lists of values.
    """
    solution = {}
    
    # Try to extract each dimension's solution
    for dim_name in puzzle['dimensions']:
        # Look for patterns like "DimensionName: [value1, value2, ...]"
        # or "DimensionName: value1, value2, ..."
        pattern = rf"{re.escape(dim_name)}\s*:\s*\[?([^\n\]]+)\]?"
        match = re.search(pattern, response, re.IGNORECASE)
        
        if match:
            values_str = match.group(1).strip()
            # Split by comma and clean up
            values = [v.strip().strip('"').strip("'") for v in values_str.split(',')]
            solution[dim_name] = values
        else:
            # Try alternative format: look for dimension name followed by values on next line
            pattern = rf"{re.escape(dim_name)}\s*:?\s*\n\s*(.+?)(?:\n|$)"
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                values_str = match.group(1).strip()
                values = [v.strip().strip('"').strip("'") for v in values_str.split(',')]
                solution[dim_name] = values
    
    return solution


def evaluate_solution(parsed_solution, gold_solution, puzzle):
    """
    Compare the parsed LLM solution against the gold standard.

    Returns a dict with evaluation metrics.
    """
    results = {
        'correct': False,
        'dimensions_correct': {},
        'num_correct_dimensions': 0,
        'total_dimensions': len(puzzle['dimensions']),
        'accuracy': 0.0,
        'errors': []
    }

    all_correct = True

    for i, dim_name in enumerate(puzzle['dimensions']):
        # Convert gold solution indices to actual entity values
        if i == 0:  # Name dimension - use entities directly
            gold = [str(v) for v in puzzle['entities'][i]]
        else:
            # For other dimensions, map indices to entity values
            gold_indices = gold_solution[i]
            gold = [str(puzzle['entities'][i][idx]) for idx in gold_indices]

        if dim_name not in parsed_solution:
            results['dimensions_correct'][dim_name] = False
            results['errors'].append(f"Missing dimension: {dim_name}")
            all_correct = False
            continue

        pred = [str(v) for v in parsed_solution[dim_name]]

        # Check if lists match exactly
        if len(pred) != len(gold):
            results['dimensions_correct'][dim_name] = False
            results['errors'].append(
                f"{dim_name}: Length mismatch (predicted {len(pred)}, expected {len(gold)})"
            )
            all_correct = False
        elif pred == gold:
            results['dimensions_correct'][dim_name] = True
            results['num_correct_dimensions'] += 1
        else:
            results['dimensions_correct'][dim_name] = False
            results['errors'].append(
                f"{dim_name}: Incorrect values (predicted {pred}, expected {gold})"
            )
            all_correct = False
    
    results['correct'] = all_correct
    results['accuracy'] = results['num_correct_dimensions'] / results['total_dimensions']
    
    return results


def test_single_puzzle(puzzle, verbose=True):
    """
    Test the LLM on a single puzzle.
    
    Returns a dict with test results.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"Testing Puzzle #{puzzle['puzzle_id']}")
        print(f"{'='*70}")
        print(f"Dimensions: {puzzle['num_persons']} persons, {len(puzzle['dimensions'])} dimensions")
        print(f"Clues: {puzzle['num_clues']}")
    
    # Format puzzle as prompt
    prompt = format_puzzle_as_prompt(puzzle)
    
    if verbose:
        print("\nPrompt sent to LLM:")
        print("-" * 70)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("-" * 70)
    
    # Query the LLM
    try:
        response = query_seek(prompt)
        
        if verbose:
            print("\nLLM Response:")
            print("-" * 70)
            print(response)
            print("-" * 70)
        
        # Parse the response
        parsed_solution = parse_llm_response(response, puzzle)
        
        # Evaluate
        evaluation = evaluate_solution(parsed_solution, puzzle['solution'], puzzle)
        
        if verbose:
            print(f"\nEvaluation:")
            print(f"Correct: {evaluation['correct']}")
            print(f"Accuracy: {evaluation['accuracy']:.2%}")
            print(f"Dimensions correct: {evaluation['num_correct_dimensions']}/{evaluation['total_dimensions']}")
            
            if evaluation['errors']:
                print("\nErrors:")
                for error in evaluation['errors']:
                    print(f"  - {error}")
        
        return {
            'puzzle_id': puzzle['puzzle_id'],
            'prompt': prompt,
            'response': response,
            'parsed_solution': parsed_solution,
            'evaluation': evaluation,
            'success': True
        }
    
    except Exception as e:
        error_msg = f"Error testing puzzle: {str(e)}"
        if verbose:
            print(f"\n{error_msg}")
        
        return {
            'puzzle_id': puzzle['puzzle_id'],
            'success': False,
            'error': error_msg
        }


def test_multiple_puzzles(puzzles_file, num_puzzles=None, output_file=None, verbose=True):
    """
    Test the LLM on multiple puzzles from a JSON file.
    
    Args:
        puzzles_file: Path to JSON file with puzzles
        num_puzzles: Number of puzzles to test (None = all)
        output_file: Path to save results JSON (None = auto-generate)
        verbose: Whether to print detailed output
    """
    # Load puzzles
    with open(puzzles_file, 'r', encoding='utf-8') as f:
        puzzles = json.load(f)
    
    if num_puzzles:
        puzzles = puzzles[:num_puzzles]
    
    print(f"\n{'='*70}")
    print(f"LLM TESTING ON ZEBRA PUZZLES")
    print(f"{'='*70}")
    print(f"Puzzles file: {puzzles_file}")
    print(f"Number of puzzles: {len(puzzles)}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # Test each puzzle
    results = []
    correct_count = 0
    total_accuracy = 0.0
    
    for i, puzzle in enumerate(puzzles, 1):
        print(f"\n[{i}/{len(puzzles)}] ", end="")
        result = test_single_puzzle(puzzle, verbose=verbose)
        results.append(result)
        
        if result['success'] and result['evaluation']['correct']:
            correct_count += 1
        
        if result['success']:
            total_accuracy += result['evaluation']['accuracy']
        
        # Brief progress update if not verbose
        if not verbose:
            status = "[OK]" if (result['success'] and result['evaluation']['correct']) else "[FAIL]"
            print(f"Puzzle #{puzzle['puzzle_id']}: {status}")
    
    # Summary statistics
    print(f"\n{'='*70}")
    print("TESTING SUMMARY")
    print(f"{'='*70}")
    print(f"Total puzzles: {len(puzzles)}")
    print(f"Successful responses: {sum(1 for r in results if r['success'])}")
    print(f"Completely correct: {correct_count}")
    print(f"Success rate: {correct_count/len(puzzles)*100:.1f}%")
    print(f"Average accuracy: {total_accuracy/len(puzzles)*100:.1f}%")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save results
    if output_file is None:
        output_file = f"llm_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    summary = {
        'test_date': datetime.now().isoformat(),
        'puzzles_file': puzzles_file,
        'num_puzzles': len(puzzles),
        'correct_count': correct_count,
        'success_rate': correct_count / len(puzzles),
        'average_accuracy': total_accuracy / len(puzzles),
        'detailed_results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_file}")
    print(f"{'='*70}\n")
    
    return summary


def main():
    """Main function to run LLM tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test LLM on zebra puzzles')
    parser.add_argument(
        '--input',
        default='data/generated/zebra_puzzles_gurobi_100.json',
        help='Input JSON file with puzzles'
    )
    parser.add_argument(
        '--num',
        type=int,
        default=None,
        help='Number of puzzles to test (default: all)'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Output JSON file for results (default: auto-generated)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )
    parser.add_argument(
        '--single',
        type=int,
        default=None,
        help='Test a single puzzle by ID'
    )
    
    args = parser.parse_args()
    
    if args.single is not None:
        # Test single puzzle
        with open(args.input, 'r', encoding='utf-8') as f:
            puzzles = json.load(f)
        
        puzzle = next((p for p in puzzles if p['puzzle_id'] == args.single), None)
        
        if puzzle is None:
            print(f"Error: Puzzle with ID {args.single} not found")
            return
        
        result = test_single_puzzle(puzzle, verbose=True)
        
        # Save single result
        output_file = f"puzzle_{args.single}_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nResult saved to: {output_file}")
    else:
        # Test multiple puzzles
        test_multiple_puzzles(
            args.input,
            num_puzzles=args.num,
            output_file=args.output,
            verbose=not args.quiet
        )


if __name__ == '__main__':
    main()
