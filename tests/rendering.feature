Feature: Rendering configuration files 

  Scenario: Rendering a simple configuration template
    Given the following config file is set for the dev environment
       """
       {
         "threshold": "10"
       }
       """
      And a template file "app.config" with the following contents:
       """
       <config>
         <add key="threshold" value="{{threshold}}" />
       </config>
       """
     When the "app.config" template is rendered for the dev environment to the "results/dev" folder
     Then the result is the following "results/dev/app.config" file
       """
       <config>
         <add key="threshold" value="10" />
       </config>
       """
