import random

from prompt_formatting import build_entities, format_setup_string


def test_build_entities_returns_lists():
    dim_names = ["Names", "Colors"]
    var_name_lst = [["Alice", "Bob"], ["Red", "Blue"]]
    random.seed(0)

    entities = build_entities(dim_names, var_name_lst)

    assert entities["Names"] is not None
    assert entities["Colors"] is not None
    assert isinstance(entities["Names"], list)
    assert isinstance(entities["Colors"], list)


def test_format_setup_string_contains_dimensions_and_values():
    dim_names = ["Names", "Colors"]
    var_name_lst = [["Alice", "Bob"], ["Red", "Blue"]]
    random.seed(1)

    entities = build_entities(dim_names, var_name_lst)
    setup_text = format_setup_string(entities)

    for dimension, values in entities.items():
        expected_line = f"{dimension}: {', '.join(values)}"
        assert expected_line in setup_text
