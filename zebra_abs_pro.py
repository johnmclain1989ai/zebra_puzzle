import random
import json
from gurobipy import Model, GRB, quicksum
from util.query_gpt import query_4o_db as query_gpt
from util.query_gpt import query_claude as query_claude
from util.query_seek import query as query_seek

# -------------------------------------------------------------------------------
# Constants or configuration can go here
ATTRIBUTE_ENTITY_FILE = 'attribute_entity.json'
NUMBERED_ENTITY_FILE = 'numbered_entity.json'
# -------------------------------------------------------------------------------



def read_attribute_entity(file_path=ATTRIBUTE_ENTITY_FILE):
    """
    Read and return the attribute entities (JSON) from the given file path.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def read_numbered_entity(file_path=NUMBERED_ENTITY_FILE):
    """
    Read and return the numbered entity (JSON) from the given file path.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def build_matrix(num_persons):
    """
    Build the puzzle matrix:
      - First row: person IDs (these will be re-labeled later as 'names')
      - Following rows: random permutations representing different dimensions/attributes.
    """
    num_dimensions = 2+num_persons  # Example dimension count

    # The first row is the list of raw "names" or IDs, e.g. 0..(num_persons-1)
    # We'll rename them in build_name_structure.
    names = [f"Person_{i}" for i in range(num_persons)]

    matrix = []
    matrix.append(names)

    # For the remaining rows, create permutations of the range [0..num_persons-1]
    for _ in range(num_dimensions - 1):
        row = list(range(num_persons))
        random.shuffle(row)
        matrix.append(row)

    return matrix


def build_name_structure(matrix, attribute_entities=None, seq_entities=None):
    """
    Construct human-readable names for each dimension (row) of the puzzle matrix.

    :param matrix: The puzzle matrix, where matrix[0] are the 'persons' (as IDs).
    :param attribute_entities: Dict loaded from attribute_entity.json
    :param seq_entities: Dict loaded from numbered_entity.json
    :return: (dim_names, var_name_lst)
        - dim_names: a list of dimension labels (e.g., ["Name", "Position", "Color", ...])
        - var_name_lst: a parallel list of attribute-lists. For example:
            var_name_lst[0] = [name1, name2, ...]  (human-friendly names for dimension 0)
            var_name_lst[1] = [pos1, pos2, ...]    (human-friendly names for dimension 1)
            ...
    """
    if attribute_entities is None:
        attribute_entities = read_attribute_entity()

    if seq_entities is None:
        seq_entities = read_numbered_entity()

    var_name_lst = []
    dim_names = ["Name"]  # The first dimension name is "Name"

    # The first row is the names of the persons
    names = attribute_entities['Name']
    random.shuffle(names)
    names = names[:len(matrix[0])]
    var_name_lst.append(names)

    # The second row is the positional attributes (from numbered_entity.json)
    numbered_category = random.choice(list(seq_entities.keys()))
    seq_entity = seq_entities[numbered_category]
    random.shuffle(seq_entity)
    seq_entity = seq_entity[:len(matrix[1])]
    var_name_lst.append(seq_entity)
    dim_names.append(numbered_category)

    # The rest of the rows are attributes from attribute_entity.json
    attribute_names = list(attribute_entities.keys())
    if 'Name' in attribute_names:
        attribute_names.remove('Name')

    for i in range(2, len(matrix)):
        attribute_name = random.choice(attribute_names)
        attribute_values = attribute_entities[attribute_name]
        random.shuffle(attribute_values)
        attribute_values = attribute_values[:len(matrix[i])]
        var_name_lst.append(attribute_values)
        dim_names.append(attribute_name)

    pass

    return dim_names, var_name_lst


