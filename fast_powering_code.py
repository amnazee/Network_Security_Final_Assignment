import sys

def fast_power(g, A, N):
    bits = bin(A)[2:]                         

    a = [g % N]                               
    for _ in range(len(bits) - 1):
        a.append(a[-1] * a[-1] % N)

    result = 1                             
    for i, bit in enumerate(reversed(bits)):
        if bit == "1":
            result = result * a[i] % N

    return result, bits, a


def main():
    g = int(input("Enter the base g: "))
    A = int(input("Enter the exponent A: "))
    N = int(input("Enter the modulus N: "))

    result, bits, a = fast_power(g, A, N)
    used = [i for i, b in enumerate(reversed(bits)) if b == "1"]
    used.reverse()                           

    print(f"Compute {g}^{A} mod {N}\n")

    powers = " + ".join(f"2^{i}" for i in used)
    values = " + ".join(str(2 ** i) for i in used)
    print(f"Step 1:  {A} = {bits}_2 = {powers} = {values}\n")

    print("Step 2:")
    for i, ai in enumerate(a):
        print(f"  a{i} = {g}^(2^{i}) mod {N} = {ai}")
    print()

    product = 1
    for i in used:
        product *= a[i]

    terms = " * ".join(f"{g}^(2^{i})" for i in used)
    names = " * ".join(f"a{i}" for i in used)
    numbers = " * ".join(str(a[i]) for i in used)

    print("Step 3:")
    print(f"  {g}^{A} = {terms}  (mod {N})")
    print(f"        = {names}")
    print(f"        = {numbers}")
    print(f"        = {product} mod {N}")
    print(f"        = {result}")


if __name__ == "__main__":
    main()
