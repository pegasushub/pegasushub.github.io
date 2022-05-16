function getREADME(organization, repo_name, default_branch) {
    $.get('https://raw.githubusercontent.com/' + organization + '/' + repo_name + '/' + default_branch + '/README.md', function (data) {
        let converter = window.markdownit();
        let base_url = 'https://github.com/' + organization + '/' + repo_name + '/raw/' + default_branch + '/';
        let readme = converter.render(data).replaceAll(/<img src="\/|<img src="(?!.*(http:\/\/|https:\/\/))/g, '<img src="' + base_url);
        console.log(readme);
        $('#wf-readme').html(readme);
    });
}

function getOverallRepoInfo(organization, repo_name, default_branch) {
    $.ajax({
        url: 'https://api.github.com/repos/' + organization + '/' + repo_name,
        type: 'GET',
        dataType: 'json',
        success: function (content) {
            console.log(content)
            let id = organization + '-' + repo_name + '-';
            $('#' + id + 'wf-title').html(content.name);
            $('#' + id + 'wf-subtitle').html(content.description);

            // date
            let date = new Date(content.updated_at);
            $('#' + id + 'wf-month').html(date.toLocaleString('default', {month: 'short'}));
            $('#' + id + 'wf-day').html(date.getDate());
            $('#' + id + 'wf-year').html(date.getFullYear());
            if (content.topics.length > 0) {
                let topics = '';
                for (let topic in content.topics) {
                    topics += '<span class="topic">' + content.topics[topic] + '</span>&nbsp;&nbsp;';
                }
                $('#' + id + 'wf-topics').html(topics);
            }
        },
        beforeSend: function (request) {
            request.setRequestHeader("Accept", 'application/vnd.github.mercy-preview+json');
        }
    });
}


function getRepoInfo(organization, repo_name, default_branch) {

    $.ajax({
        url: 'https://api.github.com/repos/' + organization + '/' + repo_name,
        type: 'GET',
        dataType: 'json',
        success: function (content) {
            console.log(content);

            // metadata file
            $.get('https://raw.githubusercontent.com/' + organization + '/' + repo_name + '/' + default_branch + '/.pegasushub.yml', function (data) {
                let content = jsyaml.load(data);
                let version = ">= " + content.pegasus.version.min ;
                if(!content.pegasus.version.min && content.pegasus.version.max){
                    version = "<= " + content.pegasus.version.max ;
                }
                else if (content.pegasus.version.min !== content.pegasus.version.max && content.pegasus.version.max){
                    version = '[' + content.pegasus.version.min + ', ' + content.pegasus.version.max + ']';
                }
                $('#wf-pegasus-version').html(version);
                let dependencies = '';
                for (let dependency in content.dependencies) {
                    if (dependencies !== '') {
                        dependencies += ', ';
                    }
                    dependencies += content.dependencies[dependency];
                }
                $('#wf-dependencies').html(dependencies);
            });

            $('#wf-title').html(content.name);
            $('#wf-subtitle').html(content.description);
            if (content.license) {
                $('#wf-license').html(content.license.name);
            } else {
                $('#wf-license').html('No licence available');
            }
            $('#wf-repo').html('<a href="https://github.com/' + organization + '/' + repo_name + '" target="_blank">https://github.com/' + organization + '/' + repo_name + '</a>');
            $('#wf-forks').html(content.forks);
            $('#wf-issues').html(content.open_issues);
            $('#wf-stargazers').html(content.stargazers_count);
            if (content.topics.length > 0) {
                let topics = '';
                for (let topic in content.topics) {
                    topics += '<span class="topic">' + content.topics[topic] + '</span>&nbsp;&nbsp;';
                }
                $('#wf-topics').html(topics);
            } else {
                $('#wf-topics').html('No topics listed');
            }

            // date
            let date = new Date(content.updated_at);
            $('#wf-month').html(date.toLocaleString('default', {month: 'short'}));
            $('#wf-day').html(date.getDate());
            $('#wf-year').html(date.getFullYear());

            // releases
            $.getJSON(content.releases_url.slice(0, -5), function (data) {
                const dateTimeFormat = new Intl.DateTimeFormat('en', {year: 'numeric', month: 'short', day: '2-digit'});
                if (data.length > 0) {
                    let release_date = dateTimeFormat.format(new Date(data[0].published_at));
                    $('#wf-release').html('<a href="' + data[0].html_url + '" target="_blank">' + data[0].name + '</a> <span class="release-date">(' + release_date + ')</span>');
                    $('#wf-releases').html('<a href="https://github.com/' + organization + '/' + repo_name + '/releases" target="_blank" class="fab fa-github">' + data.length + '</a>');
                } else {
                    $('#wf-release').html('No release available');
                    $('#wf-releases').hide();
                }
            });

            // readme file
            $.get('https://raw.githubusercontent.com/' + organization + '/' + repo_name + '/' + default_branch + '/README.md', function (data) {
                let converter = window.markdownit();
                let readme = converter.render(data).replaceAll('src="/', 'src="' + 'https://raw.githubusercontent.com/' + organization + '/' + repo_name + '/');
                console.log('===================================');
                console.log(readme);
                $('#wf-readme').html(readme);
            });

            // contributors
            $.getJSON(content.contributors_url, function (data) {
                $('#wf-contributors').html(data.length);
                let contributors_list = '';
                for (let contributor in data) {
                    contributors_list += '<a href="' + data[contributor].html_url + '" target="_blank"><img src="' + data[contributor].avatar_url + '" width="32" height="32"/></a>&nbsp;&nbsp;';
                }
                $('#wf-contributors-list').html(contributors_list);
            });

        },
        error: function (jqXHR) {
            if(jqXHR.status == 403)
                console.warn(jqXHR.status + " Rate limit exceeded, skipping for now");
          },
        beforeSend: function (request) {
            request.setRequestHeader("Accept", 'application/vnd.github.mercy-preview+json');
        }
    });
}