def build_model(matrix):
    """
    Build a Gurobi model with baseline constraints:
      1) Exactly one attribute per dimension per person.
      2) Each attribute belongs to exactly one person in that dimension.
      3) For dimension=0 (Name), fix each person p to attribute p => ensures Person p = Name p.
    """
    m = Model("ZebraPuzzle")
    # Speed up solution enumeration for small puzzles
    m.setParam('OutputFlag', 0)
    m.setParam('PoolSearchMode', 2)   # So we can find multiple solutions
    m.setParam('PoolSolutions', 1000) # Enough to check if more than 1 solution exists
    m.setParam('PoolGap', 0)

    names = matrix[0]
    num_persons = len(names)
    num_dimensions = len(matrix)

    # Create binary var[p][r][att]: 1 if Person p has attribute att in dimension r
    var = {}
    for p in range(num_persons):
        var[p] = {}
        for r in range(num_dimensions):
            var[p][r] = {}
            for att in range(num_persons):
                var[p][r][att] = m.addVar(vtype=GRB.BINARY,
                                          name=f"x_{p}_{r}_{att}")

    # Baseline constraints
    # 1) Each person p has exactly one attribute att in dimension r
    for p in range(num_persons):
        for r in range(num_dimensions):
            m.addConstr(quicksum(var[p][r][att] for att in range(num_persons)) == 1,
                        name=f"Person_{p}_Dim_{r}")

    # 2) Each attribute att in dimension r is assigned to exactly one person
    for r in range(num_dimensions):
        for att in range(num_persons):
            m.addConstr(quicksum(var[p][r][att] for p in range(num_persons)) == 1,
                        name=f"Att_{att}_Dim_{r}")

    # 3) Fix name dimension: Person p => attribute p in dimension 0
    for p in range(num_persons):
        m.addConstr(var[p][0][p] == 1, name=f"FixName_{p}")

    m.update()
    return m, var


def check_solution_count(m):
    """
    Solve the model and return:
      - sol_count (int): Number of solutions found (<= PoolSolutions).
      - status (str): "OPTIMAL" if feasible or "INFEASIBLE" if no solutions.

    Note: With PoolSearchMode=2, Gurobi will attempt to find multiple solutions.
    """
    m.update()
    m.optimize()

    if m.status == GRB.INFEASIBLE:
        return 0, 'INFEASIBLE'
    elif m.status == GRB.OPTIMAL:
        print("Found optimal solution. solution count is:", m.SolCount)

    return m.SolCount, 'OPTIMAL'


def format_clue(ctype, r_name, c_name, r1_name, c1_name, sign=None):
    """
    Render a human-readable clue string.

    :param ctype: "PositionalTwo" or "NonPositional"
    :param r_name: Name of the first attribute group
    :param c_name: Attribute value in the first group
    :param r1_name: Name of the second attribute group
    :param c1_name: Attribute value in the second group
    :param sign: "positive" or "negative" for NonPositional
    """
    if ctype == "PositionalTwo":
        return (
            f"From left to right, the person with {r_name} {c_name} is immediately left "
            f"of the person with {r1_name} {c1_name}."
        )
    if ctype == "NonPositional":
        if sign == "positive":
            return f"The person with {r_name} {c_name} also has {r1_name} {c1_name}."
        return f"The person with {r_name} {c_name} does not have {r1_name} {c1_name}."
    raise ValueError(f"Unsupported clue type: {ctype}")


def add_constraint_to_model(m, var, matrix, dim_names, var_name_lst, constraint):
    """
    Convert a high-level puzzle constraint (e.g., 'PositionalTwo' or 'NonPositional')
    into Gurobi constraints and add them to the model.

    :param constraint: Tuple describing the constraint.
                       Examples:
                         ("PositionalTwo", c1, c2, r1, r2, rPos)
                         ("NonPositional", c, r, r1, 'positive')
                         ("NonPositional", c, r, r1, 'negative')
    """
    print(f"Adding constraint: {constraint}")
    descriptions = []
    ctype = constraint[0]

    if ctype == "PositionalTwo":
        # Example placeholder logic for positional constraints
        # ("PositionalTwo", c1, c2, r1, r2, rPos)
        _, c1, c2, r1, r2, rPos = constraint
        # Could encode "c1 is left of c2" or other positional logic
        c1_name = var_name_lst[r1][c1]
        c2_name = var_name_lst[r2][c2]

        r1_name = dim_names[r1]
        r2_name = dim_names[r2]

        v = int(var_name_lst[rPos][c1]) - int(var_name_lst[rPos][c2])

        descriptions.append(
            format_clue("PositionalTwo", r1_name, c1_name, r2_name, c2_name)
        )

        # code for model

        if v < 0:
            if v == -1:
                m.addConstr(int(var_name_lst[rPos][c1])*quicksum(var[p][r1][c1] for p in range(len(matrix[0])))+1
                            == int(var_name_lst[rPos][c2])*quicksum(var[p][r1][c1] for p in range(len(matrix[0]))))
            else:
                m.addConstr(int(var_name_lst[rPos][c1]) * quicksum(var[p][r1][c1] for p in range(len(matrix[0])))
                            <= int(var_name_lst[rPos][c2]) * quicksum(var[p][r1][c1] for p in range(len(matrix[0]))))
        else:
            if v == 1:
                m.addConstr(int(var_name_lst[rPos][c1])*quicksum(var[p][r1][c1] for p in range(len(matrix[0])))-1
                            == int(var_name_lst[rPos][c2])*quicksum(var[p][r1][c1] for p in range(len(matrix[0]))))
            else:
                m.addConstr(int(var_name_lst[rPos][c1]) * quicksum(var[p][r1][c1] for p in range(len(matrix[0])))+1
                            >= int(var_name_lst[rPos][c2]) * quicksum(var[p][r1][c1] for p in range(len(matrix[0]))))

        print("added constraint:", descriptions[-1])

    elif ctype == "NonPositional":
        # ("NonPositional", c, r, r1, sign)
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

        else:  # 'negative'
            # The person with (r,c) must not have (r1,c1), where c1 is a different attribute from dimension r1
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


