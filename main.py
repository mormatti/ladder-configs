#%%
# We import numpy
import numpy as np
from utilities import *

class Dof:
    """
    This class represents a degree of freedom.
    """
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Dof(value = {self.name})"
    
    def __str__(self) -> str:
        return f"Degree of freedom: value = {self.value}"
    
    def __add__(self, other):
        assert isinstance(other, Dof) , "The object to add must be a Dof object"
        return Dof(self.name, self.value + other.value)

class Link(Dof):
    """
    This class represents a link in a lattice gauge theory.
    """
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Link(value = {self.value})"
    
    def __str__(self) -> str:
        return f"Link: value = {self.value}"
    
    def __add__(self, other):
        assert isinstance(other, Link) , "The object to add must be a Link object"
        return Link(self.value + other.value)

class IntZZ:
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
        assert isinstance(other, IntZZ) , "The object to add must be an IntZ object"
        assert self.N == other.N, "The rings must be equal"
        return IntZZ(self.N, (self.value + other.value) % self.N)
    
    def __sub__(self, other):
        assert isinstance(other, IntZZ) , "The object to subtract must be an IntZ object"
        assert self.N == other.N, "The rings must be equal"
        return IntZZ(self.N, (self.value - other.value) % self.N)
    
    def increment(self):
        self.value = (self.value + 1) % self.N

    def decrement(self):
        self.value = (self.value - 1) % self.N
    
class IntSpin:
    def __init__(self, s, sz) -> None:
        self.sx2 = int(s * 2)
        self.szx2 =  int(sz * 2)
        self.set_none_if_needed()

    def set_none_if_needed(self):
        self.szx2 = None if (self.szx2 > self.sx2 or self.szx2 < -self.szx2) else self.szx2

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
        return IntSpin(self.sx2, self.szx2 + other.szx2)
    
    def increment(self):
        self.szx2 += 1
        self.set_none_if_needed()

    def decrement(self):
        self.szx2 -= 1
        self.set_none_if_needed()

class Charge(Dof):
    """
    This class represents a fermionic charge site in an abelian lattice gauge theory.
    To init insert the type ('+','-') and the value ('+','0','-').
    There are 4 possibilities: ('+','+'), ('+','0'), ('-','0'), ('-','-').
    """  
    def __init__(self, type, value) -> None:
        if type == '+':
            self.is_positive_type = True
            if value == '+':
                self.activated = True
            elif value == '0':
                self.activated = False
            else:
                raise ValueError("Wrong value for the charge.")
        elif type == '-':
            self.positiveType = False
            if value == '-':
                self.activated = False
            elif value == '0':
                self.activated = True
            else:
                raise ValueError("Wrong value for the charge.")
        else:
            raise ValueError("Wrong type for the charge.")
    
    @property
    def is_negative_type(self):
        return not self.is_positive_type

    def __repr__(self) -> str:
        return f"ChargeValue(value={self.value})"
    
    def __str__(self) -> str:
        return f"Charge value: {self.value}"

class Plaquette:
    def __init__(self, top: Link, bottom: Link) -> None:
        self.top = top
        self.bottom = bottom
    
    @property
    def charge(self):
        pass

    def __repr__(self) -> str:
        return f"PlaquettePure(top = {self.top}, bottom = {self.bottom})"
    
    def __str__(self) -> str:
        return f"Pure plaquette: E_top = {self.top.value}, E_bottom = {self.bottom.value}"
    
    def longitudinal_polarization(self):
        return self.top + self.bottom


class PlaquettePure(Plaquette):
    def __init__(self, top: Link, bottom: Link) -> None:
        self.top = top
        self.bottom = bottom
    
    @property
    def charge(self):
        return 0

    def __repr__(self) -> str:
        return f"PlaquettePure(top = {self.top}, bottom = {self.bottom})"
    
    def __str__(self) -> str:
        return f"Pure plaquette: E_top = {self.top.value}, E_bottom = {self.bottom.value}"
    
    def longitudinal_polarization(self):
        return self.top + self.bottom
    

# %%
