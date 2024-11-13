.. |nbsp| unicode:: 0xA0 
   :trim:

.. role:: raw-html(raw)
    :format: html

.. _hsd:

********************************************
Hierarchical System Development (HSD) Cases
********************************************

The UFS Weather Model (WM) can be run in any of several configurations, from a single-component atmospheric 
model to a fully coupled model with multiple earth system components (e.g., atmosphere, ocean, sea-ice, land, and 
mediator). This chapter documents a few of the cases designed to support hierarchical system development (HSD) within the UFS. 
For a full list of supported WM configurations, view the `rt.conf <https://github.com/ufs-community/ufs-weather-model/blob/develop/tests/rt.conf>`__ file.

.. attention::

   This chapter is a work in progress. There are a multitude of options for configuring the UFS WM, 
   and this chapter merely details a few supported configurations. It will be expanded over time
   to include a wide variety of idealized test cases for use in research and testing. 

.. _ufs-test:

================
``ufs_test.sh``
================

The ``ufs-test.sh`` script ....

.. COMMENT: Expand w/background info


.. _cape-2020:

====================
2020 July CAPE Case
====================

The July 2020 CAPE case illustrates one of the shortcomings of the Global Forecast System (GFS) v16: low Convective Available Potential Energy (CAPE) predictions during summertime. The NOAA Environmental Modeling Center (EMC) Model Evaluation Group (MEG) identified this concern, and ... (:cite:t:`SunEtAl2024`).

The case runs are initialized at 00z Jul 23, 2020 with a 24 hour forecast length. The corresponding namelist options that need to be changed are listed below. The app uses ``./xmlchange`` to change the runtime settings. The settings that need to be modified to set up the start date, start time, and run time are listed below.

Initial condition (IC) files are created from GFS operational dataset in NEMSIO format. The GFS analysis dataset is used as ‘truth’ to compare with simulated synoptic dynamic fields. The CAPE field is evaluated based on Rapid Refresh (RAP) analysis dataset and atmospheric sounding.

Both MRW App v1.0 and GFS.v16.0.10 simulate a lower value of CAPE compared with RAP_ANL and sounding observation in this summertime case study. Further investigations (MEG 2021) show that this is related to the drier soil layers in GFS initial conditions. The SRW_RRFSv1alpha also underestimates the CAPE. (:cite:t:`SunEtAl2024`)

References

NOAA Environmental Modeling Center Model Evaluation Group (MEG) (2021). [Link]

Sun X., D. Heinzeller, L. Bernardet, L. Pan, W. Li, D. Turner, and J. Brown. 2024: A Case Study Investigating the Low Summertime CAPE Behavior in the Global Forecast System. Weather and Forecasting. 

https://doi.org/10.1175/WAF-D-22-0208.1

https://journals.ametsoc.org/view/journals/wefo/39/1/WAF-D-22-0208.1.xml
Last name and initials of author(s) (if nine or more, the first author is followed by "and Coauthors"), year of publication, title of paper, title of journal (italicized),* volume of journal (bolded), issue or citation number (only if required for identification), page range, and DOI (if available).

export dprefix="/scratch2/NAGAPE"
STMP="${dprefix}/stmp4"
PTMP="${dprefix}/stmp2"
