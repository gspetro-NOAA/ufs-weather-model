import yaml
import xml.etree.ElementTree as ET
from typing import Optional

class RocotoXMLBuilder:
    def __init__(self, machine: str, rt_yaml, baseline_yaml: str, project: Optional[str] = None):
        self.machine = machine
        self.project = project

        # Accept either a dict or a file path for rt_yaml
        if isinstance(rt_yaml, dict):
            self.rt_config = rt_yaml
        else:
            with open(rt_yaml) as f:
                self.rt_config = yaml.safe_load(f)

        with open(baseline_yaml) as f:
            self.baseline_config = yaml.safe_load(f)

        self.root = ET.Element("workflow")
        self._add_cycledef()

    def _add_cycledef(self):
        cycledef = ET.SubElement(self.root, "cycledef", name="forecast", start="2025010100", end="2025123100", interval="06:00:00")

    def _add_compile_task(self, key, build):
        task_name = f"build_{key}"
        task = ET.SubElement(self.root, "task", name=task_name)
        command = f"./build.sh --compiler={build.get('compiler')} {build.get('option')}"
        ET.SubElement(task, "command").text = command

        if build.get("turnoff"):
            ET.SubElement(task, "turnoff").text = ",".join(build["turnoff"])

    def _add_test_task(self, test_name, test_cfg, build_key):
        task = ET.SubElement(self.root, "task", name=test_name)
        ET.SubElement(task, "command").text = f"./run_test.sh {test_name}"

        # Link to build task
        ET.SubElement(task, "dependency").text = f"build_{build_key}"

        # Optional metadata
        if test_cfg.get("dependency"):
            ET.SubElement(task, "dependency").text = test_cfg["dependency"]

        if test_cfg.get("project"):
            ET.SubElement(task, "project").text = ",".join(test_cfg["project"])

        if test_cfg.get("turnon"):
            ET.SubElement(task, "turnon").text = ",".join(test_cfg["turnon"])

        if test_cfg.get("turnoff"):
            ET.SubElement(task, "turnoff").text = ",".join(test_cfg["turnoff"])

    def generate(self):
        for key, block in self.rt_config.items():
            build = block.get("build", {})
            tests = block.get("tests", [])

            self._add_compile_task(key, build)

            for test in tests:
                for test_name, test_cfg in test.items():
                    # Filter by project if specified
                    if self.project:
                        if "project" not in test_cfg or self.project not in test_cfg["project"]:
                            continue
                    self._add_test_task(test_name, test_cfg, key)

    def write(self, output_path: str):
        self._indent(self.root)
        tree = ET.ElementTree(self.root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

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
