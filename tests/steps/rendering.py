import os
from behave import *
import json
import confiler

templates_folder_name = 'templates'

@given(u'the template file "{template_file_name}" with the following contents')
def step_impl(context, template_file_name):
  context.templates_path = os.path.join(context.work_dir, templates_folder_name)
  ensure_folder_exists(context.templates_path)
  path = os.path.join(context.templates_path, template_file_name)
  with open(path, "w") as env_file:
    env_file.write(context.text)

@when(u'the "{template_file_name}" template is rendered for the {env_name} environment to the "{target_folder}" folder')
def step_impl(context, template_file_name, env_name, target_folder):
  target_path = os.path.join(context.work_dir, target_folder)
  ensure_folder_exists(target_path)
  confiler.render(environment_name=env_name,
                  environments_path=context.work_dir,
                  target_path=target_path,
                  template_file_path=os.path.join(context.templates_path, template_file_name + ".template"))

@when(u'all templates are rendered for the {env_name} environment to the "{target_folder}" folder')
def step_impl(context, env_name, target_folder):
  target_path = os.path.join(context.work_dir, target_folder)
  ensure_folder_exists(target_path)
  env_data = os.path.join(context.work_dir, env_name + '.env')
  confiler.render(environment_name=env_name,
                  environments_path=context.work_dir,
                  target_path=target_path,
                  templates_path=context.templates_path)

@then(u'the "{rel_file_path}" file has the following contents')
def step_impl(context, rel_file_path):
  file_path = os.path.join(context.work_dir, rel_file_path)
  with open(file_path, "r") as result_file:
    result = result_file.read()
  assert result == context.text, '%s != %s' % (result, context.text)

def ensure_folder_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)

