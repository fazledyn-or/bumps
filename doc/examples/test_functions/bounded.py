# Boundary check
# ==============
#
# Check probability at boundaries.
#
# In this case we define the probability density function (PDF) directly
# in an n-dimensional uniform box.
#
# Ideally, the correlation plots and variable distributions will be uniform.

from bumps.names import *

# Adjust domain from 1e-150 to 1e+150 and you will see that DREAM is equally
# adept at filling the box.

domain = 1

# Uniform cost function.

def box(x):
    return 0 if np.all(np.abs(x) <= domain) else np.inf

def ramp(x):
    return -abs(x[0]/domain) if np.all(np.abs(x) <= domain) else np.inf

def cone(x):
    r = np.sqrt(sum(xk**2 for xk in x))
    return -r if r <= domain else np.inf

def diamond(x):
    return 0 if np.sum(np.abs(x)) <= domain else np.inf

# Wrap it in a PDF object which turns an arbitrary probability density into
# a fitting function.  Give it a valid initial value, and set the bounds to
# a unit cube with one corner at the origin.

def triangle_constraints():
    a, b = M.a.value, M.b.value
    return 0 if a < b else 1e6 + (b-a)**2

def box_constraints():
    a, b = M.a.value, M.b.value
    return 0 if abs(a) <= domain/2 and abs(b) <= domain/2 else np.inf

def circle_constraints():
    a, b = M.a.value, M.b.value
    r = np.sqrt(a**2 + b**2)
    return 0 if r <= domain*2/3 else np.inf

#M = PDF(lambda a, b: box([a, b]))
M = PDF(lambda a, b: diamond([a, b]))
#M = PDF(lambda a, b: ramp([a, b]))
#M = PDF(lambda a, b: cone([a, b]))

constraints = None
#constraints = triangle_constraints
#constraints = box_constraints
#constraints = circle_constraints

M.a.range(-2*domain, 2*domain)
M.b.range(-2*domain, 2*domain)

# Make the PDF a fit problem that bumps can process.
problem = FitProblem(M, constraints=constraints)
