import random

# Globals: Question type
TYPE = 0    # Which type of question should be generated?
            # 0: Random
            # 1: Color difference
            # 2: Binary difference
            # 3: Base conversion
            # 4: Evaluate expression
            # 5: Order numbers

# Globals: Binary difference
LOWER_LIMIT = 9     # Smallest possible number generated 
UPPER_LIMIT = 30    # Largest possible number generated
RANGE = 10          # Max possible difference between numbers

# Globals: Evaluate expression
TERMS = 3   # Number of terms to be added together

# Globals: Order numbers
COUNT = 3   # Number of numbers to be ordered

# Globals: Number ranges
BASE_2_LOWER, BASE_2_UPPER = 16, 64         # Range for base 2 values
BASE_8_LOWER, BASE_8_UPPER = 1000, 7777     # Range for base 8 values
BASE_10_LOWER, BASE_10_UPPER = 100, 1000    # Range for base 10 values
BASE_16_LOWER, BASE_16_UPPER = 4096, 65535  # Range for base 16 values

CURRENT = 1

def config(type=None, range=None, terms=None, count=None,
           lower_limit=None, upper_limit=None,
           base_2_lower=None, base_2_upper=None,
           base_8_lower=None, base_8_upper=None,
           base_10_lower=None, base_10_upper=None,
           base_16_lower=None, base_16_upper=None):
    
    global LOWER_LIMIT, UPPER_LIMIT, RANGE, TERMS, COUNT, TYPE, \
           BASE_2_LOWER, BASE_2_UPPER, BASE_8_LOWER, BASE_8_UPPER, \
           BASE_10_LOWER, BASE_10_UPPER, BASE_16_LOWER, BASE_16_UPPER
    
    if type != None: TYPE = type
    if lower_limit != None: LOWER_LIMIT = lower_limit
    if upper_limit != None: UPPER_LIMIT = upper_limit
    if range != None: RANGE = range
    if terms != None: TERMS = terms
    if count != None: COUNT = count
    if base_2_lower != None: BASE_2_LOWER = base_2_lower
    if base_2_upper != None: BASE_2_UPPER = base_2_upper
    if base_8_lower != None: BASE_8_LOWER = base_8_lower
    if base_8_upper != None: BASE_8_UPPER = base_8_upper
    if base_10_lower != None: BASE_10_LOWER = base_10_lower
    if base_10_upper != None: BASE_10_UPPER = base_10_upper
    if base_16_lower != None: BASE_16_LOWER = base_16_lower
    if base_16_upper != None: BASE_16_UPPER = base_16_upper


# Color component difference
def generate_question_1():
    def question():
        color1 = '#' + ''.join(random.choices('0123456789ABCDEF', k=6))
        color2 = '#' + ''.join(random.choices('0123456789ABCDEF', k=6))
        component = random.choice(['red', 'green', 'blue'])

        return color1, color2, component
    
    def answer(color1, color2, component):
        rgb1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        rgb2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))

        if component == 'red': diff = abs(rgb1[0] - rgb2[0])
        elif component == 'green': diff = abs(rgb1[1] - rgb2[1])
        elif component == 'blue': diff = abs(rgb1[2] - rgb2[2])

        return f'{diff:02X}'
    
    color1, color2, component = question()
    print("Question:")
    print(f"Given the two colors {color1} and {color2}, what is the difference between the hexadecimal values of the {component} color components?")
    print("Answer:")
    print(answer(color1, color2, component))


# Binary ones difference
def generate_question_2():
    def count_ones(start, end):
        count = 0
        for num in range(start, end+1):
            count += bin(num).count('1')
        return count

    def question():
        global RANGE, UPPER_LIMIT, LOWER_LIMIT

        def generate_tuple():
            max_range = min(RANGE, UPPER_LIMIT - LOWER_LIMIT)
            val1 = random.randint(LOWER_LIMIT, UPPER_LIMIT - max_range)
            val2 = random.randint(val1 + 1, min(val1 + max_range, UPPER_LIMIT))

            return (val1, val2)
        
        range1 = generate_tuple()
        range2 = generate_tuple()
        count1 = count_ones(range1[0], range1[1])
        count2 = count_ones(range2[0], range2[1])
        
        if count2 > count1:
            return range2, range1
        
        return range1, range2

    def answer(range1, range2):  
        count1 = count_ones(range1[0], range1[1])
        count2 = count_ones(range2[0], range2[1])

        return str(count1 - count2)
    
    range1, range2 = question()
    print("Question:")
    print(f"How many more 1s are in the binary representations of (decimal) numbers from {range1[0]} to {range1[1]} than from {range2[0]} to {range2[1]}?")
    print("Answer:")
    print(answer(range1, range2))


