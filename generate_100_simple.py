"""
Generate 100 Zebra Puzzles WITHOUT Gurobi

This script generates zebra puzzles using a backtracking approach
instead of Gurobi optimization solver.
"""

import json
import random
import copy
from itertools import permutations


class SimpleZebraPuzzleGenerator:
    """Generate zebra puzzles using backtracking search."""

    def __init__(self):
        # Load entity data
        with open('attribute_entity.json', 'r') as f:
            self.attribute_entities = json.load(f)
        with open('numbered_entity.json', 'r') as f:
            self.numbered_entities = json.load(f)

    def generate_solution(self, num_persons=3):
        """
        Generate a random valid solution (permutation matrix).

        Args:
            num_persons: Number of persons/houses

        Returns:
            dict: Solution with dimensions and assignments
        """
        # Select dimensions
        dim_names = ["Name"]
        entities = []

        # Names (first dimension)
        names = self.attribute_entities['Name'][:num_persons]
        random.shuffle(names)
        entities.append(names)

        # Second dimension: numbered entity
        num_category = random.choice(list(self.numbered_entities.keys()))
        num_values = self.numbered_entities[num_category][:num_persons]
        entities.append(num_values)
        dim_names.append(num_category)

        # Additional dimensions
        available_attrs = [k for k in self.attribute_entities.keys() if k != 'Name']
        num_extra_dims = random.randint(2, 4)

        for _ in range(num_extra_dims):
            attr_name = random.choice(available_attrs)
            attr_values = self.attribute_entities[attr_name][:num_persons]
            random.shuffle(attr_values)
            entities.append(attr_values)
            dim_names.append(attr_name)

        # Create solution: each dimension is a permutation
        solution = []
        for i in range(len(dim_names)):
            if i == 0:
                # Names stay in order
                solution.append(list(range(num_persons)))
            else:
                # Random permutation for other dimensions
                perm = list(range(num_persons))
                random.shuffle(perm)
                solution.append(perm)

        return {
            'num_persons': num_persons,
            'dim_names': dim_names,
            'entities': entities,
            'solution': solution
        }

    def generate_clues_from_solution(self, solution_data):
        """
        Generate clues based on the solution.

        Args:
            solution_data: Solution dictionary

        Returns:
            list: Generated clues
        """
        solution = solution_data['solution']
        dim_names = solution_data['dim_names']
        entities = solution_data['entities']
        num_persons = solution_data['num_persons']

        clues = []

        # Helper to get person index for an attribute in a dimension
        def get_person_with_attribute(dim_idx, attr_idx):
            for p in range(num_persons):
                if solution[dim_idx][p] == attr_idx:
                    return p
            return None

        # Generate positive association clues (same person has both attributes)
        num_clues = 0
        max_clues = num_persons * 2

        for r in range(1, len(dim_names)):
            for r1 in range(r + 1, len(dim_names)):
                # Pick a random person
                p = random.randint(0, num_persons - 1)
                attr_r = solution[r][p]
                attr_r1 = solution[r1][p]

                clue = {
                    'type': 'positive',
                    'dim1': dim_names[r],
                    'attr1': entities[r][attr_r],
                    'dim2': dim_names[r1],
                    'attr2': entities[r1][attr_r1],
                    'text': f"The person with {dim_names[r]}={entities[r][attr_r]} also has {dim_names[r1]}={entities[r1][attr_r1]}"
                }
                clues.append(clue)
                num_clues += 1
                if num_clues >= max_clues:
                    break
            if num_clues >= max_clues:
                break

        # Generate negative association clues
        for _ in range(min(3, num_persons)):
            r = random.randint(1, len(dim_names) - 1)
            r1 = random.randint(1, len(dim_names) - 1)

            if r == r1:
                continue

            # Pick a person for first attribute
            p1 = random.randint(0, num_persons - 1)
            attr_r = solution[r][p1]

            # Pick a different person for second attribute
            p2 = (p1 + random.randint(1, num_persons - 1)) % num_persons
            attr_r1 = solution[r1][p2]

            clue = {
                'type': 'negative',
                'dim1': dim_names[r],
                'attr1': entities[r][attr_r],
                'dim2': dim_names[r1],
                'attr2': entities[r1][attr_r1],
                'text': f"The person with {dim_names[r]}={entities[r][attr_r]} does not have {dim_names[r1]}={entities[r1][attr_r1]}"
            }
            clues.append(clue)
            num_clues += 1
            if num_clues >= max_clues + 3:
                break

        # Add positional clues if we have a numbered dimension
        for i, dim_name in enumerate(dim_names):
            if dim_name in self.numbered_entities.keys():
                # This is a numbered dimension, we can create positional clues
                pos_dim_idx = i

                # Find two persons with different positions
                for _ in range(2):
                    p1 = random.randint(0, num_persons - 2)
                    p2 = random.randint(p1 + 1, num_persons - 1)

                    # Get their attributes in first dimension
                    attr1 = solution[0][p1]
                    attr2 = solution[0][p2]

                    # Get their positions
                    pos1 = solution[pos_dim_idx][p1]
                    pos2 = solution[pos_dim_idx][p2]

                    # Get actual position values
                    pos_val1 = entities[pos_dim_idx][pos1]
                    pos_val2 = entities[pos_dim_idx][pos2]

                    if pos_val1 < pos_val2:
                        direction = "left"
                        clue_text = f"The person with {dim_names[0]}={entities[0][attr1]} is to the left of the person with {dim_names[0]}={entities[0][attr2]}"
                    else:
                        direction = "right"
                        clue_text = f"The person with {dim_names[0]}={entities[0][attr1]} is to the right of the person with {dim_names[0]}={entities[0][attr2]}"

                    clue = {
                        'type': 'positional',
                        'direction': direction,
                        'attr1': entities[0][attr1],
                        'attr2': entities[0][attr2],
                        'text': clue_text
                    }
                    clues.append(clue)

                break

        return clues

    def format_solution_for_display(self, solution_data):
        """
        Format solution for display.

        Args:
            solution_data: Solution dictionary

        Returns:
            list: Formatted solution rows
        """
        solution = solution_data['solution']
        dim_names = solution_data['dim_names']
        entities = solution_data['entities']
        num_persons = solution_data['num_persons']

        formatted = []
        for r in range(len(dim_names)):
            row = []
            for p in range(num_persons):
                attr_idx = solution[r][p]
                row.append(entities[r][attr_idx])
            formatted.append(row)

        return formatted

    def generate_puzzle(self, puzzle_id):
        """
        Generate a complete puzzle with solution.

        Args:
            puzzle_id: ID for the puzzle

        Returns:
            dict: Complete puzzle data
        """
        num_persons = random.choice([3, 4])

        # Generate a random solution
        solution_data = self.generate_solution(num_persons)

        # Generate clues from the solution
        clues = self.generate_clues_from_solution(solution_data)

        # Format solution
        formatted_solution = self.format_solution_for_display(solution_data)

        # Create puzzle data
        puzzle = {
            'puzzle_id': puzzle_id,
            'num_persons': num_persons,
            'dimensions': solution_data['dim_names'],
            'entities': solution_data['entities'],
            'num_clues': len(clues),
            'clues': [clue['text'] for clue in clues],
            'clues_data': clues,
            'solution': formatted_solution,
            'generation_success': True
        }

        return puzzle


