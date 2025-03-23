# a Pythonesque Canvas v0.8
# Author : Jerome Alet - <alet@librelogiciel.com>
# License : ReportLab's license
#
# $Id: pycanvas.py 1821 2002-11-06 17:11:31Z rgbecker $
#
__doc__ = """pycanvas.Canvas : a Canvas class which can also output Python source code.

pycanvas.Canvas class works exactly like canvas.Canvas, but you can
call str() on pycanvas.Canvas instances. Doing so will return the
Python source code equivalent to your own program, which would, when
run, produce the same PDF document as your original program.

Generated Python source code defines a doIt() function which accepts
a filename or file-like object as its first parameter, and an
optional boolean parameter named "regenerate".

The doIt() function will generate a PDF document and save it in the
file you specified in this argument. If the regenerate parameter is
set then it will also return an automatically generated equivalent
Python source code as a string of text, which you can run again to
produce the very same PDF document and the Python source code, which
you can run again... ad nauseam ! If the regenerate parameter is
unset or not used at all (it then defaults to being unset) then None
is returned and the doIt() function is much much faster, it is also
much faster than the original non-serialized program.

the reportlab/test/test_pdfgen_pycanvas.py program is the test suite
for pycanvas, you can do the following to run it :

    First set verbose=1 in reportlab/rl_config.py

    then from the command interpreter :

    $ cd reportlab/test
    $ python test_pdfgen_pycanvas.py >n1.py

    this will produce both n1.py and test_pdfgen_pycanvas.pdf

    then :

    $ python n1.py n1.pdf >n2.py
    $ python n2.py n2.pdf >n3.py
    $ ...

    n1.py, n2.py, n3.py and so on will be identical files.
    they eventually may end being a bit different because of
    rounding problems, mostly in the comments, but this
    doesn't matter since the values really are the same
    (e.g. 0 instead of 0.0, or .53 instead of 0.53)

    n1.pdf, n2.pdf, n3.pdf and so on will be PDF files
    similar to test_pdfgen_pycanvas.pdf.

Alternatively you can import n1.py (or n3.py, or n16384.py if you prefer)
in your own program, and then call its doIt function :

    import n1
    pythonsource = n1.doIt("myfile.pdf", regenerate=1)

Or if you don't need the python source code and want a faster result :

    import n1
    n1.doIt("myfile.pdf")

When the generated source code is run directly as an independant program,
then the equivalent python source code is printed to stdout, e.g. :

    python n1.py

    will print the python source code equivalent to n1.py

Why would you want to use such a beast ?

    - To linearize (serialize?) a program : optimizing some complex
      parts for example.

    - To debug : reading the generated Python source code may help you or
      the ReportLab team to diagnose problems. The generated code is now
      clearly commented and shows nesting levels, page numbers, and so
      on. You can use the generated script when asking for support : we
      can see the results you obtain without needing your datas or complete
      application.

    - To create standalone scripts : say your program uses a high level
      environment to generate its output (databases, RML, etc...), using
      this class would give you an equivalent program but with complete
      independance from the high level environment (e.g. if you don't
      have Oracle).

    - To contribute some nice looking PDF documents to the ReportLab website
      without having to send a complete application you don't want to
      distribute.

    - ... Insert your own ideas here ...

    - For fun because you can do it !
"""

import cStringIO
from reportlab.pdfgen import canvas
from reportlab.pdfgen import pathobject
from reportlab.pdfgen import textobject

PyHeader = '''#! /usr/bin/env python

#
# This code was entirely generated by ReportLab (http://www.reportlab.com)
#

import sys
from reportlab.pdfgen import pathobject
from reportlab.pdfgen import textobject
from reportlab.lib.colors import Color

def doIt(file, regenerate=0) :
    """Generates a PDF document, save it into file.

       file : either a filename or a file-like object.

       regenerate : if set then this function returns the Python source
                    code which when run will produce the same result.
                    if unset then this function returns None, and is
                    much faster.
    """
    if regenerate :
        from reportlab.pdfgen.pycanvas import Canvas
    else :
        from reportlab.pdfgen.canvas import Canvas
'''

PyFooter = '''
    # if we want the equivalent Python source code, then send it back
    if regenerate :
        return str(c)

if __name__ == "__main__" :
    if len(sys.argv) != 2 :
        # second argument must be the name of the PDF file to create
        sys.stderr.write("%s needs one and only one argument\\n" % sys.argv[0])
        sys.exit(-1)
    else :
        # we've got a filename, we can proceed.
        print doIt(sys.argv[1], regenerate=1)
        sys.exit(0)'''

def buildargs(*args, **kwargs) :
    """Constructs a printable list of arguments suitable for use in source function calls."""
    arguments = ""
    for arg in args :
        arguments = arguments + ("%s, " % repr(arg))
    for (kw, val) in kwargs.items() :
        arguments = arguments+ ("%s=%s, " % (kw, repr(val)))
    if arguments[-2:] == ", " :
        arguments = arguments[:-2]
    return arguments

