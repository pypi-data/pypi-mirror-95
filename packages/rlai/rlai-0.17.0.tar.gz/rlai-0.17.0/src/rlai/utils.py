import importlib
import threading
from argparse import Namespace, ArgumentParser
from importlib import import_module
from typing import List, Any, Optional, Callable, Tuple, TextIO

import numpy as np
from numpy.random import RandomState

from rlai.meta import rl_text


@rl_text(chapter=2, page=30)
class IncrementalSampleAverager:
    """
    An incremental, constant-time and -memory sample averager. Supports both decreasing (i.e., unweighted sample
    average) and constant (i.e., exponential recency-weighted average, pp. 32-33) step sizes.
    """

    def reset(
            self
    ):
        self.average = self.initial_value
        self.n = 0

    def update(
            self,
            value: float,
            weight: Optional[float] = None
    ):
        """
        Update the sample average with a new value.

        :param value: New value.
        :param weight: Weight of the value. This is a generalization of the following cases:

          * constant weight for all samples:  recency-weighted average (see `alpha` in the constructor).
          * 1 / n:  standard average.
          * else:  arbitrary weighting scheme (e.g., used for off-policy importance sampling).

        If `weighted` was True in the constructor, then a non-None value must be passed here.
        """

        if weight is not None and not self.weighted:
            raise ValueError('Cannot pass a weight to an unweighted averager.')

        self.n += 1

        if self.has_alpha:
            step_size = self.alpha
        elif self.weighted:

            if weight is None:
                raise ValueError('The averager is weighted, so non-None values must be passed for weight.')

            self.cumulative_weight += weight
            step_size = weight / self.cumulative_weight

        else:
            step_size = 1 / self.n

        self.average = self.average + step_size * (value - self.average)

    def get_value(
            self
    ) -> float:
        """
        Get current average value.

        :return: Average.
        """

        return self.average

    def __init__(
            self,
            initial_value: float = 0.0,
            alpha: float = None,
            weighted: bool = False
    ):
        """
        Initialize the averager.

        :param initial_value: Initial value of the averager. Use values greater than zero to implement optimistic
        initial values, which encourages exploration in the early stages of the run.
        :param alpha: Constant step-size value. If provided, the sample average becomes a recency-weighted average with
        the weight of previous values decreasing according to `alpha^i`, where `i` is the number of time steps prior to
        the current when a previous value was obtained. If `None` is passed, then the unweighted sample average will be
        used, and every value will have the same weight.
        :param weighted: Whether or not per-value weights will be provided to calls to `update`. If this is True, then
        every call to `update` must provide a non-None value for `weight`.
        """

        if alpha is not None and alpha <= 0:
            raise ValueError('alpha must be > 0')

        if alpha is not None and weighted:
            raise ValueError('Cannot supply alpha and per-value weights.')

        self.initial_value = initial_value
        self.alpha = alpha
        self.has_alpha = self.alpha is not None
        self.weighted = weighted
        self.cumulative_weight = 0.0 if self.weighted else None
        self.average = initial_value
        self.n = 0

    def __str__(
            self
    ) -> str:

        return str(self.average)

    def __eq__(
            self,
            other
    ) -> bool:

        return self.get_value() == other.get_value()

    def __ne__(
            self,
            other
    ) -> bool:

        return self.get_value() != other.get_value()


def sample_list_item(
        x: List[Any],
        probs: Optional[np.ndarray],
        random_state: RandomState
) -> Any:
    """
    Sample a list item according to the items' probabilities.

    :param x: Items to sample.
    :param probs: Probabilities (must have same length as `x` and sum to 1), or None for uniform distribution.
    :param random_state: Random state.
    :return: Sampled list item.
    """

    if probs is None:
        probs = np.repeat(1 / len(x), len(x))

    cdf_y_rand = random_state.random_sample()

    cum_probs = probs.cumsum()
    final_cum_prob = cum_probs[-1]

    if abs(1.0 - final_cum_prob) > 0.0000001:
        raise ValueError(f'Expected cumulative probabilities to sum to 1, but got {final_cum_prob} instead.')

    x_i = next(
        i
        for i, cum_prob in enumerate(cum_probs)
        if cdf_y_rand < cum_prob
    )

    return x[x_i]


