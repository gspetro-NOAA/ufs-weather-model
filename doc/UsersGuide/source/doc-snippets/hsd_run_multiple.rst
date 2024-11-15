To run multiple cases at once, copy ``test_cases.yaml`` from the test cases directory and use the ``-l`` argument:

.. code-block:: console

   cp ${UFS_WM}/tests-dev/test_cases/test_cases.yaml ${UFS_WM}/tests-dev/
   ./ufs_test.sh -a epic -s -c -k -r -l test_cases.yaml
