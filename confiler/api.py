import os
import json
import logging
from logging import DEBUG

namespace_delimeter = "."
env_file_extension = "env"
logger = logging.getLogger('api')

def compile(environments_folder, target_env):
  logger.info("Compiling configuration data for the '%s' environment" % target_env)
  parts = target_env.split(namespace_delimeter)
  result = { }
  for i in range(0, len(parts)):
    env_name = namespace_delimeter.join(parts[0:i+1])
    env = load_env(environments_folder, env_name)
    for key in env.keys():
      result[key] = env[key]
  return json.dumps(result)

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
