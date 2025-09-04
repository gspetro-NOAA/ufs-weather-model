import os
import yaml
from datetime import datetime
from ufs_test_utils import get_testcase, write_logfile, delete_files, machine_check_off

class RegressionLogger:
    def __init__(self):
        self.pathrt = os.getenv('PATHRT')
        self.machine_id = os.getenv('MACHINE_ID')
        self.yaml_file = os.getenv('UFS_TEST_YAML')
        self.keep_rundir = os.getenv('KEEP_RUNDIR') == 'true'
        self.rocoto = os.getenv('ROCOTO') == 'true'
        self.create_baseline = os.getenv('CREATE_BASELINE') == 'true'
        self.compile_only = os.getenv('COMPILE_ONLY') == 'true'
        self.log_path = os.path.join(self.pathrt, f'logs/RegressionTests_{self.machine_id}.log')
        self.test_changes_list = os.path.join(self.pathrt, 'test_changes.list')
        self.run_logs = ""
        self.failed_tests = []
        self.stats = {
            'compile_pass': 0,
            'compile_total': 0,
            'job_total': 0,
            'test_pass': 0,
            'test_fail': 0
        }

    def get_timestamps(self, path):
        timestamps = [datetime.fromtimestamp(os.path.getmtime(os.path.join(path, f)))
                      for f in os.listdir(path)]
        return str(min(timestamps)), str(max(timestamps))

    def log_compile(self, app, config):
        # Implementation of compile log logic (same as original, modularized)
        pass

    def log_tests(self, app, tests, compiler):
        # Implementation of test log logic (same as original, modularized)
        pass

    def summarize(self):
        start, end = self.get_timestamps(os.path.join(self.pathrt, f'logs/log_{self.machine_id}/'))
        start_dt = datetime.strptime(start.split('.')[0], "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end.split('.')[0], "%Y-%m-%d %H:%M:%S")
        elapsed = end_dt - start_dt
        hours, remainder = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        summary = f"""
SYNOPSIS:
Starting Date/Time: {start}
Ending Date/Time: {end}
Total Time: {int(hours):02}h:{int(minutes):02}m:{int(seconds):02}s
Compiles Completed: {self.stats['compile_pass']}/{self.stats['compile_total']}
Tests Completed: {self.stats['test_pass']}/{self.stats['job_total']}
"""
        write_logfile(self.log_path, "a", output=summary)

    def finalize(self):
        if self.stats['test_fail'] == 0:
            delete_files(self.test_changes_list)
            open(self.test_changes_list, 'a').close()
            result = "SUCCESS"
        else:
            with open(self.test_changes_list, 'w') as f:
                for test in self.failed_tests:
                    f.write(f"{test}\n")
            result = "FAILED"

        notes = f"""
NOTES:
A file test_changes.list was generated {'but is empty' if result == 'SUCCESS' else 'with list of all failed tests'}.
Result: {result}
====END OF {self.machine_id} REGRESSION TESTING LOG====
"""
        write_logfile(self.log_path, "a", output=notes)

    def cleanup(self):
        print("Performing Cleanup...")
        delete_files(os.path.join(self.pathrt, 'fv3_*.*x*'))
        delete_files(os.path.join(self.pathrt, 'modules.fv3_*'))
        delete_files(os.path.join(self.pathrt, 'modulefiles/modules.fv3_*'))
        delete_files(os.path.join(self.pathrt, 'keep_tests.tmp'))
        if not self.keep_rundir:
            os.unlink(os.path.join(self.pathrt, 'run_dir'))
        if self.rocoto:
            delete_files(os.path.join(self.pathrt, 'rocoto*'))
        delete_files(os.path.join(self.pathrt, '*_lock.db'))

    def run(self):
        with open(self.yaml_file, 'r') as f:
            rt_yaml = yaml.load(f, Loader=yaml.FullLoader)

        for app, jobs in rt_yaml.items():
            if 'build' in jobs:
                self.log_compile(app, jobs['build'])
            if 'tests' in jobs and not self.compile_only:
                self.log_tests(app, jobs['tests'], jobs['build'][0]['compiler'])

        write_logfile(self.log_path, "a", output=self.run_logs)
        self.summarize()
        self.finalize()
        self.cleanup()

def main_log():
    logger = RegressionLogger()
    logger.run()
    
# Usage
#if __name__ == "__main__":
#    logger = RegressionLogger()
#    logger.run()
