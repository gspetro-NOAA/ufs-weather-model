.. _Configurations:

*************************
Configurations
*************************

The ``ufs-weather-model`` can be configured to form several applications, from a single-component atmospheric model to a fully coupled model with multiple earth system components (atmosphere, ocean, sea-ice and mediator). Currently, the supported configurations are:

.. _UFS-configurations:

.. list-table:: *Supported UFS Weather Model Configurations*
   :widths: 10 70
   :header-rows: 1
   
   * - Configuration Name
     - Description
   * - :ref:`ATM <atm>`
     - Standalone Atmospheric Model (:term:`ATM`)
   * - :ref:`ATMW <atmw>`
     - :term:`ATM` coupled to :term:`WW3`
   * - :ref:`ATMAERO <atmaero>`
     - :term:`ATM` coupled to :term:`GOCART`
   * - :ref:`ATMAQ <atmaq>`
     - :term:`ATM` coupled to :term:`CMAQ`
   * - :ref:`S2S <s2s>`
     - Coupled :term:`ATM` - :term:`MOM6` - :term:`CICE6` - :term:`CMEPS`
   * - :ref:`S2SA <s2sa>`
     - Coupled :term:`ATM` - :term:`MOM6` - :term:`CICE6` - :term:`GOCART` - :term:`CMEPS`
   * - :ref:`S2SW <s2sw>`
     - Coupled :term:`ATM` - :term:`MOM6` - :term:`CICE6` - :term:`WW3` - :term:`CMEPS`
   * - :ref:`S2SWA <s2swa>`
     - Coupled :term:`ATM` - :term:`MOM6` - :term:`CICE6` - :term:`GOCART` - :term:`WW3` - :term:`CMEPS`
   * - :ref:`NG-GODAS <ng-godas>`
     - Coupled :term:`CDEPS` - :term:`DATM` - :term:`MOM6` - :term:`CICE6` - :term:`CMEPS`
   * - :ref:`HAFS <hafs>`
     - Coupled :term:`ATM` - :term:`HYCOM` - :term:`CMEPS`
   * - :ref:`HAFSW <hafsw>`
     - Coupled :term:`ATM` - :term:`HYCOM` - :term:`WW3` - :term:`CMEPS`
   * - :ref:`HAFS-ALL <hafs-all>`
     - Coupled :term:`CDEPS` - :term:`ATM` - :term:`HYCOM` - :term:`WW3` - :term:`CMEPS`

.. COMMENT: Should HAFS-ALL be DATM instead of ATM?

This chapter details the build and run options for each configuration. Click on the Configuration Name in :numref:`Table %s <UFS-configurations>` to go to that section. Each configuration includes sample code for setting ``CMAKE_FLAGS`` and ``CCPP_SUITES``. Additionally, there is a list of preferred physics suites, examples of ``nems.configure`` files, and links to information on other input files required to run the model. 

====================================
Atmospheric Model Configurations
====================================

The atmospheric model configurations all use the UFS Weather Model atmospheric model and may couple it with one other model (e.g., a wave or aerosol model).

.. _atm:

ATM - Standalone Atmospheric Model
=====================================

The standalone atmospheric model (:term:`ATM`) is an :term:`FV3`-based prognostic atmospheric model that can be used for short- and medium-range research and operational forecasts. In standalone mode, ``ATM`` is not coupled to any other model. 


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=ATM -DCCPP_SUITES=FV3_GFS_v16"


Supported Physics Suites
   * ``FV3_GFS_v16``


.. Add later: 
   -----------------------------------
   Required Input Files
   -----------------------------------


.. _atmw:

ATMW
==============

The ATMW configuration couples :term:`ATM` with :term:`WW3`.

**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=ATMW -DCCPP_SUITES=FV3_GFS_2017_coupled,FV3_GFS_v16_coupled"

.. CHECK above!!


