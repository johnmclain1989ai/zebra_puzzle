# Zebra Puzzle Generation Code
---

## ⭐ New: Natural Language Clues

Our generator now creates **conversational clues** like Brainzilla.com!

**Before:**
```
"The person with Height=130 also has Nationality=Englishman"
```

**After:**
```
"The Englishman lives in the Red house."
"The person who smokes Pall Mall rears Birds."
```

See [`NATURAL_CLUES_COMPARISON.md`](NATURAL_CLUES_COMPARISON.md) for details.

---

## Quick Start

```python
import json

# Load natural language puzzles (recommended)
with open('zebra_puzzles_natural.json', 'r', encoding='utf-8') as f:
    puzzles = json.load(f)

# Display first puzzle
p = puzzles[0]
print(f"Puzzle #{p['puzzle_id']}: {p['num_clues']} clues")
for i, clue in enumerate(p['clues'][:5], 1):
    print(f"{i}. {clue}")
```

---

## Datasets

| Dataset | Puzzles | Clues | Style | File |
|---------|---------|-------|-------|------|
| **Natural** ⭐ | 50 | 9.2 avg | Conversational | `zebra_puzzles_natural.json` |
| Simple | 100 | 9.6 avg | Mechanical | `zebra_puzzles_100_simple.json` |
| Gurobi | 99 | 15-25 | Mechanical | `zebra_puzzles_gurobi_100.json` |

**Recommendations:**
- **Education/Humans** → Natural dataset
- **Testing Solvers** → Simple dataset (largest)
- **Challenge** → Gurobi dataset (hardest)

---

## Generate Puzzles

```bash
# Natural language puzzles (recommended)
python generate_natural_clues.py --generate 50

# Simple puzzles (old style)
python generate_100_simple.py

# Gurobi puzzles (old style, requires license)
python generate_100_with_gurobi.py
```

---

## Data Format

```json
{
  "puzzle_id": 4000,
  "num_persons": 4,
  "dimensions": ["Name", "Age", "CarBrand", "Drink"],
  "entities": [["Albert", "Bernard", ...], [20, 21, ...], ...],
  "num_clues": 8,
  "clues": [
    "The person who is 20 years old drives Toyota.",
    "The owner of Ford drinks Tea."
  ],
  "solution": [["Albert", "Bernard", ...], ...],
  "generation_success": true
}
```

---

## Files

**Datasets:**
- `zebra_puzzles_natural.json` (165 KB) - 50 natural puzzles ⭐
- `zebra_puzzles_100_simple.json` (422 KB) - 100 mechanical puzzles
- `zebra_puzzles_gurobi_100.json` (305 KB) - 99 mechanical puzzles

**Generators:**
- `generate_natural_clues.py` - Natural language generator ⭐
- `generate_100_simple.py` - Simple generator (no Gurobi)
- `generate_100_with_gurobi.py` - Gurobi generator (requires license)

**Tools:**
- `analyze_puzzles.py` - Statistics and analysis

**Data:**
- `attribute_entity.json` - Entity data (names, colors, etc.)
- `numbered_entity.json` - Numbered entities (positions)

**Docs:**
- `NATURAL_CLUES_COMPARISON.md` - Natural language guide ⭐
- `COMPLETE_DELIVERY_SUMMARY.md` - Full technical documentation

---

## Natural Clue Examples

**Direct:** "The Brit lives in the Red house."
**Complex:** "The person who smokes Pall Mall rears Birds."
**Positional:** "The Norwegian lives in the first house."
**Negative:** "The Brazilian does not live in house two."

---

## Stats

- **Total Puzzles:** 249
- **Success Rate:** 99.6%
- **Puzzle Sizes:** 3-4 persons, 4-6 dimensions
- **Generation Time:** ~40-90 seconds per 100 puzzles

---

**Generated:** 2025-01-31
**Version:** 2.0 (Natural Language Clues)
**Status:** Production Ready
