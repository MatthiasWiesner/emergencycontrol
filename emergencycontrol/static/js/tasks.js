$.getJSON("/tasks", function( config ) {
    config['chart']['backgroundColor'] = 'white';
    new Highcharts.Chart(config);
});
