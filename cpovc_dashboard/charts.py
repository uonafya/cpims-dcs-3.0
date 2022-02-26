
def combo_chart(request, params, data):
    """Method to get timeline."""
    try:
        categories = str(data['items'])
        html = '''
                <script>
                $(document).ready(function() {
                    var colors = ["#7cb5ec", "#e41a1c", "#434348", "#E80C7A", "#E80C7A"];
                    Highcharts.chart('container-{cont}', {
                        chart: {
                            zoomType: 'xy'
                        },
                        title: {
                            text: '{title}'
                        },
                        subtitle: {
                            text: ''
                        },
                        xAxis: [{
                            categories: {categories},
                            crosshair: true
                        }],
                        yAxis: [{ // Secondary yAxis
                            title: {
                                text: '# of OVC',
                                style: {
                                    color: Highcharts.getOptions().colors[1]
                                }
                            },
                            labels: {
                                format: '{value}',
                                style: {
                                    color: Highcharts.getOptions().colors[1]
                                }
                            }
                        }, { // Primary yAxis
                            labels: {
                                format: '{value} %',
                                style: {
                                    color: '#e41a1c'
                                }
                            },
                            title: {
                                text: 'Cascade',
                                style: {
                                    color: '#e41a1c'
                                }
                            },
                            opposite: true
                        }],
                        tooltip: {
                            shared: true
                        },
                        plotOptions: {
                            column: {
                                stacking: 'normal',
                                dataLabels: {
                                    enabled: true
                                }
                            },
                            spline:{
                               colors: colors
                            }
                        },
                        legend: {
                               backgroundColor:
                                Highcharts.defaultOptions.legend.backgroundColor || // theme
                                'rgba(255,255,255,0.25)'
                        },
                        credits: {
                            enabled: false
                        },
                        colors: colors,
                        series: [{
                            name: '# of OVC',
                            type: 'column',
                            data: [{mdata}],
                            tooltip: {
                                valueSuffix: ''
                            },

                        }, {
                            name: 'Cascade',
                            type: 'spline',
                            yAxis: 1,
                            data: [{fdata}],
                            tooltip: {
                                valueSuffix: ' %'
                            }
                        }]
                    });
                });
            </script>'''
        result = str(html).replace('{mdata}', data['mdata'])
        result = result.replace('{fdata}', data['fdata'])
        result = result.replace('{cont}', params['cont'])
        result = result.replace('{title}', params['title'])
        result = result.replace('{categories}', categories)
    except Exception as e:
        print('error with combo data - %s' % (str(e)))
        raise e
    else:
        return result


def bar_chart(request, params, data):
    """Method to get bar chart."""
    try:
        categories = str(data['items'])
        html = '''
                <script>
                $(document).ready(function() {
                    Highcharts.chart('container-services', {
                        chart: {
                            type: 'bar'
                        },
                        title: {
                            text: '{title}'
                        },
                        subtitle: {
                            text: ''
                        },
                        xAxis: {
                            categories: {categories},
                            title: {
                                text: null
                            }
                        },
                        yAxis: {
                            min: 0,
                            title: {
                                text: '# of Beneficiaries / HH',
                                align: 'high'
                            },
                            labels: {
                                overflow: 'justify'
                            }
                        },
                        tooltip: {
                            valueSuffix: ' millions'
                        },
                        plotOptions: {
                            bar: {
                                dataLabels: {
                                    enabled: true
                                }
                            }
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'top',
                            x: -40,
                            y: 80,
                            floating: true,
                            borderWidth: 1,
                            backgroundColor:
                                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
                            shadow: true
                        },
                        credits: {
                            enabled: false
                        },
                        series: [{
                            name: 'Male',
                            data: [{mdata}]
                        }, {
                            name: 'Female',
                            data: [{fdata}]
                        }]
                    });
                 });
            </script>'''
        result = str(html).replace('{mdata}', data['mdata'])
        result = result.replace('{fdata}', data['fdata'])
        result = result.replace('{categories}', categories)
    except Exception as e:
        print('error with kpi data - %s' % (str(e)))
        raise e
    else:
        return result


