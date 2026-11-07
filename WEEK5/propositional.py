import itertools

def evaluate(expr, model):
    """Evaluates propositional logic expressions under a model."""
    if isinstance(expr, str):
        return model[expr]
    
    op = expr[0]
    if op == 'NOT':
        return not evaluate(expr[1], model)
    elif op == 'AND':
        return evaluate(expr[1], model) and evaluate(expr[2], model)
    elif op == 'OR':
        return evaluate(expr[1], model) or evaluate(expr[2], model)
    elif op == 'IMPLIES':
        return (not evaluate(expr[1], model)) or evaluate(expr[2], model)

def check_all_queries(symbols, sentences, queries):
    """Generates the truth table showing KB and multiple queries at once."""
    query_names = list(queries.keys())
    
    # Table Header
    header = f"{' | '.join(symbols)} | S1 | S2 | S3 | **KB** | " + " | ".join(query_names)
    print("=" * len(header))
    print(header)
    print("=" * len(header))
    
    # Track entailment status for each query
    entails = {q: True for q in queries}
    
    # Iterate through all 2^n truth assignments
    for values in itertools.product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        
        # Evaluate KB sentences: Q->P, P->~Q, Q v R
        s1 = evaluate(sentences[0], model)
        s2 = evaluate(sentences[1], model)
        s3 = evaluate(sentences[2], model)
        
        kb_val = s1 and s2 and s3
        
        # Evaluate each query for the current row
        q_vals = {}
        for q_name, q_expr in queries.items():
            val = evaluate(q_expr, model)
            q_vals[q_name] = val
            
            # Entailment check: If KB is True, Query MUST be True
            if kb_val and not val:
                entails[q_name] = False
                
        # Formatting row outputs
        sym_str = " | ".join(" T " if model[s] else " F " for s in symbols)
        kb_str = " T  " if kb_val else " F  "
        s_str = f"{'T' if s1 else 'F'}  | {'T' if s2 else 'F'}  | {'T' if s3 else 'F'}"
        q_str = " | ".join(f"  {'T' if q_vals[q] else 'F'}   " for q in query_names)
        
        print(f"{sym_str} | {s_str} |  {kb_str} | {q_str}")

    print("=" * len(header))
    
    # Print Final Summary of Entailments
    print("\n=== Final Entailment Results ===")
    for q_name, result in entails.items():
        symbol = "⊨" if result else "⊭"
        status = "ENTAILED" if result else "NOT ENTAILED"
        print(f"• KB {symbol} ({q_name}) : {status}")

# --- Setup Problem ---
symbols = ['P', 'Q', 'R']

# KB: (Q -> P) AND (P -> ~Q) AND (Q v R)
kb_sentences = [
    ('IMPLIES', 'Q', 'P'),
    ('IMPLIES', 'P', ('NOT', 'Q')),
    ('OR', 'Q', 'R')
]

# Two queries to test: one that passes (R) and one that fails (R -> P)
queries = {
    "α1: R": 'R',
    "α2: R -> P": ('IMPLIES', 'R', 'P')
}

# --- Execute ---
check_all_queries(symbols, kb_sentences, queries)
