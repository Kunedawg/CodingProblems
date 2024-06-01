import bisect
import os


class PrimePowerChecker:
    def __init__(self, filename="prime_to_prime/prime_powers_list.txt"):
        self.prime_powers = self._load_prime_powers(filename)

    def _load_prime_powers(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        with open(filename, "r") as file:
            prime_powers = [int(line.strip()) for line in file]
        return prime_powers

    def is_prime_power(self, num):
        index = bisect.bisect_left(self.prime_powers, num)
        return (
            index < len(self.prime_powers) and self.prime_powers[index] == num
        )


# # Usage
# checker = PrimePowerChecker()
# number_to_check = 6561  # Example number to check
# if checker.is_prime_power(number_to_check):
#     print(f"{number_to_check} is a prime to a prime.")
# else:
#     print(f"{number_to_check} is not a prime to a prime.")
