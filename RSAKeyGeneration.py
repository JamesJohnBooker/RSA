import random #This is necessary to make use of Python's `random' function, as random numbers are used for generating and testing potential primes.
import math #This is necessary to make use of the `ceil' function in generating bounds for the RSA modulus and primes.



def modularExponentiation(base, exponent, modulus): #This function performs modular exponentiation using a square-and-multiply algorithm, reducing intermediate steps modulo `modulus'. The algorithm can also perform exponentiation without reducing intermediate steps, if desired, by passing 0 as the `modulus' parameter (since performing calculations modulo 0 isn't defined anyway). This is done when computing lower and upper bounds for randomly generated primes, with the bounds based on the desired bit length of the RSA modulus n.
    value = 1 #The variable `value' is initialised to 1, and is returned as `value' = `base'^(`exponent') mod (`modulus').
    while exponent > 0: #The square-and-multiply algorithm based on the one described in the RSA section of this project runs by incrementally increasing `value' based on the current value of `exponent`, until `exponent' = 0.
        if exponent % 2 == 1: #If `exponent' is odd, then `value' is multiplied by `base' and `exponent' is decremented by 1.
            value = value * base
            if modulus != 0: #If the value of `modulus' is non-zero, then `value' is reduced modulo `modulus' between calculations.
                value = value % modulus
            exponent = exponent - 1
        else: #If `exponent' is even, then `base' is squared and `exponent' is halved.
            base = base * base
            if modulus != 0: #If the value of `modulus' is non-zero, then `base' is reduced modulo `modulus' between calculations.
                base = base % modulus
            exponent //= 2
    return value #The variable `value' (which now equals `base'^(`exponent') mod (`modulus')) is passed back to wherever modularExponentiation() was called from.



def generateLargeOddNumber(lowerBound, upperBound): #This function takes an upper and lower bound for a potential prime and generates numbers in that range until an odd one is found. This eliminates trivially non-prime numbers and theoretically halves the number of numbers that would need to be tested before a prime is found (as mentioned previously in the RSA section of this project).
    pIsOdd = False #The boolean variable `pIsOdd' (determining whether or not `p' is an odd number) is initialised to be false.
    while pIsOdd == False: #This while loop runs until a generated `p' is odd.
        p = random.randint(lowerBound, upperBound) #`p' is defined to be a random integer between `lowerBound' and `upperBound' (inclusive).
        if p % 2 == 1: #If `p' is odd, then the loop ends. Otherwise another value of `p' is generated.
            pIsOdd = True
    return p #The generated odd number `p' is returned to generateRSAPrime() to be tested for primality.



def primalityTestMillerRabin(p, repetitionsOfMillerRabin): #This function performs `repetitionsOfMillerRabin' repetitions of the Miller-Rabin primality test on the number `p'. 
    pMinusOneFactor = p - 1 #`pMinusOneFactor' is initialised to be `p' - 1. Since `p' is odd, `p' - 1 is even, and so `p' - 1 = (2^(k))*t for some natural numbers k and t, where t is odd.
    powerOfTwo = 0 #`powerOfTwo' is initialised to be 0, and is incremented to be equal to k (as defined above).
    while pMinusOneFactor % 2 == 0: #This while loop divides `pMinusOneFactor' by 2 until the resulting value is odd, incrementing `powerOfTwo' by 1 with each division. That is, it divides `pMinusOneFactor' by 2 and increments `powerOfTwo' k times until `pMinusOneFactor' = t and `powerOfTwo' = k, as k and t are defined above.
        pMinusOneFactor //= 2
        powerOfTwo += 1
    t = pMinusOneFactor #Since `pMinusOneFactor' = t (as t is defined above), the variable `t' is initialised for convenience.
    k = powerOfTwo #Since `powerOfTwo' = k (as k is defined above), the variable `k' is initialised for convenience.
    parametersTested = [] #This list keeps track of all the parameters used to test `p' for primality.
    for i in range(0, repetitionsOfMillerRabin): #This for loop repeats the Miller-Rabin primality test on `p' a number of times equal to `repetitionsOfMillerRabin'. Note that `for i in range(0, repetitionsOfMillerRabin)' here means for all i in {0, 1, 2, ..., `repetitionsOfMillerRabin' - 1} and so the loop runs `repetitionsOfMillerRabin' times.
        parameterTestedAlready = True
        while parameterTestedAlready == True: #This while loop generates parameters until a new one that hasn't been tested before is generated, at which point the loop breaks and the test begins.
            a = random.randint(2, p - 2) #Generates a random parameter to test the prime `p'.
            if a not in parametersTested:
                parametersTested.append(a)
                break
        at = modularExponentiation(a, t, p) #Initialises the variable `at' as `at' = `a'^(`t') mod (`p').
        if at != 1: #These nested if statements track the conditions of the Miller-Rabin primality test. If `a'^(`t') is not congruent to 1 or -1 mod (`p') and if `a'^(`t'*2^(`j')) is not congruent to -1 mod (`p') for all 1 <= `j' <= `k' - 1, then `p' is composite, in which case the function returns false. Otherwise, the code skips to the next loop where a new parameter `a' is generated and tested.
            if at != p - 1:
                for j in range(0, k):
                    at = modularExponentiation(at, 2, p)
                    if at != p - 1:
                        if j == k - 1: #If `p' has met the conditions of each if statement up to `j' = `k' - 1, then it has met all the requirements of the test to prove that `p' is composite.
                            return False #The fact that `p' is not prime is returned to generateRSAPrime().
                        else:
                            continue
                    else:
                        break
                continue
            else:
                continue
        else:
            continue
    return True #If `p' has failed to be proven composite for each iteration of the for loop, then the probability that `p' is not prime is at most (1/4)^(-`repetitionsOfMillerRabin'), and so the fact that `p' is (almost certainly) prime is returned to generateRSAPrime().