def get_final_solution(matrix, var):
    """
    Retrieve the single solution from the model (assuming it is unique).
    For each person p and dimension r, find the attribute 'att' such that var[p][r][att] = 1.

    :return: A 2D list analogous to 'matrix', but with resolved attributes for each dimension.
    """
    names = matrix[0]
    num_persons = len(names)
    num_dimensions = len(matrix)

    solution_matrix = []
    for r in range(num_dimensions):
        row = []
        for p in range(num_persons):
            for att in range(num_persons):
                if var[p][r][att].X > 0.5:
                    if r == 0:
                        # dimension=0 => this is the 'Name' dimension
                        row.append(names[att])
                    else:
                        row.append(matrix[r][att])
                    break
        solution_matrix.append(row)
    return solution_matrix


def create_random_constraints(num_persons, matrix):
    """
    Create a list of random constraints to demonstrate usage.
    For example,  (num_persons ** 3) constraints are generated:
      - 5% chance for "PositionalTwo"
      - 95% chance for "NonPositional"
    """
    constraints = []
    for _ in range(num_persons ** 3):
        ctype = random.choices(["PositionalTwo", "NonPositional"],
                               weights=[0.05, 0.95])[0]
        if ctype == "PositionalTwo":
            # (ctype, c1, c2, r1, r2, rPos)
            c1 = random.choice([j for j in range(len(matrix[0]))])
            c2 = random.choice([j for j in range(len(matrix[0])) if j != c1])
            r1 = random.choice([j for j in range(len(matrix)) if j != 1])
            r2 = random.choice([j for j in range(len(matrix)) if j != 1])
            rPos = 1  # dimension=1 is "positional"
            constraints.append((ctype, c1, c2, r1, r2, rPos))
        else:
            # (ctype, c, r, r1, sign)
            c = random.choice([j for j in range(len(matrix[0]))])
            r = random.choice([j for j in range(len(matrix))])
            r1 = random.choice([j for j in range(len(matrix)) if j != r])
            sign = random.choices(["positive", "negative"], weights=[0.8, 0.2])[0]
            constraints.append((ctype, c, r, r1, sign))
    return constraints


