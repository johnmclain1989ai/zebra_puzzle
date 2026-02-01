# Single Zebra Puzzle Example

**Generated:** 2026-02-01
**Puzzle ID:** 8000
**Seed:** 8000

---

## Puzzle Overview

- **Number of Persons:** 4
- **Dimensions:** 6
- **Number of Clues:** 23
- **Generation Status:** ✅ Successful with unique solution

---

## Puzzle Structure

### Dimensions and Entities

1. **Name:** Thomas, Michael, Charles, William
2. **House Num:** 6, 3, 8, 10
3. **Music:** World, Downtempo, Calypso, Reggae
4. **FurnitureType:** Nightstand, Sideboard, Coffee Table, Bench
5. **City:** Chicago, Rome, Tokyo, New York
6. **FavoriteBook:** Brave New World, The Alchemist, To Kill a Mockingbird, The Hunger Games

---

## Clues (Natural Language Format)

1. The person with House Num 6 also has Name Thomas.
2. The person with House Num 8 also has Music Calypso.
3. The person with House Num 3 also has Name Michael.
4. The person with FavoriteBook To Kill a Mockingbird also has Music Calypso.
5. The person with House Num 10 also has Music Reggae.
6. The person with Music World also has City Chicago.
7. The person with FurnitureType Bench also has Music Reggae.
8. The person with FavoriteBook The Hunger Games also has House Num 10.
9. The person with Name Thomas also has Music World.
10. The person with FavoriteBook Brave New World also has FurnitureType Nightstand.
11. The person with Name Thomas also has City Chicago.
12. The person with Music World also has FavoriteBook Brave New World.
13. The person with FavoriteBook The Hunger Games does not have House Num 8.
14. The person with City Rome also has Music Downtempo.
15. The person with City New York also has Name William.
16. The person with Music Reggae also has City New York.
17. The person with House Num 10 also has Name William.
18. The person with FavoriteBook The Hunger Games also has FurnitureType Bench.
19. The person with City New York also has FavoriteBook The Hunger Games.
20. The person with FavoriteBook The Alchemist does not have House Num 10.
21. The person with Music Reggae does not have FavoriteBook The Alchemist.
22. The person with Name Thomas also has Music World.
23. The person with City Rome also has FurnitureType Sideboard.

---

## Solution

### Person 0
- **Name:** Thomas
- **House Num:** 10
- **Music:** Reggae
- **FurnitureType:** Sideboard
- **City:** New York
- **FavoriteBook:** To Kill a Mockingbird

### Person 1
- **Name:** Michael
- **House Num:** 3
- **Music:** Calypso
- **FurnitureType:** Bench
- **City:** Tokyo
- **FavoriteBook:** The Alchemist

### Person 2
- **Name:** Charles
- **House Num:** 8
- **Music:** Downtempo
- **FurnitureType:** Coffee Table
- **City:** Chicago
- **FavoriteBook:** The Hunger Games

### Person 3
- **Name:** William
- **House Num:** 6
- **Music:** World
- **FurnitureType:** Nightstand
- **City:** Rome
- **FavoriteBook:** Brave New World

---

## Puzzle File

The complete puzzle data is saved in `single_puzzle_8000.json`

---

## Key Features

1. **Natural Language Clues:** Clues are formatted in natural English similar to Brainzilla.com
2. **Unique Solution:** Verified using Gurobi optimizer to have exactly one solution
3. **Mix of Clue Types:** Includes both positive ("also has") and negative ("does not have") constraints
4. **Gold Standard:** Solution is verified and correct
5. **LLM Ready:** Perfect for testing Large Language Model reasoning capabilities

---

## Usage for LLM Testing

This puzzle can be used to evaluate LLMs' logical reasoning abilities:

1. **Deductive Reasoning:** LLM must use clues to eliminate possibilities
2. **Multi-step Inference:** Requires combining multiple clues
3. **Negative Constraints:** Includes "does not have" clues for complexity
4. **Cross-dimensional Reasoning:** Requires linking information across different attributes

---

## Generation Method

- **Generator:** `generate_100_with_gurobi.py`
- **Constraint Solver:** Gurobi Optimizer v11.0.1
- **Constraint Encoding:** Binary variables with constraint programming
- **Solution Verification:** Unique solution verified through solution counting

---

**Status:** ✅ Ready for LLM Testing
**Quality:** High - 23 clues provide good challenge level
**Format:** JSON with complete metadata and solution
