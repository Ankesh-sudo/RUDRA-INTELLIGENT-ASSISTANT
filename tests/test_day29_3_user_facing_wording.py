def test_no_confirmation_wording():
    lines = [
        "No preferences are approved yet. Nothing will change."
    ]
    assert "Nothing will change" in lines[0]
