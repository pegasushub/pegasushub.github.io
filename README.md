# PegasusHub

A Community-enabled Workflows Repository for Pegasus

### Adding your own workflow repository

In order to add your own Pegasus-enabled workflow repository, 
you only need to add your organization and repository names 
to the `_data/workflows.yml` file as follows:

```
- organization: my-github-organization
  repo_name: my-workflow-repository
  highlight: true
  priority: 2
```
The property `highlight` specifies wether the workflow is to be featured on the homepage. If highlight is set to true, the workflow must be given a priority number between 1 to 5 (5 being the most important and to be featured on top). 

The preferred way to submit your changes is via creating a 
**pull request** with the changes.