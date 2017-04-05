import sys
import argparse
import confiler
import logging
from confiler.repos import FSEnvsRepository

def main(args=None):
  """The main routine."""
  if args is None:
    args = sys.argv[1:]

  parser = argparse.ArgumentParser(
    description='Confiler: Configuration files compiler',
    epilog="Example: confiler /myapp/envs /myapp/src dev.vladik /myapp/packages/dev.vladik")
  parser.add_argument("environments", help="Folder containing environments' configurations")
  parser.add_argument("templates", help="Folder containing templates that should be rendered")
  parser.add_argument("environment", help="Name of the targetted environment")
  parser.add_argument("destination", help="Destination folder")
  parser.add_argument("-t", "--template", help="A specific template to render")
  parser.add_argument("-l", "--log", help="Log file's path")
  args = parser.parse_args()
  
  if args.log:
    logger = logging.getLogger('confiler')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(args.log)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

  confiler.render(envs_repo=FSEnvsRepository(args.environments),
                  environment_name=args.environment,
                  target_path=args.destination,
                  templates_path=args.templates,
                  template_file_path=args.template)

if __name__ == "__main__":
    main()
