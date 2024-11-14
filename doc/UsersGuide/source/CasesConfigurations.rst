.. role:: raw-html(raw)
    :format: html

.. _hsd:

********************************************
Hierarchical System Development (HSD) Cases
********************************************

Hierarchical System Development is the ability to engage in development and testing at multiple levels of complexity in numerical weather prediction (NWP) software (such as the :term:`UFS`). It typically includes multiple entry points into development (e.g., atmospheric physics, ocean and ice dynamics, or data assimilation for land models and other earth system components), and it can include both operationally relevant and idealized configurations. 

Although the UFS Weather Model (WM) can be run in any of several configurations, from a single-component atmospheric 
model to a fully coupled model with multiple earth system components (e.g., atmosphere, ocean, sea-ice, land, mediator), 
this chapter documents just a few of the cases designed to support hierarchical system development (HSD) within the UFS. 

Currently, users can find information on:

* :ref:`Running the HSD cases using ufs_test.sh <ufs-test>` and
* Two HSD cases: 

   * The :ref:`July 2020 CAPE Case <cape-2020>`
   * The :ref:`Baroclinic Instability Case <baroclinic-wave>`

For a full list of supported WM configurations, view the `rt.conf <https://github.com/ufs-community/ufs-weather-model/blob/develop/tests/rt.conf>`_ file.

.. attention::

   This chapter is a work in progress. There are a multitude of options for configuring the UFS WM, 
   and this chapter merely details a few supported configurations. It will be expanded over time
   to include a wide variety of idealized test cases for use in research and testing. 


.. _cape-2020:

====================
July 2020 CAPE Case
====================

The July 2020 CAPE case illustrates one of the shortcomings of the Global Forecast System (GFS) v16, which is low Convective Available Potential Energy (CAPE) predictions during summertime (:cite:t:`SunEtAl2024`). CAPE is an important index when it comes to forecasting storms and can be affected by a multitude of atmospheric variables. 

This case study helped identify that the lower CAPE results from the GFS were due to the overall drier atmosphere than what was observed in the lowest 1km. This can be attributed to the bias within the initial conditions taken from the Global Data Assimilation System (GDAS) that have a drier soil moisture. 

When compared to the older version of the GFS (v15.2), we see the difference can be attributed to an excessive boundary layer cloud cover that leads to a drop in net radiation at the surface and thus less latent heat flux. This makes for less heat and moisture being fed back to the low levels and ultimately changes the overall vertical 
profile of the atmosphere which changes CAPE values. And in the GFS’s case it results in lower CAPE. All these conditions and biases occuring make this a great case to experiment with as changing the different values talked about above can make for some varying results in the CAPE. See for yourself if you can get the outcome to be close to real life observations!

.. _baroclinic-wave:

============================
Baroclinic Instability Case
============================

The UFS WM baroclinic wave case adapts the test outlined in :cite:t:`Jablonowski&Williamson2006` (2006). This test is designed to evaluate the accuracy of various atmospheric models in simulating a baroclinic wave, which commonly forms in the Northern Hemisphere and influences weather patterns. This test aims to assess how well "dry dynamical cores," the foundational components of weather and climate models that handle air movement and temperature changes, perform in idealized conditions. 

The simulation sets the model's atmosphere to an initial steady state, designed to be a simple, realistic representation of atmospheric conditions using the adiabatic (no heat exchange) and inviscid (no friction) primitive equations. The test first checks whether each model can maintain this steady, zonal (west-to-east) state without developing any unintended changes. After verifying this, the next step is to introduce a small disturbance, or perturbation, which triggers the growth of a baroclinic wave. The wave then evolves over several simulated days, allowing the researchers to observe how accurately different models handle the wave's development and movement.

This test provides a standard way to assess how different atmospheric models handle the development of baroclinic waves. The results help identify which models are more accurate and can serve as benchmarks for model improvement, ultimately contributing to better simulations of atmospheric behavior in weather and climate predictions.

