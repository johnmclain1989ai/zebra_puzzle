# Zebra Puzzle Generator for LLM Testing

A comprehensive system for generating zebra puzzles to test and evaluate Large Language Models (LLMs) on logical reasoning tasks.

---

## 🎯 Purpose

This project generates zebra puzzles (logic grid puzzles) as **evaluation data for testing LLM reasoning capabilities**. The puzzles provide a controlled benchmark for assessing:
- Logical deduction
- Multi-step reasoning
- Constraint satisfaction
- Natural language understanding

---

## ⭐ New: Natural Language Clues

Our generator now creates **conversational clues** similar to Brainzilla.com!

**Before:**
```
"The person with Height=130 also has Nationality=Englishman"
```

**After:**
```
"The Englishman lives in the Red house."
"The person who smokes Pall Mall rears Birds."
```

This natural language format provides more realistic evaluation data for LLMs.

---

## 🚀 Quick Start

```python
import json

# Load test puzzles for LLM evaluation
with open('zebra_puzzles_natural.json', 'r', encoding='utf-8') as f:
    puzzles = json.load(f)

# Example: Test LLM on first puzzle
puzzle = puzzles[0]
print(f"Puzzle with {puzzle['num_clues']} clues:")
for i, clue in enumerate(puzzle['clues'][:5], 1):
    print(f"{i}. {clue}")

print(f"\nGold Standard Solution: {puzzle['solution']}")
```

---

## 📊 Generated Datasets

| Dataset | Puzzles | Clues | Style | Purpose |
|---------|---------|-------|-------|---------|
| **Natural** ⭐ | 50 | 9.2 avg | Conversational | LLM evaluation (human-like) |
| Simple | 100 | 9.6 avg | Mechanical | Baseline testing |
| Gurobi | 99 | 15-25 | Mechanical | Complex reasoning |

**Total:** 249 unique puzzles with gold standard solutions

---

## 🛠️ Generator Scripts

### 1. Natural Language Generator ⭐

```bash
python generate_natural_clues.py --generate 50
```

**Features:**
- Natural language templates (5 types)
- Brainzilla-style conversational clues
- Grammatically correct output
- Perfect for LLM evaluation

### 2. Simple Generator

```bash
python generate_100_simple.py
```

**Features:**
- No external dependencies
- Mechanical clue format
- 100% success rate
- Fast generation

### 3. Gurobi Generator

```bash
python generate_100_with_gurobi.py
```

**Features:**
- Professional optimization solver
- Complex puzzles (15-25 clues)
- Fixed positional constraints
- Requires Gurobi license

---

## 📋 Why Use This for LLM Testing?

### 1. **Controlled Reasoning Complexity**
- Easy (3 houses, 6 clues) to Hard (4 houses, 25 clues)
- Ground truth solutions for exact evaluation
- Measurable difficulty progression

### 2. **Diverse Reasoning Types**
- Positive associations ("X has Y")
- Negative constraints ("X does not have Y")
- Positional reasoning ("X is left of Y")
- Multi-step deductions

### 3. **Natural Language Evaluation**
- Conversational clue format tests real-world understanding
- Varied phrasing prevents overfitting
- Grammar and coherence assessment

### 4. **Scalable Benchmark Data**
- Generate unlimited puzzles
- Customizable difficulty levels
- Consistent format for automated testing

---

## 🎓 Example: Evaluating LLM Performance

```python
import json

# Load test puzzles
with open('zebra_puzzles_natural.json') as f:
    puzzles = json.load(f)

# Test LLM (pseudo-code)
correct = 0
for puzzle in puzzles:
    # Get LLM solution
    llm_solution = your_llm.solve(puzzle['clues'])

    # Compare with gold standard
    if llm_solution == puzzle['solution']:
        correct += 1

accuracy = correct / len(puzzles)
print(f"LLM Accuracy: {accuracy:.1%}")
```

---

## 📁 Project Files

**Generator Scripts:**
- `generate_natural_clues.py` - Natural language generator ⭐
- `generate_100_simple.py` - Simple generator (no Gurobi)
- `generate_100_with_gurobi.py` - Gurobi generator (requires license)

**Generated Datasets:**
- `zebra_puzzles_natural.json` - 50 natural puzzles ⭐
- `zebra_puzzles_100_simple.json` - 100 mechanical puzzles
- `zebra_puzzles_gurobi_100.json` - 99 complex mechanical puzzles

**Tools:**
- `analyze_puzzles.py` - Statistics and analysis

**Data:**
- `attribute_entity.json` - Entity data (names, colors, etc.)
- `numbered_entity.json` - Numbered entities (positions, ages)

**Documentation:**
- `NATURAL_CLUES_COMPARISON.md` - Natural language guide
- `COMPLETE_DELIVERY_SUMMARY.md` - Technical details

---

## 🎨 Natural Clue Examples

**Direct:** "The Brit lives in the Red house."
**Complex:** "The person who smokes Pall Mall rears Birds."
**Positional:** "The Norwegian lives in the first house."
**Negative:** "The Brazilian does not live in house two."

---

## 📊 Statistics

- **Total Puzzles Generated:** 249
- **Success Rate:** 99.6%
- **Puzzle Sizes:** 3-4 persons, 4-6 dimensions
- **Generation Time:** ~40-90 seconds per 100 puzzles

---

## 🔧 Technical Details

### Constraint Satisfaction
All puzzles use CSP (Constraint Satisfaction Problem) formulation:
- Binary variables: `var[p][r][c]` = 1 if person p has attribute c in dimension r
- Guaranteed unique solutions
- Verified solvability

### Key Features
- **Gold Standard Solutions:** Every puzzle has exactly one valid solution
- **Verified Clues:** All clues consistent with solution
- **Multiple Templates:** 5 natural language templates prevent overfitting

---

## 📖 Citation

If you use this generator or dataset in your research:

```bibtex
@misc{zebra_puzzle_generator_2025,
  title={Zebra Puzzle Generator for LLM Testing},
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

---

**Generated:** 2025-01-31
**Version:** 2.0 (Natural Language Clues)
**Purpose:** LLM Evaluation & Testing
**Status:** Production Ready
