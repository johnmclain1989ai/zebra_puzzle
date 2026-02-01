# Quick Start Guide

**Last Updated:** 2026-02-01

---

## 🎯 What Can You Do?

### 1. Generate Zebra Puzzles
```bash
python generate_100_with_gurobi.py
```
**Output:** `zebra_puzzles_gurobi_100.json` with 99 puzzles

### 2. Test LLM on Single Puzzle
```bash
python example_llm_test.py
```
**Output:** Console display of prompt, response, and evaluation

### 3. Test LLM on Multiple Puzzles
```bash
# Test first 10 puzzles
python test_llm_on_puzzles.py --num 10

# Test all puzzles
python test_llm_on_puzzles.py

# Test specific puzzle by ID
python test_llm_on_puzzles.py --single 3000

# Quiet mode (less output)
python test_llm_on_puzzles.py --num 5 --quiet
```
**Output:** `llm_test_results_[timestamp].json` with detailed results

### 4. Analyze Generated Puzzles
```bash
python analyze_puzzles.py zebra_puzzles_gurobi_100.json
```
**Output:** Statistics about puzzle difficulty, clue distribution, etc.

---

## 📂 Key Files

### Generator
- `generate_100_with_gurobi.py` - Main puzzle generator

### LLM Testing
- `test_llm_on_puzzles.py` - Test LLM on puzzles
- `example_llm_test.py` - Simple example

### Data
- `zebra_puzzles_gurobi_100.json` - 99 generated puzzles
- `attribute_entity.json` - Entity data
- `numbered_entity.json` - Numbered entities

### Documentation
- `README.md` - Project overview and usage
- `LLM_TESTING_GUIDE.md` - Detailed LLM testing guide
- `CODE_UPDATE_SUMMARY.md` - Recent changes summary
- `COMPLETE_DELIVERY_SUMMARY.md` - Technical details

---

## 💡 Python Quick Examples

### Load and Display a Puzzle
```python
import json

with open('zebra_puzzles_gurobi_100.json', 'r', encoding='utf-8') as f:
    puzzles = json.load(f)

puzzle = puzzles[0]
print(f"Puzzle #{puzzle['puzzle_id']}")
print(f"Dimensions: {', '.join(puzzle['dimensions'])}")
print(f"Clues: {puzzle['num_clues']}")
```

### Test LLM Programmatically
```python
from test_llm_on_puzzles import test_single_puzzle

result = test_single_puzzle(puzzle, verbose=True)

if result['success'] and result['evaluation']['correct']:
    print("✓ Correct!")
else:
    print(f"✗ Accuracy: {result['evaluation']['accuracy']:.1%}")
```

### Generate Custom Prompt
```python
from test_llm_on_puzzles import format_puzzle_as_prompt

prompt = format_puzzle_as_prompt(puzzle)
print(prompt)
```

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_clue_formatting.py -v
```

**Expected Output:** 6 passed in ~2 seconds

---

## 📊 Typical Results

### Puzzle Generation
- Time: ~90 seconds for 100 puzzles
- Success Rate: 98-99%
- Puzzle Size: 3-4 persons, 5-6 dimensions
- Clues: 15-25 per puzzle

### LLM Testing
- Metrics: Success rate, accuracy per dimension
- Output: JSON with prompts, responses, evaluations
- Analysis: Error tracking and detailed reports

---

## ⚙️ Requirements

- Python 3.x
- Gurobi license (for puzzle generation)
- Gurobi Python package (`gurobipy`)

---

## 🐛 Troubleshooting

### Issue: "Gurobi license not valid"
**Solution:** Ensure Gurobi is properly installed and licensed

### Issue: "Module not found: util.query_seek"
**Solution:** Ensure the util directory is properly configured

### Issue: "Import error for gurobipy"
**Solution:** Install gurobipy: `pip install gurobipy`

---

## 📖 Full Documentation

- **LLM Testing:** See `LLM_TESTING_GUIDE.md`
- **Technical Details:** See `COMPLETE_DELIVERY_SUMMARY.md`
- **Recent Changes:** See `CODE_UPDATE_SUMMARY.md`
- **Project Overview:** See `README.md`

---

## 🎯 Common Workflows

### Workflow 1: Generate and Test
```bash
# Step 1: Generate puzzles
python generate_100_with_gurobi.py

# Step 2: Test LLM on 5 puzzles
python test_llm_on_puzzles.py --num 5

# Step 3: Check results
# Results saved to: llm_test_results_[timestamp].json
```

### Workflow 2: Analyze Puzzle Difficulty
```bash
# Step 1: Generate puzzles
python generate_100_with_gurobi.py

# Step 2: Analyze statistics
python analyze_puzzles.py zebra_puzzles_gurobi_100.json

# Step 3: Review statistics output
```

### Workflow 3: Custom LLM Evaluation
```python
import json
from test_llm_on_puzzles import format_puzzle_as_prompt
from util.query_seek import query as query_seek

# Load puzzle
with open('zebra_puzzles_gurobi_100.json', 'r') as f:
    puzzle = json.load(f)[0]

# Create custom prompt
prompt = format_puzzle_as_prompt(puzzle)
custom_prompt = prompt + "\n\nThink step by step and explain your reasoning."

# Query LLM
response = query_seek(custom_prompt)
print(response)
```

---

**Quick Reference** - Keep this guide handy for common tasks!
