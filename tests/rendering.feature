Feature: Rendering configuration files 

  Background: Sample environments and templates
    Given the following config file is set for the dev environment
       """
       {
         "threshold": "10",
         "hosts": [
                     { "name": "web-server", "address": "192.168.1.100" },
                     { "name": "database", "address": "192.168.1.101" },
                     { "name": "app-server", "address": "192.168.1.102" }
                  ]
       }
       """
      And the following config file is set for the dev.vladik environment
       """
       {
         "threshold": "5"
       }
       """
      And the template file "app.config.template" with the following contents:
       """
       <config>
         <add key="threshold" value="{{threshold}}" />
         {% for host in hosts %}
         <add key="{{host.name}}" value="{{host.address}}" />
         {% endfor %}
       </config>
       """
      And the template file "hosts.template" with the following contents:
       """
       {% for host in hosts %}
       {{host.name}} {{host.address}}
       {% endfor %}
       """

  Scenario: Rendering a simple configuration template with fixed environment data
     When the "app.config" template is rendered for the dev environment to the "results/dev" folder
     Then the "results/dev/app.config" file has the following contents
       """
       <config>
         <add key="threshold" value="10" />
         <add key="web-server" value="192.168.1.100" />
         <add key="database" value="192.168.1.101" />
         <add key="app-server" value="192.168.1.102" />
       </config>
       """

  Scenario: Rendering a simple configuration template with compiled environment data
     When the "app.config" template is rendered for the dev.vladik environment to the "results/dev.vladik" folder
     Then the "results/dev.vladik/app.config" file has the following contents
       """
       <config>
         <add key="threshold" value="5" />
         <add key="web-server" value="192.168.1.100" />
         <add key="database" value="192.168.1.101" />
         <add key="app-server" value="192.168.1.102" />
       </config>
       """

  Scenario: Rendering a configuration template in a subfolder
      Given the template file "config/shared/hosts.config.template" with the following contents:
       """
       {% for host in hosts %}
       {{host.name}} {{host.address}};
       {% endfor %}
       """
     When all templates are rendered for the dev environment to the "results/dev" folder
     Then the "results/dev/config/shared/hosts.config" file has the following contents
       """
       web-server 192.168.1.100;
       database 192.168.1.101;
       app-server 192.168.1.102;
       """

  Scenario: Rendering multiple configuration templates
     When all templates are rendered for the dev environment to the "results/dev" folder
     Then the "results/dev/app.config" file has the following contents
       """
       <config>
         <add key="threshold" value="10" />
         <add key="web-server" value="192.168.1.100" />
         <add key="database" value="192.168.1.101" />
         <add key="app-server" value="192.168.1.102" />
       </config>
       """
      And the "results/dev/hosts" file has the following contents
       """
       web-server 192.168.1.100
       database 192.168.1.101
       app-server 192.168.1.102
       """
 Scenario: Render keys with special characters
    Given the following config file is set for the dev.test environment
       """
       {
         "threshold.value": "15"
       }
       """
      And the template file "app.cfg.template" with the following contents:
       """
       <config>
         <add key="threshold.value" value="{{values['threshold.value']}}" />
       </config>
       """
     When the "app.cfg" template is rendered for the dev.test environment to the "results/dev.test" folder
     Then the "results/dev.test/app.cfg" file has the following contents
       """
       <config>
         <add key="threshold.value" value="15" />
       </config>
       """

 Scenario: Enumerate all keys/values 
    Given the following config file is set for the dev.test environment
       """
       {
         "threshold.value": "15",
         "threshold.limit": "100"
       }
       """
      And the template file "app.cfg.template" with the following contents:
       """
       <config>
         {% for key, value in values.iteritems() %}
         <add key="{{key}}" value="{{value}}" />
         {% endfor %}
       </config>
       """
     When the "app.cfg" template is rendered for the dev.test environment to the "results/dev.test" folder
     Then the "results/dev.test/app.cfg" file has the following contents
       """
       <config>
         <add key="threshold" value="10" />
         <add key="threshold.limit" value="100" />
         <add key="threshold.value" value="15" />
       </config>
       """

Scenario: Rendering a configuration template within a subfolder
    Given the template file "config/app.config.template" with the following contents:
       """
       <config>
         <add key="threshold" value="{{threshold}}"></add>
         {% for host in hosts %}
         <add key="{{host.name}}" value="{{host.address}}" />
         {% endfor %}
       </config>
       """
     When the "config/app.config" template is rendered for the dev environment to the "results/dev" folder
     Then the "results/dev/config/app.config" file has the following contents
       """
       <config>
         <add key="threshold" value="10"></add>
         <add key="web-server" value="192.168.1.100" />
         <add key="database" value="192.168.1.101" />
         <add key="app-server" value="192.168.1.102" />
       </config>
       """
