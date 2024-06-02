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
The property `highlight` specifies wether the workflow is to 
be featured on the homepage. If highlight is set to true, the workflow
must be given a priority number between 1 to 5 (5 being the most 
important and to be featured on top). 

The Hub only pulls in information from the **master** branch of
a workflows repository. More details about how to add more information
describing your repository by specifying a `.pegasushub.yml` can 
be found at [here](contribute.md).

The preferred way to submit your changes is via creating a 
**pull request** with the changes.

### Starting your local instance of the Workflows Repository

The repository gets deployed automatically at https://pegasushub.io 
every 2 hours. 

The website is a Ruby Jekyll site and you can run an instance of it 
locally on your desktop by doing the following

#### Generate the html pages 

Before running the script, you need to set specify GitHub access token
that allows the `process.py` script to retrieve information from the 
various GitHub repositories. This is done by setting the environment
variable `PEGASUSHUB_TOKEN`

```bash
$ export PEGASUSHUB_TOKEN=xxxxxx
```

```bash
$./scripts/process.py 
404 Client Error: Not Found for url: https://raw.githubusercontent.com/pegasus-isi/sra-search-pegasus-workflow/master/.pegasushub.yml
404 Client Error: Not Found for url: https://raw.githubusercontent.com/pegasus-isi/freesurfer-osg-workflow/master/.pegasushub.yml
404 Client Error: Not Found for url: https://raw.githubusercontent.com/pegasus-isi/mask-detection-workflow/master/.pegasushub.yml
404 Client Error: Not Found for url: https://raw.githubusercontent.com/pegasus-isi/molecular-transformer-workflow/master/.pegasushub.yml
```
The workflow html pages get generated in the `_workflows` directory
and the `_logs` directory will have logs from the process script

#### Start the Jekyll Server

```bash
$ bundle exec jekyll serve --incremental
Configuration file: /Volumes/lfs1/devel/Pegasus/git/pegasushub.github.io/_config.yml
            Source: /Volumes/lfs1/devel/Pegasus/git/pegasushub.github.io
       Destination: /Volumes/lfs1/devel/Pegasus/git/pegasushub.github.io/_site
 Incremental build: enabled
      Generating... 
       Jekyll Feed: Generating feed for posts
                    done in 0.58 seconds.
 Auto-regeneration: enabled for '/Volumes/lfs1/devel/Pegasus/git/pegasushub.github.io'
    Server address: http://127.0.0.1:4000
  Server running... press ctrl-c to stop.

```