def generateRSAPrime(primeLength, repetitionsOfMillerRabin): #This function generates a prime `p' with `primeLength' digits, such that the probability that `p' is not prime is at most (1/4)^(-`repetitionsOfMillerRabin') (arbitrarily small).
    lowerBound = modularExponentiation(10, primeLength - 1, 0) #The lower bound for `p' is set to be the smallest `primeLength'-digit number.
    upperBound = modularExponentiation(10, primeLength, 0) - 1 #The upper bound for `p' is set to be the largest `primeLength'-digit number.
    pIsProbablyPrime = False
    while pIsProbablyPrime == False: #This while loop continually generates odd numbers `p' and tests them for primality until one is found that is not proven composite after `repetitionsOfMillerRabin' iterations of the Miller-Rabin test.
        p = generateLargeOddNumber(lowerBound, upperBound)
        pIsProbablyPrime = primalityTestMillerRabin(p, repetitionsOfMillerRabin)
    return p #Returns the (probable) prime `p' to generateRSAKeys().



def compute_n(p, q): #This function takes two primes `p' and `q' and returns the RSA modulus `n' (of bit length at least `modulusBitLengthLowerBound').
    n = p * q
    return n #The generated RSA modulus is returned to generateRSAKeys().



def computeEulerTotient(p, q): #This function takes two RSA primes `p' and `q' and returns Euler's Totient function phi(`n') = (`p' - 1)(`q' - 1).
    EulerTotient = (p - 1) * (q - 1)
    return EulerTotient #The computed value for Euler's Totient function is returned to generateRSAKeys().



def generateEncryptionExponents(EulerTotient): #This function generates the encryption and decryption exponents, `e' and `d' respectively.
    eIsCoprimeToEulerTotient = False
    while eIsCoprimeToEulerTotient == False: #This loop generates and tests potential encryption exponents (and finds their corresponding decryption exponents with respect to `EulerTotient') until one is found that is coprime to `EulerTotient'.
        e = random.randint(2, EulerTotient - 1)
        x, y, h = extendedEulideanAlgorithm(e, EulerTotient) #The integers `x',`y' and `h' computed by the extended Euclidean algorithm satisfy (`e' * `x') + (`EulerTotient' * `y') = `h', where `h' is the highest common factor of `e' and `EulerTotient'.
        if h == 1: #If `h' = 1, then the highest common factor of `e' and `EulerTotient' is 1 and so they are coprime. 
            d = x % EulerTotient #Since we want `d' in the same range as `e', we reduce `d' modulo `EulerTotient'.
            return e, d #`e' and `d' are returned to generateRSAKeys() as the encryption and decryption exponents.



