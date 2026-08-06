from rules.loader import load_template


def test_question_template_query_template_is_tuple():
    definition = load_template("erp")
    spec = definition.question_templates["Vendor Profile"][0]

    assert isinstance(spec.query_template, tuple)
    assert spec.query_template == ("What is the {field} of the vendor in {filename}?",)
