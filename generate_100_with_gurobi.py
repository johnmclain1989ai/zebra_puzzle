"""
Generate 100 Zebra Puzzles using Gurobi (with FIXED positional constraints)

This version uses the original zebra_abs_pro.py structure but with
the corrected positional constraint encoding.
"""

import sys
import os
import json
import random
import traceback
from datetime import datetime
from gurobipy import quicksum

# Setup paths - add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import zebra_abs_pro which will import from util
import zebra_abs_pro


def format_clue(ctype, r_name, c_name, r1_name, c1_name, sign=None):
    """Proxy to zebra_abs_pro.format_clue for consistent clue phrasing."""
    return zebra_abs_pro.format_clue(ctype, r_name, c_name, r1_name, c1_name, sign=sign)


def add_constraint_to_model_FIXED(m, var, matrix, dim_names, var_name_lst, constraint):
    """
    FIXED VERSION: Correctly encode positional constraints.

    This is the corrected version of the constraint addition function.
    """
    print(f"Adding constraint: {constraint}")
    descriptions = []
    ctype = constraint[0]

    if ctype == "PositionalTwo":
        # FIXED: Correctly encode positional constraints
        _, c1, c2, r1, r2, rPos = constraint

        c1_name = var_name_lst[r1][c1]
        c2_name = var_name_lst[r2][c2]

        r1_name = dim_names[r1]
        r2_name = dim_names[r2]

        v = int(var_name_lst[rPos][c1]) - int(var_name_lst[rPos][c2])
        descriptions.append(
            format_clue("PositionalTwo", r1_name, c1_name, r2_name, c2_name)
        )

        # FIXED CODE: Calculate actual positions
        num_persons = len(matrix[0])
        position_values = [int(var_name_lst[rPos][i]) for i in range(num_persons)]

        # Calculate actual position of person with attribute c1
        pos_c1 = quicksum(position_values[p] * var[p][r1][c1] for p in range(num_persons))

        # Calculate actual position of person with attribute c2
        pos_c2 = quicksum(position_values[p] * var[p][r2][c2] for p in range(num_persons))

        # Add constraint based on positional relationship
        if v < 0:
            if v == -1:
                m.addConstr(pos_c2 - pos_c1 == 1, name=f"PosLeft_{c1}_{c2}")
            else:
                m.addConstr(pos_c1 + 1 <= pos_c2, name=f"PosLeft_{c1}_{c2}")
        else:
            if v == 1:
                m.addConstr(pos_c1 - pos_c2 == 1, name=f"PosRight_{c1}_{c2}")
            else:
                m.addConstr(pos_c1 >= pos_c2 + 1, name=f"PosRight_{c1}_{c2}")

        print("added constraint:", descriptions[-1])

    elif ctype == "NonPositional":
        _, c, r, r1, sign = constraint
        if sign == 'positive':
            descriptions.append(
                format_clue(
                    "NonPositional",
                    dim_names[r],
                    var_name_lst[r][c],
                    dim_names[r1],
                    var_name_lst[r1][c],
                    sign="positive",
                )
            )
            for p in range(len(matrix[0])):
                m.addConstr(var[p][r][c] == var[p][r1][c])
        else:
            c1 = random.choice([i for i in range(len(matrix[0])) if i != c])
            descriptions.append(
                format_clue(
                    "NonPositional",
                    dim_names[r],
                    var_name_lst[r][c],
                    dim_names[r1],
                    var_name_lst[r1][c1],
                    sign="negative",
                )
            )
            for p in range(len(matrix[0])):
                m.addConstr(var[p][r][c] + var[p][r1][c1] <= 1)

        print("added constraint:", descriptions[-1])

    return descriptions