def extendedEulideanAlgorithm(e, EulerTotient): #This function computes the extended Euclidean algorithm.
    valuesToHaveHCFComputed = [EulerTotient, e] #This list of values is such that the highest common factor of entry i and i + 1 is equal to the highest common factor of entry i + 1 and i + 2. It will include the remainders at the intermediate steps of the extended Euclidean algorithm.
    quotients = [] #These are quotients from divisions performed during the extended Euclidean algorithm.
    a = EulerTotient // e #`a' is initialised to be the quotient when `EulerTotient' is divided by `e'.
    b = EulerTotient % e #`b' is initialised to be the remainder when `EulerTotient' is divided by `e'.
    if b == 0: #If `b' = 0 then `EulerTotient' = `k' * `e' for some natural number `k', in which case the highest common factor of `EulerTotient' and `e' is `e'. Hence, `x' = `k' + 1, `y' = -1 and `h' = `e' satisfy (`e' * `x') + (`EulerTotient' * `y') = `h', where `h' is the highest common factor of `e' and `EulerTotient'.
        return a + 1, -1, e
    i = 1 #`i' is initialised to be equal to 1 for the purposes of performing calculations with elements of `valuesToHaveHCFComputed'.
    while b != 0: #This while loop computes all the remainders and quotions when the `i'-th element of `valuesToHaveHCFComputed' is divided by the (`i' + 1)-th element of `valuesToHaveHCFComputed'. At the point when `b' = 0, the last value to be appended to `valuesToHaveHCFComputed' will be the highest common factor of `e' and `EulerTotient'.
        quotients.append(a) #The intermediate quotients are added to `quotients'.
        valuesToHaveHCFComputed.append(b) #The intermediate remainders are added to `valuesToHaveHCFComputed'.
        a = valuesToHaveHCFComputed[i] // valuesToHaveHCFComputed[i + 1]
        b = valuesToHaveHCFComputed[i] % valuesToHaveHCFComputed[i + 1]
        i += 1 #`i' is incremented by 1 to move onto the next pair of remainders, which will have the same highest common factor as the previous pair.
    r = 1
    s = -quotients[len(quotients) - 1] #`r' and `s' are initialised such that valuesToHaveHCFComputed[len(valuesToHaveHCFComputed) - 1] = (`r' * valuesToHaveHCFComputed[len(valuesToHaveHCFComputed) - 3]) + (`s' * valuesToHaveHCFComputed[len(valuesToHaveHCFComputed) - 2]). Computing the second half of the extended Euclidean algorithm, notice that the quotients increase (in size) alternately as the increasingly large remainders from `valuesToHaveHCFComputed' are substituted in. First `r' changes, then `s', then `r' and so on until the resulting equation gives the sought values of `x', `y'.
    for j in range(1, len(quotients)):
        if j % 2 == 0: #On every even step (2nd, 4th, 6th, ...) `s' increases, and increments by the following formula.
            s = s - (quotients[(len(quotients) - 1) - j] * r)
        elif j % 2 == 1: #On every odd step (1st, 3rd, 5th, ...) `r' increases, and increments by the following formula.
            r = r - (quotients[(len(quotients) - 1) - j] * s)
    if len(quotients) % 2 == 0: #The last value to be increased (out of `r' and `s') is equal to `x' in the expression (`e' * `x') + (`EulerTotient' * `y') = `h', where `h' is the highest common factor of `e' and `EulerTotient'. The other is equal to `y'. So if the length of the list `quotients' is even, then `r' was increased last, so `x' = `r' and `y' = `s'.
        return r, s, valuesToHaveHCFComputed[len(valuesToHaveHCFComputed) - 1] #As stated above, the final value in `valuesToHaveHCFComputed' is the highest common factor of `e' and `EulerTotient'. The relevant values are returned to generateEncryptionExponent(), to check that `e' and `EulerTotient' are coprime.
    elif len(quotients) % 2 == 1: #On the other hand if the length of the list `quotients' is odd, then `s' must have been increased last, so `x' = `s' and `y' = `r'.
        return s, r, valuesToHaveHCFComputed[len(valuesToHaveHCFComputed) - 1]



def generateRSAKeys(): #This function provides the parameters and calls the functions that generate the RSA keys. The only parameters that need to be chosen are a lower bound for the number of bits in the RSA modulus and the number of repetitions of the Miller-Rabin test. I have set them to be 1024 bits and 100 repetitions respectively by default.
    modulusBitLengthLowerBound = 1024 #This is a lower bound for the desired number of bits in the RSA modulus.
    primeBitLengthLowerBound = math.ceil(0.5 * modulusBitLengthLowerBound) #This is a lower bound for the desired number of bits in the RSA primes (so that the RSA modulus is at least as large as desired).
    primeLength = math.ceil((primeBitLengthLowerBound * math.log(2, 10)) + 1) #This is a lower bound for the desired number of decimal digits in the RSA primes (so that the RSA modulus is at least as large as desired).
    repetitionsOfMillerRabin = 100 #This is the desired number of repetitions of the Miller-Rabin test to be performed, which will determine the margin for error of the primality of the RSA primes.
    pqDistinct = False
    while pqDistinct == False: #If `p' = `q', then `p' and `q' can be found easily by computing the square root of the RSA modulus. From here, the decryption exponent `d' can be found quickly, which will render all future communications with this particular set of RSA keys insecure. This while loop generates primes `p' and `q' of the appropriate size until the two generated primes are distinct.
        p = generateRSAPrime(primeLength, repetitionsOfMillerRabin) #`p' is a (probable) prime number generated to have `primeLength' decimal digits and known to be prime with probability at least 1 - (1/4)^(-`repetitionsOfMillerRabin').
        q = generateRSAPrime(primeLength, repetitionsOfMillerRabin) #`q' is a (probable) prime number generated to have `primeLength' decimal digits and known to be prime with probability at least 1 - (1/4)^(-`repetitionsOfMillerRabin').
        if p != q:
            pqDistinct = True
    n = compute_n(p, q) #This is the RSA modulus, used for encryption and decryption.
    EulerTotient = computeEulerTotient(p, q) #This is the value of Euler's Totient function when passed `n' (phi(`n')), used to compute the encryption and decryption exponents `e' and `d'.
    e, d = generateEncryptionExponents(EulerTotient) #The encryption and decryption exponents are computed.
    #From here, a message `m' with 0 <= `m' <= `n' - 1 can be encrypted by computing `c' = modularExponentiation(`m', `e', `n'). `m' can then be recovered from `c' by computing `m' = modularExponentiation(`c', `d', `n').
    


generateRSAKeys() #This just calls the function generateRSAKeys().