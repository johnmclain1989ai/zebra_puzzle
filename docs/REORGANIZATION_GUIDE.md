# Code Reorganization Guide

## New Project Structure

```
zebra_puzzle/
├── src/                          # Source code
│   ├── __init__.py
│   ├── puzzle_generator.py      # Core puzzle generation (zebra_abs_pro.py)
│   ├── batch_generator.py       # Batch generation (generate_100_with_gurobi.py)
│   ├── llm_tester.py           # LLM testing (test_llm_on_puzzles.py)
│   ├── puzzle_analyzer.py       # Analysis tools (analyze_puzzles.py)
│   ├── prompt_formatter.py      # Prompt formatting (prompt_formatting.py)
│   └── utils.py                 # Utility functions
│
├── data/                         # Data files
│   ├── attribute_entity.json    # Attribute definitions
│   ├── numbered_entity.json     # Numerical attributes
│   └── generated/               # Generated puzzles
│       └── zebra_puzzles_gurobi_100.json
│
├── results/                      # Test results and outputs
│   ├── llm_test_results_*.json  # LLM test results
│   ├── puzzle_*_result.json     # Individual results
│   └── test_run_*.log           # Test logs
│
├── examples/                     # Example scripts
│   ├── example_llm_test.py      # Simple LLM testing example
│   ├── example_generate.py      # Puzzle generation example
│   └── example_analyze.py       # Analysis example
│
├── docs/                         # Documentation
│   ├── LLM_TESTING_GUIDE.md     # LLM testing documentation
│   ├── QUICK_START_GUIDE.md     # Quick start guide
│   └── API_REFERENCE.md         # API documentation
│
├── tests/                        # Unit tests
│   ├── test_clue_formatting.py
│   └── test_prompt_formatting.py
│
├── README.md                     # Main readme
├── requirements.txt              # Python dependencies
└── setup.py                      # Package setup

```

## Migration Steps

### Step 1: Move Source Files
```bash
# Move to src/
move zebra_abs_pro.py src/puzzle_generator.py
move generate_100_with_gurobi.py src/batch_generator.py
move test_llm_on_puzzles.py src/llm_tester.py
move analyze_puzzles.py src/puzzle_analyzer.py
move prompt_formatting.py src/prompt_formatter.py
```

### Step 2: Move Data Files
```bash
# Move to data/
move attribute_entity.json data/
move numbered_entity.json data/
move sample_puzzle.json data/
move single_puzzle_8000.json data/

# Create generated subdirectory
mkdir data\generated
move zebra_puzzles_gurobi_100.json data\generated\
```

### Step 3: Move Results
```bash
# Move to results/
move llm_test_results_*.json results/
move puzzle_*_result.json results/
move test_run_*.log results/
```

### Step 4: Move Examples
```bash
# Move to examples/
move example_llm_test.py examples/
```

### Step 5: Move Documentation
```bash
# Move to docs/
move LLM_TESTING_GUIDE.md docs/
move QUICK_START_GUIDE.md docs/
move CODE_UPDATE_SUMMARY.md docs/
move COMPLETE_DELIVERY_SUMMARY.md docs/
move EVALUATION_SUMMARY.md docs/
move SINGLE_PUZZLE_EXAMPLE.md docs/
move LLM_TEST_REPORT.md docs/
```

## Import Path Updates

After reorganization, update imports:

### Old:
```python
from zebra_abs_pro import build_matrix
from test_llm_on_puzzles import test_single_puzzle
```

### New:
```python
from src.puzzle_generator import build_matrix
from src.llm_tester import test_single_puzzle
```

## Benefits of New Structure

1. **Clear Separation**: Source code, data, results, and docs are separated
2. **Easier Navigation**: Related files are grouped together
3. **Better Scalability**: Easy to add new components
4. **Cleaner Root**: Main directory is not cluttered
5. **Standard Python Structure**: Follows Python packaging conventions

## Alternative: Keep Simple Structure

If you prefer a simpler structure for a small project:

```
zebra_puzzle/
├── zebra_abs_pro.py              # Keep core files in root
├── generate_100_with_gurobi.py
├── test_llm_on_puzzles.py
├── analyze_puzzles.py
├── prompt_formatting.py
├── example_llm_test.py
│
├── data/                          # Just separate data
│   ├── attribute_entity.json
│   ├── numbered_entity.json
│   └── puzzles/
│       └── zebra_puzzles_gurobi_100.json
│
├── results/                       # And results
│   └── (test outputs)
│
├── docs/                          # And documentation
│   └── (markdown files)
│
└── tests/
    └── (test files)
```

## Recommended Actions

**For immediate use (minimal changes):**
1. Create `data/`, `results/`, `docs/` folders
2. Move JSON data files to `data/`
3. Move test results to `results/`
4. Move documentation to `docs/`
5. Keep Python files in root

**For long-term maintainability:**
1. Implement full structure with `src/` directory
2. Create `setup.py` for package installation
3. Update all import paths
4. Add `__init__.py` files for proper Python packages
