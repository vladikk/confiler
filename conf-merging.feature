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
