from typing import Any, Iterable, Callable, Generator, get_args, get_origin
from inspect import signature
from collections import OrderedDict


class Node:
    def __init__(self, value: Any, parent: 'Node' = None):
        self.is_leaf = True
        self.value = value
        self.parent = parent

    def __getitem__(self, item: int) -> Any:
        if self.is_leaf:
            raise Exception("Can't iterate over a leaf.")
        return self.value[item]


def _expand_op(leaves, func):
    for leaf in leaves:
        yield from (Node(l, leaf) for l in func(leaf.value))


def _map_op(leaves, func):
    for leaf in leaves:
        yield Node(func(leaf.value), leaf.parent)


def _reduce_op(leaves, func):
    cur_parent = collected = None

    for leaf in leaves:
        if leaf.parent is not cur_parent:
            if cur_parent is not None:
                yield Node(func(collected), cur_parent.parent)
            cur_parent = leaf.parent
            collected = []

        collected.append(leaf.value)

    yield Node(func(collected), cur_parent.parent)


def _aggregate_op(leaves, func, init, init_factory):
    cur_parent = None
    cur_aggregate = None

    if init_factory is None:
        def init_factory():
            return init

    for leaf in leaves:
        if leaf.parent is not cur_parent:
            if cur_parent is not None:
                yield Node(cur_aggregate, cur_parent.parent)
            cur_parent = leaf.parent
            cur_aggregate = init_factory()

        if cur_aggregate is None:
            cur_aggregate = leaf.value
        else:
            cur_aggregate = func(cur_aggregate, leaf.value)

    yield Node(cur_aggregate, cur_parent.parent)


class TreeParser:
    """
    A parser that interprets the input as a tree that can be expanded, mapped and reduced.
    """

    def __init__(self, *inputs):
        """
        Creates a parser with one leaf `input`.
        :param input: The value of the initial leaf.
        """
        self.last_operation = (Node(inp) for inp in inputs)

    def expand(self, func: Callable[[Any], Iterable]) -> 'TreeParser':
        """
        Applies ``func`` to every leaf of the tree and replaces the leaf with an inner node. It
        generates leaves for this inner node by iterating over the return value of ``func``.
        """
        self.last_operation = _expand_op(self.last_operation, func)
        return self

    def map(self, func: Callable[[Any], Any]) -> 'TreeParser':
        """
        Applies ``func`` to every leaf and replaces it's old value with the return value
        of ``func``.
        """
        self.last_operation = _map_op(self.last_operation, func)
        return self

    def reduce(self, func: Callable[[Iterable], Any]) -> 'TreeParser':
        """
        Calls ``func`` with an iterable over all children of a lowest inner node (i.e. children
        with a common parent node) and replaces that node with a leaf containing the value returned
        by ``func``.

        Example: Given lowest inner nodes ``[[1,2,3,4], [5,6,7], [8,9]]``, the reduce operation
        results in ``[func([1,2,3,4]), func([5,6,7]), func([8,9])]``.
        """
        self.last_operation = _reduce_op(self.last_operation, func)
        return self

    def aggregate(self, func: Callable[[Any, Any], Any], init=None, init_factory=None) -> 'TreeParser':
        """
        Similar to ``reduce`` but instead of calling ``func`` with all children, it creates an
        aggregate by applying a binary function ``func`` successively with the intermediate
        aggregate and the next child value.

        Handling of the initial aggregate can be controlled by
        the ``init`` and ``init_factory`` parameters. If ``init`` is not ``None``, this value will
        be passed as the first aggregate. If ``init_factory`` is not ``None``, it will be called and
        the return value will be used as the first aggregate. If both parameters are ``None``, the
        first call to func will be done with the values of the first two leaves.

        Example: Given lowest inner nodes ``[[1,2,3,4], [5,6,7]]``, the aggregate operation (without
        special initialization) results in ``[func(func(func(1,2),3),4), func(func(5,6),7)]``.
        """
        self.last_operation = _aggregate_op(self.last_operation, func, init, init_factory)
        return self

    def get(self) -> Any:
        """
        Returns the value of the unique leaf of the tree. Raises an exception of there are multiple
        leaves.
        """
        # try to collapse the structure into one value
        result = list(self.last_operation)

        if len(result) > 1:
            raise Exception("Can't get value if root is not a leaf.")

        return result[0].value

    def leaves(self) -> Generator:
        """
        Returns a generator over all values of the leaves.
        """
        yield from (leaf.value for leaf in self.last_operation)

    def lowest_inner_nodes(self) -> Generator:
        """
        Returns a generator over all children of lowest nodes, packed into a list. Equivalent to
        reduce(list) and calling leaves().
        """
        self.reduce(list)
        yield from self.leaves()

    def split(self, separator: str) -> 'TreeParser':
        """
        A convenience method that calls ``split(separator)`` of the values of all leaves and
        expanding them.
        """
        return self.expand(lambda value: value.split(separator))

    @classmethod
    def from_file(cls, file):
        """
        A convenience method that creates a parser initialized with the lines of the given file.
        """

        def line_generator():
            while line := file.readline():
                yield line

        return cls(*line_generator())