# Base conversion
def generate_question_3():
    def question():
        global BASE_2_LOWER, BASE_2_UPPER, BASE_8_LOWER, BASE_8_UPPER, BASE_16_LOWER, BASE_16_UPPER

        base = random.choice([2, 8, 16])

        if base == 2: num = bin(random.randint(BASE_2_LOWER, BASE_2_UPPER))[2:]
        elif base == 8: num = oct(random.randint(BASE_8_LOWER, BASE_8_UPPER))[2:]
        elif base == 16: num = hex(random.randint(BASE_16_LOWER, BASE_16_UPPER))[2:]

        target_base = random.choice([2, 8, 16])
        while target_base == base:
            target_base = random.choice([2, 8, 16])

        return num, base, target_base

    def answer(num, base, target_base):
        if target_base == 2: return bin(int(num, base))[2:]
        elif target_base == 8: return oct(int(num, base))[2:]
        elif target_base == 16: return hex(int(num, base))[2:]

    num, base, target_base = question()
    print("Question:")
    print(f"Convert ({num})_{base} to base {target_base}.")
    print("Answer:")
    print(answer(num, base, target_base))


# Evaluate expression
def generate_question_4():
    def question():
        global BASE_2_LOWER, BASE_2_UPPER, BASE_8_LOWER, BASE_8_UPPER, BASE_16_LOWER, BASE_16_UPPER, TERMS

        base = random.choice([2, 8, 16])

        if base == 2:
            nums = [bin(random.randint(BASE_2_LOWER, BASE_2_UPPER))[2:] for _ in range(TERMS)]
        elif base == 8:
            nums = [oct(random.randint(BASE_8_LOWER, BASE_8_UPPER))[2:] for _ in range(TERMS)]
        elif base == 16:
            nums = [hex(random.randint(BASE_16_LOWER, BASE_16_UPPER))[2:] for _ in range(TERMS)]

        target_base = random.choice([2, 8, 16])

        return nums, base, target_base

    def answer(nums, base, target_base):
        nums_base_10 = [int(num, base) for num in nums]
        result_base_10 = sum(nums_base_10)

        if target_base == 2: return bin(result_base_10)[2:]
        elif target_base == 8: return oct(result_base_10)[2:]
        elif target_base == 16: return hex(result_base_10)[2:]

    nums, base, target_base = question()
    print("Question:")
    print(f"Evaluate {' + '.join([f'({num})_{base}' for num in nums])} and express the answer in base {target_base}.")
    print("Answer:")
    print(answer(nums, base, target_base))


# Order numbers
def generate_question_5():
    global COUNT

    def generate_random_number(existing_nums):
        global BASE_2_LOWER, BASE_2_UPPER, BASE_8_LOWER, BASE_8_UPPER, BASE_10_LOWER, BASE_10_UPPER, BASE_16_LOWER, BASE_16_UPPER

        base = random.choice([2, 8, 10, 16])
        while True:
            if base == 2: num = bin(random.randint(BASE_2_LOWER, BASE_2_UPPER))[2:]
            elif base == 8: num = oct(random.randint(BASE_8_LOWER, BASE_8_UPPER))[2:]
            elif base == 10: num = str(random.randint(BASE_10_LOWER, BASE_10_UPPER))
            elif base == 16: num = hex(random.randint(BASE_16_LOWER, BASE_16_UPPER))[2:]
            if (num, base) not in existing_nums:
                return num, base

    def question(count):
        values = []
        existing_nums = set()
        for i in range(count):
            num, base = generate_random_number(existing_nums)
            values.append((num, base))
            existing_nums.add((num, base))
        return values
    
    def answer(values):
        sorted_vals = sorted([(int(str(num), base), num, base) for num, base in values], key=lambda x: x[0], reverse=True)
        return [(val[1], val[2]) for val in sorted_vals]

    values = question(COUNT)
    print("Question:")
    print(f"Order these numbers largest to smallest: {', '.join([f'{num}_{base}' for num, base in values])}")
    print("Answer:")
    sorted_values = answer(values)
    print(', '.join([f'{num}_{base}' for num, base in sorted_values]))



def main():
    global TYPE, CURRENT

    if TYPE == 0:
        eval(f'generate_question_{CURRENT}()')
        if CURRENT == 5:
            CURRENT = 1
        else:
            CURRENT += 1
    else:
        eval(f'generate_question_{TYPE}()')


if __name__ == "__main__":
    main()