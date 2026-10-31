def extended_gcd(a, b):
    """Return (g, x, y) such that a*x + b*y = g = gcd(a, b).

    This is the back-substitution step from the class notes, done in a loop.
    """
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_r, old_x, old_y


def mod_inverse(a, m):
    """Return d such that a*d ≡ 1 (mod m). Raises if no inverse exists."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m} (gcd = {g})")
    return x % m


def generate_private_key(p, q, e):
    """Compute the RSA modulus n and private exponent d from primes p, q and public exponent e."""
    n = p * q
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    return n, d


def encrypt(m, e, n):
    """c = m^e mod n"""
    return pow(m, e, n)


def decrypt(c, d, n):
    """m = c^d mod n"""
    return pow(c, d, n)


def solve(p, q, e, c):
    """Solve a textbook RSA exercise: find d and the plaintext m from p, q, e, c."""
    n, d = generate_private_key(p, q, e)
    m = decrypt(c, d, n)
    return {"n": n, "phi": (p - 1) * (q - 1), "d": d, "m": m}


def read_int(prompt, min_value=None):
    """Keep asking until the user enters a valid integer."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if min_value is not None and value < min_value:
            print(f"  Please enter a number >= {min_value}.")
            continue
        return value


if __name__ == "__main__":
    print("RSA solver: enter the values from your exercise.")
    p = read_int("p (prime): ", min_value=2)
    q = read_int("q (prime): ", min_value=2)
    e = read_int("e (public exponent): ", min_value=1)
    c = read_int("c (ciphertext): ", min_value=0)

    try:
        r = solve(p, q, e, c)
    except ValueError as err:
        print(f"Error: {err}")
    else:
        print(f"n   = {r['n']}")
        print(f"phi = {r['phi']}")
        print(f"d   = {r['d']}")
        print(f"m   = {r['m']}")