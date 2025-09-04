import os
import sys
import subprocess
import yaml
from datetime import datetime
#import datetime
from ufs_test_utils import get_testcase, write_logfile, delete_files, machine_check_off, process_compile_log, process_test_log
from runtime_env import EnvConfig

env = EnvConfig()

def get_timestamps(path):
    """Obtain experiment starting and ending time marks through file timestamps

    Args:
        path (str): experiment log directory
    Returns:
        str: experiment starting and ending time strings
    """
    dir_list = os.listdir(path)
    dt = []
    for f in dir_list:
        m_time = os.path.getmtime(path+f)
        dt.append(datetime.fromtimestamp(m_time))
    dtsort=sorted(dt)
    return str(dtsort[0]),str(dtsort[-1])

def finish_log():
    """Collect regression test results and generate log file.
    """
    run_logs= f"""
"""
    COMPILE_PASS= 0
    COMPILE_NR  = 0
    JOB_NR = 0
    PASS_NR= 0
    FAIL_NR= 0
    failed_list= []
    test_changes_list= env.pathrt+'/test_changes.list'
    with open(env.ufs_test_yaml, 'r') as f:
        rt_yaml = yaml.load(f, Loader=yaml.FullLoader)
        for apps, jobs in rt_yaml.items():
            for key, val in jobs.items():
                if (str(key) == 'build'):
                    RT_COMPILER = val['compiler']
                    COMPILE_ID  = apps
                    machine_check = machine_check_off(env.machine_id, val)
                    PASS_TESTS = False
                    if machine_check:
                        COMPILE_NR += 1
                        RT_COMPILER = val['compiler']
                        COMPILE_ID = apps
                        compile_log, passed = process_compile_log(env.machine_id, COMPILE_ID, RT_COMPILER, env.pathrt)
                        run_logs += compile_log
                        if passed:
                            COMPILE_PASS += 1
                if (str(key) == 'tests' and env.compile_only == 'false' and not PASS_TESTS):
                    for test in val:
                        case, config = get_testcase(test)
                        machine_check = machine_check_off(env.machine_id, config)
                        if machine_check:
                            JOB_NR+=1
                            test_log, passed, failed_name = process_test_log(env.machine_id, case, RT_COMPILER, config)
                            run_logs += test_log
                            if passed:
                                PASS_NR += 1
                            else:
                                FAIL_NR += 1
                                failed_list.append(failed_name + " " + RT_COMPILER)
                    run_logs += '\n'
    filename = env.pathrt+'/logs/RegressionTests_'+env.machine_id+'.log'
    write_logfile(filename, "a", output=run_logs)

    TEST_START_TIME, TEST_END_TIME = get_timestamps('./logs/log_'+env.machine_id+'/')
    
    clean_START_TIME= TEST_START_TIME.split('.')[0]
    start_time      = datetime.strptime(clean_START_TIME, "%Y-%m-%d %H:%M:%S")
    clean_END_TIME= TEST_END_TIME.split('.')[0]
    end_time        = datetime.strptime(clean_END_TIME, "%Y-%m-%d %H:%M:%S")

    hours, remainder= divmod((end_time - start_time).total_seconds(), 3600)
    minutes, seconds= divmod(remainder, 60)
    hours = int(hours);    minutes=int(minutes);     seconds =int(seconds)
    hours = f"{hours:02}"; minutes= f"{minutes:02}"; seconds= f"{seconds:02}"
    elapsed_time = hours+'h:'+minutes+'m:'+seconds+'s'

    COMPILE_PASS = str(int(COMPILE_PASS))
    COMPILE_NR   = str(int(COMPILE_NR))
    JOB_NR       = str(int(JOB_NR))
    PASS_NR      = str(int(PASS_NR))
    FAIL_NR      = str(int(FAIL_NR))
    synop_log    = f"""
SYNOPSIS:
Starting Date/Time: {TEST_START_TIME}
Ending Date/Time: {TEST_END_TIME}
Total Time: {elapsed_time}
Compiles Completed: {COMPILE_PASS}/{COMPILE_NR}
Tests Completed: {PASS_NR}/{JOB_NR}

"""    
    write_logfile(filename, "a", output=synop_log)

    if (int(FAIL_NR) == 0):
        if os.path.isfile(test_changes_list):
            delete_files(test_changes_list)
        open(test_changes_list, 'a').close()
        SUCCESS = "SUCCESS"
        comment_log = f"""
NOTES:
A file test_changes.list was generated but is empty.
If you are using this log as a pull request verification, please commit test_changes.list.

Result: {SUCCESS}

====END OF {env.machine_id} REGRESSION TESTING LOG====
"""
        write_logfile(filename, "a", output=comment_log)
    else:
        with open(test_changes_list, 'w') as listfile:
            for line in failed_list:
                listfile.write(f"{line}\n")
            listfile.close()
        SUCCESS = "FAILED"
        comment_log = f"""
NOTES:
A file test_changes.list was generated with list of all failed tests.
You can use './rt.sh -c -b test_changes.list' to create baselines for the failed tests.
If you are using this log as a pull request verification, please commit test_changes.list.

Result: FAILURE

====END OF {MACHINE_ID} REGRESSION TESTING LOG====
"""
        write_logfile(filename, "a", output=comment_log)
   
    print("Performing Cleanup...")
    exefiles= env.pathrt+'/fv3_*.*x*'; delete_files(exefiles)
    modfiles= env.pathrt+'/modules.fv3_*'; delete_files(modfiles)
    modfiles= env.pathrt+'modulefiles/modules.fv3_*'; delete_files(modfiles)
    tmpfiles= env.pathrt+'/keep_tests.tmp'; delete_files(tmpfiles)
    if env.keep_rundir == 'false':
        rundir = env.pathrt+'/run_dir'
        os.unlink(rundir)
    if env.rocoto == 'true':
        rocotofiles=env.pathrt+'/rocoto*'
        delete_files(rocotofiles)
        lockfiles=env.pathrt+'/*_lock.db'
        delete_files(lockfiles)
    print("REGRESSION TEST RESULT: SUCCESS")    

#if __name__ == '__main__':
