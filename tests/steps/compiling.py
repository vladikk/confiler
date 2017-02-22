from behave import *

@given(u'the following config file is set for the {env_name} environment')
def step_impl(context, env_name):
  pass

@when(u'configuration data is compiled for the {env_name} environment')
def step_impl(context, env_name):
  pass

@then(u'the result is the following configuration document')
def step_impl(context):
  assert context.execution_id == 1234444 