class PDFAction :
    """Base class to fake method calls or attributes on PDF objects (Canvas, PDFPathObject, PDFTextObject)."""
    def __init__(self, parent, action) :
        """Saves a pointer to the parent object, and the method name."""
        self._parent = parent
        self._action = action

    def __getattr__(self, name) :
        """Probably a method call on an attribute, returns the real one."""
        return getattr(getattr(self._parent._object, self._action), name)

    def __call__(self, *args, **kwargs) :
        """The fake method is called, print it then call the real one."""
        if not self._parent._parent._in :
            self._precomment()
            self._parent._parent._PyWrite("    %s.%s(%s)" % (self._parent._name, self._action, apply(buildargs, args, kwargs)))
            self._postcomment()
        self._parent._parent._in = self._parent._parent._in + 1
        retcode = apply(getattr(self._parent._object, self._action), args, kwargs)
        self._parent._parent._in = self._parent._parent._in - 1
        return retcode

    def __hash__(self) :
        return hash(getattr(self._parent._object, self._action))

    def __coerce__(self, other) :
        """Needed."""
        return coerce(getattr(self._parent._object, self._action), other)

    def _precomment(self) :
        """To be overriden."""
        pass

    def _postcomment(self) :
        """To be overriden."""
        pass

class PDFObject :
    """Base class for PDF objects like PDFPathObject and PDFTextObject."""
    _number = 0
    def __init__(self, parent) :
        """Saves a pointer to the parent Canvas."""
        self._parent = parent
        self._initdone = 0

    def __getattr__(self, name) :
        """The user's programs wants to call one of our methods or get an attribute, fake it."""
        return PDFAction(self, name)

    def __repr__(self) :
        """Returns the name used in the generated source code (e.g. 'p' or 't')."""
        return self._name

    def __call__(self, *args, **kwargs) :
        """Real object initialisation is made here, because now we've got the arguments."""
        if not self._initdone :
            self.__class__._number = self.__class__._number + 1
            methodname = apply(self._postinit, args, kwargs)
            self._parent._PyWrite("\n    # create PDF%sObject number %i\n    %s = %s.%s(%s)" % (methodname[5:], self.__class__._number, self._name, self._parent._name, methodname, apply(buildargs, args, kwargs)))
            self._initdone = 1
        return self

class Canvas :
    """Our fake Canvas class, which will intercept each and every method or attribute access."""
    class TextObject(PDFObject) :
        _name = "t"
        def _postinit(self, *args, **kwargs) :
            self._object = apply(textobject.PDFTextObject, (self._parent, ) + args, kwargs)
            return "beginText"

    class PathObject(PDFObject) :
        _name = "p"
        def _postinit(self, *args, **kwargs) :
            self._object = apply(pathobject.PDFPathObject, args, kwargs)
            return "beginPath"

    class Action(PDFAction) :
        """Class called for every Canvas method call."""
        def _precomment(self) :
            """Outputs comments before the method call."""
            if self._action == "showPage" :
                self._parent._PyWrite("\n    # Ends page %i" % self._parent._pagenumber)
            elif self._action == "saveState" :
                state = {}
                d = self._parent._object.__dict__
                for name in self._parent._object.STATE_ATTRIBUTES:
                    state[name] = d[name]
                self._parent._PyWrite("\n    # Saves context level %i %s" % (self._parent._contextlevel, state))
                self._parent._contextlevel = self._parent._contextlevel + 1
            elif self._action == "restoreState" :
                self._parent._contextlevel = self._parent._contextlevel - 1
                self._parent._PyWrite("\n    # Restores context level %i %s" % (self._parent._contextlevel, self._parent._object.state_stack[-1]))
            elif self._action == "beginForm" :
                self._parent._formnumber = self._parent._formnumber + 1
                self._parent._PyWrite("\n    # Begins form %i" % self._parent._formnumber)
            elif self._action == "endForm" :
                self._parent._PyWrite("\n    # Ends form %i" % self._parent._formnumber)
            elif self._action == "save" :
                self._parent._PyWrite("\n    # Saves the PDF document to disk")

        def _postcomment(self) :
            """Outputs comments after the method call."""
            if self._action == "showPage" :
                self._parent._pagenumber = self._parent._pagenumber + 1
                self._parent._PyWrite("\n    # Begins page %i" % self._parent._pagenumber)
            elif self._action in [ "endForm", "drawPath", "clipPath" ] :
                self._parent._PyWrite("")

    _name = "c"
    def __init__(self, *args, **kwargs) :
        """Initialize and begins source code."""
        self._parent = self     # nice trick, isn't it ?
        self._in = 0
        self._contextlevel = 0
        self._pagenumber = 1
        self._formnumber = 0
        self._footerpresent = 0
        self._object = apply(canvas.Canvas, args, kwargs)
        self._pyfile = cStringIO.StringIO()
        self._PyWrite(PyHeader)
        try :
            del kwargs["filename"]
        except KeyError :
            pass
        self._PyWrite("    # create the PDF document\n    %s = Canvas(file, %s)\n\n    # Begins page 1" % (self._name, apply(buildargs, args[1:], kwargs)))

    def __nonzero__(self) :
        """This is needed by platypus' tables."""
        return 1

    def __str__(self) :
        """Returns the equivalent Python source code."""
        if not self._footerpresent :
            self._PyWrite(PyFooter)
            self._footerpresent = 1
        return self._pyfile.getvalue()

    def __getattr__(self, name) :
        """Method or attribute access."""
        if name == "beginPath" :
            return self.PathObject(self)
        elif name == "beginText" :
            return self.TextObject(self)
        else :
            return self.Action(self, name)

    def _PyWrite(self, pycode) :
        """Outputs the source code with a trailing newline."""
        self._pyfile.write("%s\n" % pycode)

if __name__ == '__main__':
    print 'For test scripts, look in reportlab/test'
