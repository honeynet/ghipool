$.ajax('/static/templates/table.html').then(function(tableTemplate) {
    var ractive = new Ractive({
        debug: true,
        el: 'container',
        template: tableTemplate,
        data: {
            projects_data: {},
            projects: {}
        }
    });
    $.getJSON('/projects_data', function(data) {
        ractive.set('projects_data', data);
    });

    $.getJSON('/projects', function(data) {
        ractive.set('projects', data);
    });
});