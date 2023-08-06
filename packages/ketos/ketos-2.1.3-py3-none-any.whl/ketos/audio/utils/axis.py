# ================================================================================ #
#   Authors: Fabio Frazao and Oliver Kirsebom                                      #
#   Contact: fsfrazao@dal.ca, oliver.kirsebom@dal.ca                               #
#   Organization: MERIDIAN (https://meridian.cs.dal.ca/)                           #
#   Team: Data Analytics                                                           #
#   Project: ketos                                                                 #
#   Project goal: The ketos library provides functionalities for handling          #
#   and processing acoustic data and applying deep neural networks to sound        #
#   detection and classification tasks.                                            #
#                                                                                  #
#   License: GNU GPLv3                                                             #
#                                                                                  #
#       This program is free software: you can redistribute it and/or modify       #
#       it under the terms of the GNU General Public License as published by       #
#       the Free Software Foundation, either version 3 of the License, or          #
#       (at your option) any later version.                                        #
#                                                                                  #
#       This program is distributed in the hope that it will be useful,            #
#       but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#       GNU General Public License for more details.                               # 
#                                                                                  #
#       You should have received a copy of the GNU General Public License          #
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
# ================================================================================ #

""" 'audio.utils.axis' module within the ketos library

    This module provides utilities to convert bin numbers to 
    continuous variable values and vice versa.

    Bins are numbered 0,1,2,3,...,N-1, counting from lower to 
    higher values, where N is the number of bins.

    By default, each bin represents a half-open interval, including 
    the lower (left) boundary while excluding the upper (right) 
    boudary, i.e., [a,b), except for the last bin, which represents 
    a closed interval with both boundaries included, i.e. [a,b].

    Contents:
        Axis class:
        LinearAxis class:
        Log2Axis class
"""
import numpy as np
import copy

def bin_number(x, pos_func, bins, truncate=False, closed_right=False):
    """ Compute bin number corresponding to a given value.

        If the value lies outside the axis range, a negative 
        bin number or a bin number above N-1 will be returned. 
        This behaviour can be changed using the argument 'truncate'.

        Args:
            x: array-like
                Value
            pos_func: function
                Calculates the position on the axis of any given input value.
            bins: int
                Number of bins
            truncate: bool
                Return 0 if x is below the lower axis boundary 
                and N-1 if x is above the upper boundary. Default 
                is False.
            closed_right: bool
                If False, bin is closed on the left and open on the 
                right. If True, bin is open on the left and closed 
                on the right. Default is False.                    

        Returns: 
            b: array-like
                Bin number
    """
    if np.ndim(x) == 0:
        scalar = True
        x = [x]
    else:
        scalar = False

    if isinstance(x, list):
        x = np.array(x)

    b = pos_func(x)

    if closed_right:
        idx = np.nonzero(np.logical_and(b%1==0, b>0))
        b[idx] = b[idx] - 1
    else:
        b[b == bins] = bins - 1

    if truncate:
        b[b < 0] = 0
        b[b >= bins] = bins - 1
    else:
        idx = np.nonzero(b<0)
        b[idx] = b[idx] - 1

    b = b.astype(dtype=int, copy=False)

    if scalar:
        b = b[0]

    return b

