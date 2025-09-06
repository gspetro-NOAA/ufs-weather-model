import argparse
import yaml
from pathlib import Path
from xmlbuilder import RocotoXMLBuilder

def load_manifest(manifest_path):
    with open(manifest_path) as f:
        return yaml.safe_load(f).get("apps", [])

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

def main():
    parser = argparse.ArgumentParser(description="Generate Rocoto XML workflow")
    parser.add_argument("--machine", required=True, help="Target machine name")
    parser.add_argument("--baseline_yaml", required=True, help="Path to baseline.yaml")
    parser.add_argument("--project", default=None, help="Optional project filter")
    parser.add_argument("--manifest", default="app_manifest.yaml", help="Path to app_manifest.yaml")
    parser.add_argument("--yamls_dir", default="tests-yamls/configs/by_app", help="Directory containing app YAMLs")
    parser.add_argument("--output", default="rocoto_workflow.xml", help="Output XML path")

    args = parser.parse_args()

    apps = load_manifest(args.manifest)
    rt_yaml = merge_app_yamls(apps, args.yamls_dir)

    builder = RocotoXMLBuilder(
        machine=args.machine,
        rt_yaml=rt_yaml,
        baseline_yaml=args.baseline_yaml,
        project=args.project
    )
    builder.generate()
    builder.write(args.output)

if __name__ == "__main__":
    main()