def main():
    # 1. Generate the puzzle matrix
    num_persons = random.choice([3, 4])
    matrix = build_matrix(num_persons)
    print("Puzzle matrix (randomly generated):")
    for row in matrix:
        print(row)

    # 2. Build the baseline model
    m, var = build_model(matrix)

    # 2.1 Build dimension/attribute names for clarity
    dim_names, var_name_lst = build_name_structure(matrix)
    print("Dimension names and variable names:")
    print("dim_names:", dim_names)
    print("var_name_lst:", var_name_lst)

    # 3. Generate a set of random constraints
    constraints = create_random_constraints(num_persons, matrix)

    descriptions = []

    # 4. Incrementally add constraints; check solution counts after each addition
    unique_solution_found = False
    for idx, con in enumerate(constraints):
        print("-" * 40)
        print(f"Adding constraint {idx+1}/{len(constraints)}")
        descriptions += add_constraint_to_model(m, var, matrix, dim_names, var_name_lst, con)

        sol_count, status = check_solution_count(m)

        if sol_count == 0:
            # Infeasible => remove or revert. Here we do a naive skip (not removing from the model).
            print(f"Dropping constraint {con} because it caused infeasibility.")
            # Real implementation would revert or remove the constraint.
            pass
        elif sol_count == 1:
            # We have a unique solution; stop adding more constraints.
            print(f"Unique solution found after adding constraint: {con}")
            unique_solution_found = True
            break
        else:
            # Multiple solutions remain => keep going
            pass

    # 5. If a unique solution was found, retrieve and print it
    if unique_solution_found:
        solution_matrix = get_final_solution(matrix, var)
        print("\nUnique solution assignment (each row is a dimension):")
        for row in solution_matrix:
            print(row)

        print("\nDescriptions of constraints:")
        for desc in descriptions:
            print(desc)

        zebra_puzzle = ask_gpt_to_generate_a_zebra_puzzle(dim_names, var_name_lst, descriptions)

        print("Zebra Puzzle generated by GPT:", zebra_puzzle)
    else:
        print("No unique solution found with the given constraints.")

