# Zebra Puzzle Generator for LLM Testing

A Gurobi-based system for generating zebra puzzles to test and evaluate Large Language Models (LLMs) on logical reasoning tasks.

---

## 🎯 Purpose

This project generates zebra puzzles (logic grid puzzles) as **evaluation data for testing LLM reasoning capabilities**. The puzzles provide a controlled benchmark for assessing:
- Logical deduction
- Multi-step reasoning
- Constraint satisfaction
- Natural language understanding

---

## 🚀 Quick Start

```python
import json

# Load test puzzles for LLM evaluation
with open('zebra_puzzles_gurobi_100.json', 'r', encoding='utf-8') as f:
    puzzles = json.load(f)

# Example: Test LLM on first puzzle
puzzle = puzzles[0]
print(f"Puzzle with {puzzle['num_clues']} clues:")
for i, clue in enumerate(puzzle['clues'][:5], 1):
    print(f"{i}. {clue}")

print(f"\nGold Standard Solution: {puzzle['solution']}")
```

---

## 📊 Generated Dataset

| Dataset | Puzzles | Clues | Style | Purpose |
|---------|---------|-------|-------|---------|
| **Gurobi** | 99 | 15-25 avg | Mechanical | Complex reasoning testing |

All puzzles generated with professional optimization solver (Gurobi) and guaranteed unique solutions.

---

## 🛠️ Generator

### Gurobi-Based Generator

```bash
python generate_100_with_gurobi.py
```

**Requirements:**
- Valid Gurobi license
- Python 3.x
- Gurobi Python package (`gurobipy`)

**Features:**
- Professional optimization solver (Gurobi Optimizer)
- Complex puzzles (15-25 clues per puzzle)
- Fixed positional constraints (bug-free implementation)
- Guaranteed unique solutions via constraint satisfaction
- 99% success rate

---

## 📋 Why Use This for LLM Testing?

### 1. **Controlled Reasoning Complexity**
- 3-4 persons per puzzle
- 15-25 clues per puzzle (complex multi-step reasoning)
- Ground truth solutions for exact evaluation
- Consistent puzzle format

### 2. **Diverse Reasoning Types**
- Positive associations ("X has Y")
- Negative constraints ("X does not have Y")
- Positional reasoning ("X is left of Y", "X is next to Y")
- Multi-step deductions required

### 3. **Quality Guaranteed**
- Gold standard solutions (exactly one valid solution)
- All clues verified and consistent
- Professional constraint satisfaction solver
- Unique solution guarantee

### 4. **Scalable Benchmark Data**
- Generate unlimited puzzles with Gurobi
- Customizable difficulty levels
- Consistent format for automated testing

---

## 🎓 Example: Evaluating LLM Performance

```python
import json

# Load test puzzles
with open('zebra_puzzles_gurobi_100.json') as f:
    puzzles = json.load(f)

# Test LLM (pseudo-code)
correct = 0
total = len(puzzles)

for puzzle in puzzles:
    # Get LLM solution
    llm_solution = your_llm.solve(puzzle['clues'])

    # Compare with gold standard
    if llm_solution == puzzle['solution']:
        correct += 1

accuracy = correct / total
print(f"LLM Accuracy: {accuracy:.1%} ({correct}/{total} puzzles)")
```

---

## 📁 Project Files

**Generator:**
- `generate_100_with_gurobi.py` - Gurobi-based generator ⭐

**Generated Dataset:**
- `zebra_puzzles_gurobi_100.json` - 99 complex puzzles with gold solutions

**Tools:**
- `analyze_puzzles.py` - Statistics and analysis

**Data:**
- `attribute_entity.json` - Entity data (names, colors, etc.)
- `numbered_entity.json` - Numbered entities (positions, ages)

**Documentation:**
- `COMPLETE_DELIVERY_SUMMARY.md` - Technical details and methodology

---

## 🔧 Technical Details

### Constraint Satisfaction
All puzzles use CSP (Constraint Satisfaction Problem) formulation:
- Binary variables: `var[p][r][c]` = 1 if person p has attribute c in dimension r
- Solved with Gurobi optimizer (professional-grade solver)
- Guaranteed unique solutions
- Verified solvability

### Positional Constraints (FIXED)
This generator includes a **critical bug fix** for positional constraints:

**Original Bug:**
```python
# WRONG: Static comparison
position_value * sum(binary_vars) <= position_value * sum(binary_vars)
```

**Fixed Version (implemented here):**
```python
# CORRECT: Dynamic position calculation
pos_c1 = quicksum(position_values[p] * var[p][r1][c1] for p in range(num_persons))
pos_c2 = quicksum(position_values[p] * var[p][r2][c2] for p in range(num_persons))
m.addConstr(pos_c1 + 1 <= pos_c2)  # c1 is left of c2
```

### Key Features
- **Gold Standard Solutions:** Every puzzle has exactly one valid solution
- **Verified Clues:** All clues consistent with solution
- **Professional Solver:** Uses Gurobi optimization for constraint satisfaction
- **Fixed Positional Bugs:** Correct encoding of left/right positional constraints

---

## 📊 Statistics

- **Total Puzzles Generated:** 99
- **Success Rate:** 99% (1 failed to find unique solution)
- **Puzzle Sizes:** 3-4 persons, 4-6 dimensions
- **Clues per Puzzle:** 15-25 (complex reasoning)
- **Generation Time:** ~90 seconds for 100 puzzles

---

## 📖 Citation

If you use this generator or dataset in your research:

```bibtex
@misc{zebra_puzzle_generator_2025,
  title={Zebra Puzzle Generator for LLM Testing Using Gurobi Optimization},
  author={Your Name},
  year={2025},
  url={https://github.com/johnmclain1989ai/REPO_NAME}
}
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- More complex positional clues
- Conjunction clues ("X and Y")
- Conditional clues ("If X, then Y")
- Difficulty estimation metrics
- LLM evaluation benchmarks
- Alternative constraint solvers (CP-SAT, OR-Tools, etc.)

---

## 📝 License

This project is provided for research and educational purposes.

**Requirements:**
- Gurobi license (https://www.gurobi.com/)
- Academic license available for research use

---

**Generated:** 2025-01-31
**Version:** 2.0 (Gurobi-Based with Fixed Positional Constraints)
**Purpose:** LLM Evaluation & Testing
**Status:** Production Ready
