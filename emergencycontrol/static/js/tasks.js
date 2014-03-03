$(function () {
    $('#container').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Tasks'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: null,
                enabled: false
            },
            min: 0
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false
                }
            }
        },
        series: [{
            name: 'task open',
            data: taskOpen

        }, {
            name: 'task executed',
            data: taskExecuted
        }]
    });
});
