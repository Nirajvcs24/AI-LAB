class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"?{self.name}"

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


def is_variable(expr):
    """Utility to check if an expression is a variable."""
    return isinstance(expr, Variable)


def occurs_in(var, expr):
    """Occurs Check: Returns True if var appears inside expr."""
    if var == expr:
        return True
    elif isinstance(expr, list):
        # Recursively check elements/arguments of expressions/predicates
        return any(occurs_in(var, arg) for arg in expr[1:])
    return False


def apply_subst(subst, expr):
    """Applies a substitution set (dictionary) to an expression."""
    if not subst:
        return expr
    if is_variable(expr):
        return subst.get(expr, expr)
    if isinstance(expr, list):
        return [apply_subst(subst, item) for item in expr]
    return expr


def unify(psi1, psi2, subst=None):
    """
    Implementation of the FOL Unification Algorithm from the image.
    psi1, psi2: Expressions represented as variables, constants, or lists.
                e.g., ['Knows', Variable('x'), 'Jane']
    """
    if subst is None:
        subst = {}

    # Step 1: If psi1 or psi2 is a variable or constant
    if not isinstance(psi1, list) or not isinstance(psi2, list):

        # a) If psi1 or psi2 are identical, return NIL (empty substitution set / no changes)
        if psi1 == psi2:
            return {}

        # b) Else if psi1 is a variable
        elif is_variable(psi1):
            # a. If psi1 occurs in psi2, return FAILURE
            if occurs_in(psi1, psi2):
                return "FAILURE"
            # b. Else return {(psi2 / psi1)}
            return {psi1: psi2}

        # c) Else if psi2 is a variable
        elif is_variable(psi2):
            # a. If psi2 occurs in psi1, return FAILURE
            if occurs_in(psi2, psi1):
                return "FAILURE"
            # b. Else return {(psi1 / psi2)}
            return {psi2: psi1}

        # d) Else return FAILURE (e.g., two different constants like 'John' and 'Bill')
        else:
            return "FAILURE"

    # Step 2: If the initial Predicate/Function symbol are not same, return FAILURE
    if psi1[0] != psi2[0]:
        return "FAILURE"

    # Step 3: If psi1 and psi2 have a different number of arguments, return FAILURE
    if len(psi1) != len(psi2):
        return "FAILURE"

    # Step 4: Set Substitution set (SUBST) to NIL
    accumulated_subst = dict(subst)

    # Step 5: For i=1 to number of arguments (skipping the predicate symbol at index 0)
    for i in range(1, len(psi1)):
        arg1 = psi1[i]
        arg2 = psi2[i]

        # a) Call Unify function with the ith elements, put result into S
        S = unify(arg1, arg2)

        # b) If S = failure then return Failure
        if S == "FAILURE":
            return "FAILURE"

        # c) If S != NIL then do:
        if S != {}:
            # a. Apply S to the remainder of both lists (psi1 and psi2)
            psi1 = apply_subst(S, psi1)
            psi2 = apply_subst(S, psi2)

            # b. SUBST = APPEND(S, SUBST)
            # Apply new bindings to existing accumulator and merge
            accumulated_subst = {var: apply_subst(S, val) for var, val in accumulated_subst.items()}
            accumulated_subst.update(S)

    # Step 6: Return SUBST
    return accumulated_subst


# ---------------------------------------------------------
# Example Usage & Test Cases
# ---------------------------------------------------------
if __name__ == "__main__":
    x = Variable("x")
    y = Variable("y")

    # Example 1: Knows(John, x) and Knows(John, Jane)
    expr1 = ["Knows", "John", x]
    expr2 = ["Knows", "John", "Jane"]
    print("Test 1 Result:", unify(expr1, expr2))
    # Output: {?x: 'Jane'}

    # Example 2: Knows(x, x) and Knows(John, y)
    expr3 = ["Knows", "Jane", x]
    expr4 = ["Knows", "John", y]
    print("Test 2 Result:", unify(expr3, expr4))
    # Output: {?x: 'John', ?y: 'John'}

    # Example 3: Occurs Check Failure - P(x) and P(f(x))
    expr5 = ["P", x]
    expr6 = ["P", ["f", x]]
    print("Test 3 Result:", unify(expr5, expr6))
    # Output: FAILURE
