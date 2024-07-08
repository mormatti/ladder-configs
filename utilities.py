def subscript_numbers(str):
    "This function takes a string and returns the same string with the numbers in subscript."
    return str.translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))

def superscript_numbers(str):
    "This function takes a string and returns the same string with the numbers in superscript."
    return str.translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))