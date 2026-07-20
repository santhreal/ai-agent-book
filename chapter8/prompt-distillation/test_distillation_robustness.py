from compare import compare


def test_compare_zero_division():
    report = compare(
        prompt_template="Classify this text: {text}",
        texts=[],
        teacher_labels={},
        eval_results=None,
        count_tokens=lambda s: len(s.split()),
        token_method="space",
        num_examples=3,
    )
    assert report["teacher_input_avg"] == 0.0
    assert report["student_input_avg"] == 0.0
    assert report["input_token_reduction_pct"] == 0.0
    assert report["teacher_student_ratio"] == float("inf")
