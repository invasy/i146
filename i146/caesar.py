#!/usr/bin/env python
def caesar(s: str, k: int) -> str:
    """Шифр Цезаря — сдвиговый подстановочный шифр."""

    A = ord('А')
    E = ord('Ж') - A
    N = 33

    t = []
    for c in s:
        lower, c = c.islower(), c.upper()

        if 'А' <= c <= 'Я' or c == 'Ё':
            if c == 'Ё':
                i = E
            else:
                i = ord(c) - A

            if 'Ж' <= c <= 'Я':
                i += 1

            i = (i + k) % N

            if i == E:
                c = 'Ё'
            else:
                if i > E:
                    i -= 1
                c = chr(A + i)

        if lower:
            c = c.lower()

        t += c

    return ''.join(t)


if __name__ == '__main__':
    s1 = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    s2 = s1.lower()

    print(f'{s1}\n{caesar(s1, -4)}')
    print(f'{s2}\n{caesar(s2, 4)}')
