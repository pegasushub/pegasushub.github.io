$(function () {
    let searchJSON;

    $.getJSON("/search.json", function (json) {
        searchJSON = json;
    });

    $("#search-input").on("keyup", function () {
        let resultsContainer = $("#results-container");
        resultsContainer.css('visibility', 'visible').html('');
        let input_value = $(this).val();

        if (input_value.length === 0) {
            resultsContainer.css('visibility', 'hidden');
            return;
        }

        let termsList = input_value.toLowerCase().split(" ");
        let terms = termsList.filter(function (el) {
            return el != null && el.length > 0;
        });

        searchJSON.forEach(function (entry) {
            terms.forEach(function (term) {
                if (entry.title.toLowerCase().includes(term) ||
                    entry.tags.toLowerCase().includes(term)) {
                    let tagsList = entry.tags.split(" ").filter(function (tag) {
                        return tag != null && tag.length > 0;
                    });
                    let tags = '';
                    tagsList.forEach(function (tag) {
                        tags += '<span class="topic">' + tag + '</span>';
                    });
                    $("#results-container").append(
                        '<div class="search-item"><a href="' + entry.url + '"><h1><i class="fab fa-github"></i> ' +
                        entry.repo_name + '</h1></a>' + tags + '</div>'
                    );
                }
            });
        });
    });
});
