from number_generator import LinearCongruential, Xorshift, SUPPORTED_LENGTHS
from primality_check import MillerRabin, Fermat

def log_result(result):
    is_prime_check = result["algorithm"] in ["miller-rabin", "fermat"]
    print(f"\nLog Result {'Primality Check' if is_prime_check else 'Pseudo Random Number Generator'}")
    print("Algorithm:", result["algorithm"])

    if is_prime_check:
        print("results:")
        for duration in result["results"]:
            print(f"Bit length: {duration['bit_length']}, Duration: {duration['duration']}, Is Prime: {duration["is_prime"]}, Number: {duration['number']}")
    else:
        print("Seed:", result["seed"])
        print("results:")
        for duration in result["results"]:
            print(f"Bit length: {duration['bit_length']}, Duration: {duration['duration']}, Number: {duration['number']}")
        
def pseudo_random_number_generator():
    all_results_lcg = []
    summary_results_lcg = {}

    for i in range(100):
        linear_congruential = LinearCongruential(seed="INE5420")
        result = linear_congruential.generate()
        all_results_lcg.append(result)
    
    all_results_lcg = all_results_lcg[1:]

    for lcg in all_results_lcg:
        for duration in lcg["results"]:
            bit_length = duration["bit_length"]
            summary_results_lcg[bit_length] = summary_results_lcg.get(bit_length, 0) + duration["duration"]

    for bit_length in summary_results_lcg:
        summary_results_lcg[bit_length] = summary_results_lcg[bit_length] / len(all_results_lcg)

    print()
    print("linear_congruential | Average Exec Duration (by bits size):", summary_results_lcg)
    log_result(all_results_lcg[0])    


    all_results_xorshift = []
    summary_results_xorshift = {}
    
    for i in range(1000):
        xorshift = Xorshift(seed="INE5420")
        result = xorshift.generate()
        all_results_xorshift.append(result)
    
    all_results_xorshift = all_results_xorshift[1:]

    for xorshift in all_results_xorshift:
        for duration in xorshift["results"]:
            bit_length = duration["bit_length"]
            summary_results_xorshift[bit_length] = summary_results_xorshift.get(bit_length, 0) + duration["duration"]
    
    for bit_length in summary_results_xorshift:
        summary_results_xorshift[bit_length] = summary_results_xorshift[bit_length] / len(all_results_xorshift)
    
    print()
    print("xorshift | Average Exec Duration (by bits size):", summary_results_xorshift)
    log_result(all_results_xorshift[0])    

def primality_check():
    miller_rabin = MillerRabin()
    result = miller_rabin.check()
    log_result(result)

    fermat = Fermat()
    result = fermat.check()
    log_result(result)

def primality_generator():
    miller_rabin = MillerRabin()
    for bit_length in SUPPORTED_LENGTHS:
        result = miller_rabin.generate_prime(bit_length)
        log_result(result)
    
    fermat = Fermat()
    for bit_length in SUPPORTED_LENGTHS:
        result = fermat.generate_prime(bit_length)
        log_result(result)
    

if __name__ == '__main__':
    pseudo_random_number_generator()
    # primality_check()
    
    # primality_generator()