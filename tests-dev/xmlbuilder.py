import xml.etree.ElementTree as ET
import yaml
from typing import Optional


class RocotoXMLBuilder:
    def __init__(self, machine: str, rt_yaml: str, baseline_yaml: str, project: Optional[str] = None):
        self.machine = machine
        self.project = project
        self.rt_config = yaml.safe_load(open(rt_yaml))
        self.baseline_config = yaml.safe_load(open(baseline_yaml))
        self.machine_config = self.baseline_config.get(machine, {})
        self.root = ET.Element("workflow", attrib={
            "scheduler": self.machine_config.get("SCHEDULER", "slurm"),
            "taskthrottle": "10"
        })

    def build_doctype(self) -> str:
        lines = ["<!DOCTYPE workflow ["]
        for key, value in self.machine_config.items():
            if key.isupper() and value:
                lines.append(f'  <!ENTITY {key} "{value}">')
        lines.append("]>")
        return "\n".join(lines)

    def add_cycledef(self):
        ET.SubElement(self.root, "cycledef").text = "197001010000 197001010000 01:00:00"

    def add_compile_task(self, app: str, compiler: str, option: str):
        metatask = ET.SubElement(self.root, "metatask", {"name": f"compile_{app}"})
        ET.SubElement(metatask, "var", {"name": "zero"}).text = "0"
        task = ET.SubElement(metatask, "task", {"name": f"compile_{app}"})
        ET.SubElement(task, "command").text = f"&PATHRT;/compile.sh &PATHRT; &RUNDIR_ROOT; \"{option}\" {app} 2>&1 | tee &LOG;/compile_{app}.log"
        ET.SubElement(task, "jobname").text = f"compile_{app}"
        ET.SubElement(task, "queue").text = "&COMPILE_QUEUE;"
        ET.SubElement(task, "partition").text = "&PARTITION;"
        ET.SubElement(task, "walltime").text = "01:00:00"

    def add_test_task(self, test_name: str, app: str, compiler: str, dependency: Optional[str] = None):
        task_id = f"{test_name}_{compiler}"
        task = ET.SubElement(self.root, "task", {"name": task_id})
        ET.SubElement(task, "command").text = f"&PATHRT;/run_test.sh &PATHRT; &RUNDIR_ROOT; {test_name} {compiler} 2>&1 | tee &LOG;/{task_id}.log"
        ET.SubElement(task, "jobname").text = task_id
        ET.SubElement(task, "queue").text = "&QUEUE;"
        ET.SubElement(task, "partition").text = "&PARTITION;"
        ET.SubElement(task, "walltime").text = "01:00:00"
        if dependency:
            dep = ET.SubElement(task, "dependency", {"type": "task"})
            ET.SubElement(dep, "task").text = f"{dependency}_{compiler}"

    def generate(self):
        self.add_cycledef()
        for app, config in self.rt_config.items():
            build = config.get("build", {})
            compiler = build.get("compiler")
            option = build.get("option")
            turnoff = build.get("turnoff", [])
            turnon = build.get("turnon", [])

            if self.machine in turnoff:
                continue
            if turnon and self.machine not in turnon:
                continue

            self.add_compile_task(app, compiler, option)

            for test in config.get("tests", []):
                for test_name, test_cfg in test.items():
                    if self.machine in test_cfg.get("turnoff", []):
                        continue
                    if "turnon" in test_cfg and self.machine not in test_cfg["turnon"]:
                        continue
                    if self.project and test_cfg.get("project") != self.project:
                        continue

                    dep = test_cfg.get("dependency")
                    self.add_test_task(test_name, app, compiler, dep)

    def write(self, filename: str):
        self._indent(self.root)
        xml_body = ET.tostring(self.root, encoding="unicode")
        with open(filename, "w") as f:
            f.write('<?xml version="1.0"?>\n')
            f.write(self.build_doctype() + "\n")
            f.write(xml_body + "\n</workflow>\n")

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
