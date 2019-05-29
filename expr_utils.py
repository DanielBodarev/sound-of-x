from Equation import Expression

def fix(fn, args = ["x"]):
    mult_suffix = args + ["("]
    for i in range(1, len(fn)):
        if (fn[i] in mult_suffix and fn[i-1].isnumeric()) or (fn[i] in mult_suffix and fn[i-1] == ")"):
            return fn[:i] + "*" + fix(fn[i:], args)
    return fn

def Expr(fn, args = ["x"]):
    fn = fix(fn, args)
    return Expression(fn, args)