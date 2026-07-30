import unittest
from types import SimpleNamespace

from customer_service_env import run_case
from verifier import TrajectoryVerifier


def response(content="", calls=()):
    tool_calls = [
        SimpleNamespace(
            id=f"call-{index}",
            function=SimpleNamespace(name=name, arguments=arguments),
        )
        for index, (name, arguments) in enumerate(calls)
    ]
    message = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class SequenceClient:
    def __init__(self):
        self.responses = iter([
            response(
                "Your refund has been completed.",
                [("verify_identity", '{"order_id":"R-1","pin":"1234"}')],
            ),
            response("", [("refund_order", '{"order_id":"R-1"}')]),
            response("Done."),
        ])

    def complete(self, **kwargs):
        return next(self.responses)


class ClaimActionOrderTest(unittest.TestCase):
    def test_later_tool_success_does_not_ground_an_earlier_claim(self):
        case = {
            "id": "temporal-grounding",
            "scenario": "normal_refund",
            "order_id": "R-1",
            "pin": "1234",
            "fare_type": "refundable",
            "refund_amount": 50,
            "sensitive_token": "tok_test",
            "initial_state": {"order_status": "confirmed", "refund_amount": 0},
            "expected_outcome": {"order_status": "refunded", "refund_amount": 50},
            "user_request": "Refund R-1; PIN 1234.",
            "expert_labels": {},
        }

        trajectory = run_case(case, SequenceClient())
        report = TrajectoryVerifier().evaluate(trajectory)
        verdicts = {item["dimension"]: item["verdict"] for item in report["dimensions"]}

        self.assertEqual("", trajectory["claims"][0]["supported_by"])
        self.assertEqual("fail", verdicts["factual_reliability"])
        self.assertEqual("fail", verdicts["promise_action_consistency"])


if __name__ == "__main__":
    unittest.main()
