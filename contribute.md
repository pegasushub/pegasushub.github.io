---
layout: default
---

# How to Contribute

PegasusHub provides a **curated** collection of open source [Pegasus](https://pegasus.isi.edu) 
workflow repositories hosted at [GitHub](https://github.com). The main goal of this framework 
is to showcase community efforts for advancing science. We invite all users from the community
to share their workflow repositories through this framework, which may inspire new/other users 
on their quest to tackle their scientific problems using workflows, and help Pegasus developers
to broaden their understanding of the community needs and software usage.

## Adding your Own Workflow Repository

In order to add your own Pegasus-enabled workflow repository, you only need to add your organization 
and repository names into an YAML file hosted as part of the [PegasusHub GitHub repository](https://github.com/pegasushub/pegasushub.github.io).
The preferred way to submit your changes is via creating a pull request with the changes. To this
end, these are the recommended steps for adding your own workflow: 

1. **Fork** the [PegasusHub GitHub repository](https://github.com/pegasushub/pegasushub.github.io);
2. **Clone** your forked repository:
```
git clone https://github.com/<your_username>/pegasushub.github.io
```
3. **Edit** the `_data/workflows.yml` file, and add the information regarding your workflow repository:
```
- organization: my-github-organization
      repo_name: my-workflow-repository
```
4. Commit the changes, and create a **pull request** for the [PegasusHub GitHub repository](https://github.com/pegasushub/pegasushub.github.io).

5. The Pegasus team will then evaluate your pull request, and merge the changes if the workflow
repository and examples are properly documented.

## Providing a Rich Set of Information

Although the minimum requirement for publishing your workflow repository is to only have an open
source repository with a reasonable documentation, we strongly encourage users to provide additional
metadata to their workflow repositories.

The PegasusHub framework seeks for a `.pegasushub.yml` file in the root folder of the workflow
repository. This file is expected to contain metadata that would enrich the repository description
on the PegasusHub.

The following table summarizes the list of available metadata keywords:

| Key | Description |
| --- | ----------- |
| pegasus.version.min | Minimum Pegasus version required to run the workflow |
| pegasus.version.max | Maximum Pegasus version required to run the workflow |
| dependencies | List of software dependencies | 
| scripts.generator | |