Supported Physics Suites
   * ``FV3_GFS_v16``

      .. Check!

   * ``FV3_GFS_2017_coupled``
   * ``FV3_GFS_v16_coupled``

.. _atmaero:

ATMAERO
==============

The ATMAERO configuration couples :term:`ATM` with :term:`GOCART`. 


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=ATMAERO -DCCPP_SUITES=FV3_GFS_v16" 


Supported Physics Suites
   * ``FV3_GFS_v16``


.. _atmaq:

ATMAQ
==============

The ATMAQ configuration couples :term:`ATM` with :term:`CMAQ`.

**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=ATMAQ -DCCPP_SUITES=FV3_GFS_v15p2" 
    

Supported Physics Suites
   * FV3_GFS_v15p2



==========================================
Seasonal to Subseasonal Configurations
==========================================

.. _s2s:

S2S
==============

The S2S configuration couples atmosphere (:term:`ATM`), ocean (:term:`MOM6`), and sea ice (:term:`CICE6`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`). 


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=S2S -DCCPP_SUITES=FV3_GFS_2017_coupled,FV3_GFS_2017_satmedmf_coupled,FV3_GFS_v15p2_coupled,FV3_GFS_v16_coupled,FV3_GFS_v16_couplednsst" 

To run the ``S2S`` configuration with activating CCPP host model under CMEPS and receiving atmosphere-ocean fluxes from mediator:

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=S2S -DCCPP_SUITES=FV3_GFS_v17_coupled_p8_sfcocn -DCMEPS_AOFLUX=ON"

..
   COMMENT: Need some clarification on what the above code does with CCPP/CMEPS... not clear from description. 
    

Supported Physics Suites
   * ``FV3_GFS_2017_coupled``
   * ``FV3_GFS_2017_satmedmf_coupled``
   * ``FV3_GFS_v15p2_coupled``
   * ``FV3_GFS_v16_coupled``
   * ``FV3_GFS_v16_couplednsst``
   * ``FV3_GFS_v17_coupled_p8_sfcoc``


.. _s2sw:

S2SW
==============

The S2SW configuration couples atmosphere (:term:`ATM`), ocean (:term:`MOM6`), and sea ice (:term:`CICE6`), and wave (:term:`WW3`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`).


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=S2SW -DCCPP_SUITES=FV3_GFS_2017_coupled,FV3_GFS_v15p2_coupled,FV3_GFS_v16_coupled,FV3_GFS_v16_coupled_noahmp" 
    

Supported Physics Suites
   * 


.. _s2sa:

S2SA
==============

The S2SW configuration couples atmosphere (:term:`ATM`), ocean (:term:`MOM6`), and sea ice (:term:`CICE6`), wave (:term:`WW3`), and aerosol (:term:`GOCART`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`).


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=S2SA -DCCPP_SUITES=FV3_GFS_2017_coupled,FV3_GFS_v15p2_coupled,FV3_GFS_v16_coupled,FV3_GFS_v16_coupled_noahmp" 

.. CHECK: DAPP flag and physics suites
    

Supported Physics Suites
   * 


.. _s2swa:

S2SWA
==============
The S2SW configuration couples atmosphere (:term:`ATM`), ocean (:term:`MOM6`), and sea ice (:term:`CICE6`), and aerosol (:term:`GOCART`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`).


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=S2SWA -DCCPP_SUITES=FV3_GFS_2017_coupled,FV3_GFS_v15p2_coupled,FV3_GFS_v16_coupled,FV3_GFS_v16_coupled_noahmp" 

.. CHECK: physics suites
    

Supported Physics Suites
   * 


.. _ng-godas:

==============
NG-GODAS
==============

