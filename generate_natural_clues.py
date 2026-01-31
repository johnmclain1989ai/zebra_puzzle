"""
Generate Zebra Puzzles with Natural Language Clues (Brainzilla-style)

This script generates zebra puzzles using natural language clues similar to
the format used on Brainzilla.com, instead of mechanical "The person with X=Y" format.
"""

import json
import random
import copy
from itertools import permutations


class NaturalZebraPuzzleGenerator:
    """Generate zebra puzzles with natural language clues."""

    # Verb mappings for different dimension types
    VERB_TEMPLATES = {
        'Nationality': ['lives in', 'resides in', 'inhabits'],
        'Color': ['is', 'has color', 'is painted'],
        'Pet': ['keeps', 'owns', 'has'],
        'Drink': ['drinks', 'prefers', 'enjoys'],
        'Cigarette': ['smokes', 'prefers to smoke'],
        'Sport': ['plays', 'enjoys'],
        'BookTitle': ['is reading', 'enjoys reading'],
        'FavoriteActor': ['likes', 'admires'],
        'PhoneBrand': ['uses', 'owns'],
        'Car': ['drives', 'owns'],
        'Food': ['prefers', 'enjoys eating'],
        'MusicGenre': ['listens to', 'enjoys'],
        'MovieGenre': ['watches', 'enjoys'],
        'BeverageBrand': ['drinks', 'prefers'],
        'Brand': ['uses', 'owns', 'prefers'],
        'SocialMediaPlatform': ['uses', 'prefers'],
        'AccessoryTypes': ['has', 'owns', 'wears'],
        'MusicalInstrument': ['plays', 'owns'],
        'Height': ['is', 'has a height of'],
        # Add more as needed
    }

    # Position phrase templates
    POSITIONAL_TEMPLATES = {
        'left': {
            'directly': ['directly to the left of', 'immediately to the left of'],
            'general': ['to the left of', 'somewhere to the left of']
        },
        'right': {
            'directly': ['directly to the right of', 'immediately to the right of'],
            'general': ['to the right of', 'somewhere to the right of']
        },
        'next_to': ['next to', 'beside', 'adjacent to'],
        'between': ['between', 'somewhere between']
    }

    def __init__(self):
        # Load entity data
        with open('attribute_entity.json', 'r') as f:
            self.attribute_entities = json.load(f)
        with open('numbered_entity.json', 'r') as f:
            self.numbered_entities = json.load(f)

    def get_verb_for_dimension(self, dim_name):
        """Get an appropriate verb for a dimension."""
        dim_base = dim_name.split()[0]  # Get first word

        # Direct match
        if dim_name in self.VERB_TEMPLATES:
            return random.choice(self.VERB_TEMPLATES[dim_name])

        # Partial match
        for key, verbs in self.VERB_TEMPLATES.items():
            if key in dim_name or dim_name in key:
                return random.choice(verbs)

        # Default verb
        return 'has'

    def generate_natural_positive_clue(self, dim1, attr1, dim2, attr2, solution_data):
        """
        Generate a natural language positive association clue.

        Examples:
        - "The Brit lives in the Red house."
        - "The person who smokes Pall Mall rears Birds."
        - "The owner of the Green house drinks Coffee."
        """
        dim_names = solution_data['dim_names']
        entities = solution_data['entities']

        # Determine which dimension makes a better subject
        # Nationality, Name, and distinctive attributes work well as subjects
        subject_priority = ['Nationality', 'Name', 'Pet', 'Drink', 'Sport']

        # Decide on template type - weighted random choice
        template_choice = random.random()
        if template_choice < 0.4:
            template_type = 'person_who'
        elif template_choice < 0.6:
            template_type = 'owner_of'
        else:
            template_type = 'direct_statement'

        if template_type == 'person_who' and dim1 not in ['Color', 'HouseNumber', 'Position', 'Height', 'LinePosition']:
            # "The person who [verb1] [attr1] [verb2] [attr2]"
            verb1 = self.get_verb_for_dimension(dim1)
            verb2 = self.get_verb_for_dimension(dim2)

            if random.random() > 0.5:
                # Swap dimensions for variety
                dim1, dim2 = dim2, dim1
                attr1, attr2 = attr2, attr1
                verb1, verb2 = verb2, verb1

            clue = f"The person who {verb1} {attr1} {verb2} {attr2}."

        elif template_type == 'owner_of' and dim1 in ['Color', 'House']:
            # "The owner of the [attr1] [dim1] [verb2] [attr2]"
            verb2 = self.get_verb_for_dimension(dim2)

            if 'Color' in dim1 or 'House' in dim1:
                clue = f"The owner of the {attr1} house {verb2} {attr2}."
            else:
                clue = f"The owner of {attr1} {verb2} {attr2}."

        else:
            # Direct statement: "[The/Name] [dim1_value] [verb] [dim2_value]"
            verb = self.get_verb_for_dimension(dim2)

            # Use "The" for nationalities, animals, drinks
            if dim1 in ['Nationality', 'Pet']:
                clue = f"The {attr1} {verb} {attr2}."
            elif dim1 == 'Name':
                clue = f"{attr1} {verb} {attr2}."
            else:
                clue = f"The person with {attr1} {verb} {attr2}."

        return clue

    def generate_natural_negative_clue(self, dim1, attr1, dim2, attr2, solution_data):
        """
        Generate a natural language negative association clue.

        Examples:
        - "The Brazilian does not live in house two."
        - "The German doesn't drink beer."
        """
        verb = self.get_verb_for_dimension(dim2)

        # Fix verb form for negative (e.g., "drives" → "drive", "has" → "have")
        if verb == 'has':
            verb_base = 'have'
        elif verb.endswith('s'):
            verb_base = verb[:-1]  # Remove 's'
        else:
            verb_base = verb

        if dim1 in ['Nationality', 'Pet']:
            clue = f"The {attr1} does not {verb_base} {attr2}."
        elif dim1 == 'Name':
            clue = f"{attr1} does not {verb_base} {attr2}."
        else:
            clue = f"The person with {attr1} does not {verb_base} {attr2}."

        return clue

    def generate_natural_positional_clue(self, attr1, pos1, attr2, pos2, dim_names, entities, pos_dim_name):
        """
        Generate a natural language positional clue.

        Examples:
        - "The Norwegian lives in the first house."
        - "The Green house is exactly to the left of the White house."
        - "The person with the Dogs lives directly to the right of the Green house."
        """
        # Sometimes generate simple "lives in house X" clue instead
        if random.random() < 0.3:
            # Generate simple position clue for one person
            target = random.choice([attr1, attr2])
            position = pos1 if target == attr1 else pos2

            # Convert position to ordinal if it's numeric
            if isinstance(position, int):
                ordinals = ['first', 'second', 'third', 'fourth', 'fifth']
                if position - 1 < len(ordinals):
                    position_text = ordinals[position - 1]
                else:
                    position_text = f"position {position}"
            else:
                position_text = str(position)

            return f"The person with {target} lives in the {position_text} house."

        # Determine if positions are adjacent
        is_adjacent = abs(pos1 - pos2) == 1

        if is_adjacent:
            if pos1 < pos2:
                templates = self.POSITIONAL_TEMPLATES['left']['directly']
                direction_word = random.choice(templates)
                # attr1 is to the left of attr2
                clue = f"The person with {attr1} lives {direction_word} the person with {attr2}."
            else:
                templates = self.POSITIONAL_TEMPLATES['right']['directly']
                direction_word = random.choice(templates)
                # attr1 is to the right of attr2
                clue = f"The person with {attr1} lives {direction_word} the person with {attr2}."
        else:
            if pos1 < pos2:
                templates = self.POSITIONAL_TEMPLATES['left']['general']
                direction_word = random.choice(templates)
                clue = f"The person with {attr1} lives {direction_word} the person with {attr2}."
            else:
                templates = self.POSITIONAL_TEMPLATES['right']['general']
                direction_word = random.choice(templates)
                clue = f"The person with {attr1} lives {direction_word} the person with {attr2}."

        return clue

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

        # Second dimension: numbered entity (positions)
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
            elif i == 1:
                # Position dimension stays in order
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
        Generate natural language clues based on the solution.

        Args:
            solution_data: Solution dictionary

        Returns:
            list: Generated clues with natural language
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

        # Generate positive association clues
        num_clues = 0
        max_clues = num_persons * 2

        for r in range(1, len(dim_names)):
            for r1 in range(r + 1, len(dim_names)):
                # Pick a random person
                p = random.randint(0, num_persons - 1)
                attr_r = solution[r][p]
                attr_r1 = solution[r1][p]

                clue_text = self.generate_natural_positive_clue(
                    dim_names[r], entities[r][attr_r],
                    dim_names[r1], entities[r1][attr_r1],
                    solution_data
                )

                clue = {
                    'type': 'positive',
                    'dim1': dim_names[r],
                    'attr1': entities[r][attr_r],
                    'dim2': dim_names[r1],
                    'attr2': entities[r1][attr_r1],
                    'text': clue_text
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

            clue_text = self.generate_natural_negative_clue(
                dim_names[r], entities[r][attr_r],
                dim_names[r1], entities[r1][attr_r1],
                solution_data
            )

            clue = {
                'type': 'negative',
                'dim1': dim_names[r],
                'attr1': entities[r][attr_r],
                'dim2': dim_names[r1],
                'attr2': entities[r1][attr_r1],
                'text': clue_text
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

                    clue_text = self.generate_natural_positional_clue(
                        entities[0][attr1], pos_val1,
                        entities[0][attr2], pos_val2,
                        dim_names, entities, dim_name
                    )

                    # Determine direction
                    if pos_val1 < pos_val2:
                        direction = "left"
                    else:
                        direction = "right"

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
        Generate a complete puzzle with natural language clues.

        Args:
            puzzle_id: ID for the puzzle

        Returns:
            dict: Complete puzzle data
        """
        num_persons = random.choice([3, 4])

        # Generate a random solution
        solution_data = self.generate_solution(num_persons)

        # Generate natural language clues from the solution
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
            'generation_success': True,
            'clue_style': 'natural'  # Mark as natural language style
        }

        return puzzle


def generate_natural_puzzles(num_puzzles=50, output_file="zebra_puzzles_natural.json"):
    """Generate puzzles with natural language clues."""
    print("=" * 70)
    print(f"GENERATING {num_puzzles} ZEBRA PUZZLES WITH NATURAL LANGUAGE CLUES")
    print("=" * 70)
    print(f"Output file: {output_file}")
    print()

    generator = NaturalZebraPuzzleGenerator()

    puzzles = []
    success_count = 0

    for i in range(num_puzzles):
        puzzle_id = 4000 + i
        print(f"Generating puzzle {i+1}/{num_puzzles} (ID={puzzle_id})...", end=" ")

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
            print(f"  -> Progress saved ({len(puzzles)} puzzles)")

    # Final save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total puzzles: {len(puzzles)}")
    print(f"Success rate: {success_count/num_puzzles*100:.1f}%")
    print(f"Output saved to: {output_file}")

    return puzzles


def main():
    """Generate sample puzzles and display them."""
    print("Generating sample natural language zebra puzzles...\n")

    # Generate a few sample puzzles
    generator = NaturalZebraPuzzleGenerator()

    print("=" * 70)
    print("SAMPLE PUZZLE #1")
    print("=" * 70)

    puzzle1 = generator.generate_puzzle(4001)
    print(f"\nPuzzle #{puzzle1['puzzle_id']}:")
    print(f"  {puzzle1['num_persons']} persons, {len(puzzle1['dimensions'])} dimensions")
    print(f"\nDimensions: {', '.join(puzzle1['dimensions'])}")
    print(f"\nClues ({puzzle1['num_clues']}):")
    for i, clue in enumerate(puzzle1['clues'], 1):
        print(f"  {i}. {clue}")

    print("\n" + "=" * 70)
    print("SAMPLE PUZZLE #2")
    print("=" * 70)

    puzzle2 = generator.generate_puzzle(4002)
    print(f"\nPuzzle #{puzzle2['puzzle_id']}:")
    print(f"  {puzzle2['num_persons']} persons, {len(puzzle2['dimensions'])} dimensions")
    print(f"\nDimensions: {', '.join(puzzle2['dimensions'])}")
    print(f"\nClues ({puzzle2['num_clues']}):")
    for i, clue in enumerate(puzzle2['clues'], 1):
        print(f"  {i}. {clue}")

    print("\n" + "=" * 70)
    print("Comparison with Old Style")
    print("=" * 70)
    print("\nOld style clue:")
    print('  "The person with Height=130 also has Nationality=Englishman"')
    print("\nNew natural style:")
    print('  "The Englishman is 130cm tall."')
    print('  OR "The person who is 130cm tall is Englishman."')
    print('  OR "The 130cm person is Englishman."')


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--generate':
        num_puzzles = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        generate_natural_puzzles(num_puzzles)
    else:
        main()
