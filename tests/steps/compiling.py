import os
from behave import *
import json
import confiler

@given(u'the following config file is set for the {env_name} environment')
def step_impl(context, env_name):
  path = os.path.join(context.work_dir, "%s.env" % env_name)
  with open(path, "w") as env_file:
    env_file.write(context.text)

@when(u'configuration data is compiled for the {env_name} environment')
def step_impl(context, env_name):
  context.result_json = confiler.compile(context.work_dir, env_name)

@then(u'the result is the following configuration document')
def step_impl(context):
  result = json.loads(context.result_json)
  expected = json.loads(context.text)
  assert ordered(result) == ordered(expected)

def ordered(obj):
  if isinstance(obj, dict):
    return sorted((k, ordered(v)) for k, v in obj.items())
  if isinstance(obj, list):
    return sorted(ordered(x) for x in obj)
  else:
    return obj
