from Functions import *
from Methods import *

def resolution_solver(clauses, p=False):
    clauses = [frozenset(clause) for clause in clauses]
    idx = 1

    for clause in clauses:
        if p: print(f"{idx}: {set(clause)}")
        idx += 1

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
                resolvent = frozenset(resolvent)
                if not resolvent:
                    if p:
                        print(f"({idx}) {{}} from {set(ci)} and {set(cj)}")
                    print("UNSATISFIABLE")
                    return False
                if resolvent not in clause_set and resolvent not in new_clause_set:
                    if p: print(f"{idx}: {set(resolvent)} from {set(ci)} and {set(cj)}")
                    new_clause_set.add(resolvent)
                    idx += 1
        if not new_clause_set:
            if p:
                print("\n  No new resolvent to be added")
            print("SATISFIABLE")
            return True
        clauses.extend(new_clause_set)


def dp_solver(clauses, p=False):
    print_clause_set(clauses, p)
    clauses = unit_clause_rule(clauses, p)
    if clauses == {frozenset()}:
        print("UNSATISFIABLE")
        return False

    clauses = pure_literal_rule(clauses, p)
    if clauses == {frozenset()}:
        print("UNSATISFIABLE")
        return False

    if not clauses:
        print("SATISFIABLE")
        return True

    if p: print("Can't apply anymore DP rules, applying resolution")
    return resolution_solver(clauses, p)


def dpll(clauses, s, splits=0, p=False):
    print_clause_set(clauses, p)
    clauses = unit_clause_rule(clauses, p)
    e = {frozenset()}

    if e in clauses or clauses == e:
        if p: print(f"UNSATISFIABLE (contains empty clause)")
        return False, splits
    elif not clauses:
        if p: print(f"SATISFIABLE (no clauses left)")
        return True, splits

    clauses = pure_literal_rule(clauses, p)
    if not clauses:
        if p: print(f"SATISFIABLE (pure literal rule)")
        return True, splits

    if p: print(f"No more unit clause or pure literal rules, choosing a literal to branch on...")
    s += 1
    l = literal_choice(clauses, "moms")
    if p: print(f"Adding literal {l} to positive clause set")


    splits += 1


    new_clauses_pos = clauses.copy()
    new_clauses_pos.add(frozenset({l}))
    print_clause_set(new_clauses_pos, p)

    if p: print(f"Recursively calling DPLL with positive branch for literal {l}")
    result, splits = dpll(new_clauses_pos, s, splits, p)
    if result:
        return True, splits

    if p: print(f"Adding literal {l}, to negative clause set")
    new_clauses_neg = clauses.copy()
    new_clauses_neg.add(frozenset({-l}))
    print_clause_set(new_clauses_neg, p)

    if p: print(f"Recursively calling DPLL with negative branch for literal {-l}")
    return dpll(new_clauses_neg, s, splits, p)


def dpll_solver(clauses, p=False):
    s = 0
    if p: print("Starting DPLL Solver:")
    result, splits = dpll(clauses, s, 0, p=p)
    if result:
        print("SATISFIABLE")
    else:
        print("UNSATISFIABLE")
    if p: print(f"Number of splits: {splits}")


###### MAIN #######

clauses = load_from_file("clauses1.txt")
print("\n--- Resolution Solver Output ---")
#resolution_solver(clauses, p=False)
print("\n--- DP Solver Output ---")
#dp_solver(clauses, p=False)
print("\n--- DPLL Solver Output ---")
dpll_solver(clauses, p=False)