In the UFS WM, the idealized baroclinic wave test case is an atmosphere-only, :term:`dycore`-only forecast run at C192 resolution with 127 vertical levels. It uses default values from the WM's ``export_fv3`` function, along with default values for a tiled grid namelist (``export_tiled``) and for the `Unified Gravity Wave Physics <https://dtcenter.ucar.edu/GMTB/v7.0.0/sci_doc/ugwpv1_gsldrag.html>`_ (``export_ugwpv1``) version 1. These initial values are all set based on values from `default_vars.sh <https://github.com/ufs-community/ufs-weather-model/blob/develop/tests/default_vars.sh>`_. 

The test is set to run a 24-hour forecast from 2019-12-03 at 0z using the `FV3_GFS_v17_p8_ugwpv1 <https://dtcenter.ucar.edu/GMTB/v7.0.0/sci_doc/_g_f_s_v17_p8_ugwpv1_page.html>`_ physics suite. However, it is recommended that users modify the case to run it as a 5-10 day forecast by setting the forecast length (``FHMAX``) to 120-240 hours in the test file (see :numref:`Section %s <test-config>` for instructions). Users will also need to update ``OUTPUT_FH`` accordingly. 

.. _ufs-test:

============================================
Running the HSD Cases Using ``ufs_test.sh``
============================================

This section explains how to run the idealized cases described above using the ``ufs-test.sh`` script.

Clone the Repository
--------------------

To start, recursively clone the repository:

.. code-block:: console

   git clone --recursive -b develop https://github.com/ufs-community/ufs-weather-model.git
   cd ufs-weather-model

After cloning, users may save (or "export") the path to the UFS WM in an environment variable:

.. code-block:: console

   export UFS_WM=$PWD

Although this step is optional, users may find it convenient when navigating between directories. This documentation will use ``${UFS_WM}`` to refer to the path to the ``ufs-weather-model`` directory, but users may choose to type out the full path instead. 

.. _machine-config:

Machine Configuration
-----------------------

The HSD cases are configured to be run on NOAA Tier-1 platforms, and the configuration files for each platform are located at:

.. code-block:: console

   ${UFS_WM}/tests-dev/machine_config/machine_<PLATFORM>.config

where ``<PLATFORM>`` corresponds to the name of the platform. These configuration files load the necessary Python and Rocoto modules for each platform. Users generally do not need to make any changes to these files. 

.. _test-config:

Test Configuration
----------------------

The July 2020 CAPE case can be run as-is without adjusting the configuration. However, it is recommended that users adjust certain values in the baroclinic wave case. Currently, the forecast length (``FHMAX``) is set to 24 hours, but it is recommended that users run the case for 5 or 10 days (120 or 240 hours). To do this, open ``${UFS_WM}/tests-dev/test_cases/tests/baroclinic_wave`` using ``vi``/``vim`` or a code editor. Then, add ``FHMAX`` and update ``OUTPUT_FH`` to extend by increments of 6 to the new ``FHMAX``. 

.. code-block:: console

   export FHMAX=120      # (or 240) 
   export OUTPUT_FH='0 6 12 18 24 30 36 42 48 54 60 66 72 78 84 90 96 102 108 114 120'

In general, it is preferable to make ``FHMAX`` a multiple of 24. 

.. _baseline-config:

Baseline Configuration
----------------------

Users may need to modify the baseline configuration file (``${UFS_WM}/tests-dev/baseline_setup.yaml``), which contains details on the location of staged input data, user-specific output directories, and batch job scheduling. The following variables are of particular importance:

* ``dprefix``: Set this value to an existing directory where the user has write permissions. 
* ``STMP``: Directory for baseline test output (typically ``${dprefix}/stmp4``)
* ``PTMP``: Directory for runtime files (typically ``${dprefix}/stmp2``)

.. _run-tests:

Running Tests
-------------

