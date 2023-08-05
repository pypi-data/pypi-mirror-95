
**Before instantiating any instruments or starting a measurement** we change the directory in which the experiments are saved using the :meth:`~quantify.data.handling.set_datadir` [:meth:`~quantify.data.handling.get_datadir`] functions.


.. tip::

    We **highly recommended to** settle for a single common data directory for all notebooks/experiments within your measurement setup/PC (e.g. *~/quantify-data* (unix) or *D:\\Data\\quantify-data* (Windows).
    The utilities to find/search/extract data only work if all the experiment containers are located within the same directory.

.. jupyter-execute::
    :hide-code:

    # We recommend to always set the directory at the start of the python kernel
    # and stick to a single common data directory for all
    # notebooks/experiments within your measurement setup/PC

.. jupyter-execute::

    # This sets a default data directory for tutorial purposes. Change it to your desired data directory.
    from pathlib import Path
    from os.path import join
    from quantify.data.handling import get_datadir, set_datadir
    set_datadir(join(Path.home(), 'quantify-data')) # change me!
    print(f"Data will be saved in:\n{get_datadir()}")