def column_chart(request, params, data):
    """Method to get bar chart."""
    try:
        categories = str(data['items'])
        html = '''
                <script>
                $(document).ready(function() {
                    Highcharts.chart('container-{cont}', {
                        chart: {
                            type: 'column'
                        },
                        title: {
                            text: '{title}'
                        },
                        xAxis: {
                            categories: {categories}
                        },
                        yAxis: {
                            min: 0,
                            title: {
                                text: '# of OVC'
                            },
                            stackLabels: {
                                enabled: true,
                                style: {
                                    fontWeight: 'bold',
                                    color: ( // theme
                                        Highcharts.defaultOptions.title.style &&
                                        Highcharts.defaultOptions.title.style.color
                                    ) || 'gray'
                                }
                            }
                        },
                        tooltip: {
                            headerFormat: '<b>{point.x}</b><br/>',
                            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
                        },
                        plotOptions: {
                            column: {
                                stacking: 'normal',
                                dataLabels: {
                                    enabled: true
                                }
                            }
                        },
                        credits: {
                            enabled: false
                        },
                        series: [{
                            name: 'Male',
                            data: [{mdata}]
                        }, {
                            name: 'Female',
                            data: [{fdata}]
                        }]
                    });
                 });
            </script>'''
        result = str(html).replace('{mdata}', data['mdata'])
        result = result.replace('{fdata}', data['fdata'])
        result = result.replace('{cont}', params['cont'])
        result = result.replace('{title}', params['title'])
        result = result.replace('{categories}', categories)
    except Exception as e:
        print('error with column chart - %s' % (str(e)))
        raise e
    else:
        return result


def column_pie_chart(request, params, data):
    """Method to get bar chart."""
    try:
        categories = str(data['items'])
        html = '''
                <script>
                $(document).ready(function() {
                    Highcharts.chart('container-{cont}', {
                        chart: {
                            type: 'column'
                        },
                        title: {
                            text: '{title}'
                        },
                        xAxis: {
                            categories: {categories}
                        },
                        yAxis: {
                            min: 0,
                            title: {
                                text: '# of OVC'
                            },
                            stackLabels: {
                                enabled: true,
                                style: {
                                    fontWeight: 'bold',
                                    color: ( // theme
                                        Highcharts.defaultOptions.title.style &&
                                        Highcharts.defaultOptions.title.style.color
                                    ) || 'gray'
                                }
                            }
                        },
                        tooltip: {
                            headerFormat: '<b>{point.x}</b><br/>',
                            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
                        },
                        plotOptions: {
                            column: {
                                stacking: 'normal',
                                dataLabels: {
                                    enabled: true
                                }
                            }
                        },
                        credits: {
                            enabled: false
                        },
                        series: [{
                            name: 'Male',
                            type: 'column',
                            data: [{mdata}]
                        }, {
                            name: 'Female',
                            type: 'column',
                            data: [{fdata}]
                        },{
                            type: 'pie',
                            name: 'OVC_HIVSTAT',
                            data: [{
                                name: '+Ve',
                                y: 13,
                                color: Highcharts.getOptions().colors[0] // Jane's color
                            }, {
                                name: '-Ve',
                                y: 23,
                                color: Highcharts.getOptions().colors[1] // John's color
                            }],
                            center: [100, 80],
                            size: 100,
                            showInLegend: false,
                            dataLabels: {
                                enabled: false
                            }
                        }]
                    });
                 });
            </script>'''
        result = str(html).replace(',{mdata}', data['mdata'])
        result = result.replace('{fdata}', data['fdata'])
        result = result.replace('{cont}', params['cont'])
        result = result.replace('{title}', params['title'])
        result = result.replace('{categories}', categories)
    except Exception as e:
        print('error with column chart - %s' % (str(e)))
        raise e
    else:
        return result
