"""
fxpmath

---

A python library for fractional fixed-point arithmetic.

---

This software is provided under MIT License:

MIT License

Copyright (c) 2020 Franco, francof2a

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class Callback():
    """
    Abstract class used for build callbacks.
    """

    def __init__(self):
        pass

    def on_value_change(self, fxp_object, logs=None):
        """Called when fxp_object value is changed."""
        pass

    def on_status_overflow(self, fxp_object, logs=None):
        """Called when fxp_object get overflow status."""
        pass

    def on_status_underflow(self, fxp_object, logs=None):
        """Called when fxp_object get underflow status."""
        pass

    def on_status_inaccuracy(self, fxp_object, logs=None):
        """Called when fxp_object get inaccuracy status."""
        pass