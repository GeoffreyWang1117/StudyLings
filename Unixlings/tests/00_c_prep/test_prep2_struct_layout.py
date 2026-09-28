from studylings.probe import assert_ok, run


def test_self_checks(exe):
    assert_ok(run(exe), "ALL CHECKS PASSED")