class Axis():
    """ Base class for all Axis classes.

        Child classes must implement the methods `bin` and  `low_edge`.

        Args: 
            bins: int
                Number of bins
            x_min: float
                Left edge of first bin
            label: str
                Descriptive label. Optional

        Attributes:
            bins: int
                Number of bins
            x_min: float
                Left edge of first bin
            label: str
                Descriptive label.
    """
    def __init__(self, bins, x_min, label):
        self.bins = int(bins)
        self.x_min = x_min
        self.label = label

    def up_edge(self, b):
        """ Get the upper-edge value of a given bin.

            Args:
                b: array-like
                    Bin number.
            
            Returns: 
                x: array-like
                    Upper-edge bin value
        """
        return self.low_edge(b+1)

    def min(self):
        """ Get the lower boundary of the axis.

            Returns: 
                : float
                    Lower edge of first bin
        """
        return self.x_min

    def max(self):
        """ Get the upper boundary of the axis.

            Returns: 
                : float
                    Upper edge of the last bin
        """
        x = self.up_edge(self.bins - 1)
        return x

    def bin_width(self, b=0):
        """ Get the width of a given bin.

            Args:
                b: int
                    Bin number

            Returns: 
                : float
                    Bin width
        """
        w = self.low_edge(b+1) - self.low_edge(b)
        return w

    def cut(self, x_min=None, x_max=None, bins=None):
        """ Cut the axis by specifing either a minimum and a maximum value, 
            or by specifying a minimum value and the axis length (as an integer 
            number of bins).

            At both ends of the axis, the bins containing the cut values are 
            included. 

            Args:
                x_min: float
                    Position of lower cut. Defaults to the axis' lower limit.
                x_max: float 
                    Position of upper cut.
                bins: int
                    Cut length, given as a integer number of bins. When `bins` is 
                    specified, the argument `x_max` is ignored.
            
            Returns: 
                b_min, b_max: int, int
                    Lower and upper bin number of the cut

            Example:
                >>> from ketos.audio.utils.axis import LinearAxis
                >>> #Linear axis between 0. and 10. with 20 bins.
                >>> ax = LinearAxis(bins=20, extent=(0.,10.))
                >>> #Select interval from 5.3 to 8.7
                >>> b_min, b_max = ax.cut(x_min=5.3, x_max=8.7)
                >>> print(ax.x_min, ax.x_max, ax.bins, ax.dx)
                5.0 9.0 8 0.5
                >>> print(b_min, b_max)
                10 17
                >>> #Select 6-bin long interval with lower cut at 3.2
                >>> ax = LinearAxis(bins=20, extent=(0.,10.))
                >>> b_min, b_max = ax.cut(x_min=3.2, bins=6)
                >>> print(ax.x_min, ax.x_max, ax.bins, ax.dx)
                3.0 6.0 6 0.5
        """
        # lower bin
        if x_min is not None:
            b_min = self.bin(x_min, truncate=True)
        else:
            b_min = 0

        # upper bin
        if bins is not None:
            b_max = min(self.bins - 1, b_min + bins - 1)
        elif x_max is not None:
            b_max = self.bin(x_max, truncate=True, closed_right=True)
        else:
            b_max = self.bins - 1

        # update attributes
        x_min = self.low_edge(b_min)
        x_max = self.up_edge(b_max)
        self.bins = b_max - b_min + 1
        self.x_min = x_min
        self.x_max = x_max

        return b_min, b_max

    def bin(self, x, truncate=False, closed_right=False):
        """ Get bin number corresponding to a given value.

            By default bins are closed on the left and open on the 
            right, i.e., [a,b). Use the argument `closed_right` to 
            reverse this.

            If the value lies outside the axis range, a negative 
            bin number or a bin number above N-1 will be returned. 
            This behaviour can be changed using the argument 'truncate'.

            Args:
                x: array-like
                    Value
                truncate: bool
                    Return 0 if x is below the lower axis boundary 
                    and N-1 if x is above the upper boundary. Default 
                    is False.
                closed_right: bool
                    If False, bin is closed on the left and open on the 
                    right. If True, bin is open on the left and closed 
                    on the right. Default is False.                    

            Returns: 
                b: array-like
                    Bin number
        """
        pass

    def low_edge(self, b):
        """ Get the lower-edge value of a given bin.

            Must be implemented in child class.

            Args:
                b: array-like
                    Bin number.
            
            Returns: 
                x: array-like
                    Lower-edge bin value
        """
        pass

class LinearAxis(Axis):
    """ Linear axis.

        Args: 
            bins: int
                Number of bins
            extent: tuple(float,float)
                Axis range, e.g. (0., 100.)
            label: str
                Descriptive label. Optional

        Attributes:
            bins: int
                Number of bins
            x_min: float
                Left edge of first bin
            dx: float
                Bin width
            label: str
                Descriptive label.
    """
    def __init__(self, bins, extent, label=None):
        super().__init__(bins=bins, x_min=extent[0], label=label)
        self.dx = (extent[1] - extent[0]) / bins

    def _pos_func(self, x):
        """ Compute the position of a given input value on the axis.

            Args:
                x: array-like
                    Value

            Returns: 
                : array-like
                    Position
        """  
        return (x - self.x_min) / self.dx    

    def bin(self, x, truncate=False, closed_right=False):
        """ Get bin number corresponding to a given value.

            By default bins are closed on the left and open on the 
            right, i.e., [a,b). Use the argument `closed_right` to 
            reverse this.

            If the value lies outside the axis range, a negative 
            bin number or a bin number above N-1 will be returned. 
            This behaviour can be changed using the argument 'truncate'.

            Args:
                x: array-like
                    Value
                truncate: bool
                    Return 0 if x is below the lower axis boundary 
                    and N-1 if x is above the upper boundary. Default 
                    is False.
                closed_right: bool
                    If False, bin is closed on the left and open on the 
                    right. If True, bin is open on the left and closed 
                    on the right. Default is False.                    

            Returns: 
                b: array-like
                    Bin number

            Example:
                >>> from ketos.audio.utils.axis import LinearAxis
                >>> #Linear axis between 0. and 100. with 200 bins.
                >>> ax = LinearAxis(bins=200, extent=(0.,100.))
                >>> #Get bin number corresponding to x=0.6
                >>> b = ax.bin(0.6)
                >>> print(b)
                1
                >>> #Get several bin numbes in one call 
                >>> b = ax.bin([0.6,11.1])
                >>> print(b)
                [ 1 22]
                >>> #Get bin number for values at bin edges
                >>> b = ax.bin([0.0,0.5,1.0,100.])
                >>> print(b)
                [  0   1   2 199]
                >>> #Note that when the value sits between two bins, 
                >>> #the higher bin number is returned.
                >>> #This behaviour can be reversed using the closed_right 
                >>> #argument,
                >>> b = ax.bin([0.0,0.5,1.0,100.], closed_right=True)
                >>> print(b)
                [  0   0   1 199]
                >>> #Note that the lower edge of the first bin and the 
                >>> #upper edge of the last bin are special cases: for 
                >>> #these values, the first (0) and last (199) bin 
                >>> #numbers are always returned.
                >>> #Get bin numbers outside the axis range
                >>> b = ax.bin([-2.1, 100.1])
                >>> print(b)
                [ -5 200]
                >>> b = ax.bin([-2.1, 100.1], truncate=True)
                >>> print(b)
                [  0 199]
        """
        b = bin_number(x, pos_func=self._pos_func, bins=self.bins, truncate=truncate, closed_right=closed_right)
        return b

    def low_edge(self, b):
        """ Get the lower-edge value of a given bin.

            Args:
                b: array-like
                    Bin number.
            
            Returns: 
                x: array-like
                    Lower-edge bin value

            Example:
                >>> from ketos.audio.utils.axis import LinearAxis
                >>> #Linear axis between 12. and 22. with 5 bins.
                >>> ax = LinearAxis(bins=5, extent=(12.,22.))
                >>> #Get lower-edge values of bins 1 and 4
                >>> x = ax.low_edge([1,4])
                >>> print(x)
                [14. 20.]
        """
        if isinstance(b, list):
            b = np.array(b)

        x = self.x_min + b * self.dx
        return x

    def zero_offset(self):
        """ Shift axis lower boundary to zero.
        """
        self.x_min = 0

