  function jsUcfirst(string){
      return string.charAt(0).toUpperCase() + string.slice(1);
  }

  function prettifystringnames(string){
      if (string == 'allordsperatio'){
      return 'All Ords PE Ratio'}
      else if (string == 'allords'){
      return 'All Ords'}
      else {
      return string}
  }

  function _formatEpochDate(eTS) {
    return new Date(eTS).toLocaleDateString();
  }

  function plot_chart(commodity_one, commodity_two, undervalue, overvalue){
  var plotbandcolour = 'rgba(127,127,27,0.15)';

  $.getJSON(`/getdata/?commodity_one=${commodity_one}&commodity_two=${commodity_two}`, function (data) {
      // Create the chart

      Highcharts.stockChart(`container_${commodity_one}_${commodity_two}`, {

          rangeSelector: {
              selected: 3,
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
          },
          credits:{enabled:false},
          exporting:{enabled:false},
          title: {
              enabled: true,
              text: `${jsUcfirst(prettifystringnames(commodity_one))} : ${jsUcfirst(prettifystringnames(commodity_two))}`,
              align: 'left',
              style: {'fontWeight':'bold'},
          },
          subtitle: {
              enabled: true,
              text: `from ${_formatEpochDate(data[0][0])} to ${_formatEpochDate(data[data.length-1][0])}`,
              align: 'left',
              style: {'fontSize':'10px'},
          },
          series: [{
              name: `${jsUcfirst(prettifystringnames(commodity_one))} : ${jsUcfirst(prettifystringnames(commodity_two))}`,
              data: data,
              tooltip: {
                  valueDecimals: 2
              }
          }],

          yAxis: {
              plotLines: [{
                            value: undervalue,
                            label: {
                                      text:`Switch to ${jsUcfirst(prettifystringnames(commodity_one))}`,
                                      style: {'fontSize':'11px', 'color': 'rgba(68,114,196,0.9)',}
                                    },
                            color: 'rgba(68,114,196,0.5)',
                            width: 1,
                            zIndex: 9,
                          },
                          {
                            value: overvalue,
                            label: {
                                      text:`Switch to ${jsUcfirst(prettifystringnames(commodity_two))}`,
                                      style: {'fontSize':'11px', 'color': 'rgba(255,80,80,0.9)',}
                                    },
                            color: 'rgba(255,80,80,0.5)',
                            width: 1,
                            zIndex: 9,
                          },
                          ],
          },

          xAxis: {
                    plotBands: [{
                                  color: plotbandcolour, // Color value
                                  from: 120873600000, // Nov 1973
                                  to: 162777600000, // Mar 1975
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 315446400000, // Jan 1980
                                  to: 331171200000, //  June 1980
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 362707200000, // July 1981
                                  to: 404870400000, // Nov 1982
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 646704000000, // July 1990
                                  to: 667699200000, // March 1991
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 867715200000, // July 1997
                                  to: 899251200000, // July 1998
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 983318400000, // March 2001
                                  to: 1004486400000, // Nov 2001
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 1196380800000, // Dec 2007
                                  to: 1243728000000, // June 2009
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                ],
                },
      }

    );
  })};


  function plot_allordsPEratio(commodity_one, undervalue, overvalue){
  var plotbandcolour = 'rgba(127,127,27,0.15)';

  $.getJSON(`/getdata/?commodity_one=${commodity_one}&commodity_two=identity`, function (data) {
      // Create the chart

      Highcharts.stockChart(`container_${commodity_one}`, {

          rangeSelector: {
              selected: 3,
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
          },
          credits:{enabled:false},
          exporting:{enabled:false},
          title: {
              enabled: true,
              text: `${jsUcfirst(prettifystringnames(commodity_one))}` ,
              align: 'left',
              style: {'fontWeight':'bold'},
          },
          subtitle: {
              enabled: true,
              text: `from ${_formatEpochDate(data[0][0])} to ${_formatEpochDate(data[data.length-1][0])}`,
              align: 'left',
              style: {'fontSize':'10px'},
          },
          series: [{
              name: `${jsUcfirst(prettifystringnames(commodity_one))}`,
              data: data,
              tooltip: {
                  valueDecimals: 2
              }
          }],

          yAxis: {
              plotLines: [{
                            value: undervalue,
                            label: {
                                      text:`Buy All Ords`,
                                      style: {'fontSize':'11px', 'color': 'rgba(68,114,196,0.9)',}
                                    },
                            color: 'rgba(68,114,196,0.5)',
                            width: 1,
                            zIndex: 9,
                          },
                          {
                            value: overvalue,
                            label: {
                                      text:`Sell All Ords`,
                                      style: {'fontSize':'11px', 'color': 'rgba(255,80,80,0.9)',}
                                    },
                            color: 'rgba(255,80,80,0.5)',
                            width: 1,
                            zIndex: 9,
                          },
                          ],
          },

          xAxis: {
                    plotBands: [{
                                  color: plotbandcolour, // Color value
                                  from: 120873600000, // Nov 1973
                                  to: 162777600000, // Mar 1975
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 315446400000, // Jan 1980
                                  to: 331171200000, //  June 1980
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 362707200000, // July 1981
                                  to: 404870400000, // Nov 1982
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 646704000000, // July 1990
                                  to: 667699200000, // March 1991
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 867715200000, // July 1997
                                  to: 899251200000, // July 1998
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 983318400000, // March 2001
                                  to: 1004486400000, // Nov 2001
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                {
                                  color: plotbandcolour, // Color value
                                  from: 1196380800000, // Dec 2007
                                  to: 1243728000000, // June 2009
                                  label: {
                                          text:'',
                                          rotation: 90,
                                          align:'left',
                                          style:{"fontSize": "11px"},
                                          y: 3,
                                          x: 3,
                                          color: 'rgb(34,42,53)'       },
                                },
                                ],
                },
      }

    );
  })};
