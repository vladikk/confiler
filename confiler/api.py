import os
import ntpath
import json
import logging
from logging import DEBUG
from jinja2 import Template

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
  logger.info("Compiling configuration data for the '%s' environment" % target_env)
  parts = target_env.split(namespace_delimeter)
  result = { }
  for i in range(0, len(parts)):
    env_name = namespace_delimeter.join(parts[0:i+1])
    env = load_env(environments_folder, env_name)
    for key in env.keys():
      val = env[key]
      if not isinstance(val, list):
        if not isinstance(val, basestring):
          raise Exception('Complex objects are not supported (%s). All values should be strings' % key)
        result[key] = val
      else:
        list_actions = [i for i in val if action in i.keys()]
        if any(list_actions):
          if key not in result:
            raise Exception('Attempt to execute action on unexisting collection "%s"' % key)
          if not isinstance(result[key], list):
            raise Exception('Attempt to execute lists action on a non-collection key "%s"' % key)
          if len(list_actions) != len(val):
            raise Exception('Invalid input in the "%s" key - both items and list actions' % key)
          current_value = result[key]
          for a in list_actions:
            if a[action] == append:
              result[key].append(a[item])
            if a[action] == remove:
              for i in get_matching_list_items(current_value, a[matching]):
                result[key].remove(i)
            if a[action] == update:
              for i in get_matching_list_items(current_value, a[matching]):
                for k in a[data].keys():
                  i[k] = a[data][k]
        else: 
          result[key] = val
  return json.dumps(result)

def get_matching_list_items(source, conditions_dict):
  return [i for i in source if all([c in i.keys() and i[c]==conditions_dict[c] for c in conditions_dict.keys()])]

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

def render(environment_file_path=None, 
           target_path=None, 
           template_file_path=None,
           templates_path=None):
  env_data = json.loads(read_file(environment_file_path))
  if template_file_path:
    render_template(env_data, template_file_path, target_path)
  elif templates_path:
    for f in os.listdir(templates_path):
      template_file_path = os.path.join(templates_path, f)
      render_template(env_data, template_file_path, target_path)

def render_template(env_data, template_file_path, target_path):
  template = Template(read_file(template_file_path), trim_blocks=True, lstrip_blocks=True)
  target_file_path = os.path.join(target_path, ntpath.basename(template_file_path))
  rendered = template.render(env_data)
  with open(target_file_path, "w") as result_file:
    result_file.write(rendered.strip())

def read_file(path):
  with open(path, "r") as f:
    return f.read()
