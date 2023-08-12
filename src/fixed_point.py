import itertools      as  it
import more_itertools as mit
import operator       as op
from   type_t         import T
from   typing         import Callable


def fixed_point(base_state: T, evolution_func: Callable[[T], T], compare_func: Callable[[T, T], bool] = op.eq) -> T:
    """
    Generates the fixed point of a function starting from a base state. 

    Args:
    - `evolution_func: Callable`: The function which is repeatedly applied.
    - `base_state: T`: The starting state for the evolution function. 
       Must implement `compare_func`. 
       Defaults to `__eq__`. 

    Returns:
    - `_: T`: The fixed point of the evolved function.

    Notes:
    - May iterate indefinitely. This is considered user error.
    """

    return next(filter(lambda ab: ab[0] == ab[1], mit.windowed(it.islice(it.accumulate(it.repeat(base_state), lambda x, _: evolution_func(x)), 1, None), 2)))[0]

    # alternatively, if you're not as cool...  
    # r = it.accumulate(it.repeat(base_state), lambda x, _: evolution_func(x)) # functional way of calling the `evolution_func` successively on `base_state`
    # r = it.islice(r, 1, None)                                                # chop off the first result because it's the `base_state`, not an iterator
    # r = mit.windowed(r, 2)                                                   # moving window, such that you can use `compare_func` current and previous
    # r = filter(lambda ab: compare_func(ab[0], ab[1]), r)                     # only return windows which pass the `compare_func`
    # r = next(r)[0]                                                           # return the left side of the first such window, i.e. the fixed point
    # return r