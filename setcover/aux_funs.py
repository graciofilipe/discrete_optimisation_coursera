def generage_set_coverage_vector(s, total_items):
    items = s.items
    set_coverage_vector = [0 for _ in range(total_items)]
    for item in items:
        set_coverage_vector[item]=1
    return set_coverage_vector
