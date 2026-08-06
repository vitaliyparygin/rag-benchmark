from types import SimpleNamespace

from rag_benchmark.diagnostics.analyzers.missing_improvements_analyzer import (
    MissingImprovementsAnalyzer,
)


def make_result(
    *,
    missing_fields=None,
    regex_stats=None,
    question_templates=None,
    questions=None,
):
    return SimpleNamespace(
        missing_fields=missing_fields or [],
        regex_stats=regex_stats or [],
        question_templates=question_templates or {},
        questions=questions or [],
        classified=SimpleNamespace(
            classification=SimpleNamespace(
                document_type="Vendor Profile",
            ),
        ),
    )


def test_unmatched_regex_for_present_field_is_regex_improvement():
    result = make_result(
        regex_stats=[
            SimpleNamespace(
                field="address",
                matched=False,
            ),
        ],
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert len(improvements) == 1
    assert improvements[0].category == "Regex"
    assert improvements[0].item == "address"
    assert improvements[0].suggestion == "Regex does not match 'address'"


def test_missing_field_does_not_produce_regex_improvement_when_field_is_absent_from_document():
    result = make_result(
        missing_fields=["address"],
        regex_stats=[
            SimpleNamespace(
                field="address",
                matched=False,
            ),
        ],
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert not any(
        improvement.category == "Regex" and improvement.item == "address"
        for improvement in improvements
    )


def test_missing_question_field_produces_questions_improvement():
    result = make_result(
        question_templates={
            "Vendor Profile": [
                SimpleNamespace(
                    fields=[
                        SimpleNamespace(name="vendor"),
                        SimpleNamespace(name="vendor_id"),
                        SimpleNamespace(name="address"),
                    ],
                ),
            ],
        },
        questions=[
            SimpleNamespace(
                expected_fields=["vendor"],
            ),
            SimpleNamespace(
                expected_fields=["vendor_id"],
            ),
        ],
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert len(improvements) == 1
    assert improvements[0].category == "Questions"
    assert improvements[0].item == "address"
    assert improvements[0].suggestion == "Question was not generated"


def test_missing_field_with_existing_unmatched_regex_is_not_regex_improvement():
    result = SimpleNamespace(
        missing_fields=["address"],
        regex_stats=[
            SimpleNamespace(
                field="address",
                matched=False,
            ),
        ],
        question_templates={},
        questions=[],
        classified=SimpleNamespace(
            classification=SimpleNamespace(
                document_type="Vendor Profile",
            ),
        ),
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert improvements == []


def test_missing_question_field_gets_question_improvement():
    result = SimpleNamespace(
        missing_fields=[],
        regex_stats=[],
        question_templates={
            "Vendor Profile": [
                SimpleNamespace(
                    fields=[
                        SimpleNamespace(name="vendor"),
                        SimpleNamespace(name="vendor_id"),
                        SimpleNamespace(name="address"),
                    ],
                ),
            ],
        },
        questions=[
            SimpleNamespace(expected_fields=["vendor"]),
            SimpleNamespace(expected_fields=["vendor_id"]),
        ],
        classified=SimpleNamespace(
            classification=SimpleNamespace(
                document_type="Vendor Profile",
            ),
        ),
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert len(improvements) == 1
    assert improvements[0].category == "Questions"
    assert improvements[0].item == "address"
    assert improvements[0].suggestion == "Question was not generated"


def test_missing_field_with_unmatched_regex_does_not_produce_regex_improvement():
    result = SimpleNamespace(
        missing_fields=["address"],
        regex_stats=[
            SimpleNamespace(
                field="address",
                matched=False,
            ),
        ],
        question_templates={},
        questions=[],
        classified=SimpleNamespace(
            classification=SimpleNamespace(
                document_type="Vendor Profile",
            ),
        ),
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert improvements == []
