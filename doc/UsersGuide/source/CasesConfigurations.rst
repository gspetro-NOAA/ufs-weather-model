.. role:: raw-html(raw)
    :format: html

.. _hsd:

********************************************
Hierarchical System Development (HSD) Cases
********************************************

Hierarchical System Development ... _____ADD MORE HERE_____ ...

The UFS Weather Model (WM) can be run in any of several configurations, from a single-component atmospheric 
model to a fully coupled model with multiple earth system components (e.g., atmosphere, ocean, sea-ice, land, mediator). 
This chapter documents a few of the cases designed to support hierarchical system development (HSD) within the UFS. 
For a full list of supported WM configurations, view the `rt.conf <https://github.com/ufs-community/ufs-weather-model/blob/develop/tests/rt.conf>`__ file.

.. attention::

   This chapter is a work in progress. There are a multitude of options for configuring the UFS WM, 
   and this chapter merely details a few supported configurations. It will be expanded over time
   to include a wide variety of idealized test cases for use in research and testing. 

.. _ufs-test:

================
``ufs_test.sh``
================

This section will include details on how to run idealized cases using the ``ufs-test.sh`` script.

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

Machine Configuration
-----------------------

The HSD cases are configured to be run on NOAA Tier-1 platforms, and the configuration files for each platform are located at:

.. code-block:: console

   ${UFS_WM}/tests-dev/machine_config/machine_<PLATFORM>.config

where ``<PLATFORM>`` corresponds to the name of the platform. These configuration files load the necessary Python and Rocoto modules for each platform. Users generally do not need to make any changes to these files. 

Baseline Configuration
----------------------

Users may need to modify the baseline configuration file (``${UFS_WM}/tests-dev/baseline_setup.yaml``), which contains details on the location of staged input data, user-specific output directories, and batch job scheduling. The following variables are of particular importance:

* ``dprefix``: Set this value to an existing directory where the user has write permissions. 
* ``STMP``: Directory for baseline test output (typically ``${dprefix}/stmp4``)
* ``PTMP``: Directory for runtime files (typically ``${dprefix}/stmp2``)

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

.. _cape-2020:

====================
2020 July CAPE Case
====================

The July 2020 CAPE case illustrates one of the shortcomings of the Global Forecast System (GFS) v16, which is low Convective Available Potential Energy (CAPE) predictions during summertime (:cite:t:`SunEtAl2024`). CAPE is an important index when it comes to forecasting storms and can be affected by a multitude of atmospheric variables. 

This case study helped identify that the lower CAPE results from the GFS were due to the overall drier atmosphere than what was observed in the lowest 1km. This can be attributed to the bias within the initial conditions taken from the Global Data Assimilation System (GDAS) that have a drier soil moisture. 

When compared to the older version of the GFS (v15.2), we see the difference can be attributed to an excessive boundary layer cloud cover that leads to a drop in net radiation at the surface and thus less latent heat flux. This makes for less heat and moisture being fed back to the low levels and ultimately changes the overall vertical 

profile of the atmosphere which changes CAPE values. And in the GFS’s case it results in lower CAPE. All these conditions and biases occuring make this a great case to experiment with as changing the different values talked about above can make for some varying results in the CAPE. See for yourself if you can get 

the outcome to be close to real life observations!

References

NOAA Environmental Modeling Center Model Evaluation Group (MEG) (2021). [Link]

Sun X., D. Heinzeller, L. Bernardet, L. Pan, W. Li, D. Turner, and J. Brown. 2024: A Case Study Investigating the Low Summertime CAPE Behavior in the Global Forecast System. Weather and Forecasting. 

https://doi.org/10.1175/WAF-D-22-0208.1

https://journals.ametsoc.org/view/journals/wefo/39/1/WAF-D-22-0208.1.xml
Last name and initials of author(s) (if nine or more, the first author is followed by "and Coauthors"), year of publication, title of paper, title of journal (italicized),* volume of journal (bolded), issue or citation number (only if required for identification), page range, and DOI (if available).

export dprefix="/scratch2/NAGAPE"
STMP="${dprefix}/stmp4"
PTMP="${dprefix}/stmp2"

.. _baroclinicwave:

============================
Baroclinic Instability Case
============================

The paper "A baroclinic instability test case for atmospheric model dynamical cores" by Christiane Jablonowski and David L. Williamson outlines a test designed to evaluate the accuracy of various atmospheric models in simulating a specific type of wave, known as a baroclinic wave, that commonly forms in the Northern Hemisphere and influences weather patterns. This test aims to assess how well "dry dynamical cores," the foundational components of weather and climate models that handle air movement and temperature changes, perform in idealized conditions.

The simulation begins by setting the model’s atmosphere to an initial steady state, designed to be a simple, realistic representation of atmospheric conditions using the adiabatic (no heat exchange) and inviscid (no friction) primitive equations. The test first checks whether each model can maintain this steady, zonal (west-to-east) state without developing any unintended changes. After verifying this, the next step is to introduce a small disturbance, or perturbation, which triggers the growth of a baroclinic wave. The wave then evolves over several simulated days, allowing the researchers to observe how accurately each model handles the wave’s development and movement.

The study includes four different dynamical cores with varying grid resolutions: NASA/NCAR’s Finite Volume package, NCAR’s spectral transform Eulerian and semi Lagrangian cores from the CAM3 model, and the German Weather Service’s GME model. Each of these hydrostatic cores, which assume no vertical acceleration in the atmosphere, uses different numerical methods to simulate changes in atmospheric pressure, temperature, and wind. Higher resolution grids provide a more detailed look at these processes but require more computing power, while lower resolution grids offer broader, less precise results.

The test showed that models with higher resolutions, which captured atmospheric changes in finer detail, produced more accurate wave patterns that matched expected high resolution "reference solutions." However, the 1 degree resolution (used in lower resolution models) often missed some of the finer details in the wave's growth and behavior. By comparing each model’s results against these high resolution references, the study could analyze how well each model captured the core aspects of wave formation and its growth.

To conclude, this test case provides a standard way to assess how different atmospheric models handle the development of baroclinic waves. The results help identify which models are more accurate and serve as benchmarks for model improvement, ultimately contributing to better simulations of atmospheric behavior in weather and climate predictions.

References

Jablonowski, C., & Williamson, D. L. (2006). A baroclinic instability test case for atmospheric model dynamical cores. Quarterly Journal of the Royal Meteorological Society, 132(621C), 2943-2975. https://doi.org/10.1256/qj.06.12

https://doi.org/10.1256/qj.06.12