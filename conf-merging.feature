Feature: Merging configuration files
  In order to support efficient management of configuration values across
  multiple environments(dev, qa, staging, prod + multi-tenant)
  I want to be able to specify configuration values in multiple namespaces,
  and to be able to merge them into a single configuration file that will
  inherit and override values from underlying namespaces.

  Scenario: A value that was set, will be emitted after merging
    Given "max-threshold" is set to "10" for the dev environment
     When a configuration file is compiled for the dev environment
     Then "max-threshold" is "10" for the dev environment
    
  Scenario: A child environment's values  override the values set in its parent
    Given "max-threshold" is set to "10" for the dev environment
      And "max-threshold" is set to "5" for the dev.vladik environment
     When a configuration file is compiled for the dev.vladik environment
     Then "max-threshold" is "5" for the dev.vladik environment

  Scenario: Configuration cannot be compiled for parent environments
    Given "max-threshold" is set to "10" for the dev environment
      And "max-threshold" is set to "5" for the dev.vladik environment
     When a configuration file is compiled for the dev environment
     Then an error is raised
