BusPyrate – Python interface for BusPirate binary mode
======================================================

[BusPirate][buspirate] is a digital electronics debugging tool. It has
a [binary mode][bitbang] for interfacing with software rather than
a human. This library provides Python interface for that binary mode.

It's early stage and incomplete: only partial support for bitbang mode
and SPI mode is implemented. SPI mode is completely supported, with
exception of the SPI sniffer. There's no proper documentation yet.

See [examples/](./examples) for example usage.

Note: I only searched PyPi before starting to write this and
wasn't aware of Python 3 port of [pyBusPirateLite][pybuspiratelite].

[buspirate]: http://dangerousprototypes.com/docs/Bus_Pirate
[bitbang]: http://dangerousprototypes.com/docs/Bitbang
[pybuspiratelite]: https://github.com/juhasch/pyBusPirateLite
