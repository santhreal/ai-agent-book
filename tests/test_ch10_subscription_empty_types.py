import sys
from pathlib import Path

ch10_pwr = Path(__file__).resolve().parent.parent / "chapter10" / "parallel-web-research"
if str(ch10_pwr) not in sys.path:
    sys.path.insert(0, str(ch10_pwr))

from message_bus import Envelope, Subscription


def test_subscription_empty_types_list():
    # A subscription initialized with an empty list should subscribe to NO message types,
    # not fallback to subscribing to ALL types (which happens when `if types:` evaluates to False).
    sub = Subscription(owner_id="worker_1", types=[])

    # Should not accept any message types when types=[] is explicitly passed
    env = Envelope(sender_id="coord", target="*", type="task_assignment", payload={})
    assert sub.accepts(env) is False
