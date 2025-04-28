
####### Function for printing clause set ########
def print_clause_set(clauses):
    idx = 1
    for clause in clauses:
        if clause:
            print(f"{idx}: {set(clause)}")
            idx += 1
        else:
            print("EMPTY SET")

####### Function for reading from file ########
def load_from_file(filename):
    clauses = set()
    with open(filename, 'r') as f:
        for line in f:
            literals = {int(x) for x in line.strip().split() if x != '0'}
            if literals:
                clauses.add(frozenset(literals))
    return clauses


######## Function for set of literals #######
def literal_set(clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)  # Add all elements from each frozenset
    return literals


######Functions for RESOLUTION #######
def resolve(ci, cj):
    resolvents = []
    for lit in ci:
        if -lit in cj:
            resolvent = (ci - {lit}) | (cj - {-lit})
            if not is_tautology(resolvent):
                resolvents.append(resolvent)
    return resolvents

def is_tautology(clause):
    return any(-lit in clause for lit in clause)



######Functions for DP and DPLL #######


def is_unit_clause(clause):
    return len(clause) == 1

def find_unit_clauses(clauses):
    return {next(iter(c)) for c in clauses if is_unit_clause(c)}

def unit_clause_rule(clauses):
    while True:
        unit_literals = find_unit_clauses(clauses)
        if not unit_literals:
            break
        for lit in unit_literals:
            if clauses and clauses != {frozenset()}:
                print(f"Applying unit clause rule with literal {lit}")
                clauses = {c for c in clauses if lit not in c}
                neg_literal = -lit
                new_clauses = set()
                for clause in clauses:
                    if neg_literal in clause:
                        new_clause = frozenset(l for l in clause if l != neg_literal)
                        if not new_clause:
                            return {frozenset()}
                        new_clauses.add(new_clause)
                    else:
                        new_clauses.add(clause)
                clauses = new_clauses
                print_clause_set(clauses)
    return clauses




def find_pure_literals(clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)
    pure_literals = {lit for lit in literals if -lit not in literals}
    return pure_literals


def pure_literal_rule(clauses):
    while True:
        if not clauses:
            return clauses

        pure_literals = find_pure_literals(clauses)
        if not pure_literals:
            break

        for lit in pure_literals:
            if clauses == {frozenset()}:
                return clauses
            print(f"Applying pure literal rule for {lit}")
            clauses = {clause for clause in clauses if lit not in clause}
            print_clause_set(clauses)

            if not clauses:
                return clauses
    return clauses





