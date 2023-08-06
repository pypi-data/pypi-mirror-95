.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_source_auto_examples_plot_raw_minimpl.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_source_auto_examples_plot_raw_minimpl.py:


Example on how to read and plot a PPI from mini-MPL
---------------------------------------------------

Example of how to read in raw data from the mini-MPL
and plot out the PPI by converting it to PyART

Author: Adam Theisen



.. image:: /source/auto_examples/images/sphx_glr_plot_raw_minimpl_001.png
    :alt: plot raw minimpl
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    ## You are using the Python ARM Radar Toolkit (Py-ART), an open source
    ## library for working with weather radar data. Py-ART is partly
    ## supported by the U.S. Department of Energy as part of the Atmospheric
    ## Radiation Measurement (ARM) Climate Research Facility, an Office of
    ## Science user facility.
    ##
    ## If you use this software to prepare a publication, please cite:
    ##
    ##     JJ Helmus and SM Collis, JORS 2016, doi: 10.5334/jors.119

    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:378: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attributes = {k: var.getncattr(k) for k in var.ncattrs()}
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:411: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attrs = FrozenDict((k, self.ds.getncattr(k)) for k in self.ds.ncattrs())
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:411: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attrs = FrozenDict((k, self.ds.getncattr(k)) for k in self.ds.ncattrs())
    /Users/atheisen/anaconda3/lib/python3.7/site-packages/xarray/backends/netCDF4_.py:411: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
      attrs = FrozenDict((k, self.ds.getncattr(k)) for k in self.ds.ncattrs())
    /Users/atheisen/Code/pyart/pyart/graph/radardisplay.py:104: UserWarning: RadarDisplay does not correct for moving platforms
      warnings.warn('RadarDisplay does not correct for moving platforms')
    /Users/atheisen/Code/ACT/examples/plot_raw_minimpl.py:33: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()






|


.. code-block:: default



    import act
    from matplotlib import pyplot as plt

    try:
        import pyart
        PYART_AVAILABLE = True
    except ImportError:
        PYART_AVAILABLE = False

    # Read in sample mini-MPL data
    files = act.tests.sample_files.EXAMPLE_SIGMA_MPLV5
    obj = act.io.mpl.read_sigma_mplv5(files)

    # Create a PyART Radar Object
    radar = act.utils.create_pyart_obj(obj, azimuth='azimuth_angle', elevation='elevation_angle',
                                       range_var='range')

    # Creat Plot Display
    if PYART_AVAILABLE:
        display = pyart.graph.RadarDisplay(radar)
        display.plot('nrb_copol', sweep=0, title_flag=False, vmin=0, vmax=1., cmap='jet')
        plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.899 seconds)


.. _sphx_glr_download_source_auto_examples_plot_raw_minimpl.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_raw_minimpl.py <plot_raw_minimpl.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_raw_minimpl.ipynb <plot_raw_minimpl.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
