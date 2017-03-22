import logging
import json
import os

env_file_extension = "env"

logger = logging.getLogger('confiler.repositories')

class FSEnvsRepository(object):
  def __init__(self, path):
    self.path = path

  def load(self, env_name):
    logger.info("Loading data file for the '%s' environment" % env_name)
    file_name = '%s.%s' % (env_name, env_file_extension)
    file_path = os.path.join(self.path, file_name)
    logger.info("Loading data from file %s" % file_path)
    if not os.path.exists(file_path):
      return { }
    with open(file_path, "r") as json_file:
      env_json = json_file.read()
      return json.loads(env_json) 
