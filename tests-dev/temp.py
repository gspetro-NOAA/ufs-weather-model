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
