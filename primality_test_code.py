#!/usr/bin/env python3
def decompose(n_minus_1: int) -> tuple[int, int]:
    s, d = 0, n_minus_1
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def power_lines(a: int, d: int, n: int) -> tuple[int, list[str]]:
    q, r = divmod(d, 10)
    lines: list[str] = []

   
    if q > 12:
        x = pow(a, d, n)
        lines.append(f"        {a}^{d} = {x}  (mod {n})   "
                     f"[long exponent: shown directly]")
        return x, lines

    if q == 0:                         
        x = pow(a, d, n)
        lines.append(f"        {a}^{d} = {x}  (mod {n})")
        return x, lines

    p10 = pow(a, 10, n)
    lines.append(f"        {a}^10 = {p10}  (mod {n})")

    cur = p10                         
    for k in range(2, q + 1):
        nxt = cur * p10 % n
        if k == 2:
            lines.append(f"        {a}^20 = {p10}^2 = {nxt}  (mod {n})")
        else:
            lines.append(f"        {a}^{10 * k} = {cur} * {p10} = {nxt}  (mod {n})")
        cur = nxt

    if r:
        ar = pow(a, r, n)
        prod = cur * ar
        x = prod % n
        if prod == x:
            lines.append(
                f"        {a}^{d} = {a}^{10 * q} * {a}^{r} = "
                f"{cur} * {ar} = {x}  (mod {n})"
            )
        else:
            lines.append(
                f"        {a}^{d} = {a}^{10 * q} * {a}^{r} = "
                f"{cur} * {ar} = {prod} = {x}  (mod {n})"
            )
    else:
        x = cur
        lines.append(f"        {a}^{d} = {a}^{10 * q} = {x}  (mod {n})")
    return x, lines


def solve(n: int, a: int = 2) -> bool:
    """Print the complete classroom solution. Returns True if probably prime."""
    print("=" * 66)
    print(f"n = {n},   a = {a}")
    print("=" * 66)

    s, d = decompose(n - 1)
    print(f"Step 1   n - 1 = {n - 1} = 2^{s} * {d}      ->   s = {s},  d = {d}")
    print(f"Step 2   a = {a}      (1 < a < n-1)")

    x, lines = power_lines(a, d, n)
    print(f"Step 3   x = a^d mod n = {a}^{d} mod {n}")
    for line in lines:
        print(line)
    print(f"         x = {x}")

    
    if x == 1 or x == n - 1:
        why = "x = 1" if x == 1 else f"x = {n - 1} = -1 (mod {n})"
        print(f"Step 4   {why}, so the witness test fails immediately.")
        print(f"\nRESULT: {n} is PROBABLY PRIME")
        return True

   
    print("Step 4   square repeatedly and look for -1 (= %d):" % (n - 1))
    seq = [x]
    for i in range(1, s):
        prev = x
        x = x * x % n
        seq.append(x)
        if x == n - 1:
            print(f"         x{i} = {prev}^2 mod {n} = {x}   <- -1 found")
            print(f"\nRESULT: {n} is PROBABLY PRIME "
                  f"(no witness for base a = {a})")
            return True
        if x == 1:
            print(f"         x{i} = {prev}^2 mod {n} = 1   <- reached 1, "
                  f"so never -1")
            break
        print(f"         x{i} = {prev}^2 mod {n} = {x}")

    print(f"         sequence: {seq}   (-1 = {n - 1} never appears)")
    print(f"\nRESULT: {n} is COMPOSITE "
          f"(a = {a} is a Miller-Rabin witness)")
    return False


def read_int(prompt: str, default: int | None = None) -> int:
    """Prompt until a whole number is entered; empty input uses `default`."""
    while True:
        try:
            text = input(prompt).strip()
        except EOFError:             
            print()
            raise SystemExit(1)
        if not text and default is not None:
            return default
        try:
            return int(text)
        except ValueError:
            print("  Please enter a whole number.")


def main() -> None:
    print("Primality test")

    while True:
        n = read_int("Enter an odd number n (>= 3): ")
        if n >= 3 and n % 2 == 1:
            break
        print("n must be odd and at least 3.")

    if n == 3:
        print("\nRESULT: 3 is PRIME.")
        return

    prompt = f"Enter a base a (1 < a < {n - 1}) [default 2]: "
    a = read_int(prompt, default=2)
    while not 1 < a < n - 1:
        print(f"  a must satisfy 1 < a < {n - 1}.")
        a = read_int(prompt, default=2)

    solve(n, a)


if __name__ == "__main__":
    main()
