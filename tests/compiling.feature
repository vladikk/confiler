Feature: Compiling configuration data
  In order to support efficient management of configuration values across
  multiple environments(dev, qa, staging, prod + multi-tenant)
  I want to be able to specify configuration values in multiple namespaces,
  and to be able to merge them into a single configuration that will
  inherit and override values from underlying namespaces.

  Scenario: A value that was set will be emitted after compilation
    Given the following config file is set for the dev environment
       """
       {
         "threshold": "10"
       }
       """
     When configuration data is compiled for the dev environment
     Then the result is the following configuration document
       """
       {
         "threshold": "10"
       }
       """
    
  Scenario: A child environment's values  override the values set in its parent
    Given the following config file is set for the dev environment
       """
       {
         "threshold": "10"
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "threshold": "5"
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "threshold": "5"
       }
       """

  Scenario: Configuration can be compiled even if one of the parents is missing
    Given the following config file is set for the dev.vladik environment
       """
       {
         "threshold": "10"
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "threshold": "10"
       }
       """

  Scenario: Configuration can be compiled even if the child is missing
    Given the following config file is set for the dev environment
       """
       {
         "threshold": "10"
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "threshold": "10"
       }
       """

  Scenario: Configuration files support collections
    Given the following config file is set for the dev environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database", "address": "192.168.1.101" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """
     When configuration data is compiled for the dev environment
     Then the result is the following configuration document
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database", "address": "192.168.1.101" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """

  Scenario: Collection can be replace in a child environment
    Given the following config file is set for the dev environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "10.0.0.1" },
           { "name": "database", "address": "10.0.0.2" }
         ]
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database", "address": "192.168.1.101" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database", "address": "192.168.1.101" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """

  Scenario: A child environment can delete items from its parent's collection
    Given the following config file is set for the dev environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database-m", "address": "192.168.1.111" },
           { "name": "database-s1", "address": "192.168.1.112" },
           { "name": "database-s2", "address": "192.168.1.113" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "$action": "remove", "$matching": { "name": "database-s1" } },
           { "$action": "remove", "$matching": { "name": "database-s2" } }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database-m", "address": "192.168.1.111" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """

  Scenario: A child environment can append items to its parent's collection
    Given the following config file is set for the dev environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database-m", "address": "192.168.1.111" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "$action": "append", "$item": { "name": "database-s1", "address": "192.168.1.112" } },
           { "$action": "append", "$item": { "name": "database-s2", "address": "192.168.1.113" } }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database-m", "address": "192.168.1.111" },
           { "name": "app-server", "address": "192.168.1.103" },
           { "name": "database-s1", "address": "192.168.1.112" },
           { "name": "database-s2", "address": "192.168.1.113" }
         ]
       }
       """

  Scenario: A child environment can update values in its parent's collection
    Given the following config file is set for the dev environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "database-m", "address": "192.168.1.111" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "$action": "update", "$matching": { "name": "web-server" }, "$data": { "address": "10.0.1.100" } },
           { "$action": "update", "$matching": { "name": "database-m" }, "$data": { "address": "10.0.1.101" } },
           { "$action": "update", "$matching": { "name": "app-server" }, "$data": { "address": "10.0.1.102" } }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the result is the following configuration document
       """
       {
         "hosts": [
           { "name": "web-server", "address": "10.0.1.100" },
           { "name": "database-m", "address": "10.0.1.101" },
           { "name": "app-server", "address": "10.0.1.102" }
         ]
       }
       """

  Scenario: List operations without base list
    Given the following config file is set for the dev environment
       """
       {
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "$action": "append", "$item": { "name": "database-s1", "address": "192.168.1.112" } },
           { "$action": "append", "$item": { "name": "database-s2", "address": "192.168.1.113" } }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the error is returned: Attempt to execute action on unexisting collection "hosts"

  Scenario: List actions on a non-collection value
    Given the following config file is set for the dev environment
       """
       {
         "hosts": "a primitive value"
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "$action": "append", "$item": { "name": "database-s1", "address": "192.168.1.112" } },
           { "$action": "append", "$item": { "name": "database-s2", "address": "192.168.1.113" } }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the error is returned: Attempt to execute lists action on a non-collection key "hosts"

  Scenario: List operations and items in the same value
    Given the following config file is set for the dev environment
       """
       {
         "hosts": [
           { "name": "web-server", "address": "192.168.1.100" },
           { "name": "app-server", "address": "192.168.1.103" }
         ]
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "hosts": [
           { "$action": "append", "$item": { "name": "database-s1", "address": "192.168.1.112" } },
           { "$action": "append", "$item": { "name": "database-s2", "address": "192.168.1.113" } },
           { "name": "database-m", "address": "192.168.1.111" }
         ]
       }
       """
     When configuration data is compiled for the dev.vladik environment
     Then the error is returned: Invalid input in the "hosts" key - both items and list actions

  Scenario: Complex object are not supported (yet)
    Given the following config file is set for the dev environment
       """
       {
         "hosts": {
           "host1": "10.0.0.1",
           "host2": "10.0.0.2",
           "host3": "10.0.0.3"
         }
       }
       """
     When configuration data is compiled for the dev environment
     Then the error is returned: Complex objects are not supported (hosts). All values should be strings 

  @wip
  Scenario: Support complex objects - nested objects except nested collections
