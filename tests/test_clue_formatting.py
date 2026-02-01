import generate_100_with_gurobi
import zebra_abs_pro


def test_format_clue_positional():
    text = zebra_abs_pro.format_clue(
        "PositionalTwo", "Color", "Blue", "Pet", "Cat"
    )
    assert text.startswith("From left to right,")
    assert "person with Color Blue" in text
    assert "person with Pet Cat" in text
    assert text.endswith(".")


def test_format_clue_nonpositional_positive():
    text = zebra_abs_pro.format_clue(
        "NonPositional", "Color", "Blue", "Pet", "Cat", sign="positive"
    )
    assert text == "The person with Color Blue also has Pet Cat."


def test_format_clue_nonpositional_negative():
    text = zebra_abs_pro.format_clue(
        "NonPositional", "Color", "Blue", "Pet", "Cat", sign="negative"
    )
    assert text == "The person with Color Blue does not have Pet Cat."


def test_generate_module_format_clue_matches_base():
    text = generate_100_with_gurobi.format_clue(
        "NonPositional", "Color", "Blue", "Pet", "Cat", sign="positive"
    )
    assert text == "The person with Color Blue also has Pet Cat."
