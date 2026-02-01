# LLM Testing Guide for Zebra Puzzles

This guide explains how to use the newly implemented LLM testing system to evaluate language models on zebra puzzles.

## Overview

The testing system:
1. Loads generated puzzles from JSON
2. Converts them into natural language prompts
3. Sends prompts to an LLM via the `query_seek` API
4. Parses and evaluates the LLM's responses
5. Generates detailed evaluation reports

## Files

- **`test_llm_on_puzzles.py`**: Main testing script with full functionality
- **`example_llm_test.py`**: Simple examples demonstrating usage

## Quick Start

### Test a Single Puzzle

```python
python example_llm_test.py
```

This will:
- Load the first puzzle from the dataset
- Show the formatted prompt
- Send it to the LLM
- Display the response and evaluation

### Test Multiple Puzzles

```bash
# Test all puzzles in the dataset
python test_llm_on_puzzles.py

# Test first 10 puzzles
python test_llm_on_puzzles.py --num 10

# Test quietly (less output)
python test_llm_on_puzzles.py --num 5 --quiet

# Test a specific puzzle by ID
python test_llm_on_puzzles.py --single 3000
```

## Usage Examples

### Example 1: Test One Puzzle Programmatically

```python
import json
from test_llm_on_puzzles import test_single_puzzle

# Load puzzles
with open('zebra_puzzles_gurobi_100.json', 'r') as f:
    puzzles = json.load(f)

# Test first puzzle
result = test_single_puzzle(puzzles[0], verbose=True)

# Check result
if result['success'] and result['evaluation']['correct']:
    print("✓ LLM solved the puzzle correctly!")
else:
    print("✗ LLM failed to solve the puzzle")
    print("Errors:", result['evaluation']['errors'])
```

### Example 2: Test Multiple Puzzles and Analyze

```python
from test_llm_on_puzzles import test_multiple_puzzles

# Test first 20 puzzles
summary = test_multiple_puzzles(
    'zebra_puzzles_gurobi_100.json',
    num_puzzles=20,
    output_file='my_test_results.json',
    verbose=False
)

# Print statistics
print(f"Success rate: {summary['success_rate']:.1%}")
print(f"Average accuracy: {summary['average_accuracy']:.1%}")
```

### Example 3: Custom Prompt Format

```python
from test_llm_on_puzzles import format_puzzle_as_prompt
from util.query_seek import query as query_seek
import json

# Load a puzzle
with open('zebra_puzzles_gurobi_100.json', 'r') as f:
    puzzle = json.load(f)[0]

# Generate prompt
prompt = format_puzzle_as_prompt(puzzle)

# Customize prompt if needed
custom_prompt = prompt + "\n\nPlease explain your reasoning step by step."

# Query LLM
response = query_seek(custom_prompt)
print(response)
```

## Prompt Format

Puzzles are formatted as natural language prompts with the following structure:

```
# Zebra Puzzle

## Puzzle Setup
There are 3 persons, each with different attributes.

The dimensions and possible values are:
- **Name**: Alice, Bob, Charlie
- **Age**: 20, 25, 30
- **Color**: Red, Blue, Green

## Clues
Use the following 5 clues to determine the complete assignment:

1. The person with Age 20 also has Color Red.
2. The person with Name Alice also has Age 25.
3. ...

## Question
Based on the clues above, determine the complete solution.
For each dimension, provide the sequence of values corresponding to each person.

## Output Format
Please provide your answer in the following format:

Name: [value1, value2, value3]
Age: [value1, value2, value3]
Color: [value1, value2, value3]

Provide ONLY the solution in this exact format, no additional explanation.
```

## Output Format

### Console Output

When running tests, you'll see:
- Progress for each puzzle
- LLM responses
- Evaluation results
- Summary statistics

### JSON Output

Results are saved to JSON files with this structure:

```json
{
  "test_date": "2026-02-01T10:30:00",
  "puzzles_file": "zebra_puzzles_gurobi_100.json",
  "num_puzzles": 10,
  "correct_count": 7,
  "success_rate": 0.7,
  "average_accuracy": 0.85,
  "detailed_results": [
    {
      "puzzle_id": 3000,
      "prompt": "# Zebra Puzzle\n...",
      "response": "Name: [Alice, Bob, Charlie]\n...",
      "parsed_solution": {...},
      "evaluation": {
        "correct": true,
        "accuracy": 1.0,
        "num_correct_dimensions": 5,
        "total_dimensions": 5,
        "errors": []
      },
      "success": true
    },
    ...
  ]
}
```

## Evaluation Metrics

The system evaluates LLM responses using:

- **Correct**: Whether the entire solution is 100% correct
- **Accuracy**: Percentage of dimensions correctly solved
- **Dimension-level correctness**: Which specific dimensions were correct/incorrect
- **Errors**: Detailed error messages for incorrect dimensions

## Command-Line Options

```bash
python test_llm_on_puzzles.py [OPTIONS]

Options:
  --input FILE      Input JSON file with puzzles (default: zebra_puzzles_gurobi_100.json)
  --num N          Number of puzzles to test (default: all)
  --output FILE    Output JSON file for results (default: auto-generated)
  --quiet          Reduce output verbosity
  --single ID      Test a single puzzle by ID
```

## Advanced Usage

### Custom Evaluation Function

```python
from test_llm_on_puzzles import parse_llm_response, evaluate_solution

# Test with your own response
response = "Name: [Alice, Bob, Charlie]\nAge: [20, 25, 30]"
puzzle = {...}  # Your puzzle object

parsed = parse_llm_response(response, puzzle)
evaluation = evaluate_solution(parsed, puzzle['solution'], puzzle)

print(f"Accuracy: {evaluation['accuracy']:.1%}")
```

### Batch Processing

```python
import json
from test_llm_on_puzzles import test_single_puzzle

# Load all puzzles
with open('zebra_puzzles_gurobi_100.json', 'r') as f:
    puzzles = json.load(f)

# Test only puzzles with 4 persons
four_person_puzzles = [p for p in puzzles if p['num_persons'] == 4]

results = []
for puzzle in four_person_puzzles:
    result = test_single_puzzle(puzzle, verbose=False)
    results.append(result)

# Analyze
correct = sum(1 for r in results if r['success'] and r['evaluation']['correct'])
print(f"4-person puzzles: {correct}/{len(results)} correct")
```

## Troubleshooting

### Issue: LLM Response Format Not Recognized

**Solution**: The parser looks for patterns like `DimensionName: [value1, value2, ...]`. If the LLM uses a different format, you may need to adjust the `parse_llm_response` function.

### Issue: API Query Fails

**Solution**: Ensure the `util.query_seek` module is properly configured and accessible. Check API credentials if needed.

### Issue: Incorrect Evaluation

**Solution**: Verify that the puzzle JSON has the correct `solution` field format (list of lists, one per dimension).

## Next Steps

1. Run initial tests: `python example_llm_test.py`
2. Test on small batch: `python test_llm_on_puzzles.py --num 5`
3. Analyze results and adjust prompts if needed
4. Run full evaluation: `python test_llm_on_puzzles.py`
5. Compare different LLM models or prompt variations

## Integration with Existing Code

The testing system is designed to work seamlessly with the existing puzzle generation pipeline:

```
generate_100_with_gurobi.py  →  zebra_puzzles_gurobi_100.json
                                            ↓
                                 test_llm_on_puzzles.py
                                            ↓
                                llm_test_results_[timestamp].json
```

You can now have a complete workflow:
1. Generate puzzles with Gurobi
2. Test LLM performance
3. Analyze results
4. Iterate on puzzle difficulty or prompt design
