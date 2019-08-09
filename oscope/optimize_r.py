import fractions
import itertools

from ortools.sat.python import cp_model


# From http://www.resistorguide.com/resistor-values/
class E96Resistor:
    VALUES = [
        100, 102, 105, 107, 110, 113,
        115, 118, 121, 124, 127, 130,
        133, 137, 140, 143, 147, 150,
        154, 158, 162, 165, 169, 174,
        178, 182, 187, 191, 196, 200,
        205, 210, 215, 221, 226, 232,
        237, 243, 249, 255, 261, 267,
        274, 280, 287, 294, 301, 309,
        316, 324, 332, 340, 348, 357,
        365, 374, 383, 392, 402, 412,
        422, 432, 442, 453, 464, 475,
        487, 499, 511, 523, 536, 549,
        562, 576, 590, 604, 619, 634,
        649, 665, 681, 698, 715, 732,
        750, 768, 787, 806, 825, 845,
        866, 887, 909, 931, 953, 976]

    MULTIPLES = [int(10**i) for i in range(6)]

    def __init__(self, name: str, model: cp_model.CpModel):
        self._model = model

        # This forces the optimizer to pick from one of the 96 * 6 available values
        self._r_values = [v * m for v in self.VALUES for m in self.MULTIPLES]
        self._r_exprs = [model.NewBoolVar(name + "=" + str(val)) for val in self._r_values]
        self._model.Add(sum(self._r_exprs) == 1)

        self._expr = sum(exp * val for (exp, val) in zip(self._r_exprs, self._r_values))

    def expr(self):
        return self._expr

    def compute_value(self, solver: cp_model.CpSolver):
        return solver.Value(self.expr())


def require_ratio_tolerance(model: cp_model.CpModel, e1: E96Resistor, e2: E96Resistor, upper: float, lower: float):
    """
    Require that:
             e1
    lower < ---- < upper
             e2
    """
    upper_frac = fractions.Fraction(upper).limit_denominator(2**32)
    lower_frac = fractions.Fraction(lower).limit_denominator(2**32)

    model.Add(e1 * upper_frac.numerator < e2 * upper_frac.denominator)
    model.Add(e1 * lower_frac.numerator > e2 * lower_frac.denominator)


def add_bounded_constraint(model: cp_model.CpModel, expression, lower, upper):
    model.Add(expression < upper)
    model.Add(expression > lower)


model = cp_model.CpModel()
solver = cp_model.CpSolver()

r1 = E96Resistor("R1", model)
r2 = E96Resistor("R2", model)
r3 = E96Resistor("R3", model)

add_bounded_constraint(model, r1.expr() + r2.expr() + r3.expr(), 990000, 1010000)
require_ratio_tolerance(model, r1.expr() + r2.expr(), r3.expr(), 3.99, 4.01)

model.Minimize(r1.expr() + r2.expr())
solver.Solve(model)

r1_v = r1.compute_value(solver)
r2_v = r2.compute_value(solver)
r3_v = r3.compute_value(solver)

print("R1=", r1_v)
print("R2=", r2_v)
print("R3=", r3_v)

print("Input Impedence:", r1_v + r2_v + r3_v)
