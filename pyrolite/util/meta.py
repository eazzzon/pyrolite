import os, sys
import io
import inspect
import webbrowser
from pathlib import Path
from numpydoc.docscrape import FunctionDoc, ClassDoc
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def pyrolite_datafolder(subfolder=None):
    """
    Returns the path of the pyrolite data folder.

    Parameters
    -----------
    subfolder : :class:`str`
        Subfolder within the pyrolite data folder.

    Returns
    -------
    :class:`pathlib.Path`
    """
    pth = Path(sys.modules["pyrolite"].__file__).parent / "data"
    if subfolder:
        pth /= subfolder
    return pth


class ToLogger(io.StringIO):
    """
    Output stream which will output to logger module instead of stdout.
    """

    logger = None
    level = None
    buf = ""

    def __init__(self, logger, level=None):
        super(ToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip("\r\n\t ")

    def flush(self):
        self.logger.log(self.level, self.buf)


def stream_log(module, level="INFO"):
    """
    Stream the log from a specific package or subpackage.

    Parameters
    ----------
    module : :class:`str` | :class:`logging.Logger`
        Name of the module to monitor logging from.
    level : :class:`str`, :code:`'INFO'`
        Logging level at which to set the handler output.

    Returns
    -------
    :class:`logging.Logger`
        Logger for the specified package with stream handler added.
    """
    if isinstance(module, str):
        logger = logging.getLogger(module)
    elif isinstance(module, logging.Logger):
        logger = module  # enable passing a logger instance
    else:
        raise NotImplementedError

    # check there are no handlers other than Null
    active_handlers = [
        i
        for i in logger.handlers
        if (
            not isinstance(i, (logging.NullHandler))  # not a null handler
            # and i.level > getattr(logging, level)  # more specific handler pressent
        )
    ]
    if not active_handlers:
        ch = logging.StreamHandler()
        fmt = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        logger.setLevel(getattr(logging, level))
    return logger


def take_me_to_the_docs():
    """Opens the pyrolite documentation in a webbrowser."""
    webbrowser.open("https://pyrolite.rtfd.io")


def sphinx_doi_link(doi):
    """
    Generate a string with a restructured text link to a given DOI.

    Parameters
    ----------
    doi : :class:`str`

    Returns
    --------
    :class:`str`
        String with doi link.
    """
    return "`{} <https://dx.doi.org/{}>`__".format(doi, doi)


def subkwargs(kwargs, *f):
    """
    Get a subset of keyword arguments which are accepted by a function.

    Parameters
    ----------
    kwargs : :class:`dict`
        Dictionary of keyword arguments.
    f : :class:`callable`
        Function(s) to check.

    Returns
    --------
    :class:`dict`
        Dictionary containing only relevant keyword arguments.
    """
    return {k: v for k, v in kwargs.items() if inargs(k, *f)}


def inargs(name, *f):
    """
    Check if an argument is a possible input for a specific function.

    Parameters
    ----------
    name : :class:`str`
        Argument name.
    f : :class:`callable`
        Function(s) to check.

    Returns
    --------
    :class:`bool`
    """
    args = []
    for f in f:
        args += inspect.getfullargspec(f).args
    return name in args


def numpydoc_str_param_list(iterable, indent=4):
    """
    Format a list of numpydoc parameters.

    Parameters
    -------------
    iterable : :class:`list`
        List of numpydoc parameters.
    indent : :class:`int`
        Indent as number of spaces.

    Returns
    -------
    :class:`str`
    """
    out = []
    for param in iterable:
        if param[1]:
            out += ["%s : %s" % (param[0], param[1])]
        else:
            out += [param[0]]
        if param[2] and "".join(param[2]).strip():
            out += [indent * " " + i for i in param[2]]
    out += [""]
    return ("\n" + indent * " ").join(out)


def get_additional_params(
    *fs, t="Parameters", header="", indent=4, subsections=False, subsection_delim="Note"
):
    """
    Checks the base Parameters section of docstrings to get 'Other Parameters'
    for a specific function. Designed to incorporate information on inherited
    or forwarded parameters.

    Parameters
    -------------
    fs : :class:`list`
        List of functions.
    t : :class:`str`
        Target block of docstrings.
    header : :class:`str`
        Optional seciton header.
    indent : :class:`int` | :class:`str`
        Indent as number of spaces, or a string of a given length.
    subsections : :class:`bool`, `False`
        Whether to include headers specific for each function, creating subsections.
    subsection_delim : :class:`str`
        Subsection delimiter.

    Returns
    --------
    :class:`str`

    Todo
    --------
        * Add delimiters between functions to show where arguments should be passed.
    """
    if isinstance(indent, str):
        indent = len(indent)

    if header:
        sectionheader = [header, "-" * (len(header) + 1)]
    else:
        sectionheader = []

    docs = [(f, FunctionDoc(f)) for f in fs]
    pars = []
    subsects = []
    p0 = [i[0] for i in docs[0][1][t]]
    for (f, d) in docs[1:]:  # add things which haven't already been registered
        new = [o for o in d[t] if not (o[0] in p0 or o[0] in pars)]
        if subsections:
            subsection = numpydoc_str_param_list(new, indent=indent)
            if subsection:
                subsection = ("\n" + " " * indent) + ("\n" + " " * indent).join(
                    [
                        ("\n" + " " * indent).join(
                            [subsection_delim, "-" * (len(subsection_delim) + 1)]
                        )
                    ]
                    + [
                        "The following additional parameters are from :func:`{}`.".format(
                            ".".join([f.__module__, f.__name__])
                        )
                    ]
                    + [("\n" + " " * indent).join([header, "-" * (len(header) + 1)])]
                    + [subsection]
                )
                subsects.append(subsection)
        else:
            pars += new

    if not subsections:
        section = numpydoc_str_param_list(pars, indent=indent)
        section = ("\n" + " " * indent).join(sectionheader + [section])
    else:
        section = ("\n" + " " * indent).join(subsects)
    return section


def update_docstring_references(obj, ref="ref"):
    """
    Updates docstring reference names to strings including the function name.
    Decorator will return the same function with a modified docstring. Sphinx
    likes unique names - specifically for citations, not so much for footnotes.

    Parameters
    -----------
    obj : :class:`func` | :class:`class`
        Class or function for which to update documentation references.
    ref : :class:`str`
        String to replace with the object name.

    Returns
    -------
    :class:`func` | :class:`class`
        Object with modified docstring.
    """
    obj.__doc__ = str(obj.__doc__).replace(ref, obj.__name__)
    return obj
