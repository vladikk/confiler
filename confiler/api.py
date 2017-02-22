import os
import json

namespace_delimeter = "."
env_file_extension = ".env"

def compile(environments_folder, target_env):
  parts = target_env.split(namespace_delimeter)
  indexes = range(1, len(parts) + 1)
  indexes.reverse()
  for i in indexes:
    namespace = namespace_delimeter.join(parts[0, i])
    env = load_env(environments_folder, env_name)

def load_env(environments_folder, env_name):
  file_name = '%s.%s' % (env_name, env_file_extension)
  file_path = os.path.join(environments_folder, file_name)
  if not os.path.exists(file_path):
    return { }
  with (file_path, "w") as json_file:
    env_json = json_file.read()
    return json.loads(env_json)
