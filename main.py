import argparse
from functools import reduce
from math import gcd

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-k', '--known-elements', metavar='ELEMENT', dest='known', nargs='+', type=int,
                           help='Known values', required=True)
parser.add_argument('-m', '--modulus', metavar='MODULUS', dest='modulus', type=int, help='LCG modulus')
parser.add_argument('-a', '--multiplier', metavar='MULTIPLIER', dest='multi', type=int, help='LCG multiplier')
parser.add_argument('-c', '--increment', metavar='INCREMENT', dest='inc', type=int, help='LCG increment')
parser.add_argument('-n', '--next', metavar='COUNT', dest='next', type=int, help='Calculate next values')
args = parser.parse_args()


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return multiplier


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus


class LCG:
    # Xn = (a*Xn-1 + c) % n
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed


known_elements = args.known
modulus = args.modulus
multiplier = args.multi
increment = args.inc
if modulus is None:
    if len(known_elements) < 6:
        print('At least 6 known values are needed to calculate the modulus')
        exit()
    modulus = crack_unknown_modulus(known_elements)

if multiplier is None:
    if len(known_elements) < 3:
        print('At least 3 known values are needed to calculate the multiplier')
        exit()
    multiplier = crack_unknown_multiplier(known_elements, modulus)

if increment is None:
    if len(known_elements) < 2:
        print('At least 2 known values are needed to calculate the increment')
        exit()
    increment = crack_unknown_increment(known_elements, modulus, multiplier)

print('''Modulus: {}
Multiplier: {}
Increment: {}'''.format(modulus, multiplier, increment))

if args.next is not None:
    print('\nCalculating next values:')
    lcg = LCG(known_elements[-1], multiplier, increment, modulus)
    for _ in range(args.next):
        print(lcg.next())
