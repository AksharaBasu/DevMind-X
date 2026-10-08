
def calculate_total(values):
    return sum(values)


def process_data(data):
    if not data:
        return []

    return [item * 2 for item in data]


def find_matching_items(items, value):
    return [item for item in items if item == value]


def process_items(items):
    return [item.strip() for item in items]


def get_sorted_values(values):
    return sorted(values)
