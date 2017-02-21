Feature: Compiling configuration data
  In order to support efficient management of configuration values across
  multiple environments(dev, qa, staging, prod + multi-tenant)
  I want to be able to specify configuration values in multiple namespaces,
  and to be able to merge them into a single configuration that will
  inherit and override values from underlying namespaces.

  Scenario: A value that was set, will be emitted after merging
    Given "threshold" is set to "10" for the dev environment
     When configuration data is compiled for the dev environment
     Then "threshold" is "10"
    
  Scenario: A child environment's values  override the values set in its parent
    Given "threshold" is set to "10" for the dev environment
      And "threshold" is set to "5" for the dev.vladik environment
     When configuration data is compiled for the dev.vladik environment
     Then "threshold" is "5"

  Scenario: Configuration cannot be compiled for parent environments
    Given "threshold" is set to "10" for the dev environment
      And "threshold" is set to "5" for the dev.vladik environment
     When configuration data is compiled for the dev environment
     Then an error is raised

  Scenario: Configuration can be compiled even if one of the parents is missing
    Given "threshold" is set to "5" for the dev.vladik environment
     When configuration data is compiled for the dev.vladik environment
     Then "threshold" is "5"

  Scenario: Configuration can be compiled even if the child is missing
    Given "threshold" is set to "5" for the dev environment
     When configuration data is compiled for the dev.vladik environment
     Then "threshold" is "5"

  Scenario: Configuration files support collections
    Given "hosts" is set to the following values for the dev environment
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database   | 192.168.1.101 |
       | app-server | 192.168.1.103 |
     When configuration data is compiled for the dev environment
     Then "hosts" holds the following values
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database   | 192.168.1.101 |
       | app-server | 192.168.1.103 |

  Scenario: Collection can be replace in a child environment
    Given "hosts" is set to the following values for the dev environment
       | name       | address  |
       | web-server | 10.0.0.1 |
       | database   | 10.0.0.2 |
      And "hosts" is set to the following values for the dev.vladik environment
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database   | 192.168.1.101 |
       | app-server | 192.168.1.103 |
     When configuration data is compiled for the dev.vladik environment
     Then "hosts" holds the following values
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database   | 192.168.1.101 |
       | app-server | 192.168.1.103 |

  Scenario: A child environment can delete items from its parent's collection
    Given "hosts" is set to the following values for the dev environment
       | name        | address       |
       | web-server  | 192.168.1.100 |
       | database-m  | 192.168.1.111 |
       | database-s1 | 192.168.1.112 |
       | database-s2 | 192.168.1.113 |
       | app-server  | 192.168.1.103 |
      And the following items are set to be deleted from "hosts" in the dev.vladik environment
       | name        |
       | database-s1 | 
       | database-s2 | 
     When configuration data is compiled for the dev.vladik environment
     Then "hosts" holds the following values
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database-m | 192.168.1.111 |
       | app-server | 192.168.1.103 |

  Scenario: A child environment can append items to its parent's collection
    Given "hosts" is set to the following values for the dev environment
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database-m | 192.168.1.111 |
       | app-server | 192.168.1.103 |
      And the following items are added to the "hosts" collection in the dev.vladik environment
       | name        | address       |
       | database-s1 | 192.168.1.112 |
       | database-s2 | 192.168.1.113 |
     When configuration data is compiled for the dev.vladik environment
     Then "hosts" holds the following values
       | name        | address       |
       | web-server  | 192.168.1.100 |
       | database-m  | 192.168.1.111 |
       | database-s1 | 192.168.1.112 |
       | database-s2 | 192.168.1.113 |
       | app-server  | 192.168.1.103 |

  Scenario: A child environment can update values in its parent's collection
    Given "hosts" is set to the following values for the dev environment
       | name       | address       |
       | web-server | 192.168.1.100 |
       | database-m | 192.168.1.111 |
       | app-server | 192.168.1.103 |
      And the following items are set to be updated in the "hosts" collection in the dev.vladik environment
       | key  | name       | address    |
       | name | web-server | 10.0.1.100 |
       | name | database-m | 10.0.1.101 |
       | name | app-server | 10.0.1.102 |
     When configuration data is compiled for the dev.vladik environment
     Then "hosts" holds the following values
       | name       | address    |
       | web-server | 10.0.1.100 |
       | database-m | 10.0.1.101 |
       | app-server | 10.0.1.102 |
