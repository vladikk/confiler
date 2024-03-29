import os
import uuid
import shutil
from confiler.repos import FSEnvsRepository

def before_scenario(context, scenario):
  execution_id = uuid.uuid4()
  work_dir = os.path.join("temp", str(execution_id))
  if not os.path.exists(work_dir):
    os.makedirs(work_dir)
  context.work_dir = work_dir
  context.envs_repo = FSEnvsRepository(work_dir)

def after_scenario(context, scenario):
  shutil.rmtree(context.work_dir) 
