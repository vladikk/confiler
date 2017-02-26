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
  parser.add_argument("environment", help="Name of the targetted environment")
  parser.add_argument("destination", help="Destination folder")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-t", "--template", help="Template file that should be rendered")
  group.add_argument("-s", "--templates", help="Templates folder that should be rendered")
  args = parser.parse_args()
  if not (args.template or args.templates):
    parser.error('No template was set. Please add -t/--template or -s/--templates')
  confiler.render(environment_name=args.environment,
                  environments_path=args.environments,
                  target_path=args.destination,
                  templates_path=args.templates,
                  template_file_path=args.template)

if __name__ == "__main__":
    main()
