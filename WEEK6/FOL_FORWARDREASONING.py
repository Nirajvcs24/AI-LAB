class ForwardChainingEngine:
    def __init__(self, facts, rules):
        self.facts = set(facts)
        self.rules = rules

    def unify_and_match(self, conditions, current_subs=None):
        """Finds all variable substitutions that satisfy a rule's conditions."""
        if current_subs is None:
            current_subs = {}
        if not conditions:
            return [current_subs]

        first_cond = conditions[0]
        rest_conds = conditions[1:]
        results = []

        for fact in self.facts:
            if len(fact) == len(first_cond) and fact[0] == first_cond[0]:
                new_subs = current_subs.copy()
                match = True
                for pattern_arg, fact_arg in zip(first_cond[1:], fact[1:]):
                    # Lowercase strings = variables ('p', 'q', 'r', 'x')
                    if pattern_arg.islower():
                        if pattern_arg in new_subs:
                            if new_subs[pattern_arg] != fact_arg:
                                match = False
                                break
                        else:
                            new_subs[pattern_arg] = fact_arg
                    # Capitalized strings = constants ('Robert', 'A', 'America')
                    elif pattern_arg != fact_arg:
                        match = False
                        break

                if match:
                    results.extend(self.unify_and_match(rest_conds, new_subs))
        return results

    def substitute(self, predicate, subs):
        """Replaces variables in a conclusion with matched constants."""
        return tuple(subs.get(arg, arg) for arg in predicate)

    def run(self, goal):
        """Runs forward chaining until no new facts can be inferred or goal is reached."""
        print(f"\nInitial Facts: {sorted(self.facts)}")
        step = 1

        while True:
            new_facts_inferred = False
            for conditions, conclusion in self.rules:
                matches = self.unify_and_match(conditions)
                for subs in matches:
                    inferred = self.substitute(conclusion, subs)
                    if inferred not in self.facts:
                        self.facts.add(inferred)
                        new_facts_inferred = True
                        print(f"Step {step}: Inferred {inferred} using {subs}")
                        step += 1
                        if inferred == goal:
                            print(f"\nRESULT: {goal[0]}({goal[1]}) is TRUE (Robert IS a criminal).")
                            print("-" * 55)
                            return True

            if not new_facts_inferred:
                break

        print(f"\nRESULT: {goal[0]}({goal[1]}) is FALSE (Robert is NOT a criminal).")
        print("-" * 55)
        return False


def parse_fact(fact_str):
    """Converts string input like 'American(Robert)' into tuple ('American', 'Robert')."""
    fact_str = fact_str.strip()
    if '(' not in fact_str or not fact_str.endswith(')'):
        raise ValueError("Format must be Predicate(Arg1, Arg2, ...)")
    predicate, args_part = fact_str[:-1].split('(', 1)
    args = [arg.strip() for arg in args_part.split(',') if arg.strip()]
    return tuple([predicate.strip()] + args)


def get_facts_from_user(scenario_name):
    """Prompts the user to enter facts line by line."""
    print(f"\n=== {scenario_name} ===")
    print("Enter facts in format Predicate(Arg1, Arg2), e.g., American(Robert)")
    print("Type 'done' when finished:")
    
    user_facts = []
    while True:
        entry = input("> ").strip()
        if entry.lower() == 'done':
            break
        if not entry:
            continue
        try:
            parsed = parse_fact(entry)
            user_facts.append(parsed)
        except ValueError as e:
            print(f"Invalid format ({e}). Try again.")
    return user_facts


# --- KNOWLEDGE BASE RULES ---
rules = [
    # Rule 1: American(p) ^ Weapon(q) ^ Sells(p, q, r) ^ Hostile(r) => Criminal(p)
    (
        [('American', 'p'), ('Weapon', 'q'), ('Sells', 'p', 'q', 'r'), ('Hostile', 'r')],
        ('Criminal', 'p')
    ),
    # Rule 2: Missile(x) ^ Owns(A, x) => Sells(Robert, x, A)
    (
        [('Missile', 'x'), ('Owns', 'A', 'x')],
        ('Sells', 'Robert', 'x', 'A')
    ),
    # Rule 3: Missile(x) => Weapon(x)
    (
        [('Missile', 'x')],
        ('Weapon', 'x')
    ),
    # Rule 4: Enemy(x, America) => Hostile(x)
    (
        [('Enemy', 'x', 'America')],
        ('Hostile', 'x')
    )
]

goal = ('Criminal', 'Robert')

# Run Scenario 1 (User enters facts for Robert being a criminal)
facts_1 = get_facts_from_user("SCENARIO 1: Prove Robert IS a Criminal")
engine_1 = ForwardChainingEngine(facts_1, rules)
engine_1.run(goal)

# Run Scenario 2 (User enters facts for Robert NOT being a criminal)
facts_2 = get_facts_from_user("SCENARIO 2: Prove Robert is NOT a Criminal")
engine_2 = ForwardChainingEngine(facts_2, rules)
engine_2.run(goal)
