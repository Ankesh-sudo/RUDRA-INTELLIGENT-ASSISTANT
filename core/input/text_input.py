def read_text():
    """
    Read a single line of text from user.
    """
    try:
        return input("You > ").strip()
    except EOFError:
        return ""