Launch tests from the ``${UFS_WM}/tests-dev`` directory with the following command:

.. code-block:: console

   cd tests-dev
   ./ufs_test.sh -a <ACCOUNT> [-s] [-c] -k -r -n "<CASE_NAME> <COMPILER>"

where:

* ``<ACCOUNT>``: Account/project number for batch jobs.
* ``<CASE_NAME>``: Name of the test case (e.g., ``2020_CAPE`` or ``baroclinic_wave``).
* ``<COMPILER>``: Compiler used for the tests (``intel`` or ``gnu``).

**Comand-line Options:**

- ``-s``: Syncs scripts from ``./ufs-wm/tests`` to ``./ufs-wm/tests-dev`` (only required on the first run)
- ``-c``: Creates a new baseline (necessary until idealized case baselines are staged in the ``UFS_WM_RT`` directory).  
- ``-k``: Keeps runtime directories after test completion
- ``-r``: Uses Rocoto workflow manager
- ``-n``: Runs a single test case

.. COMMENT: What is the -m option? It should be listed here. 

.. note::

   After the initial run of ``ufs_test.sh`` with the ``-s`` option, users do not need to use ``-s`` again. 

Examples
^^^^^^^^^^

A user with access to the ``epic`` account can run the ``2020_CAPE`` test case with the ``intel`` compiler on ``Hera``, ``Orion``, or ``Gaea`` using the following command:

.. code-block:: console

   ./ufs_test.sh -a epic -s -c -k -r -n "2020_CAPE intel"

For the ``baroclinic_wave`` test case, which takes longer, the same user would run:

.. code-block:: console

   ./ufs_test.sh -a epic -s -c -k -r -n "baroclinic_wave intel"

Running Multiple Cases
^^^^^^^^^^^^^^^^^^^^^^^^

To run multiple cases at once, copy ``test_cases.yaml`` from the test cases directory and use the ``-l`` argument:

.. code-block:: console

   cp ${UFS_WM}/tests-dev/test_cases/test_cases.yaml ${UFS_WM}/tests-dev/
   ./ufs_test.sh -a epic -s -c -k -r -l test_cases.yaml

Checking Results
-----------------

When the test case finishes running, users should see console output that includes a ``SUCCESS`` message: 

.. code-block:: console
   :emphasize-lines: 2 

   Performing Cleanup...
   REGRESSION TEST RESULT: SUCCESS
   + echo 'ufs_test.sh finished'
   ufs_test.sh finished
   + cleanup
   ++ awk '{print $2}'
   + PID_LOCK=2133541
   + [[ 2133541 == \2\1\3\3\5\4\1 ]]
   + rm -rf /scratch2/NAGAPE/epic/Gillian.Petro/ufs-weather-model/tests-dev/lock
   + [[ false == true ]]
   + trap 0
   + exit

Compilation and model run directories can be accessed in the local repository via the ``run_dir`` softlink, which points to the actual ``FV3_RT`` directory. Each test generates ``atm*.nc`` and ``sfc*.nc`` files at specified forecast hour intervals. 

Users can view progress of compile or model run phases by using the ``tail -f <file>`` command or ``vi``/``vim`` on the ``err`` or ``out`` files in the ``run_dir/compile*`` or ``run_dir/<case_name>`` directories. For example, to monitor progress or check results for the ``2020_CAPE_intel`` case, run:

.. code-block:: console

   tail -f ${UFS_WM}/tests-dev/run_dir/2020_CAPE_intel/err
   tail -f ${UFS_WM}/tests-dev/run_dir/2020_CAPE_intel/out

.. note::
   
   Once the tests run successfully with the ``-c`` option (baseline created), users can compare future test results with the newly created baseline using ``-m`` instead of ``-c``.

For further test management, users may save the test directory location in an environment variable:

.. code-block:: console

   export UFS_WM_TEST=/path/to/expt_dirs/ufs_test
