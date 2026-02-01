import zebra_abs_pro


def test_format_nonpositional_clue_negative_uses_does_not_have():
    dim_names = ["Name", "Color"]
    var_name_lst = [["Alice", "Bob"], ["Red", "Blue"]]

    clue = zebra_abs_pro.format_nonpositional_clue(
        dim_names, var_name_lst, r=0, c=0, r1=1, c1=1, sign="negative"
    )

    assert clue == "The person with dimension Name=Alice does not have dimension Color=Blue"


def test_format_nonpositional_clue_positive_consistent_phrase():
    dim_names = ["Name", "Pet"]
    var_name_lst = [["Alice", "Bob"], ["Cat", "Dog"]]

    clue = zebra_abs_pro.format_nonpositional_clue(
        dim_names, var_name_lst, r=0, c=1, r1=1, c1=0, sign="positive"
    )

    assert clue == "The person with dimension Name=Bob also has dimension Pet=Cat"
