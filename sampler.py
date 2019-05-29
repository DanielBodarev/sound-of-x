from expr_utils import Expr
import Equation
import sinestring as ss

"""def sample(fn, sample_rate):
    if type(fn) == ss.SineFull or type(fn) == ss.SineBase:
        fn = str(fn)
    if type(fn) == str:
        fn = Expr(fn)
    return _sample_fn(fn, sample_rate)"""

# Returns sample_rate amount of (x,y) values 
def sample_fn(fn, sample_rate):
    x_span = fn.get_span()
    if x_span * fn.dur * sample_rate == 0:
        raise Exception("Neither Length, Sample Rate, nor Start - End can be zero.")
    # What span on the x-axis counts as one second
    x_per_second = x_span / fn.dur

    # How much to increase x-value each sample cycle
    x_increments = x_per_second / sample_rate

    # How many samples required for this sound
    total_samples = int(fn.dur * sample_rate)

    # Resulting samples and their x-values
    xy_values = []

    # Turns the function into a callable expression
    fn_call = Expr(str(fn))

    for i in range(total_samples):
        x = (i * x_increments) + fn.start
        xy_values.append((x, fn_call(x)))
    
    return xy_values
