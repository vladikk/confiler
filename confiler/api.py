import codecs
import copy
import os
import ntpath
import json
import logging
from logging import DEBUG
from jinja2 import Template
from core import *

namespace_delimeter = "."
template_file_extension = ".template"
logger = logging.getLogger('confiler.api')

def compile(envs_repo, target_env):
  environments_names = get_env_and_its_ancestors(target_env)
  environments_data = { }
  environments_commands = { }
  for env_name in environments_names:
    env_data = envs_repo.load(env_name)
    environments_data[env_name] = env_data
    environments_commands[env_name] = parse_env_commands(env_name, env_data)
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

def render(envs_repo,
           environment_name, 
           target_path, 
           templates_path,
           template_file_path=None):
  env_data = json.loads(compile(envs_repo, environment_name))
  env_data["values"] = {}
  for key in env_data.keys():
    if key != "values" and isinstance(env_data[key], basestring):
      env_data["values"][key] = env_data[key]
  ensure_folder_exists(target_path)
  if template_file_path:
    render_template(env_data, template_file_path, templates_path, target_path)
  elif templates_path:
    for template_file_path in get_files(templates_path, template_file_extension):
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
    c = f.read()
    if c.startswith(codecs.BOM_UTF8):
      c = c[3:]
    return c

def get_files(path, extension):
  for root, dirs, files in os.walk(path):
    for file in files:
      if file.endswith(extension):
        yield os.path.join(root, file)

def ensure_folder_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)
