import numbers

import numpy as np
import scipy.integrate
import scipy.interpolate
import scipy.optimize

from pylab import plot, show, figure, title, savefig

lines_per_hour = 350.0 / 8.0
cost_per_line_per_day = 3e-4

WORKDAY_IN_HOURS = 8
WORKDAYS_PER_YEAR = 261

def hours_maint_per_day(codelines: np.array):
    return codelines * cost_per_line_per_day

def hours_new_per_day(codelines: np.array):
    return WORKDAY_IN_HOURS - hours_maint_per_day(codelines)

def loc_per_day(codelines: np.array, t0: numbers.Number):
    hours_for_new = hours_new_per_day(codelines)
    
    return lines_per_hour * hours_for_new

times = np.linspace(0, WORKDAYS_PER_YEAR, 1000)
codelines = scipy.integrate.odeint(loc_per_day, np.zeros((1)), t=times).flatten()

time_at_codeline = scipy.interpolate.interp1d(codelines, times)

figure(figsize=(8,6))
title("Codebase Size")
plot(times, codelines, alpha=0.8)
savefig("CodebaseSize.png", transperent=True)

figure(figsize=(8,6))
title("Time breakdown")
plot(times, hours_new_per_day(codelines) / WORKDAY_IN_HOURS, alpha=0.8)
plot(times, hours_maint_per_day(codelines) / WORKDAY_IN_HOURS, alpha=0.8)
savefig("TimeBreakdown.png", transperent=True)

crossover_func = lambda c: abs(hours_maint_per_day(c)-hours_new_per_day(c))
crossover_lines = scipy.optimize.fmin(crossover_func, 20000)

print(crossover_lines)
print(time_at_codeline(crossover_lines))
