def line(width: int) -> str:
    return '\u2500' * width


def subscript(x: int) -> str:
    if x == 0:
        return '₀'
    s = []
    while x:
        x, d = divmod(x, 10)
        s.append(chr(0x2080 + d))
    return ''.join(reversed(s))
