from   type_t         import T
from   typing         import Callable, Collection, Iterator


def interact(collection: Collection[T], interaction_func: Callable[[T, Collection[T]], T]) -> Iterator[T]:
    """
    Apply the `interaction_func` to each item in the collection `collection`, 
    where `interaction_func` generates a new item based on the current item and the
    remaining items in the collection. *This is a generator function!*

    Args:
    - `collection: Collection[T]`: The collection of items to modifiy.
    - `interaction_func: Callable[[T, Collection[T]], T]`: The interaction 
      function, which must take an item and a collection of items, returning
      a new (modified) item. The `interact()` function handles excluding the
      current item from the collection in each iteration.

    Yields:
    - `_: Iterator[T]`: The modified items after interaction.

    Notes:
    - This may be useful in things like n-body simulations. 

    Example:
    - Consider a scenario where you have a list of numbers, and you want to apply an
      interaction function that replace each number with the sum of all the others,
      divided by the number itself.

        ```python
        def add_and_divide(item, others):
            return sum(others) / item

        numbers = [1, 2, 3, 4, 5]
        modified_numbers = list(interact(numbers, add_and_divide))
        print(modified_numbers) # Output: [15, 7.5, 5, 3.75, 3]
        ```
    """
    
    yield from (interaction_func(item, [*zip(*filter(lambda i: i[0] != index, enumerate(collection)))[1]]) for index, item in enumerate(collection))

    # alternatively, if you're not as cool...
    # for index, item in enumerate(collection):
    #     r = filter(lambda i: i[0] != index, enumerate(collection)) # filter out the current item from the collection
    #     r = [*zip(*r)[1]]                                          # retrieve the remaining items
    #     r = interaction_func(item, r)                              # apply the interaction
    #     yield r
