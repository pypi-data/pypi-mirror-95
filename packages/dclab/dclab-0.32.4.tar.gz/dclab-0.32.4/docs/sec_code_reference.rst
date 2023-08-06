==============
Code reference
==============

.. toctree::
  :maxdepth: 2



.. _sec_ref_definitions:


module-level methods
====================
.. autofunction:: dclab.new_dataset


global definitions
==================
These definitionas are used throughout the dclab/Shape-In/Shape-Out ecosystem.

configuration
-------------
Valid configuration sections and keys are described in:
:ref:`sec_analysis_meta` and :ref:`sec_experiment_meta`.


.. data:: dclab.dfn.CFG_ANALYSIS

    User-editable configuration for data analysis.
    
.. data:: dclab.dfn.CFG_METADATA

    Measurement-specific metadata.

.. data:: dclab.dfn.config_funcs

    Dictionary of dictionaries containing functions to convert input data
    to the predefined data type

.. data:: dclab.dfn.config_keys

    Dictionary with sections as keys and configuration parameter
    names as values

.. data:: dclab.dfn.config_types

    Dictionary of dictionaries containing the data type of each
    configuration parameter


features
--------
Features are discussed in more detail in: :ref:`sec_features`.


.. autofunction:: dclab.dfn.feature_exists

.. autofunction:: dclab.dfn.get_feature_label

.. autofunction:: dclab.dfn.scalar_feature_exists


.. data:: dclab.dfn.FEATURES_NON_SCALAR

    Non-scalar features

.. data:: dclab.dfn.feature_names

    List of valid feature names

.. data:: dclab.dfn.feature_labels

    List of human-readable labels for each valid feature

.. data:: dclab.dfn.feature_name2label

    Dictionary that maps feature names to feature labels

.. data:: dclab.dfn.scalar_feature_names

    List of valid scalar feature names

parse functions
---------------
.. automodule:: dclab.parse_funcs
   :members:
   :undoc-members:


.. _sec_ref_rtdc_dataset:

RT-DC dataset manipulation
==========================

Base class
----------

.. autoclass:: dclab.rtdc_dataset.RTDCBase
    :members:


.. _sec_ref_rtdc_dataset_dcor:

DCOR (online) format
--------------------

.. autoclass:: dclab.rtdc_dataset.RTDC_DCOR
    :members:


.. autoclass:: dclab.rtdc_dataset.fmt_dcor.APIHandler
    :members:



Dictionary format
-----------------

.. autoclass:: dclab.rtdc_dataset.RTDC_Dict

HDF5 (.rtdc) format
-------------------

.. autoclass:: dclab.rtdc_dataset.RTDC_HDF5
    :members:

.. autodata:: dclab.rtdc_dataset.fmt_hdf5.MIN_DCLAB_EXPORT_VERSION


Hierarchy format
----------------

.. autoclass:: dclab.rtdc_dataset.RTDC_Hierarchy

TDMS format
-----------

.. autoclass:: dclab.rtdc_dataset.RTDC_TDMS

.. autofunction:: dclab.rtdc_dataset.fmt_tdms.get_project_name_from_path

.. autofunction:: dclab.rtdc_dataset.fmt_tdms.get_tdms_files

.. _sec_ref_rtdc_config:


Ancillaries
-----------
.. automodule:: dclab.rtdc_dataset.ancillaries.ancillary_feature
    :members:
    :undoc-members:


config
------
.. autoclass:: dclab.rtdc_dataset.config.Configuration
    :members:

.. autofunction:: dclab.rtdc_dataset.config.load_from_file

.. _sec_ref_rtdc_export:

export
------
.. autoexception:: dclab.rtdc_dataset.export.LimitingExportSizeWarning

.. autoclass:: dclab.rtdc_dataset.export.Export
    :members:


.. _sec_ref_rtdc_filter:

filter
------
.. autoclass:: dclab.rtdc_dataset.filter.Filter
    :members:


low-level functionalities
=========================

.. _sec_ref_downsampling:

downsampling
------------

.. automodule:: dclab.downsampling
   :members:
   :undoc-members:


.. _sec_ref_features:

features
--------

image-based
...........

.. autofunction:: dclab.features.contour.get_contour

.. autofunction:: dclab.features.bright.get_bright

.. autofunction:: dclab.features.inert_ratio.get_inert_ratio_cvx

.. autofunction:: dclab.features.inert_ratio.get_inert_ratio_raw

.. autofunction:: dclab.features.volume.get_volume


emodulus
........

.. automodule:: dclab.features.emodulus
    :members:

.. automodule:: dclab.features.emodulus.load
    :members:

.. automodule:: dclab.features.emodulus.pxcorr
    :members:

.. automodule:: dclab.features.emodulus.scale_linear
    :members:

.. automodule:: dclab.features.emodulus.viscosity
    :members:


fluorescence
............

.. autofunction:: dclab.features.fl_crosstalk.correct_crosstalk

.. autofunction:: dclab.features.fl_crosstalk.get_compensation_matrix



.. _sec_ref_isoelastics:

isoelastics
-----------

.. automodule:: dclab.isoelastics
   :members:
   :undoc-members:



.. _sec_ref_kde_contours:

kde_contours
------------

.. automodule:: dclab.kde_contours
   :members:
   :undoc-members:


.. _sec_ref_kde_methods:

kde_methods
-----------

.. automodule:: dclab.kde_methods
   :members:
   :undoc-members:


.. _sec_ref_polygon_filter:

polygon_filter
--------------

.. automodule:: dclab.polygon_filter
   :members:
   :undoc-members:


.. _sec_ref_statistics:

statistics
----------

.. automodule:: dclab.statistics
   :members:
   :undoc-members:


R and lme4
==========

.. _sec_ref_lme4:

.. automodule:: dclab.lme4.rlibs
   :members:
   :undoc-members:
   :exclude-members: MockPackage

.. automodule:: dclab.lme4.rsetup
   :members:
   :undoc-members:

.. automodule:: dclab.lme4.wrapr
   :members:
   :undoc-members:



machine learning
================

.. _sec_ref_ml_mllibs:

.. automodule:: dclab.ml.mllibs
   :members:
   :undoc-members:
   :exclude-members: MockPackage

.. _sec_ref_ml_modc:

.. automodule:: dclab.ml.modc
   :members:
   :undoc-members:

.. _sec_ref_ml_models:

.. automodule:: dclab.ml.models
   :members:
   :undoc-members:

.. _sec_ref_ml_tf_dataset:

.. automodule:: dclab.ml.tf_dataset
   :members:
   :undoc-members: