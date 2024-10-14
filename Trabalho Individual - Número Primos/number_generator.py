import time

SUPPERTED_ALGORITHMS = ['linear-congruential', 'xorshift']
SUPPORTED_LENGTHS = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]


class PseudoRandomNumberGenerator:
    def __init__(self, algorithm, seed):
        if algorithm not in SUPPERTED_ALGORITHMS:
            raise ValueError('Algorithm not supported')
        if not seed:
            raise ValueError('Seed must be provided')
        
        self.algorithm = algorithm

        if isinstance(seed, str):
            seed = hash(seed)

        self.seed = seed

    def _generate(self, bit_length):
        raise NotImplementedError('Subclass must implement abstract method')

    def generate(self):
        result = {
            "algorithm": self.algorithm,
            "seed": self.seed,
            "results": []
        }

        for bit_length in SUPPORTED_LENGTHS:
            start_time = time.time()
            number = self._generate(bit_length)
            end_time = time.time()

            result["results"].append({
                "number": number,
                "bit_length": bit_length,
                "duration": end_time - start_time
            })
        
        return result
    
    def single_generate(self, bit_length):
        start_time = time.time()
        number = self._generate(bit_length)
        end_time = time.time()

        return {
            "number": number,
            "bit_length": bit_length,
            "duration": end_time - start_time
        }
        

class LinearCongruential(PseudoRandomNumberGenerator):
    def __init__(self, seed):
        super().__init__('linear-congruential', seed)
        self.state = self.seed & 0xFFFFFFFF # 32-bit seed

    def _linear_congruential(self):
        """Linear congruential generator."""
        a = 1664525
        c = 1013904223
        m = 2**32

        x = self.state
        x = (a * x + c) % m

        self.state = x

        return self.state
    
    def _generate(self, bit_length):
        """Generates a random number with the given bit length."""
        num_bits = 0
        result = 0

        while num_bits < bit_length:
            chunk = self._linear_congruential()
            num_bits += 32
            result = (result << 32) | chunk

        # Mask out the bits we don't need
        mask = (1 << bit_length) - 1
        return result & mask



class Xorshift(PseudoRandomNumberGenerator):
    def __init__(self, seed):
        super().__init__('xorshift', seed)
        self.state = self.seed & 0xFFFFFFFF # 32-bit seed

    def _xorshift32(self):
        """Xorshift generator."""
        x = self.state

        x ^= x << 13
        x ^= x >> 17 
        x ^= x << 5 
        self.state = x & 0xFFFFFFFF

        return self.state 

    def _generate(self, bit_length):
        """Generates a random number with the given bit length."""
        num_bits = 0
        result = 0

        while num_bits < bit_length:
            chunk = self._xorshift32()
            num_bits += 32
            result = (result << 32) | chunk

        # Mask out the bits we don't need
        mask = (1 << bit_length) - 1
        return result & mask        
        
