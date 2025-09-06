import argparse
import yaml
from pathlib import Path
from xmlbuilder import RocotoXMLBuilder

def parse_test_changes(path):
    test_map = {}
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            test_name, compiler = parts
            key = f"{test_name}_{compiler}"
            app = test_name.split("_")[0]
            test_map.setdefault((app, compiler), []).append(key)
    return test_map

def load_manifest(manifest_path):
    with open(manifest_path) as f:
        return yaml.safe_load(f).get("apps", [])

def load_baseline_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def load_all_app_yamls(yaml_dir):
    merged = {}
    for path in Path(yaml_dir).glob("*.yaml"):
        with open(path) as f:
            merged.update(yaml.safe_load(f))
    return merged

def merge_app_yamls(apps, base_dir):
    merged = {}
    for app in apps:
        app_path = Path(base_dir) / f"{app}.yaml"
        if app_path.exists():
            with open(app_path) as f:
                merged.update(yaml.safe_load(f))
        else:
            print(f"⚠️ Missing app YAML: {app_path}")
    return merged

def filter_yaml_by_test_map(rt_yaml, test_map):
    filtered = {}
    for key, block in rt_yaml.items():
        build = block.get("build", {})
        compiler = build.get("compiler", "unknown").lower()
        option = build.get("option", "")
        app = option.split("-DAPP=")[-1].split()[0].lower() if "-DAPP=" in option else key.split("_")[0]

        matched_tests = []
        for test in block.get("tests", []):
            for test_name in test:
                if (app, compiler) in test_map and test_name in test_map[(app, compiler)]:
                    matched_tests.append(test)

        if matched_tests:
            filtered[key] = {
                "build": build,
                "tests": matched_tests
            }
    return filtered

def main():
    parser = argparse.ArgumentParser(description="Generate Rocoto XML workflow")
    parser.add_argument("--machine", required=True)
    parser.add_argument("--baseline_yaml", default="baseline_setup.yaml")
    parser.add_argument("--yamls_dir", default="tests-yamls/configs/by_app")
    parser.add_argument("--manifest", default="app_manifest.yaml")
    parser.add_argument("--changes_list", default=None)
    parser.add_argument("--output", default="workflow.xml")
    parser.add_argument("--project", default=None)

    args = parser.parse_args()
    baseline_config = load_baseline_config(args.baseline_yaml)

    if args.machine not in baseline_config:
        raise ValueError(f"❌ Machine '{args.machine}' not found in baseline setup.")

    if args.changes_list:
        test_map = parse_test_changes(args.changes_list)
        full_yaml = load_all_app_yamls(args.yamls_dir)
        rt_yaml = filter_yaml_by_test_map(full_yaml, test_map)
        filter_tests = {test for tests in test_map.values() for test in tests}
    else:
        apps = load_manifest(args.manifest)
        rt_yaml = merge_app_yamls(apps, args.yamls_dir)
        filter_tests = None

    builder = RocotoXMLBuilder(
        machine=args.machine,
        rt_yaml=rt_yaml,
        baseline_yaml=args.baseline_yaml,
        project=args.project,
        filter_tests=filter_tests
    )
    builder.generate()
    builder.write(args.output)

if __name__ == "__main__":
    main()
