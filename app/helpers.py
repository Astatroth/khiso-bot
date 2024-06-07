import re


def sanitize(string: str) -> str:
    forbidden_symbols = [
        '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
    ]
    escaped_string = string

    for i in range(len(forbidden_symbols)):
        escaped_string = escaped_string.replace(forbidden_symbols[i], "\\{}".format(forbidden_symbols[i]))

    return escaped_string


def remove_emoji(string):
    regex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        u"\u23EA"  # Rewind
                                        u"\u23E9"  # Fast-forward
                                        u"\u274C"  # Remove
                                        u"\u2757"  # Exclamation mark
                                        u"\u2705"  # Heavy check
                                        u"\u27A1"  # Backwards button
                                        u"\u2139"  # Info sign
                                        "]+\s", flags=re.UNICODE)

    return regex_pattern.sub(r'', string)
