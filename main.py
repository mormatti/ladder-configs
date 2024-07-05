#%%
# We import numpy
import numpy as np

def subscript_numbers(str):
    "This function takes a string and returns the same string with the numbers in subscript."
    return str.translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))

def superscript_numbers(str):
    "This function takes a string and returns the same string with the numbers in superscript."
    return str.translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))

class IntZ:
    """
    This class represents an integer in the ring ℤ_N.
    """

    def __init__(self, N, value) -> None:
        self.N = int(N)
        self.value = int(value) % self.N

    @property
    def centered_value(self):
        return self.value - int(self.N / 2)
    
    @property
    def spin_value(self):
        return self.value - self.N / 2

    @property
    def phase_value(self):
        return np.exp(2 * np.pi * 1j * self.value / self.N)

    def __repr__(self) -> str:
        return f"SpinZ(N={self.N}, value={self.value})"
    
    def __str__(self) -> str:
        return f"ℤ_{self.N} instance, value = e^(2πi * {self.value} / N)"
    
    def __add__(self, other):
        assert isinstance(other, IntZ) , "The object to add must be an IntZ object"
        assert self.N == other.N, "The rings must be equal"
        return IntZ(self.N, (self.value + other.value) % self.N)
    
    # TODO: Define the increment operator

    # TODO: Define the decrement operator
    
class IntSpin:
    def __init__(self, s, sz) -> None:
        self.sx2 = int(s * 2)
        szx2 = int(sz * 2)
        self.szx2 =  None if (szx2 > self.sx2 or self.sx2 < -szx2) else szx2

    @property
    def sz(self):
        return None if self.szx2 is None else self.szx2 / 2
    
    @property
    def s(self):
        return self.sx2 / 2
    
    def __repr__(self) -> str:
        return f"Spin(s={self.s}, sz={self.sz})" if self.szx2 is not None else f"Spin(s={self.s}, sz=None)"
    
    def __str__(self) -> str:
        return f"Spin instance, s={self.sx2}/2, sᶻ={self.szx2}/2" if self.szx2 is not None else "Spin, s={self.sx2}/2, invalid sᶻ"
    
    def __add__(self, other):
        assert isinstance(other, IntSpin) , "The object to add must be an IntSpin object"
        assert self.sx2 == other.sx2, "The spins must be equal"
        szx2_sum = self.szx2 + other.szx2
        szx2_sum = None if (szx2_sum > self.sx2 or szx2_sum < self.sx2) else szx2_sum
        return IntSpin(self.sx2, szx2_sum)
    
    # TODO: Define the increment operator

    # TODO: Define the decrement operator
# %%