def import_function(
        name: Optional[str]
) -> Optional[Callable]:
    """
    Import function from fully-qualified name.

    :param name: Fully-qualified name.
    :return: Function.
    """

    if name is None:
        return None

    module_name, function_name = name.rsplit('.', maxsplit=1)
    function_module = import_module(module_name)
    function = getattr(function_module, function_name)

    return function


def load_class(
        fully_qualified_class_name: str
):
    """
    Load class from its fully-qualified name (e.g., xxx.yyy.Class).

    :param fully_qualified_class_name: Name.
    :return: Class reference.
    """

    (module_name, fully_qualified_class_name) = fully_qualified_class_name.rsplit('.', 1)
    module_ref = importlib.import_module(module_name)
    class_ref = getattr(module_ref, fully_qualified_class_name)

    return class_ref


def get_argument_parser(
        fully_qualified_class_name
) -> ArgumentParser:
    """
    Get argument parser for a class.

    :param fully_qualified_class_name: Name.
    :return: Argument parser.
    """

    parser = None
    try:
        loaded_class = load_class(fully_qualified_class_name)
        parser = loaded_class.get_argument_parser()
    except Exception:
        pass

    return parser


def get_base_argument_parser(
        **kwargs
) -> ArgumentParser:
    """
    Get base argument parser.

    :param kwargs: Keyword arguments to pass to the ArgumentParser constructor.
    :return: Argument parser.
    """

    parser = ArgumentParser(
        allow_abbrev=False,
        add_help=False,
        **kwargs
    )

    parser.add_argument(
        '--help',
        action='store_true',
        help='Pass this flag to print usage and argument descriptions.'
    )

    return parser


def parse_arguments(
        parser_or_cls,
        args: List[str]
) -> Tuple[Namespace, List[str]]:
    """
    Parse arguments and display help if specified.

    :param parser_or_cls: Argument parser or a class that has a get_argument_parser function to get the parser.
    :param args: Arguments.
    :return: 2-tuple of parsed arguments and unparsed arguments. The `help` argument will be deleted from the parsed
    arguments. If `help` is True, then it will be added to the unparsed argument list so that subsequent argument
    parsers will also receive it.
    """

    if isinstance(parser_or_cls, ArgumentParser):
        parser = parser_or_cls
    else:
        parser = parser_or_cls.get_argument_parser()

    parsed_args, unparsed_args = parser.parse_known_args(args)

    if parsed_args.help:
        parser.print_help()
        print()
        unparsed_args.append('--help')

    del parsed_args.help

    return parsed_args, unparsed_args


class StdStreamTee:
    """
    Standard stream tee.
    """

    def write(
            self,
            s: str
    ):
        """
        Write.

        :param s: String.
        """

        if self.print_to_stream:
            self.stream.write(s)

        if s != '\n':
            self.buffer.append(s)
            while len(self.buffer) > self.max_buffer_len:
                del self.buffer[0]

    def flush(
            self
    ):
        """
        Flush the stream.
        """

        self.stream.flush()

    def __init__(
            self,
            stream: TextIO,
            max_buffer_len: int,
            print_to_stream: bool
    ):
        """
        Initialize the reader.

        :param stream: Standard stream.
        :param max_buffer_len: Maximum buffer length.
        :param print_to_stream: Whether or not to print back to stream.
        """

        self.stream = stream
        self.max_buffer_len = max_buffer_len
        self.print_to_stream = print_to_stream

        self.buffer = []


class RunThreadManager(threading.Event):
    """
    Manager for run threads, combining a wait event with an abort signal.
    """

    def __init__(
            self,
            initial_flag: bool
    ):
        """
        Initialize the thread manager.

        :param initial_flag: Initial flag value (see threading.Thread for the use of this argument).
        """

        super().__init__()

        if initial_flag:
            self.set()
        else:
            self.clear()

        self.abort = False
