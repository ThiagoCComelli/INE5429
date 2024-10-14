import time
import random

from number_generator import Xorshift

SUPPERTED_ALGORITHMS = ["miller-rabin", "fermat"]
SUPPORTED_LENGTHS = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]


class PrimalityCheck:
    def __init__(self, algorithm):
        if algorithm not in SUPPERTED_ALGORITHMS:
            raise ValueError("Algorithm not supported")

        self.algorithm = algorithm

    def _check(self, bit_length):
        raise NotImplementedError("Subclass must implement abstract method")

    def check(self):
        result = {"algorithm": self.algorithm, "results": []}

        xorshift = Xorshift(seed="INE5420")

        for bit_length in SUPPORTED_LENGTHS:
            start_time = time.time()
            number = xorshift.single_generate(bit_length)["number"]
            is_prime = self._check(number)
            end_time = time.time()

            result["results"].append(
                {
                    "is_prime": is_prime,
                    "number": number,
                    "bit_length": bit_length,
                    "duration": end_time - start_time,
                }
            )

        return result

    def generate_prime(self, bit_length):
        xorshift = Xorshift(seed="INE5420")

        start_time = time.time()
        number = 0
        while True:
            number = xorshift.single_generate(bit_length)["number"]
            if self._check(number):
                break

        end_time = time.time()

        return {
            "algorithm": self.algorithm,
            "results": [{"bit_length": bit_length, "duration": end_time - start_time, "is_prime": True, "number": number}],
        }


class MillerRabin(PrimalityCheck):
    def __init__(self):
        super().__init__("miller-rabin")

    def miller_rabin_test(self, n, k):
        r = 0
        d = n - 1

        while d % 2 == 0:
            r += 1
            d //= 2

        def _witness(_a, _d, _n):
            _x = pow(_a, _d, _n)
            if _x == 1 or _x == _n - 1:
                return False

            for _ in range(r - 1):
                _x = pow(_x, 2, _n)
                if _x == _n - 1:
                    return False

            return True

        for _ in range(k):
            a = random.randint(2, n - 2)
            if _witness(a, d, n):
                return False

        return True

    def _check(self, bit_length):
        if self.miller_rabin_test(bit_length, 100):
            return True
        return False


class Fermat(PrimalityCheck):
    def __init__(self):
        super().__init__("fermat")

    def fermat_test(self, n, k):
        def _witness(_a, _n):
            return pow(_a, _n - 1, _n) != 1

        if n == 2:
            return True
        if n % 2 == 0:
            return False

        for _ in range(k):
            a = random.randint(2, n - 2)
            if _witness(a, n):
                return False

        return True

    def _check(self, number):
        if self.fermat_test(number, 100):
            return True
        return False
