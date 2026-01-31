"""
Analyze and visualize the generated 100 zebra puzzles.
"""

import json
import os
from collections import Counter


def load_puzzles(filepath="zebra_puzzles_100_simple.json"):
    """Load puzzles from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_statistics(puzzles):
    """Print statistics about the puzzles."""
    print("=" * 70)
    print("PUZZLE STATISTICS")
    print("=" * 70)
    print()

    # Basic counts
    print(f"Total puzzles: {len(puzzles)}")
    print()

    # Distribution by number of persons
    person_counts = Counter(p['num_persons'] for p in puzzles)
    print("Distribution by number of persons:")
    for num_persons in sorted(person_counts.keys()):
        count = person_counts[num_persons]
        percentage = count / len(puzzles) * 100
        print(f"  {num_persons} persons: {count} puzzles ({percentage:.1f}%)")
    print()

    # Clue count distribution
    clue_counts = Counter(p['num_clues'] for p in puzzles)
    print("Clue count distribution:")
    for num_clues in sorted(clue_counts.keys()):
        count = clue_counts[num_clues]
        percentage = count / len(puzzles) * 100
        print(f"  {num_clues} clues: {count} puzzles ({percentage:.1f}%)")
    print()

    # Average clue count
    avg_clues = sum(p['num_clues'] for p in puzzles) / len(puzzles)
    print(f"Average clues per puzzle: {avg_clues:.1f}")
    print()

    # Dimension count distribution
    dim_counts = Counter(len(p['dimensions']) for p in puzzles)
    print("Dimension count distribution:")
    for num_dims in sorted(dim_counts.keys()):
        count = dim_counts[num_dims]
        percentage = count / len(puzzles) * 100
        print(f"  {num_dims} dimensions: {count} puzzles ({percentage:.1f}%)")
    print()

    # Dimension names
    all_dims = []
    for p in puzzles:
        all_dims.extend(p['dimensions'])
    dim_freq = Counter(all_dims)

    print("Most common dimensions:")
    for dim, count in dim_freq.most_common(10):
        percentage = count / len(puzzles) * 100
        print(f"  {dim}: {count} puzzles ({percentage:.1f}%)")
    print()


def analyze_clue_types(puzzles, sample_size=5):
    """Analyze clue types across puzzles."""
    print("=" * 70)
    print("CLUE ANALYSIS")
    print("=" * 70)
    print()

    total_clues = sum(p['num_clues'] for p in puzzles)

    # Count clue types
    positive_count = 0
    negative_count = 0
    positional_count = 0

    for p in puzzles:
        for clue in p.get('clues_data', []):
            clue_type = clue.get('type', 'unknown')
            if clue_type == 'positive':
                positive_count += 1
            elif clue_type == 'negative':
                negative_count += 1
            elif clue_type == 'positional':
                positional_count += 1

    if total_clues > 0:
        print(f"Total clues across all puzzles: {total_clues}")
        print()
        print("Clue type distribution:")
        print(f"  Positive associations: {positive_count} ({positive_count/total_clues*100:.1f}%)")
        print(f"  Negative associations: {negative_count} ({negative_count/total_clues*100:.1f}%)")
        print(f"  Positional clues: {positional_count} ({positional_count/total_clues*100:.1f}%)")
        print()

    # Sample clues
    print("Sample clues from first puzzle:")
    puzzle = puzzles[0]
    for i, clue in enumerate(puzzle['clues'][:sample_size], 1):
        print(f"  {i}. {clue}")
    print()


def export_single_puzzle(puzzle, output_file):
    """Export a single puzzle to a text file."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"PUZZLE #{puzzle['puzzle_id']}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("SETUP:")
    lines.append(f"  Number of persons: {puzzle['num_persons']}")
    lines.append("")
    lines.append("  Dimensions and values:")

    for dim_name, entities in zip(puzzle['dimensions'], puzzle['entities']):
        entities_str = ", ".join(str(e) for e in entities)
        lines.append(f"    {dim_name}: {entities_str}")

    lines.append("")
    lines.append("CLUES:")
    for i, clue in enumerate(puzzle['clues'], 1):
        lines.append(f"  {i}. {clue}")

    lines.append("")
    lines.append("SOLUTION:")
    for dim_name, solution_row in zip(puzzle['dimensions'], puzzle['solution']):
        solution_str = " | ".join(str(s) for s in solution_row)
        lines.append(f"  {dim_name}: {solution_str}")

    lines.append("")
    lines.append("=" * 70)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Exported puzzle #{puzzle['puzzle_id']} to {output_file}")


def export_all_puzzles_separately(puzzles, output_dir="individual_puzzles"):
    """Export each puzzle to a separate text file."""
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for puzzle in puzzles:
        output_file = os.path.join(output_dir, f"puzzle_{puzzle['puzzle_id']}.txt")
        export_single_puzzle(puzzle, output_file)

    print(f"\nExported {len(puzzles)} puzzles to {output_dir}/")


def print_puzzle_summary(puzzle):
    """Print a brief summary of a puzzle."""
    print(f"Puzzle #{puzzle['puzzle_id']}:")
    print(f"  {puzzle['num_persons']} persons, {len(puzzle['dimensions'])} dimensions, {puzzle['num_clues']} clues")
    print(f"  Dimensions: {', '.join(puzzle['dimensions'])}")
    print()


def main():
    """Main analysis function."""
    # Load puzzles
    print("Loading puzzles...")
    puzzles = load_puzzles()
    print(f"Loaded {len(puzzles)} puzzles\n")

    # Print statistics
    print_statistics(puzzles)

    # Analyze clues
    analyze_clue_types(puzzles)

    # Show sample puzzles
    print("=" * 70)
    print("SAMPLE PUZZLES")
    print("=" * 70)
    print()

    for i in range(min(3, len(puzzles))):
        print_puzzle_summary(puzzles[i])

    # Export options
    print("=" * 70)
    print("EXPORT OPTIONS")
    print("=" * 70)
    print()
    print("To export individual puzzles:")
    print("  python analyze_puzzles.py --export-all")
    print()
    print("To export a specific puzzle:")
    print("  python analyze_puzzles.py --export-id 2000")
    print()


if __name__ == "__main__":
    import sys

    puzzles = load_puzzles()

    if "--export-all" in sys.argv:
        export_all_puzzles_separately(puzzles)
    elif "--export-id" in sys.argv:
        idx = sys.argv.index("--export-id")
        if idx + 1 < len(sys.argv):
            puzzle_id = int(sys.argv[idx + 1])
            puzzle = next((p for p in puzzles if p['puzzle_id'] == puzzle_id), None)
            if puzzle:
                export_single_puzzle(puzzle, f"puzzle_{puzzle_id}.txt")
            else:
                print(f"Puzzle #{puzzle_id} not found")
        else:
            print("Please provide a puzzle ID")
    else:
        main()
