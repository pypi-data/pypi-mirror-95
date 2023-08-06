import math
import magma
from magma import *
from mantle import And, Decode, Or
from .counter import Counter, counter_name


__all__ = ['DefineUpCounterModM', 'UpCounterModM']
__all__ += ['DefineCounterModM', 'CounterModM', 'SizedCounterModM']


def DefineCounterModM(m, n, cin=False, cout=True, incr=1,
                      has_ce=False, has_reset=False):
    """Create an n-bit mod-m counter"""

    name_ = counter_name(f'Counter{n}_Mod{m}', incr, has_ce, has_reset, cin, cout)
    args = []
    if cin:
        args += ['CIN', In(Bit)]

    args += ["O", Out(UInt[n])]
    if cout:
        args += ["COUT", Out(Bit)]

    args += ClockInterface(has_ce, has_reset)

    class CounterModM(Circuit):
        name = name_
        io = IO(**dict(zip(args[::2], args[1::2])))

        counter = Counter(n, cin=cin, cout=False, incr=incr,
                       has_ce=has_ce, has_reset=True)
        reset = Decode(m - 1, n)(counter.O)

        if has_reset:
            reset = Or(2)(reset, m.bit(io.RESET))

        if has_ce:
            CE = io.CE
            reset = And(2)(reset, CE)
            # reset is sometimes called rollover or RO
            # note that we don't return RO in Counter

            # should also handle r in the definition

        wire(magma.reset(reset), counter.RESET) # synchronous reset

        if has_ce:
            wire(CE, counter.CE)

        if cin:
            wire( io.CIN, counter.CIN )

        wire( counter.O, io.O )

        if cout:
            wire( reset, io.COUT )

    return CounterModM

def CounterModM(m, n, cin=False, cout=True, incr=1,
    has_ce=False, has_reset=False, **kwargs):
    return DefineCounterModM(m, n, cin, cout, incr, has_ce, has_reset=has_reset)(**kwargs)

def SizedCounterModM(m, cin=False, cout=False, incr=1,
    has_ce=False, has_reset=False, **kwargs):
    """
    This is that counts from 0 to m - 1 that uses the minimum number of bits
    :param m: The value the counter counts up to
    :param cin: Whether this counter should have a carry input
    :param cout: Whether this counter should a carry output
    :param incr: How much this counter should increment by per clock. Default is 1.
    :param has_ce: Whether this counter should a clock-enable input
    :param kwargs: Args passed to the counter circuit when it is being initialized
    :return: A counter circuit
    """
    return DefineCounterModM(m, math.ceil(math.log(m, 2)), cin, cout, incr, has_ce, has_reset)(**kwargs)

DefineUpCounterModM = DefineCounterModM
UpCounterModM = CounterModM