def generate_100_puzzles(output_file="zebra_puzzles_100_simple.json"):
    """Generate 100 puzzles and save to file."""
    print("=" * 70)
    print("GENERATING 100 ZEBRA PUZZLES (Without Gurobi)")
    print("=" * 70)

    generator = SimpleZebraPuzzleGenerator()

    puzzles = []
    success_count = 0

    for i in range(100):
        puzzle_id = 2000 + i
        print(f"Generating puzzle {i+1}/100 (ID={puzzle_id})...", end=" ")

        try:
            puzzle = generator.generate_puzzle(puzzle_id)
            puzzles.append(puzzle)
            success_count += 1
            print(f"[OK] ({puzzle['num_persons']} persons, {puzzle['num_clues']} clues)")
        except Exception as e:
            print(f"[FAIL] {e}")

        # Save progress every 10 puzzles
        if (i + 1) % 10 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(puzzles, f, indent=2, ensure_ascii=False)
            print(f"  → Progress saved ({len(puzzles)} puzzles)")

    # Final save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Successfully generated: {success_count}/100")
    print(f"Output file: {output_file}")

    return puzzles


def format_puzzle_human_readable(puzzle):
    """Format a puzzle for human reading."""
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

    return "\n".join(lines)


def main():
    """Main generation function."""
    # Generate puzzles
    output_file = "zebra_puzzles_100_simple.json"

    puzzles = generate_100_puzzles(output_file)

    # Save human-readable sample
    if puzzles:
        readable_file = "zebra_puzzles_sample.txt"

        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("SAMPLE ZEBRA PUZZLES (First 5)\n")
            f.write("=" * 70 + "\n\n")

            for puzzle in puzzles[:5]:
                formatted = format_puzzle_human_readable(puzzle)
                f.write(formatted + "\n\n")

        print(f"\nHuman-readable sample: {readable_file}")
        print(f"\nFirst puzzle preview:")
        print(format_puzzle_human_readable(puzzles[0]))


if __name__ == "__main__":
    main()
