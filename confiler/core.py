import json
import logging

action = "$action"
matching = "$matching"
item = "$item"
data = "$data"
remove = "remove"
append = "append"
update = "update"

logger = logging.getLogger('confiler.core')

def get_matching_list_items(source, conditions_dict):
  return [i for i in source if all([c in i.keys() and i[c]==conditions_dict[c] for c in conditions_dict.keys()])]

class SetValue(object):
  def __init__(self, key, value, namespace):
    self.key = key
    self.value = value
    self.namespace = namespace
  
  def execute(self, data):
    if self.key in data.keys():
      logger.debug("%s: Replacing value of '%s': '%s' => '%s'" % 
                   (self.namespace, self.key, data[self.key], self.value))
    else:
      logger.debug("%s: Initializeing value of '%s' to %s" % 
                   (self.namespace, self.key, self.value))

    data[self.key] = self.value


class SetCollection(object):
  def __init__(self, name, items, namespace):
    self.name = name
    self.items = items
    self.namespace = namespace

  def execute(self, data):
    if self.name in data.keys():
      logger.debug("%s: Replacing collection '%s': '%s' => '%s'" % 
                   (self.namespace, self.name, 
                    json.dumps(data[self.name]), json.dumps(self.items)))
    else:
      logger.debug("%s: Initializing collection '%s': %s" % 
                   (self.namespace, self.name, json.dumps(self.items)))
    data[self.name] = self.items


class CollectionCommand(object):
  def execute(self, data):
    if self.name not in data.keys():
      raise Exception('Attempt to execute action on unexisting collection "%s"' % self.name)
    if not isinstance(data[self.name], list):
      raise Exception('Attempt to execute lists action on a non-collection key "%s"' % self.name) 


class AppendItemToCollection(CollectionCommand):
  def __init__(self, name, item, namespace):
    self.name = name
    self.item = item
    self.namespace = namespace

  def execute(self, data):
    super(AppendItemToCollection, self).execute(data)
    logger.debug("%s: Appending item to collection '%s': %s" % 
                 (self.namespace, self.name, json.dumps(self.item)))
    data[self.name].append(self.item)


class RemoveItemFromCollection(CollectionCommand):
  def __init__(self, name, conditions, namespace):
    self.name = name
    self.conditions = conditions
    self.namespace = namespace

  def execute(self, data):
    super(RemoveItemFromCollection, self).execute(data)
    items = get_matching_list_items(data[self.name], self.conditions)
    for i in items:
      logger.debug("%s: Removing item from collection '%s': %s" % 
                 (self.namespace, self.name, json.dumps(i)))
      data[self.name].remove(i)


class UpdateItemInCollection(CollectionCommand):
  def __init__(self, name, conditions, new_data, namespace):
    self.name = name
    self.conditions = conditions
    self.new_data = new_data
    self.namespace = namespace

  def execute(self, data):
    super(UpdateItemInCollection, self).execute(data)
    items = get_matching_list_items(data[self.name], self.conditions)
    for i in items:
      logger.debug("%s: Updating item in collection '%s': %s" % 
                   (self.namespace, self.name, json.dumps(i)))
      for k in self.new_data.keys():
        i[k] = self.new_data[k]
      logger.debug("%s: Updated item in collection '%s': %s" % 
                   (self.namespace, self.name, json.dumps(i)))

def parse_env_commands(env_name, env_data):
  commands = []
  for key in env_data.keys():
    val = env_data[key]
    if not isinstance(val, list):
      if not isinstance(val, basestring):
        raise Exception('Complex objects are not supported (%s). All values should be strings' % key)
      commands.append(SetValue(key, val, env_name))
    else:
      list_actions = [i for i in val if action in i.keys()]
      if not any(list_actions):
        commands.append(SetCollection(key, val, env_name))
      else:
        if len(list_actions) != len(val):
          raise Exception('Invalid input in the "%s" key - both items and list actions' % key)
        for a in list_actions:
          if a[action] == append:
            commands.append(AppendItemToCollection(key, a[item], env_name))
          if a[action] == remove:
            commands.append(RemoveItemFromCollection(key, a[matching], env_name))
          if a[action] == update:
            commands.append(UpdateItemInCollection(key, a[matching], a[data], env_name))
  return commands