class Log2Axis(Axis):
    """ Logarithmic axis with base 2.
    
        The lower-edge value of bin no. :math:`i` is calculated 
        from the formula,

        .. math:: 
            x_{i} = 2^{i / m} \cdot x_{0}

        where :math:`m` is the number of bins per octave and 
        :math:`x_0` is the lower-edge value of the first bin.

        Args: 
            bins: int
                Total number of bins
            bins_per_oct: int
                Number of bins per octave
            min_value: float
                Left edge of first bin
            label: str
                Descriptive label. Optional

        Attributes:
            bins: int
                Total number of bins
            bins_per_oct: int
                Number of bins per octave
            x_min: float
                Left edge of first bin
            label: str
                Descriptive label
    """
    def __init__(self, bins, bins_per_oct, min_value, label=None):
        super().__init__(bins=bins, x_min=min_value, label=label)
        self.bins_per_oct = int(bins_per_oct)

    def _pos_func(self, x):
        """ Compute the position of a given input value on the axis.

            Args:
                x: array-like
                    Value

            Returns: 
                : array-like
                    Position
        """  
        return self.bins_per_oct * np.log2(x / self.x_min)

    def bin(self, x, truncate=False, closed_right=False):
        """ Get bin number corresponding to a given value.

            By default bins are closed on the left and open on the 
            right, i.e., [a,b). Use the argument `closed_right` to 
            reverse this.

            If the value lies outside the axis range, a negative 
            bin number or a bin number above N-1 will be returned. 
            This behaviour can be changed using the argument 'truncate'.

            Args:
                x: array-like
                    Value
                truncate: bool
                    Return 0 if x is below the lower axis boundary 
                    and N-1 if x is above the upper boundary. Default 
                    is False.
                closed_right: bool
                    If False, bin is closed on the left and open on the 
                    right. If True, bin is open on the left and closed 
                    on the right. Default is False.                    

            Returns: 
                b: array-like
                    Bin number

            Example:
                >>> from ketos.audio.utils.axis import Log2Axis
                >>> ax = Log2Axis(bins=4*8, bins_per_oct=8, min_value=200.)
                >>> ax.bin([400.,800.])
                array([ 8, 16])
        """
        b = bin_number(x, pos_func=self._pos_func, bins=self.bins, truncate=truncate, closed_right=closed_right)
        return b

    def low_edge(self, b):
        """ Get the lower-edge value of a given bin.

            Args:
                b: array-like
                    Bin number.
            
            Returns: 
                x: array-like
                    Lower-edge bin value

            Example:
                >>> from ketos.audio.utils.axis import Log2Axis
                >>> ax = Log2Axis(bins=4*8, bins_per_oct=8, min_value=200.)
                >>> ax.low_edge([0,16])
                array([200., 800.])
        """
        if isinstance(b, list):
            b = np.array(b)

        x = 2**(b / self.bins_per_oct) * self.x_min
        return x

    def ticks_and_labels(self):
        """ Create ticks and labels for drawing the axis.

            Returns: 
                ticks: numpy.array
                    Tick positions
                labels: list(str)
                    Labels
        """
        i = np.arange(0, self.bins, self.bins_per_oct)

        ticks = self.min() + i * (self.max() - self.min()) / self.bins

        labels = 2**(i / self.bins_per_oct) * self.min()
        labels = ['{0:.1f}'.format(l) for l in labels.tolist()]

        return ticks, labels
