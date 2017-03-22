def get_matching_list_items(source, conditions_dict):
  return [i for i in source if all([c in i.keys() and i[c]==conditions_dict[c] for c in conditions_dict.keys()])]

class SetValue(object):
  def __init__(self, key, value, namespace):
    self.key = key
    self.value = value
    self.namespace = namespace
  
  def execute(self, data):
    data[self.key] = self.value


class SetCollection(object):
  def __init__(self, name, items, namespace):
    self.name = name
    self.items = items
    self.namespace = namespace

  def execute(self, data):
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
      for k in self.new_data.keys():
        i[k] = self.new_data[k]

