import itertools      as  it
import more_itertools as mit
import operator       as op
from   ._type_t       import T
from   typing         import Callable, Iterator, Literal


def fixed_point(
   base_state: T, 
   evolution_func: Callable[[T], T], 
   compare_func: Callable[[T, T], bool] = op.eq, 
   return_mode: Literal['value', 'infiter', 'callable'] = 'callable'
) -> T | Iterator[T] | Callable[[], T]:
   
   """
   Generates the fixed point of a function starting from a base state. 

   Args:
   - `evolution_func: Callable`: The function which is repeatedly applied.
   - `base_state: T`: The starting state for the evolution function. 
     Must implement `compare_func`. 
   - `compare_func: Callable[[T, T], bool]`: The comparison function. 
     Defaults to `__eq__`.
   - `return_mode: Literal['value', 'infiter', 'callable']`: The requested
     behavior of the returned value.

   Returns:
   - `_: T|Iterator[T]|Callable[[],T]`: The fixed point of the evolved function
     as either the value itself, an infinite iterator (for use in iterchains),
     or a callable that returns the value.

   Notes:
   - May iterate indefinitely. This is considered user error.
   """

   r = filter(lambda ab: compare_func(ab[0], ab[1]), mit.windowed(it.islice(it.accumulate(it.repeat(base_state), lambda x, _: evolution_func(x)), 1, None), 2))

   match return_mode:
      case 'value':
         return next(r)[0]
      case 'callable':
         return lambda:next(r)[0]
      case 'infiter':
         return map(op.getitem, r, it.repeat(1))

   # alternatively, if you're not as cool...  
   #  r = it.accumulate(it.repeat(base_state), lambda x, _: evolution_func(x)) # functional way of calling the `evolution_func` successively on `base_state`
   #  r = it.islice(r, 1, None)                                                # chop off the first result because it's the `base_state`, not an iterator
   #  r = mit.windowed(r, 2)                                                   # moving window, such that you can use `compare_func` current and previous
   #  r = filter(lambda ab: compare_func(ab[0], ab[1]), r)                     # only return windows which pass the `compare_func`.
   # at this point, r is an infinite filter pairs of fixed points