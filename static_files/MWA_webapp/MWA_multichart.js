$(function() {
   var seriesOptions = [],
      seriesCounter = 0,
      names = [
         ['houseprice', 'gold'],
         ['allords', 'gold'],
         ['allordsperatio', 'identity'],
      ];

   var city = $("#citylist_1").val();

   var rangeselector = {
      selected: 5,
      buttons: [{
         type: 'month',
         count: 6,
         text: '6m'
      }, {
         type: 'year',
         count: 1,
         text: '1y'
      }, {
         type: 'year',
         count: 5,
         text: '5y'
      }, {
         type: 'year',
         count: 15,
         text: '15y'
      }, {
         type: 'ytd',
         text: 'YTD'
      }, {
         type: 'all',
         text: 'ALL'
      }]
   };

   var plotbandcolour = 'rgba(127,127,27,0.15)';
   var plotbands = [{
         color: plotbandcolour, // Color value
         from: 120873600000, // Nov 1973
         to: 162777600000, // Mar 1975
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
      {
         color: plotbandcolour, // Color value
         from: 315446400000, // Jan 1980
         to: 331171200000, //  June 1980
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
      {
         color: plotbandcolour, // Color value
         from: 362707200000, // July 1981
         to: 404870400000, // Nov 1982
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
      {
         color: plotbandcolour, // Color value
         from: 646704000000, // July 1990
         to: 667699200000, // March 1991
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
      {
         color: plotbandcolour, // Color value
         from: 867715200000, // July 1997
         to: 899251200000, // July 1998
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
      {
         color: plotbandcolour, // Color value
         from: 983318400000, // March 2001
         to: 1004486400000, // Nov 2001
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
      {
         color: plotbandcolour, // Color value
         from: 1196380800000, // Dec 2007
         to: 1243728000000, // June 2009
         label: {
            text: '',
            rotation: 90,
            align: 'left',
            style: {
               "fontSize": "11px"
            },
            y: 3,
            x: 3,
            color: 'rgb(34,42,53)'
         },
      },
   ];

   function createChart() {
      Highcharts.stockChart('container_multichart', {
         rangeSelector: rangeselector,
         credits: {
            enabled: false
         },
         exporting: {
            enabled: false
         },
         colors: ['#7CB5EC', '#FF9900', '#FF5050'],
         tooltip: {
            valueDecimals: 2,
            split: true,
         },

         yAxis: [{ // Primary yAxis
            title: {
               text: null,
            },
         }, { // Secondary yAxis
            gridLineWidth: 0,
            title: {
               text: null,
            },
            opposite: false
         }],

         xAxis: {
            plotBands: plotbands
         },
         plotOptions: {
            series: {
               showInNavigator: true
            }
         },
         series: seriesOptions,
         title: {
            enabled: true,
            text: "Median House Price : Gold  /  All Ords : Gold  /  All Ords PE Ratio",
            align: 'left',
            style: {
               'fontWeight': 'bold'
            },
         },
      });
   }

   $.each(names, function(i, name) {
         $.getJSON(`/getdata/?commodity_one=${name[0]}&commodity_two=${name[1]}&city=${city}`, function(data) {

               if (name[0] == 'houseprice') {
                  seriesOptions[i] = {
                     name: `${jsUcfirst(prettifystringnames(name[0]))} : ${jsUcfirst(prettifystringnames(name[1]))}`,
                     data: data,
                     yAxis: 1,
                  }
               } else {
                  seriesOptions[i] = {
                     name: `${jsUcfirst(prettifystringnames(name[0]))} : ${jsUcfirst(prettifystringnames(name[1]))}`,
                     data: data,
                     yAxis: 0,
                  }
               }

            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter += 1;

            if (seriesCounter === names.length) {
               createChart();
            }
         });
   });
});
