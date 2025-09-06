import argparse
from xmlbuilder import RocotoXMLBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate Rocoto XML workflow for UFS regression tests.")
    parser.add_argument("--machine", required=True, help="Target machine name (e.g., hera, orion)")
    parser.add_argument("--project", help="Filter tests by project name (e.g., global, chem)")
    parser.add_argument("--rt_yaml", default="tests-dev/rt.yaml", help="Path to rt.yaml")
    parser.add_argument("--baseline_yaml", default="tests-dev/baseline_setup.yaml", help="Path to baseline_setup.yaml")
    parser.add_argument("--output", default="tests-dev/rocoto_workflow.xml", help="Output XML file path")

    args = parser.parse_args()

    builder = RocotoXMLBuilder(
        machine=args.machine,
        rt_yaml=args.rt_yaml,
        baseline_yaml=args.baseline_yaml,
        project=args.project
    )
    builder.generate()
    builder.write(args.output)

if __name__ == "__main__":
    main()
