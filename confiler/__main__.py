import sys
import argparse
import confiler

def main(args=None):
  """The main routine."""
  if args is None:
    args = sys.argv[1:]

  parser = argparse.ArgumentParser(
    description='Confiler: Configuration files compiler',
    epilog="Example: confiler /myapp/envs dev.vladik /myapp/packages/dev.vladik --templates /myapp/src")
  parser.add_argument("environments", help="Folder containing environments' configurations")
  parser.add_argument("templates", help="Folder containing templates that should be rendered")
  parser.add_argument("environment", help="Name of the targetted environment")
  parser.add_argument("destination", help="Destination folder")
  parser.add_argument("-t", "--template", help="A specific template to render")
  args = parser.parse_args()
  confiler.render(environment_name=args.environment,
                  environments_path=args.environments,
                  target_path=args.destination,
                  templates_path=args.templates,
                  template_file_path=args.template)

if __name__ == "__main__":
    main()
