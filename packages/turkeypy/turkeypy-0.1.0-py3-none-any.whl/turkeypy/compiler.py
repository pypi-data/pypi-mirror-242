from turkeypy.vm import OPCODE


class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)


def compile(code: str):
    """Compiles source code into a list of tokens."""
    lines = code.splitlines()
    tokens = []
    for line_no, line in enumerate(lines, start=1):
        words = line.split()
        # Raise syntax error if any word other than 'turkey' or whitespace is found
        if word_set := (set(words) - {"turkey", " "}):
            raise ParseError(f"Invalid token(s) on line {line_no}: {' '.join(word_set)}")
            return False

        num_turkeys = len(line.split())
        # Any number of turkeys > 9 is used as is
        if num_turkeys > 9:
            tokens.append(num_turkeys)
        else:
            tokens.append(OPCODE(num_turkeys))
    return tokens
