import copy
import os
import ntpath
import json
import logging
from logging import DEBUG
from jinja2 import Template
from core import *

namespace_delimeter = "."
env_file_extension = "env"
action = "$action"
matching = "$matching"
item = "$item"
data = "$data"
remove = "remove"
append = "append"
update = "update"
logger = logging.getLogger('api')

def compile(environments_folder, target_env):
  environments_names = get_env_and_its_ancestors(target_env)
  environments_data = { }
  environments_commands = { }
  for env_name in environments_names:
    env_data = load_env(environments_folder, env_name)
    environments_data[env_name] = env_data
    environments_commands[env_name] = parse_env_data(env_name, env_data)
  result = {}
  for env in environments_names:
    logger.info("Applying environment '%s' with %s commands" % (env, len(environments_commands[env])))
    for cmd in environments_commands[env]:
      cmd.execute(result)
  return json.dumps(result)

def get_env_and_its_ancestors(env):
  parts = env.split(namespace_delimeter)
  result = []
  for i in range(0, len(parts)):
    result.append(namespace_delimeter.join(parts[0:i+1]))
  return result

def load_env(environments_folder, env_name):
  logger.info("Loading data file for the '%s' environment" % env_name)
  file_name = '%s.%s' % (env_name, env_file_extension)
  file_path = os.path.join(environments_folder, file_name)
  logger.info("Loading data from file %s" % file_path)
  if not os.path.exists(file_path):
    return { }
  with open(file_path, "r") as json_file:
    env_json = json_file.read()
    return json.loads(env_json)

def parse_env_data(env_name, env_data):
  commands = []
  for key in env_data.keys():
    val = env_data[key]
    if not isinstance(val, list):
      if not isinstance(val, basestring):
        raise Exception('Complex objects are not supported (%s). All values should be strings' % key)
      commands.append(SetValue(key, val, env_name))
    else:
      list_actions = [i for i in val if action in i.keys()]
      if not any(list_actions):
        commands.append(SetCollection(key, val, env_name))
      else:
        if len(list_actions) != len(val):
          raise Exception('Invalid input in the "%s" key - both items and list actions' % key)
        for a in list_actions:
          if a[action] == append:
            commands.append(AppendItemToCollection(key, a[item], env_name))
          if a[action] == remove:
            commands.append(RemoveItemFromCollection(key, a[matching], env_name))
          if a[action] == update:
            commands.append(UpdateItemInCollection(key, a[matching], a[data], env_name))
  return commands

def render(environments_path,
           environment_name, 
           target_path, 
           templates_path,
           template_file_path=None):
  env_data = json.loads(compile(environments_path, environment_name))
  env_data["values"] = {}
  for key in env_data.keys():
    if key != "values" and isinstance(env_data[key], basestring):
      env_data["values"][key] = env_data[key]
  ensure_folder_exists(target_path)
  if template_file_path:
    render_template(env_data, template_file_path, templates_path, target_path)
  elif templates_path:
    for template_file_path in get_files(templates_path, ".template"):
      render_template(env_data, template_file_path, templates_path, target_path)

def render_template(env_data, template_file_path, templates_root_path, target_path):
  logger.info("Rendering template file %s to folder %s. Data: %s" 
    % (template_file_path, target_path, json.dumps(env_data)))
  relative_path = os.path.relpath(template_file_path, templates_root_path)
  template = Template(read_file(template_file_path), trim_blocks=True, lstrip_blocks=True)
  target_file_path = os.path.join(target_path, 
                                  os.path.dirname(relative_path),
                                  os.path.splitext(ntpath.basename(template_file_path))[0])
  logger.info("Target file path: %s" % target_file_path)
  rendered = template.render(env_data)
  ensure_folder_exists(os.path.dirname(target_file_path))
  with open(target_file_path, "w") as result_file:
    result_file.write(rendered.strip())

def read_file(path):
  with open(path, "r") as f:
    return f.read()

def get_files(path, extension):
  for root, dirs, files in os.walk(path):
    for file in files:
      if file.endswith(extension):
        yield os.path.join(root, file)

def ensure_folder_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)