def generate_single_puzzle_FIXED(seed=None):
    """Generate a single puzzle using FIXED constraints."""
    if seed is not None:
        random.seed(seed)

    try:
        num_persons = random.choice([3, 4])
        matrix = zebra_abs_pro.build_matrix(num_persons)

        m, var = zebra_abs_pro.build_model(matrix)
        dim_names, var_name_lst = zebra_abs_pro.build_name_structure(matrix)

        constraints = zebra_abs_pro.create_random_constraints(num_persons, matrix)

        descriptions = []
        unique_solution_found = False
        constraint_added_count = 0

        for idx, con in enumerate(constraints):
            try:
                # Use FIXED version
                descriptions += add_constraint_to_model_FIXED(
                    m, var, matrix, dim_names, var_name_lst, con
                )
                constraint_added_count += 1

                sol_count, status = zebra_abs_pro.check_solution_count(m)

                if sol_count == 0:
                    break
                elif sol_count == 1:
                    unique_solution_found = True
                    break
                else:
                    continue

            except Exception as e:
                print(f"Warning: Failed to add constraint {con}: {e}")
                continue

        if unique_solution_found:
            solution_matrix = zebra_abs_pro.get_final_solution(matrix, var)

            puzzle_data = {
                "puzzle_id": seed,
                "num_persons": num_persons,
                "dimensions": dim_names,
                "entities": var_name_lst,
                "num_clues": constraint_added_count,
                "clues": descriptions,
                "solution": solution_matrix,
                "generation_success": True
            }

            return puzzle_data
        else:
            return {
                "puzzle_id": seed,
                "generation_success": False,
                "reason": "No unique solution found",
                "constraints_added": constraint_added_count
            }

    except Exception as e:
        return {
            "puzzle_id": seed,
            "generation_success": False,
            "reason": f"Error: {str(e)}",
            "traceback": traceback.format_exc()
        }


def generate_100_puzzles_with_gurobi(num_puzzles=100, output_file="data/generated/zebra_puzzles_gurobi_100.json"):
    """Generate puzzles using Gurobi with FIXED constraints."""
    print("=" * 70)
    print(f"GENERATING {num_puzzles} ZEBRA PUZZLES WITH GUROBI (FIXED)")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output file: {output_file}")
    print()

    puzzles = []
    success_count = 0
    failure_count = 0

    for i in range(num_puzzles):
        seed = 3000 + i
        print(f"Generating puzzle {i+1}/{num_puzzles} (seed={seed})...", end=" ")

        puzzle = generate_single_puzzle_FIXED(seed=seed)

        if puzzle and puzzle.get("generation_success", False):
            puzzles.append(puzzle)
            success_count += 1
            print(f"[OK] ({puzzle['num_persons']} persons, {puzzle['num_clues']} clues)")
        else:
            failure_count += 1
            reason = puzzle.get("reason", "Unknown error") if puzzle else "No puzzle data"
            print(f"[FAIL] {reason}")

        if (i + 1) % 10 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(puzzles, f, indent=2, ensure_ascii=False)
            print(f"  -> Progress saved ({len(puzzles)} puzzles)")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total attempted: {num_puzzles}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Success rate: {success_count/num_puzzles*100:.1f}%")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output saved to: {output_file}")

    return puzzles


def main():
    """Main generation function."""
    try:
        import gurobipy
        print(f"Gurobi version: {gurobipy.gurobi.version()}")
        print("Gurobi license: VALID")
        print()
    except Exception as e:
        print(f"ERROR: Gurobi issue: {e}")
        return

    puzzles = generate_100_puzzles_with_gurobi()

    if puzzles:
        # Show first puzzle
        print("\n" + "=" * 70)
        print("FIRST PUZZLE PREVIEW")
        print("=" * 70)
        p = puzzles[0]
        print(f"\nPuzzle #{p['puzzle_id']}:")
        print(f"  {p['num_persons']} persons, {len(p['dimensions'])} dimensions, {p['num_clues']} clues")
        print(f"\nDimensions: {', '.join(p['dimensions'])}")
        print(f"\nFirst 3 clues:")
        for i, clue in enumerate(p['clues'][:3], 1):
            print(f"  {i}. {clue}")


if __name__ == "__main__":
    main()
