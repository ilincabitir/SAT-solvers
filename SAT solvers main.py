from Functions import *
from Methods import *


def resolution_solver(clauses):
    clauses = [frozenset(clause) for clause in clauses]
    idx = 1
    '''
    for clause in clauses:
        print(f"{idx}: {set(clause)}")
        idx += 1
    '''
    while True:
        new_clause_set = set()
        clause_set = set(clauses)

        if not clauses:
            print("SATISFIABLE")
            return True
        clause_pairs = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                clause_pairs.append((clauses[i], clauses[j]))
        for (ci, cj) in clause_pairs:
            resolvents = resolve(ci, cj)
            for resolvent in resolvents:
                frozen_resolvent = frozenset(resolvent)
                if not frozen_resolvent:
                    print(f"({idx}) {{}} from {set(ci)} and {set(cj)}")
                    print("UNSATISFIABLE")
                    return False

                if frozen_resolvent not in clause_set and frozen_resolvent not in new_clause_set:
                    print(f"{idx}: {set(resolvent)} from {set(ci)} and {set(cj)}")
                    new_clause_set.add(frozen_resolvent)
                    idx += 1
        if not new_clause_set:
            print("\nNo new resolvent to be added")
            print("SATISFIABLE")
            return True
        clauses.extend(new_clause_set)


def dp_solver(clauses):
    print_clause_set(clauses)

    clauses = unit_clause_rule(clauses)
    if clauses == {frozenset()}:
        print("UNSATISFIABLE")
        return False

    clauses = pure_literal_rule(clauses)
    if clauses == {frozenset()}:
        print("UNSATISFIABLE")
        return False

    if not clauses:
        print("SATISFIABLE")
        return True

    # Otherwise, need to use resolution
    print("Can't apply anymore DP rules, applying resolution")
    return resolution_solver(clauses)


def dpll(clauses):

    clauses = unit_clause_rule(clauses)
    if clauses == {frozenset()}:
        return False
    elif not clauses:
        return True
    clauses = pure_literal_rule(clauses)
    if not clauses:
        return True
    l = literal_choice(clauses, "first_literal")
    new_clauses_pos = clauses.copy()
    new_clauses_pos.add(frozenset({l}))
    print_clause_set(new_clauses_pos)
    new_clauses_pos = unit_clause_rule(new_clauses_pos)
    if dpll(new_clauses_pos):
        return True
    new_clauses_neg = clauses.copy()
    new_clauses_neg.add(frozenset({-l}))
    new_clauses_neg = unit_clause_rule(new_clauses_neg)
    print_clause_set(new_clauses_neg)
    return dpll(new_clauses_neg)


def dpll_solver(clauses):
    if dpll(clauses):
        print("SATISFIABLE")
    else:
        print("UNSATISFIABLE")



###### MAIN ######

clauses = load_from_file("clauses1.txt")
#resolution_solver(clauses)
#dp_solver(clauses)
dpll_solver(clauses)



