import sympy


def generate_prime_powers(max_value, filename):
    # Generate a list of prime numbers up to a reasonable limit for both p and
    # q
    primes = list(
        sympy.primerange(2, 10**6)
    )  # Adjust the upper limit as needed
    power_set = set()

    for p in primes:
        for q in primes:
            if q > 1:
                value = p**q
                if value >= max_value:
                    break
                power_set.add(value)

    power_list = sorted(power_set)

    with open(filename, "w") as file:
        for number in power_list:
            file.write(f"{number}\n")


# Usage
generate_prime_powers(100000000000, "prime_powers_list.txt")
