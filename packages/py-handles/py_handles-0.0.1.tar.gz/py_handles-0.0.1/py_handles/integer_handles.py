"""
Integer handles:

Used for handling integer values (prime numbers, adding)
"""


# Basic operations - add, sub, mult, div
def add(*args: int) -> int:
    """
    Takes in multiple parameters and adds them together.
    """

    val = 0
    for i in args:
        val += i

    return val


def sub(*args: int) -> int:
    """
    Takes in multiple parameters and takes the first given
    parameter as a starting point. From there it subtracts.
    """

    val = args[0]
    for i in args[1:]:
        val -= i

    return val


def mult(*args: int) -> int:
    """
    Takes in multiple parameters and multiplies them together.
    """

    val = args[0]
    for i in args[1:]:
        val *= i

    return val


def div(*args: int) -> int:
    """
        Takes in multiple parameters and takes the first given
        parameter as a starting point. From there it divides.
    """

    val = args[0]
    for i in args[1:]:
        val /= i

    return val


# Prime numbers
def is_prime(num: int) -> bool:
    """
    Takes in a number and checks if it is prime.

    :param num:
    """

    if num <= 1:
        return False

    return all(num % i != 0 for i in range(2, num))


def primes_till(max_limit: int) -> list:
    """
    Find prime numbers from 0 till the max_limit
    and returns a list. Uses the is_prime() function.

    :param max_limit:
    """

    primes = list()
    for i in range(2, max_limit):
        if is_prime(i):
            primes.append(i)

    return primes
