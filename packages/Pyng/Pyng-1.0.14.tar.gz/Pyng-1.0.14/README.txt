====
Pyng
====

Pyng is a collection of Python utility functions I've written over the years,
and that I keep wishing were available everywhere. Sadly, in many cases I've
simply pasted copies of individual functions as needed. But no more!

It's organized as follows:

* **commands:** decorator to automatically build an argparse.ArgumentParser by
  decorating functions you want to expose as script subcommands

* **dicts:** dict subsets, dict searching

* **exc:** manipulate exceptions, e.g. reraise, retry

* **genio:** generator-based file I/O, loosely related to Java file streams

* **graph:** filter DAG represented as dict of (key, otherkeys)

* **iters:** generic iterator functionality, akin to itertools

* **out:** construct a file-like output object to wrap a specified sink
  function, with buffer_lines as a useful example and syslogger as a practical
  use case

* **relwalk:** os.walk() filtered to produce pathnames relative to the
  starting directory

* **replacefile:** filter a text file in-place

* **timing:** time-related utilities, e.g. duration() to produce a
  human-friendly description of a specified interval and ProgressTimer to
  abstract ETA computations

* **tk:** Tkinter utilities, e.g. prompt for a single password or construct a
  prompt dialog from (description, type) tuples

* **toposort:** topological sort of DAG represented as dict of (key, otherkeys)

In addition...

* **ProgressBar** provides experimental progress-bar support for a long-
  running console script, from self-overwriting console messages through
  wxPython, zenity, Tkinter. This is very much a work in progress, though
  functional subsets have been successfully used.

Please see the individual docstrings for more information.