class LinearParser:
    def __init__(self, tree: TreeParser):
        self.tree = tree
        self.next_item_is_new_node = True
        self.items_iterator = iter(self._get_items_iterator())

    def _get_items_iterator(self):
        for line in self.tree.lowest_inner_nodes():
            for i, item in enumerate(line):
                self.next_item_is_new_node = i == len(line) - 1
                yield item

    def _get_one(self):
        return next(self.items_iterator)

    def _get_n(self, n):
        return [self._get_one() for _ in range(n)]

    def assert_linebreak(self):
        if not self.next_item_is_new_node:
            raise AssertionError(f"Next item '{self._get_one()}' was still on the same line.")

    def assert_finished(self):
        try:
            raise AssertionError(f"Parsing not finished. Next item would have been "
                                 f"'{self._get_one()}'.")
        except StopIteration:
            pass

    def parse(self, parse_fn):
        if parse_fn in (str, int, float):
            return parse_fn(self._get_one())
        elif parse_fn is list:
            raise Exception("To declare a list, use 'ParseList'. Otherwise the number of items is "
                            "ambiguous and cannot be handled.")
        elif get_origin(parse_fn) is list:
            ...
        else:
            s = signature(parse_fn)
            params = OrderedDict()
            for param in s.parameters.values():
                # special handling of ParseList
                if type(param.default) is ParseList:
                    # check if definition is valid
                    assert get_origin(param.annotation) is list
                    assert len(get_args(param.annotation)) == 1
                    list_type = get_args(param.annotation)[0]
                    list_length = None

                    if param.default.fixed_length is not None:
                        list_length = param.default.fixed_length
                    elif param.default.length_parameter is not None:
                        list_length = params[param.default.length_parameter]
                    elif param.default.length_callable is not None:
                        list_length = param.default.length_callable()

                    params[param.name] = self.parse_n(list_type, n=list_length)
                else:
                    params[param.name] = self.parse(param.annotation)

            return parse_fn(*params.values())

    def parse_n(self, parse_fn, n):
        return [self.parse(parse_fn) for _ in range(n)]

    @classmethod
    def from_string(cls, string, line_sep='\n', item_sep=' '):
        tree = (TreeParser(string)
                .split(line_sep)
                .map(lambda line: line.strip())
                .split(item_sep))
        return cls(tree)

    @classmethod
    def from_file(cls, file, separator=' '):
        tree = (TreeParser
                .from_file(file)
                .map(lambda line: line.strip())
                .split(separator))
        return cls(tree)


class ParseList:
    def __init__(self, fixed_length=None, length_parameter=None, length_callable=None):
        # check that exactly one of the params is not None
        assert sum(0 if v is None else 1 for v in
                   (fixed_length, length_parameter, length_callable)) == 1

        self.fixed_length = fixed_length
        self.length_parameter = length_parameter
        self.length_callable = length_callable