The Next Generation-Global Ocean Data Assimilation System (NG-GODAS) is a UFS Weather Model configuration that couples ocean (:term:`MOM6`), sea ice (:term:`CICE6`), and Data Assimilation (DA) capabilities with the :term:`DATM` component of :term:`CDEPS`. It also uses a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`).



**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=NG-GODAS -DCCPP_SUITES=FV3_GFS_2017_coupled,FV3_GFS_v15p2_coupled,FV3_GFS_v16_coupled"

..
   COMMENT: NG-GODAS --> Coupled CDEPS-DATM-MOM6-CICE6-CMEPS
   What is the DAPP argument? And the physics suites?


Supported Physics Suites
   * 



========================================================
Hurricane Analysis and Reforecast System Configurations
========================================================

The Hurricane Analysis and Forecast System (:term:`HAFS`) is a :term:`UFS` application for hurricane forecasting. It is an :term:`FV3`-based multi-scale model and data assimilation (DA) system capable of providing analyses and forecasts of the inner core structure of tropical cyclones (TC) --- including hurricanes and typhoons --- out to 7 days. HAFS also provides analyses and forecasts of the large-scale environment that is known to influence a TC's motion. HAFS development targets an operational analysis and forecast system for hurricane forecasters with reliable, robust and skillful guidance on TC track and intensity (including rapid intensification), storm size, genesis, storm surge, rainfall, and tornadoes associated with TCs. 

.. _hafs:

HAFS
==============

The HAFS configuration couples atmosphere (:term:`ATM`) and ocean (:term:`HYCOM`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`). HAFS configurations should be run in 32-bit. 

.. COMMENT: Why are all the HAFS configurations 32-bit?

**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=HAFS -D32BIT=ON -DCCPP_SUITES=FV3_HAFS_v0_gfdlmp_tedmf_nonsst,FV3_HAFS_v0_gfdlmp_tedmf,FV3_HAFS_v0_hwrf_thompson,FV3_HAFS_v0_hwrf" 
    

Supported Physics Suites
   * ``FV3_HAFS_v0_gfdlmp_tedmf_nonsst``
   * ``FV3_HAFS_v0_gfdlmp_tedmf``
   * ``FV3_HAFS_v0_hwrf_thompson``
   * ``FV3_HAFS_v0_hwrf``

.. _hafsw:

HAFSW
==============

The HAFSW configuration couples atmosphere (:term:`ATM`), ocean (:term:`HYCOM`), and wave (:term:`WW3`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`).


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=HAFSW -D32BIT=ON -DCCPP_SUITES=FV3_HAFS_v0_gfdlmp_tedmf_nonsst,FV3_HAFS_v0_gfdlmp_tedmf,FV3_HAFS_v0_hwrf_thompson,FV3_HAFS_v0_hwrf" 
    

Supported Physics Suites
   * ``FV3_HAFS_v0_gfdlmp_tedmf_nonsst``
   * ``FV3_HAFS_v0_gfdlmp_tedmf``
   * ``FV3_HAFS_v0_hwrf_thompson``
   * ``FV3_HAFS_v0_hwrf``

.. _hafs-all:

HAFS-ALL
==============

The HAFS-ALL configuration couples atmosphere (:term:`ATM`), ocean (:term:`HYCOM`), and wave (:term:`WW3`) models through a :term:`NUOPC`-compliant :term:`mediator` (:term:`CMEPS`). It also incorporates :term:`CDEPS` for 


**Sample** ``CMAKE_FLAGS`` **Setting**

.. code-block:: console

    export CMAKE_FLAGS="-DAPP=HAFS-ALL -D32BIT=ON -DCCPP_SUITES=FV3_HAFS_v0_gfdlmp_tedmf_nonsst,FV3_HAFS_v0_gfdlmp_tedmf,FV3_HAFS_v0_hwrf_thompson,FV3_HAFS_v0_hwrf" 
    

Supported Physics Suites
   * ``FV3_HAFS_v0_gfdlmp_tedmf_nonsst``
   * ``FV3_HAFS_v0_gfdlmp_tedmf``
   * ``FV3_HAFS_v0_hwrf_thompson``
   * ``FV3_HAFS_v0_hwrf``






