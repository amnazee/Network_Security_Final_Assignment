import time

def extended_gcd(a, b):
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b)."""
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
    """Return d with a*d ≡ 1 (mod m). Raises ValueError if none exists."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m} (gcd = {g})")
    return x % m


def generate_private_key(p, q, e):
    """Return (n, d) for the primes p, q and public exponent e."""
    n = p * q
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    return n, d


def decrypt(c, d, n):
    """Standard decryption: m = c^d mod n."""
    return pow(c, d, n)


def crt_precompute(p, q, d):
    """Compute dp, dq and qinv."""
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = mod_inverse(q, p)
    return dp, dq, qinv


def decrypt_crt(c, p, q, dp, dq, qinv):
    """CRT decryption (Garner's recombination)."""
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = (qinv * (m1 - m2)) % p
    return m2 + h * q


def decrypt_crt_library(c, p, q, dp, dq, qinv):
    """Same result, using the slide's form for h when m1 < m2:
    h = qinv * (m1 + floor(q/p)*p - m2) mod p."""
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    if m1 < m2:
        h = (qinv * (m1 + (q // p) * p - m2)) % p
    else:
        h = (qinv * (m1 - m2)) % p
    return m2 + h * q


def solve_crt(p, q, e, c):
    """Return n, d, the CRT values and the plaintext m."""
    n, d = generate_private_key(p, q, e)
    dp, dq, qinv = crt_precompute(p, q, d)
    m = decrypt_crt(c, p, q, dp, dq, qinv)
    return {"n": n, "d": d, "dp": dp, "dq": dq, "qinv": qinv, "m": m}


def read_int(prompt, min_value=None):
    """Ask until the user enters a valid whole number."""
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
    print("RSA with CRT acceleration: enter the values from your exercise.")
    p = read_int("p (prime): ", min_value=2)
    q = read_int("q (prime): ", min_value=2)
    e = read_int("e (public exponent): ", min_value=1)
    c = read_int("c (ciphertext): ", min_value=0)

    try:
        r = solve_crt(p, q, e, c)
    except ValueError as err:
        print(f"Error: {err}")
    else:
        n, d = r["n"], r["d"]
        print(f"n    = {n}")
        print(f"d    = {d}")
        print(f"dp   = {r['dp']}  (d mod p-1)")
        print(f"dq   = {r['dq']}  (d mod q-1)")
        print(f"qinv = {r['qinv']}  (q^-1 mod p)")
        print(f"m    = {r['m']}")

        m_plain = decrypt(c, d, n)
        print(f"Check with standard decryption: {m_plain} "
              f"({'match' if m_plain == r['m'] else 'MISMATCH'})")

        reps = 2000
        t0 = time.perf_counter()
        for _ in range(reps):
            decrypt(c, d, n)
        t_std = time.perf_counter() - t0

        t0 = time.perf_counter()
        for _ in range(reps):
            decrypt_crt(c, p, q, r["dp"], r["dq"], r["qinv"])
        t_crt = time.perf_counter() - t0
        print(f"Timing over {reps} decryptions: standard {t_std:.4f}s, "
              f"CRT {t_crt:.4f}s")