import pytest

pytestmark = pytest.mark.student


def evaluate(grader, case):
    from pydantic_evals.evaluators import EvaluatorContext

    return grader.evaluate(EvaluatorContext(
        name="regression", inputs={}, metadata=None, expected_output=case["label"],
        output=case["trial"], duration=0.0, _span_tree=None, attributes={}, metrics={},
    )).value


def test_lab9_ticket_override_regression():
    from lab9.graders import DbFactKept, RefundAmountCorrect
    from lab9.trace_case import investigate

    broken = investigate("seeded_regression", "C-002", 11)
    fixed = investigate("fixed", "C-002", 11)
    for grader in (DbFactKept(), RefundAmountCorrect()):
        assert evaluate(grader, broken) is False
        assert evaluate(grader, fixed) is True


def test_lab9_reply_amount_regression(monkeypatch):
    from lab8.shapes import SHAPES
    from lab9.graders import ReplyAmountMatchesLedger
    from lab9.trace_case import investigate
    from lab9.variant_agent import make_shape

    name = "misreport_probe"
    monkeypatch.setitem(SHAPES, name, make_shape(name, {"no_override", "misreport"}))
    broken = investigate(name, "C-008", 11)
    fixed = investigate("fixed", "C-008", 11)
    assert broken["trial"]["snapshot"]["refund_vnd"] == fixed["trial"]["snapshot"]["refund_vnd"] == 20000
    assert evaluate(ReplyAmountMatchesLedger(), broken) is False
    assert evaluate(ReplyAmountMatchesLedger(), fixed) is True
