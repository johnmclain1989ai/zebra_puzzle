import random


def build_entities(dim_names, var_name_lst):
    entities = {}
    for dim_name, values in zip(dim_names, var_name_lst):
        shuffled_values = values[:]
        random.shuffle(shuffled_values)
        entities[dim_name] = shuffled_values
    return entities


def format_setup_string(entities):
    return "\n".join(
        f"{dimension}: {', '.join(values)}" for dimension, values in entities.items()
    )
