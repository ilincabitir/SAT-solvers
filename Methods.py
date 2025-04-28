import random
from Functions import literal_set

def literal_choice(clauses,method):
    if method=="first_literal":
        return next(iter(next(iter(clauses))))
    if method=="random_literal":
        return random.choice(list(literal_set(clauses)))

