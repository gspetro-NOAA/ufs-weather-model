#python build_rocotoxml.py \
#  --machine orion \
#  --baseline_yaml baseline_setup.yaml \
#  --changes_list test_changes.list \
#  --yamls_dir tests-yamls/configs/by_app \
#  --output workflow.xml

python build_rocotoxml.py \
  --machine orion \
  --user_yaml ufs_test.new.yaml \
  --baseline_yaml baseline_setup.yaml \
  --output workflow.xml
