"""Library of I/O routines to get data into a LightCurve object.

"""

import matplotlib as mpl
import matplotlib.pyplot as plt
#-- Don't render plots to screen
mpl.use('Agg')

from astropy.io import fits as pyfits

from .lightcurve import LightCurve
from .cos import CosCurve
from .stis import StisCurve

__all__ = ['open']

#-------------------------------------------------------------------------------

def open(**kwargs):
    """ Open file into lightcurve

    filename must be supplied in kwargs

    Parameters
    ----------
    **kwargs : dict
        Additional arguements to be passed to lightcurve instantiations

    Returns
    -------
    LightCurve or subclass

    Raises
    ------
    IOError
        If filename is not supplied in **kwargs

    """

    if not 'filename' in kwargs:
        raise IOError('filename must be supplied')

    filetype = check_filetype(kwargs['filename'])

    if filetype == 'corrtag':
        return CosCurve(**kwargs)
    elif filetype == 'tag':
        return StisCurve(**kwargs)
    elif filetype == 'lightcurve':
        return open_lightcurve(kwargs['filename'])
    else:
        raise IOError("Filetype not recognized: {}".format(filetype))

#-------------------------------------------------------------------------------

def check_filetype(filename):
    """Determine the type of data being input.

    File type is determined by the culumns in the first data extension.

    Parameters
    ----------
    filename : str
        name of the input file

    Returns
    -------
    filetype : str
        determined type of file

    """

    corrtag_names = set( ['TIME',
                          'RAWX',
                          'RAWY',
                          'XCORR',
                          'YCORR',
                          'XDOPP',
                          'XFULL',
                          'YFULL',
                          'WAVELENGTH',
                          'EPSILON',
                          'DQ',
                          'PHA'] )

    lightcurve_names = set( ['TIMES',
                             'MJD',
                             'GROSS',
                             'COUNTS',
                             'NET',
                             'FLUX',
                             'FLUX_ERROR',
                             'BACKGROUND',
                             'ERROR'] )

    tag_names = set(['TIME',
                     'AXIS1',
                     'AXIS2',
                     'DETAXIS1'])

    with pyfits.open(filename) as hdu:
        input_names = set([item.upper() for
                           item in hdu[1].data.names])

    if input_names == corrtag_names:
        filetype = 'corrtag'
    elif input_names == lightcurve_names:
        filetype = 'lightcurve'
    elif input_names == tag_names:
        filetype = 'tag'
    else:
        filetype = None

    return filetype

#-------------------------------------------------------------------------------

def open_lightcurve(filename):
    """ Read lightcurve from fits file back into base object

    Parameters
    ----------
    filename : str
        Filename of FITS lightcurve to open

    Returns
    -------
    out_lc : LightCurve
        LightCurve instantiation containing data from file

    """

    out_lc = LightCurve()

    hdu = pyfits.open(filename)

    out_lc.times = hdu[1].data['times']
    out_lc.gross = hdu[1].data['gross']
    out_lc.mjd = hdu[1].data['mjd']
    out_lc.flux = hdu[1].data['flux']
    out_lc.background = hdu[1].data['background']

    return out_obj

#-------------------------------------------------------------------------------

def quicklook(filename):
    """ Quick plotting function for extracted lightcurves
    """


    hdu = pyfits.open(filename)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(hdu[1].data['times'], hdu[1].data['gross'], 'o')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Gross Counts')

    fig.suptitle(filename)
    fig.savefig(filename.replace('.fits', '.pdf'))

#-------------------------------------------------------------------------------

