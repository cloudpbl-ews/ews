
function CPUusage() {
    Highcharts.SparkLine = function (options, callback) {
        var defaultOptions = {
            chart: {
                renderTo: (options.chart && options.chart.renderTo) || this,
                backgroundColor: null,
                borderWidth: 0,
                type: 'area',
                margin: [2, 0, 2, 0],
                width: 120,
                height: 20,
                style: {
                    overflow: 'visible'
                },
                skipClone: true
            },
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            xAxis: {
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                startOnTick: false,
                endOnTick: false,
                tickPositions: []
            },
            yAxis: {
                endOnTick: false,
                startOnTick: false,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                tickPositions: [0]
            },
            legend: {
                enabled: false
            },
            tooltip: {
                backgroundColor: null,
                borderWidth: 0,
                shadow: false,
                useHTML: true,
                hideDelay: 0,
                shared: true,
                padding: 0,
                positioner: function (w, h, point) {
                    return { x: point.plotX - w / 2, y: point.plotY - h};
                }
            },
            plotOptions: {
                series: {
                    //animation: false,
                    lineWidth: 1,
                    shadow: false,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    marker: {
                        radius: 1,
                        states: {
                            hover: {
                                radius: 2
                            }
                        }
                    },
                    fillOpacity: 0.25
                },
                column: {
                    negativeColor: '#910000',
                    borderColor: 'silver'
                }
            }
        };
        options = Highcharts.merge(defaultOptions, options);

        return new Highcharts.Chart(options, callback);
    };

        $tds = $("td[data-sparkline]"),
        fullLen = $tds.length,
        n = 0;

    function getAndDraw($td){
            console.log("td");
            console.log($td);
            stringdata = $td.data('sparkline');
            console.log(stringdata);
            jQuery.ajax({ 
              url: stringdata,
              type: "GET",
              dataType: "text",
              success: function(data) {
                      data = data.split(/\r\n|\r|\n/);
                      for(j=0; j<data.length; j++){
                              if(isNaN(data[j].split(":")[1])){
                                data[j] = 0;
                              }else{
                              data[j] = Number(data[j].split(":")[1]);
                              }
                      }
                      console.log("data");
                      console.log(data);
            chart = {};
            $td.highcharts('SparkLine', {
                series: [{
                    data: data,
                    pointStart: 1
                }],
                tooltip: {
                    headerFormat: '<span style="font-size: 10px">' + $td.parent().find('th').html() + ', Q{point.x}:</span><br/>',
                    pointFormat: '<b>{point.y}.000</b> USD'
                },
                chart: chart
            });
           }
         });
    }
    
    function doChunk() {
      console.log("debug");
        var i,
            len = $tds.length,
            $td,
            stringdata,
            arr
        for (i = 0; i < len; i += 1) {
            $td = $($tds[i]);
            getAndDraw($td);

        }
    }
    doChunk();
};

