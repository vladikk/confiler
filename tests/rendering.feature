Feature: Rendering configuration files 

  Scenario: Rendering a simple configuration template
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
      And a template file "app.config" with the following contents:
       """
       <config>
         <add key="threshold" value="{{threshold}}" />
         {% for host in hosts %}
         <add key="{{host.name}}" value="{{host.address}}" />
         {% endfor %}
       </config>
       """
     When the "app.config" template is rendered for the dev environment to the "results/dev" folder
     Then the result is the following "results/dev/app.config" file
       """
       <config>
         <add key="threshold" value="10" />
         <add key="web-server" value="192.168.1.100" />
         <add key="database" value="192.168.1.101" />
         <add key="app-server" value="192.168.1.102" />
       </config>
       """