def ask_gpt_to_generate_a_zebra_puzzle(dim_names, var_name_lst, cons_descriptions):
    previous_examples = """
example 1: 
    Puzzle Setup
        Houses: 3 in a row (House #1, House #2, House #3)
        Colors: Blue, Red, White
        Nationalities: Italian, Norwegian, Spanish
    Clues
        The Spanish occupant lives directly to the right of the Red house.
        The Norwegian occupant lives in the Blue house.
        The Italian occupant lives in House #2.
    Objective
        Determine the sequence of house colors in sequence of (House #1, House #2, House #3).

example 2:
    Puzzle Setup
        Below is a text‐based “Zebra Puzzle” version of the image. We have 3 houses in a row, each with four attributes:
        Houses: 3 in a row (House #1, House #2, House #3)
        Color: blue, green, red
        Nationality: Australian, Brazilian, German
        Animal: cats, dogs, fishes
        Sport: basketball, football, soccer
    
    Puzzle Setup
        The Brazilian does not live in house two.
        The person with the Dogs plays Basketball.
        There is exactly one house between the house of the person who plays Football and the Red house on the right.
        The person with the Fishes lives directly to the left of the person with the Cats.
        The person with the Dogs lives directly to the right of the Green house.
        The German lives in house three.
    
    Objective
        Determine the sequence of house colors in sequence of (House #1, House #2, House #3).
        
example 3:
    Puzzle Setup
        Shirt color: black, blue, green, red
        Name: Daniel, Joshua, Nicholas, Ryan
        Movie genre: action, comedy, horror, thriller
        Snack: chips, cookies, crackers, popcorn
        Age: 11, 12, 13, 14
    
    Clues
        Joshua is in one of the ends.
        The boy wearing the Black shirt is somewhere to the left of the youngest boy (the boy who is 11 years old).
        Joshua likes Horror movies.
        The 14‐year‐old boy is in the third position.
        The boy wearing the Red shirt is somewhere between the 13‐year‐old boy and the one who likes Action movies, in that order.
        Daniel likes Thriller movies.
        The boy who will eat Cookies is in one of the ends.
        The boy wearing the Black shirt is exactly to the left of the boy who likes Thriller movies.
        The boy who will eat Crackers is exactly to the right of the boy who likes Comedy movies.
        The boy wearing the Red shirt is somewhere between the boy who will eat Popcorn and Nicholas, in that order.
        In one of the ends is the boy who likes Thriller movies.
        Nicholas is somewhere between Joshua and Daniel, in that order.
        In the first position is the boy wearing the Green shirt.
    
    Objective
        Determine the sequence of shirt colors in sequence of (Daniel, Joshua, Nicholas, Ryan).

example 4:
    Puzzle Setup
        Houses: House #1, House #2, House #3, House #4
        Attributes (each house has one in each category):
        Color: black, blue, red, white
        Nationality: American, British, Canadian, Irish
        Animal: butterflies, dolphins, horses, turtles
        Sport: bowling, handball, swimming, tennis
    
    Clues
        There are two houses between the person who likes Bowling and the person who likes Swimming.
        There is one house between the Irish person and the person who likes Handball on the left.
        The second house is Black.
        There is one house between the person who likes Horses and the Red house on the right.
        The American lives directly to the left of the person who likes Turtles.
        There are two houses between the person who likes Horses and the person who likes Butterflies on the right.
        The person who likes Bowling lives somewhere to the right of the person who likes Tennis.
        There is one house between the person who likes Handball and the White house on the right.
        The British person lives in House #1.
    
    Objective
        Determine the sequence of Nationality in sequence of (House #1, House #2, House #3, House #4).
        
example 5:
    Puzzle Setup
        Puzzle Setup
        Positions (left to right): Boy #1, Boy #2, Boy #3, Boy #4, Boy #5
        Bike colors (one per boy): black, blue, green, red, white
        Names: Adrian, Charles, Henry, Joel, Richard
        Sandwiches: bacon, chicken, cheese, pepperoni, tuna
        Juices: apple, cranberry, grapefruit, orange, pineapple
        Ages: 12, 13, 14, 15, 16
        Sports: baseball, basketball, hockey, soccer, swimming
    
    Clues
        In the middle is the boy who likes Baseball (so the 3rd position is the Baseball fan).
        The cyclist who is going to eat Tuna sandwich is at one of the ends (position 1 or position 5).
        The owner of the White bike is somewhere between the 15-year-old boy and the youngest boy, in that order (15-year-old on the left, youngest on the right, White bike somewhere in between).
        The boy that is going to drink Pineapple juice is at the 4th position.
        Henry is exactly to the left of the Soccer fan (Henry is immediately left, the Soccer fan is immediately right).
        The boy who will drink Grapefruit juice is somewhere between the boy who brought Tuna sandwich and the boy who brought Pineapple juice, in that order.
        The boy riding the Black bike is at the 3rd position.
        The one who likes Swimming is next to the friend who likes Baseball (positions are side by side).
        The cyclist that brought Pineapple juice is somewhere between the 14-year-old and the boy that brought Orange juice, in that order.
        In one of the ends is the boy riding the Green bicycle.
        The boy who likes the sport played on ice (i.e., Hockey) is going to eat Pepperoni sandwich.
        The boy riding the White bike is somewhere between the boy riding the Blue bike and the boy riding the Black bike, in that order (Blue on the left, White in the middle, Black on the right).
        Joel is next to the 16-year-old cyclist.
        Adrian is exactly to the left of the boy who is going to eat Pepperoni sandwich (Adrian immediately left, Pepperoni boy immediately right).
        The 12-year-old is somewhere between the 14-year-old and the oldest boy, in that order.
        The boy who is going to eat Bacon sandwich is somewhere to the right of the owner of the White bicycle.
        The 16-year-old brought Cheese sandwich.
        In the 5th position is the 13-year-old boy.
        The cyclist riding the White bike is somewhere between Richard and the boy riding the Red bike, in that order (Richard on the left, White bike in the middle, Red bike on the right).
        The Baseball fan is next to the boy who is going to drink Apple juice.
        The boy who likes Hockey is at the 5th position.
        Charles is somewhere between Richard and Adrian, in that order (Richard on the left, Charles in the middle, Adrian on the right).
    
    Objective
        Determine the sequence of Bike colors in sequence of boys (Boy #1, Boy #2, Boy #3, Boy #4, Boy #5)
    """

    # entities
    # need to shuffle the entities
    entities = { k: random.shuffle(v) for k, v in zip(dim_names, var_name_lst)}

    # input
    input_text = f"""
You are given a puzzle setup and a set of clues. Your task is to rewrite the clues in clear, natural‐sounding language, matching the style and structure shown in the example clues.
Puzzle Setup:
    {entities},
Clues:
    {cons_descriptions}
Examples:
{previous_examples}

Now, you need to generate the clues for the puzzle setup, clues and objective.
"""

    # ask gpt
    # response = query_claude(input_text)
    response = query_seek(input_text)

    return response




if __name__ == '__main__':


    # print("=" * 40)
    # print("Zebra Puzzle Solver")
    # seed = random.randint(0, 1000)
    # print("seed:", seed)
    #
    # # set seed
    # random.seed(975)

    main()
