import os
import uuid

def before_scenario(context, scenario):
  execution_id = uuid.uuid4()
  work_dir = os.path.join("temp", str(execution_id))
  if not os.path.exists(work_dir):
    os.makedirs(work_dir)
  context.work_dir = work_dir
