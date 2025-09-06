import yaml
import xml.etree.ElementTree as ET
from typing import Optional
import os
import re

def resolve_env_vars(value: str) -> str:
    pattern = re.compile(r"\$\{(\w+)\}")
    return pattern.sub(lambda m: os.environ.get(m.group(1), m.group(0)), value)

class RocotoXMLBuilder:
    def __init__(self, machine: str, rt_yaml, baseline_yaml: str, project: Optional[str] = None, filter_tests: Optional[set] = None):
        self.machine = machine
        self.project = project
        self.filter_tests = filter_tests

        self.rt_config = rt_yaml if isinstance(rt_yaml, dict) else yaml.safe_load(open(rt_yaml))
        self.baseline_config = yaml.safe_load(open(baseline_yaml))

        self.root = ET.Element("workflow", attrib={
            "realtime": "F",
            "scheduler": "slurm",
            "taskthrottle": "10"
        })
        self._add_cycledef()
        self._add_log()

    def _add_cycledef(self):
        ET.SubElement(self.root, "cycledef", name="forecast", start="2025010100", end="2025123100", interval="06:00:00")

    def _add_log(self):
        ET.SubElement(self.root, "log").text = "&LOG;"

    def _add_compile_task(self, key, build):
        compiler = build.get("compiler", "unknown").lower()
        option = build.get("option", "")
        app = option.split("-DAPP=")[-1].split()[0].lower() if "-DAPP=" in option else key.split("_")[0]
        task_name = f"compile_{app}_{compiler}"

        task = ET.SubElement(self.root, "task", name=task_name)
        cmd = f'bash -c "set -xe -o pipefail; ./build.sh --compiler={compiler} {option} |& tee &LOG;/${{TASK}}.log"'
        ET.SubElement(task, "command").text = cmd
        ET.SubElement(task, "jobname").text = task_name
        ET.SubElement(task, "account").text = "GFS-DEV"
        ET.SubElement(task, "queue").text = "batch"
        ET.SubElement(task, "partition").text = self.machine
        ET.SubElement(task, "nodes").text = "1"
        ET.SubElement(task, "walltime").text = "00:30:00"
        ET.SubElement(task, "join").text = "yes"
        ET.SubElement(task, "maxtries").text = "2"

    def _add_test_metatask(self, key, tests):
        build = self.rt_config[key]["build"]
        compiler = build.get("compiler", "unknown").lower()
        option = build.get("option", "")
        app = option.split("-DAPP=")[-1].split()[0].lower() if "-DAPP=" in option else key.split("_")[0]
        compile_task = f"compile_{app}_{compiler}"
        metatask = ET.SubElement(self.root, "metatask", name=f"{compile_task}_tasks")

        for test in tests:
            for test_name, test_cfg in test.items():
                if self.project and ("project" not in test_cfg or self.project not in test_cfg["project"]):
                    continue
                if self.filter_tests and test_name not in self.filter_tests:
                    continue

                ET.SubElement(metatask, "var", name="TEST", value=test_name)
                task = ET.SubElement(metatask, "task", name=test_name)
                cmd = f'bash -c "set -xe -o pipefail; ./run_test.sh $TEST |& tee &LOG;/${{TASK}}.log"'
                ET.SubElement(task, "command").text = cmd

                dep = ET.SubElement(task, "dependency")
                ET.SubElement(dep, "taskdep").text = compile_task

                ET.SubElement(task, "jobname").text = test_name
                ET.SubElement(task, "account").text = "GFS-DEV"
                ET.SubElement(task, "queue").text = "batch"
                ET.SubElement(task, "partition").text = self.machine
                ET.SubElement(task, "nodes").text = "1"
                ET.SubElement(task, "walltime").text = "00:30:00"
                ET.SubElement(task, "join").text = "yes"
                ET.SubElement(task, "maxtries").text = "2"

                if test_cfg.get("turnon"):
                    ET.SubElement(task, "turnon").text = ",".join(test_cfg["turnon"])
                if test_cfg.get("turnoff"):
                    ET.SubElement(task, "turnoff").text = ",".join(test_cfg["turnoff"])
                if test_cfg.get("project"):
                    ET.SubElement(task, "project").text = ",".join(test_cfg["project"])

    def generate(self):
        for key, block in self.rt_config.items():
            self._add_compile_task(key, block.get("build", {}))
            self._add_test_metatask(key, block.get("tests", []))

    def write(self, output_path: str):
        machine_config = self.baseline_config.get(self.machine, {})
        entity_defaults = {
            "LOG": "&PATHRT;/logs",
            "RUNDIR_ROOT": "&PATHRT;/rundir",
            "NEW_BASELINE": f"{machine_config.get('STMP', '/tmp')}/FV3_RT/REGRESSION_TEST"
        }

        entities = {**machine_config, **entity_defaults}
        resolved_entities = {k: resolve_env_vars(v) for k, v in entities.items() if v}
        entity_lines = [f'  <!ENTITY {k} "{v}">' for k, v in resolved_entities.items()]
        doctype = "<!DOCTYPE workflow [\n" + "\n".join(entity_lines) + "\n]>"

        self._indent(self.root)
        xml_str = ET.tostring(self.root, encoding="unicode")
        with open(output_path, "w") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(doctype + "\n")
            f.write(xml_str)

    def _indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                self._indent(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
