import os
from behave import *

@given(u'the following config file is set for the {env_name} environment')
def step_impl(context, env_name):
  path = os.path.join(context.work_dir, "%s.env" % env_name)
  with open(path, "w") as env_file:
    env_file.write(context.text)

@when(u'configuration data is compiled for the {env_name} environment')
def step_impl(context, env_name):
  pass

@then(u'the result is the following configuration document')
def step_impl(context):
  pass
