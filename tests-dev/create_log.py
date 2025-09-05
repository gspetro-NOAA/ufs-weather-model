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
    compile_pass= 0
    compile_nr  = 0
    job_nr = 0
    pass_nr= 0
    fail_nr= 0
    failed_list= []
    test_changes_list= env.pathrt+'/test_changes.list'
    with open(env.ufs_test_yaml, 'r') as f:
        rt_yaml = yaml.load(f, Loader=yaml.FullLoader)
        for apps, jobs in rt_yaml.items():
            for key, val in jobs.items():
                if (str(key) == 'build'):
                    rt_compiler = val['compiler']
                    Ccompile_id  = apps
                    machine_check = machine_check_off(env.machine_id, val)
                    pass_tests = False
                    if machine_check:
                        compile_nr += 1
                        rt_compiler = val['compiler']
                        compile_id = apps
                        compile_log, passed = process_compile_log(env.machine_id, compile_id, rt_compiler, env.pathrt)
                        run_logs += compile_log
                        if passed:
                            compile_pass += 1
                if (str(key) == 'tests' and env.compile_only == 'false' and not pass_tests):
                    for test in val:
                        case, config = get_testcase(test)
                        machine_check = machine_check_off(env.machine_id, config)
                        if machine_check:
                            job_nr+=1
                            test_log, passed, failed_name = process_test_log(env.machine_id, case, rt_compiler, config)
                            run_logs += test_log
                            if passed:
                                pass_nr += 1
                            else:
                                fail_nr += 1
                                failed_list.append(failed_name + " " + rt_compiler)
                    run_logs += '\n'
    filename = env.pathrt+'/logs/RegressionTests_'+env.machine_id+'.log'
    write_logfile(filename, "a", output=run_logs)

    test_start_time, test_end_time = get_timestamps('./logs/log_'+env.machine_id+'/')
    
    clean_start_time= test_start_time.split('.')[0]
    start_time      = datetime.strptime(clean_start_time, "%Y-%m-%d %H:%M:%S")
    clean_end_time  = test_end_time.split('.')[0]
    end_time        = datetime.strptime(clean_end_time, "%Y-%m-%d %H:%M:%S")

    hours, remainder= divmod((end_time - start_time).total_seconds(), 3600)
    minutes, seconds= divmod(remainder, 60)
    hours = int(hours);    minutes=int(minutes);     seconds =int(seconds)
    hours = f"{hours:02}"; minutes= f"{minutes:02}"; seconds= f"{seconds:02}"
    elapsed_time = hours+'h:'+minutes+'m:'+seconds+'s'

    compile_pass = str(int(compile_pass))
    compile_nr   = str(int(compile_nr))
    job_nr       = str(int(job_nr))
    pass_nr      = str(int(pass_nr))
    fail_nr      = str(int(fail_nr))
    synop_log    = f"""
SYNOPSIS:
Starting Date/Time: {test_start_time}
Ending Date/Time: {test_end_time}
Total Time: {elapsed_time}
Compiles Completed: {compile_pass}/{compile_nr}
Tests Completed: {pass_nr}/{job_nr}

"""    
    write_logfile(filename, "a", output=synop_log)

    if (int(fail_nr) == 0):
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
