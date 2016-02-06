window.name = "BoomBoard";
angular.module('boomboard',
  [
    // 'ngAnimate',
    ])
// AWS Controller
.controller('aws_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {

  function sort_by_key (obj) {
    var keys = [];
    var sorted_obj = {};
    for(var key in obj){
        if(obj.hasOwnProperty(key)){
            keys.push(key);
        }
    }
    // sort keys
    keys.sort();
    // create new array based on Sorted Keys
    jQuery.each(keys, function(i, key){
        sorted_obj[key] = obj[key];
    });

    $scope.aws_data_computed.curr_month = keys[keys.length - 1]
    $scope.aws_data_computed.prev_month = keys[keys.length - 2]

    return {"result": sorted_obj, "curr_month": $scope.aws_data_computed.curr_month, "prev_month": $scope.aws_data_computed.prev_month};
  }

  function draw_cost_graph () {
    $('#aws_cost_graph').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: null
        },
        xAxis: {
            allowDecimals: false,
            categories: $scope.aws_data_computed.costs_array["year"],
            labels: {
                formatter: function () {
                    return this.value; // clean, unformatted number for year
                }
            }
        },
        yAxis: {
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            lineWidth: 0,
            minorTickLength: 0,
            tickLength: 0,
            lineColor: 'transparent',
        },
        tooltip: {
            pointFormat: '{series.name} : <strong>$ {point.y:,.0f} </strong>'
        },
        plotOptions: {
            series: {
                fillColor: {
                    linearGradient: [0, 0, 0, 100],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                }
            },
            area: {
                marker: {
                    enabled: false,
                    radius: 3,
                }
            }
        },
        series: [
          { name: 'Total Cost', data: $scope.aws_data_computed.costs_array["total"] },
          { name: 'EC2',  data: $scope.aws_data_computed.costs_array["ec2"] },
          { name: 'RDS',  data: $scope.aws_data_computed.costs_array["rds"] },
          { name: 'REDSHIFT', data: $scope.aws_data_computed.costs_array["rsft"]  },
          { name: 'EMR',  data: $scope.aws_data_computed.costs_array["emr"] }
        ]
    });
  }

  function prepare_cost_graph_data () {
    console.group('Prepare AWS Graph data')
    var sorted_cost_history = sort_by_key( $scope.aws_data_raw.cost_history )
    console.log(sorted_cost_history)
    $scope.aws_data_computed.costs_diff = { "ec2": 0, "rds": 0, "rsft": 0, "emr": 0, "total": 0 }
    $scope.aws_data_computed.costs_now = { "ec2": 0, "rds": 0, "rsft": 0, "emr": 0, "total": 0 }
    $scope.aws_data_computed.costs_array = { "ec2": [], "rds": [], "rsft": [], "emr": [], "total": [], "year": [] }
    for( var year in sorted_cost_history["result"]){
      //key to month-name,yyyy
      var month_year_name = new Date(year).toLocaleString('en-us', { month: "long" }).substring(0,3)+", "+new Date(year).getFullYear()
      $scope.aws_data_computed.costs_array["year"].push(month_year_name)

      if( year.indexOf(sorted_cost_history["curr_month"]) >= 0 ){
        $scope.aws_data_computed.costs_array["ec2"].push($scope.aws_data_raw.predicted_costs["ec2"])
        $scope.aws_data_computed.costs_array["rds"].push($scope.aws_data_raw.predicted_costs["rds"])
        $scope.aws_data_computed.costs_array["rsft"].push($scope.aws_data_raw.predicted_costs["redshift"])
        $scope.aws_data_computed.costs_array["emr"].push($scope.aws_data_raw.predicted_costs["emr"])
        $scope.aws_data_computed.costs_array["total"].push($scope.aws_data_raw.predicted_costs["total"])

        //insert diff data
        var curr_month = $scope.aws_data_computed.curr_month
        var prev_month = $scope.aws_data_computed.prev_month

        $scope.aws_data_computed.costs_diff["ec2"] = ($scope.aws_data_raw.predicted_costs["ec2"]/sorted_cost_history["result"][prev_month]["ec2"]) - 1
        $scope.aws_data_computed.costs_diff["rds"] = ($scope.aws_data_raw.predicted_costs["rds"]/sorted_cost_history["result"][prev_month]["rds"]) - 1
        $scope.aws_data_computed.costs_diff["rsft"] = ($scope.aws_data_raw.predicted_costs["redshift"]/sorted_cost_history["result"][prev_month]["redshift"]) - 1
        $scope.aws_data_computed.costs_diff["emr"] = ($scope.aws_data_raw.predicted_costs["emr"]/sorted_cost_history["result"][prev_month]["emr"]) - 1
        $scope.aws_data_computed.costs_diff["total"] = ($scope.aws_data_raw.predicted_costs["total"]/sorted_cost_history["result"][prev_month]["total"]) - 1

        $scope.aws_data_computed.costs_now["ec2"] = sorted_cost_history["result"][curr_month]["ec2"]
        $scope.aws_data_computed.costs_now["rds"] = sorted_cost_history["result"][curr_month]["rds"]
        $scope.aws_data_computed.costs_now["rsft"] = sorted_cost_history["result"][curr_month]["redshift"]
        $scope.aws_data_computed.costs_now["emr"] = sorted_cost_history["result"][curr_month]["emr"]
        $scope.aws_data_computed.costs_now["total"] = sorted_cost_history["result"][curr_month]["total"]

        $scope.aws_data_computed.prediction_factor = $scope.aws_data_raw.predicted_costs["total"]/sorted_cost_history["result"][curr_month]["total"]

      }else{
        $scope.aws_data_computed.costs_array["ec2"].push(sorted_cost_history["result"][year]["ec2"])
        $scope.aws_data_computed.costs_array["rds"].push(sorted_cost_history["result"][year]["rds"])
        $scope.aws_data_computed.costs_array["rsft"].push(sorted_cost_history["result"][year]["redshift"])
        $scope.aws_data_computed.costs_array["emr"].push(sorted_cost_history["result"][year]["emr"])
        $scope.aws_data_computed.costs_array["total"].push(sorted_cost_history["result"][year]["total"])
      }

    }
    console.log($scope.aws_data_computed)
    console.groupEnd('Prepare AWS Graph data')
  }

  function prepare_system_cost_data () {
    console.group('Prepare AWS System Cost data')

    $scope.aws_data_computed.selected_infra = "total"
    $scope.aws_data_computed.selected_order = "asec"

    for( var system in $scope.aws_data_raw.system_costs ){
      for( var aws_service in $scope.aws_data_raw.system_costs[system] ){
        if( aws_service in $scope.aws_data_computed.infra_costs ){
          $scope.aws_data_computed.infra_costs[aws_service][system] = {}
          $scope.aws_data_computed.infra_costs[aws_service][system]["predicted_costs"] = $scope.aws_data_raw.system_costs[system][aws_service][$scope.aws_data_computed.curr_month]*$scope.aws_data_computed.prediction_factor
          $scope.aws_data_computed.infra_costs[aws_service][system]["diff_costs"] = null
          if($scope.aws_data_raw.system_costs[system][aws_service][$scope.aws_data_computed.prev_month] != undefined )
            $scope.aws_data_computed.infra_costs[aws_service][system]["diff_costs"] =($scope.aws_data_computed.infra_costs[aws_service][system]["predicted_costs"]/$scope.aws_data_raw.system_costs[system][aws_service][$scope.aws_data_computed.prev_month]) - 1
          $scope.aws_data_computed.infra_cost_array[aws_service].push({'system': system, 'predicted_costs': $scope.aws_data_computed.infra_costs[aws_service][system]["predicted_costs"], 'diff_costs': $scope.aws_data_computed.infra_costs[aws_service][system]["diff_costs"]})
        }
      }
    }
    console.log($scope.aws_data_computed)
    console.groupEnd('Prepare AWS System Cost data')
  }

  $scope.adjust_numerics = function adjust_numerics (value, style, threshold) {
    if(isNaN(value))
      return {"value": value, "color":"", "symbol": ""}

    if(parseFloat(value) > parseFloat(threshold) ){
      return {"value": numeral(value).format(style), "color":"#44DA44", "symbol": "▲"}
    }else{
      return {"value": numeral(value).format(style), "color":"#E03030", "symbol": "▼"}
    }

  }

  function prepare_stats_data () {
    $scope.aws_data_computed.costs_this_month = $scope.aws_data_raw.cost_history[$scope.aws_data_computed.curr_month]
  }

  function draw_system_cost_graph (argument) {
    $('#aws_system_cost_graph').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: null
        },
        tooltip: {
            pointFormat: '{series.name}: <b>${point.y:.2f}</b> <br> {point.percentage:.2f}%'
        },
        legend: {
          align: 'right',
          verticalAlign: 'top',
          layout: 'vertical',
          x: -10,
          y: 30
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: "Cost",
            colorByPoint: true,
            data: $scope.aws_data_computed.pie_system_cost_data
            // [
            //   {
            //       name: "Staples US",
            //       y: $scope.boombar_stats_computed.client_array["staples"],
            //       sliced: true,
            //       selected: true
            //   },
            //   {
            //       name: "Homedepot",
            //       y: $scope.boombar_stats_computed.client_array["homedepot"]
            //   },
            //   {
            //       name: "Officedepot",
            //       y: $scope.boombar_stats_computed.client_array["officedepot"]
            //   },
            //   {
            //       name: "Zalando",
            //       y: $scope.boombar_stats_computed.client_array["zalando"]
            //   }
            // ]
        }]
    });
  }

  function prepare_system_cost_graph_data (argument) {
    $scope.aws_data_computed.pie_system_cost_data = []
    var teams = {"CI": 0, "CM": 0, "PO + SS": 0, "DP" :0, "Other": 0}
    teams["CI"] = $scope.aws_data_raw.system_costs["automatcher"]["total"][$scope.aws_data_computed.curr_month]+
                  $scope.aws_data_raw.system_costs["matching"]["total"][$scope.aws_data_computed.curr_month]

    teams["DP"] = $scope.aws_data_raw.system_costs["data_platform_v2"]["total"][$scope.aws_data_computed.curr_month]

    teams["CM"] = $scope.aws_data_raw.system_costs["competitor_monitoring"]["total"][$scope.aws_data_computed.curr_month]+
                  $scope.aws_data_raw.system_costs["product_scraper"]["total"][$scope.aws_data_computed.curr_month]+
                  $scope.aws_data_raw.system_costs["distributed_crawler"]["total"][$scope.aws_data_computed.curr_month]

    teams["PO + SS"] = $scope.aws_data_raw.system_costs["po-sqs"]["total"][$scope.aws_data_computed.curr_month]+
                  $scope.aws_data_raw.system_costs["sku_selector"]["total"][$scope.aws_data_computed.curr_month]+
                  $scope.aws_data_raw.system_costs["price_optimizer"]["total"][$scope.aws_data_computed.curr_month]

    teams["Other"] = $scope.aws_data_computed.costs_this_month['total'] - (teams["CI"] + teams["PO + SS"] + teams["CM"] + teams["DP"])

    for( var system_team in teams){
      $scope.aws_data_computed.pie_system_cost_data.push({"name": system_team, "y": teams[system_team]})
    }
    $scope.aws_data_computed.pie_system_cost_data[0]["sliced"]=true
    $scope.aws_data_computed.pie_system_cost_data[0]["selected"]=true
  }

  $scope.refresh_aws_graph = function refresh_aws_graph (argument) {
    console.group('Refresh AWS Graph')
    $http.get('http://boomboard.rboomerang.com/api/aws-cost').
        success(function(data, status, headers, config) {
          console.log(data)
          if ("error" in data){
            console.error("[BoomBoard] AWS API Failed")
          }
          $scope.aws_data_raw = data.result
          $scope.aws_data_computed = {}
          $scope.aws_data_computed.infra_costs = {"ec2": {}, "rds": {}, "redshift": {}, "emr": {}, "total": {}}
          $scope.aws_data_computed.infra_cost_array = {"ec2": [], "rds": [], "redshift": [], "emr": [], "total": []}

          prepare_cost_graph_data()
          prepare_system_cost_data()
          draw_cost_graph()
          prepare_stats_data()
          prepare_system_cost_graph_data()
          draw_system_cost_graph()
        }).
        error(function(data, status, headers, config) {
          console.error(data)
        });
    console.groupEnd('Refresh AWS Graph')
    $timeout(refresh_aws_graph, 180000); // run every 3 min
  }

  $scope.refresh_aws_graph()
  //globals
  $scope.welcome = "AWS"

}])

// Date Time Controller
.controller('date_time_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
  $scope.tickInterval = 1000 //ms
  $scope.timer={}
  var monthNames = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"];
  var dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

  var tick = function() {
      // $scope.timer.weekday=new Date(Date.now()).toDateString().split(" ")[0] // Wed, Sat
      $scope.timer.weekday=dayNames[new Date(Date.now()).getDay()]
      $scope.timer.day=new Date(Date.now()).toDateString().split(" ")[2] //26
      // $scope.timer.month=new Date(Date.now()).toDateString().split(" ")[1] //Aug
      $scope.timer.month=monthNames[new Date(Date.now()).getMonth()]

      var date_now = new Date(Date.now()).toLocaleTimeString()
      $scope.timer.time_24=date_now.split(':')[0]+":"+date_now.split(':')[1]+" "+date_now.split(' ')[1]
      $timeout(tick, $scope.tickInterval); // reset the timer
      // $('iframe').css("height","350px");
      // $('iframe').contents().find('div.root').css("backgroundColor","#001C33");
  }
  // Start the timer
  tick()
}])

// BoomBar Controller
.controller('boombar_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
  $scope.welcome = "BoomBar"

  function sort_by_key (obj) {
    var keys = [];
    var sorted_obj = {};
    for(var key in obj){
        if(obj.hasOwnProperty(key)){
            keys.push(key);
        }
    }
    // sort keys
    keys.sort();
    // create new array based on Sorted Keys
    jQuery.each(keys, function(i, key){
        sorted_obj[key] = obj[key];
    });
    return sorted_obj;
  }

  function draw_boombar_stats_graph () {
    $('#boombar_stats_graph').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: null
        },
        xAxis: {
            allowDecimals: false,
            categories: $scope.boombar_stats_computed.hits_array["day"],
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
        },
        yAxis: {
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            lineWidth: 0,
            minorTickLength: 0,
            tickLength: 0,
            lineColor: 'transparent',
        },
        tooltip: {
            pointFormat: '{series.name} : <strong>{point.y:,.0f}</strong>'
        },
        plotOptions: {
            series: {
                fillColor: {
                    linearGradient: [0, 0, 0, 135],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                }
            },
            area: {
                marker: {
                    enabled: false,
                    radius: 3,
                }
            }
        },
        series: [
          { name: 'Total Hits', data: $scope.boombar_stats_computed.hits_array["total"] }
        ]
    });
  }

  function draw_boombar_clients_graph () {
    $('#boombar_clients_graph').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: null
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y}</b> <br> {point.percentage:.2f}%'
        },
        legend: {
          align: 'right',
          verticalAlign: 'top',
          layout: 'vertical',
          x: -10,
          y: 30
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: "Hits",
            colorByPoint: true,
            data: [
            {
                name: "Staples US",
                y: $scope.boombar_stats_computed.client_array["staples"],
                sliced: true,
                selected: true
            },
            {
                name: "Homedepot",
                y: $scope.boombar_stats_computed.client_array["homedepot"]
            },
            {
                name: "Officedepot",
                y: $scope.boombar_stats_computed.client_array["officedepot"]
            },
            {
                name: "Zalando",
                y: $scope.boombar_stats_computed.client_array["zalando"]
            }
            ]
        }]
    });
  }

  function prepare_clients_stats_graph_data (argument) {
    $scope.boombar_stats_computed.client_array={"staples": 0, "homedepot": 0, "officedepot": 0, "zalando":0}
    $scope.boombar_stats_computed.client_array["staples"] = $scope.boombar_stats_raw.stats_by_week["week-0"].clients["www.staples.com"]
    $scope.boombar_stats_computed.client_array["homedepot"] = $scope.boombar_stats_raw.stats_by_week["week-0"].clients["www.homedepot.com"]
    $scope.boombar_stats_computed.client_array["officedepot"] = $scope.boombar_stats_raw.stats_by_week["week-0"].clients["www.officedepot.com"]
    $scope.boombar_stats_computed.client_array["zalando"] = $scope.boombar_stats_raw.stats_by_week["week-0"].clients["www.zalando.de"]
  }

  function prepare_stats_graph_data () {
    console.group('Prepare Data BoomBar Graph')
    $scope.boombar_stats_computed.hits_array={"total": [], "day": []}
    sorted_by_day = sort_by_key($scope.boombar_stats_raw["hits_by_date"])
    for( var day in sorted_by_day){
      $scope.boombar_stats_computed.hits_array["total"].push(sorted_by_day[day])
      //convert day to dd:mm
      var cust_day = new Date(day).toDateString().split(" ")
      $scope.boombar_stats_computed.hits_array["day"].push(cust_day[2]+", "+cust_day[1])
    }
    console.log($scope.boombar_stats_computed.hits_array)
    console.groupEnd('Prepare Data BoomBar Graph')
  }

  function prepare_stats_data () {
    // total hits + inc/dec
    // total user-NB + inc/dec
    // compact-expansion + inc/dec
    // total clients used + inc/dec
    console.group('Prepare Stats BoomBar')

    $scope.boombar_stats_computed.total_hits={"week-0": 0, "week-1": 0, "week-2": 0, "week-3": 0}
    $scope.boombar_stats_computed.unique_nb_users={"week-0": [], "week-1": [], "week-2": [], "week-3": []}
    $scope.boombar_stats_computed.expand_action={"week-0": {"compact":0, "expand":0, "conversion": 0.00}, "week-1": {"compact":0, "expand":0, "conversion": 0.00}, "week-2": {"compact":0, "expand":0, "conversion": 0.00}, "week-3": {"compact":0, "expand":0, "conversion": 0.00}}
    $scope.boombar_stats_computed.total_clients={"week-0": [], "week-1": [], "week-2": [], "week-3": []}

    for( var week in $scope.boombar_stats_raw["stats_by_week"] ){
      //total hits
      $scope.boombar_stats_computed.total_hits[week] = $scope.boombar_stats_raw["stats_by_week"][week]["total"]
      // conversions
      $scope.boombar_stats_computed.expand_action[week] = { "compact":$scope.boombar_stats_raw["stats_by_week"][week]["action"]["viewCompact"],
                                                            "expand":$scope.boombar_stats_raw["stats_by_week"][week]["action"]["viewExpanded"],
                                                            "conversion": $scope.boombar_stats_raw["stats_by_week"][week]["action"]["viewExpanded"]*100/$scope.boombar_stats_raw["stats_by_week"][week]["action"]["viewCompact"],}
      // non-zero clients
      for( var client in $scope.boombar_stats_raw["stats_by_week"][week]["clients"] ){
        if( $scope.boombar_stats_raw["stats_by_week"][week]["clients"][client] > 0 )
          $scope.boombar_stats_computed.total_clients[week].push(client)
      }
      // nob-boomerang users
      for( var user in $scope.boombar_stats_raw["stats_by_week"][week]["users"] ){
        if( user.indexOf('@boomerangcommerce.com') < 0 &&
          user.indexOf('venkata') < 0 &&
          user.indexOf('haider') < 0)
          $scope.boombar_stats_computed.unique_nb_users[week].push(user)
      }
    }
    console.log($scope.boombar_stats_computed)
    console.groupEnd('Prepare Stats BoomBar')
  }

  $scope.adjust_numerics = function adjust_numerics (value, style, threshold) {

    var return_attr = {"value": value, "color":"", "symbol": ""}
    if(isNaN(value)){
      return return_attr
    }
    if(parseFloat(value) > parseFloat(threshold) ){
      return_attr = {"value": numeral(value).format(style), "color":"#44DA44", "symbol": "▲"}
    }else{
      return_attr = {"value": numeral(value).format(style), "color":"#E03030", "symbol": "▼"}
    }
    return return_attr
  }

  $scope.refresh_boombar_stats = function refresh_boombar_stats (argument) {
    console.group('Refresh BoomBar Graph')
    $http.get('http://boomboard.rboomerang.com/api/boombar').
        success(function(data, status, headers, config) {
          console.log(data)
          if ("error" in data){
            console.error("[BoomBoard] BoomBar API Failed")
          }
          $scope.boombar_stats_raw = data.result
          $scope.boombar_stats_computed={}
          prepare_stats_graph_data()
          draw_boombar_stats_graph()
          prepare_stats_data()
          prepare_clients_stats_graph_data()
          draw_boombar_clients_graph()
        }).
        error(function(data, status, headers, config) {
          console.error(data)
        });
    console.groupEnd('Refresh BoomBar Graph')
    $timeout(refresh_boombar_stats, 180000); // run every 3 min
  }

  $scope.refresh_boombar_stats()
}])

// Code Commit Controller
.controller('code_commit_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {

  function sort_by_key (obj) {
    var keys = [];
    var sorted_obj = {};
    for(var key in obj){
        if(obj.hasOwnProperty(key)){
            keys.push(key);
        }
    }
    // sort keys
    keys.sort();
    // create new array based on Sorted Keys
    jQuery.each(keys, function(i, key){
        sorted_obj[key] = obj[key];
    });
    return sorted_obj;
  }

  function draw_code_commit_graph () {
    $('#code_commit_stats_graph').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: null
        },
        xAxis: {
            allowDecimals: false,
            categories: $scope.code_commit_stats_computed.commit_array["day"],
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
        },
        yAxis: {
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            lineWidth: 0,
            minorTickLength: 0,
            tickLength: 0,
            lineColor: 'transparent',
        },
        tooltip: {
            pointFormat: '{series.name} : <strong>{point.y:,.0f} </strong>'
        },
        plotOptions: {
            series: {
                fillColor: {
                    linearGradient: [0, 0, 0, 125],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                }
            },
            area: {
                marker: {
                    enabled: false,
                    radius: 3,
                }
            }
        },
        series: [
          { name: 'Total Commits', data: $scope.code_commit_stats_computed.commit_array["total"] },
          { name: 'REPOS',  data: $scope.code_commit_stats_computed.commit_array["repos"] },
          { name: 'USERS',  data: $scope.code_commit_stats_computed.commit_array["users"] }
        ]
    });
  }

  function prepare_stats_graph_data () {
    $scope.code_commit_stats_computed.commit_array={"total":[], "repos":[], "users":[], "day": []}
    sorted_obj = sort_by_key($scope.code_commit_stats_raw.stats_by_date)
    for( var day in sorted_obj){
      $scope.code_commit_stats_computed.commit_array["repos"].push(sorted_obj[day]["repos"])
      $scope.code_commit_stats_computed.commit_array["total"].push(sorted_obj[day]["total_commits"])
      $scope.code_commit_stats_computed.commit_array["users"].push(sorted_obj[day]["users"])
      var date = day.split("-")[2]+"-"+day.split("-")[1]+"-"+day.split("-")[0]
      var cust_day = new Date(date).toDateString().split(" ")
      $scope.code_commit_stats_computed.commit_array["day"].push(cust_day[2]+", "+cust_day[1])
    }
  }

  $scope.adjust_numerics = function adjust_numerics (value, style, threshold) {

    var return_attr = {"value": value, "color":"", "symbol": ""}
    if(isNaN(value)){
      return return_attr
    }
    if(parseFloat(value) > parseFloat(threshold) ){
      return_attr = {"value": numeral(value).format(style), "color":"#44DA44", "symbol": "▲"}
    }else{
      return_attr = {"value": numeral(value).format(style), "color":"#E03030", "symbol": "▼"}
    }
    return return_attr
  }

  function prepare_stats_data () {
    // total commits - inc/dec
    // total repos - inc/dec
    // total users - inc/dec
    // total commit/user - inc/dec
    console.group('Refresh Code Commit Graph')
    for( var week in $scope.code_commit_stats_raw.stats_by_week ){
      $scope.code_commit_stats_computed.metrics.total_commits[week] = $scope.code_commit_stats_raw.stats_by_week[week]["commits"]
      $scope.code_commit_stats_computed.metrics.total_repos[week] = $scope.code_commit_stats_raw.stats_by_week[week]["repos"]
      $scope.code_commit_stats_computed.metrics.total_users[week] = $scope.code_commit_stats_raw.stats_by_week[week]["users"]
      $scope.code_commit_stats_computed.metrics.commit_per_user[week] = $scope.code_commit_stats_raw.stats_by_week[week]["commits"]/$scope.code_commit_stats_raw.stats_by_week[week]["users"]
    }
    console.log($scope.code_commit_stats_computed.metrics)
    console.groupEnd('Refresh Code Commit Graph')
  }

  $scope.refresh_code_commit_stats = function refresh_code_commit_stats (argument) {
    console.group('Refresh Code Commit Graph')
    $http.get('http://boomboard.rboomerang.com/api/code_commit').
        success(function(data, status, headers, config) {
          console.log(data)
          if ("error" in data){
            console.error("[BoomBoard] BoomBar API Failed")
          }
          $scope.code_commit_stats_raw = data.result
          $scope.code_commit_stats_computed={}
          prepare_stats_graph_data()
          draw_code_commit_graph()
          $scope.code_commit_stats_computed.metrics = { "total_commits":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                        "total_repos":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                        "total_users":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                        "commit_per_user":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                      }
          prepare_stats_data()
        }).
        error(function(data, status, headers, config) {
          console.error(data)
        });
    console.groupEnd('Refresh Code Commit Graph')
    $timeout(refresh_code_commit_stats, 180000); // run every 3 min
  }

  $scope.refresh_code_commit_stats()
}])

// VUI Controller
.controller('vui_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {

  function sort_by_key (obj) {
    var keys = [];
    var sorted_obj = {};
    for(var key in obj){
        if(obj.hasOwnProperty(key)){
            keys.push(key);
        }
    }
    // sort keys
    keys.sort();
    // create new array based on Sorted Keys
    jQuery.each(keys, function(i, key){
        sorted_obj[key] = obj[key];
    });
    return sorted_obj;
  }

  function draw_vui_graph () {
    $('#vui_stats_graph').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: null
        },
        xAxis: {
            allowDecimals: false,
            categories: $scope.vui_stats_computed.validation_array["day"],
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
        },
        yAxis: {
            labels: {
                enabled: false
            },
            title: {
                text: null
            },
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            lineWidth: 0,
            minorTickLength: 0,
            tickLength: 0,
            lineColor: 'transparent',
        },
        tooltip: {
            pointFormat: '{series.name} : <strong>{point.y:,.0f} </strong>'
        },
        plotOptions: {
            series: {
                fillColor: {
                    linearGradient: [0, 0, 0, 125],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                }
            },
            area: {
                marker: {
                    enabled: false,
                    radius: 3,
                }
            }
        },
        series: [
          { name: 'Total Validations', data: $scope.vui_stats_computed.validation_array["total"] },
          { name: 'CLIENTS',  data: $scope.vui_stats_computed.validation_array["clients"] },
          { name: 'USERS',  data: $scope.vui_stats_computed.validation_array["users"] }
        ]
    });
  }

  function draw_vui_clients_graph () {
    $('#vui_clients_graph').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: null
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y}</b> <br> {point.percentage:.2f}%'
        },
        legend: {
          align: 'right',
          verticalAlign: 'top',
          layout: 'vertical',
          x: -10,
          y: 30
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: "Hits",
            colorByPoint: true,
            data: $scope.vui_stats_computed.pie_client_data
            // [
            //   {
            //       name: "Staples US",
            //       y: $scope.boombar_stats_computed.client_array["staples"],
            //       sliced: true,
            //       selected: true
            //   },
            //   {
            //       name: "Homedepot",
            //       y: $scope.boombar_stats_computed.client_array["homedepot"]
            //   },
            //   {
            //       name: "Officedepot",
            //       y: $scope.boombar_stats_computed.client_array["officedepot"]
            //   },
            //   {
            //       name: "Zalando",
            //       y: $scope.boombar_stats_computed.client_array["zalando"]
            //   }
            // ]
        }]
    });
  }

  function prepare_stats_graph_data (argument) {
    console.group('Prepare Data VUI Graph')
    $scope.vui_stats_computed.validation_array={ "total": [], "clients": [], "users": [], "day": [] }
    sorted_obj = sort_by_key($scope.vui_stats_raw.stats_by_day)
    for( var day in sorted_obj){
      $scope.vui_stats_computed.validation_array.total.push(sorted_obj[day]["validations"])
      $scope.vui_stats_computed.validation_array.users.push(sorted_obj[day]["users"])
      $scope.vui_stats_computed.validation_array.clients.push(sorted_obj[day]["clients"])
      var cust_day = new Date(day).toDateString().split(" ")
      $scope.vui_stats_computed.validation_array.day.push(cust_day[2]+", "+cust_day[1])
    }
    console.log($scope.vui_stats_computed.validation_array)
    console.groupEnd('Prepare Data VUI Graph')
  }

  function prepare_stats_pie_data (argument) {
    $scope.vui_stats_computed.pie_client_data = []
    for( var client in $scope.vui_stats_raw.stats_by_week["week-0"]["clients_dist"]){
      $scope.vui_stats_computed.pie_client_data.push({"name": client.toUpperCase(),
                                                      "y": $scope.vui_stats_raw.stats_by_week["week-0"]["clients_dist"][client]})
    }
    $scope.vui_stats_computed.pie_client_data[0]["sliced"]=true
    $scope.vui_stats_computed.pie_client_data[0]["selected"]=true
  }

  $scope.adjust_numerics = function adjust_numerics (value, style, threshold) {

    var return_attr = {"value": value, "color":"", "symbol": ""}
    if(isNaN(value)){
      return return_attr
    }
    if(parseFloat(value) > parseFloat(threshold) ){
      return_attr = {"value": numeral(value).format(style), "color":"#44DA44", "symbol": "▲"}
    }else{
      return_attr = {"value": numeral(value).format(style), "color":"#E03030", "symbol": "▼"}
    }
    return return_attr
  }

  function prepare_stats_data (argument) {
    console.group('Prepare VUI Stats')
    for(var week in $scope.vui_stats_raw.stats_by_week){
      $scope.vui_stats_computed.metrics.total_validations[week] = $scope.vui_stats_raw.stats_by_week[week]["validations"]
      $scope.vui_stats_computed.metrics.total_clients[week] = $scope.vui_stats_raw.stats_by_week[week]["clients"]
      $scope.vui_stats_computed.metrics.total_users[week] = $scope.vui_stats_raw.stats_by_week[week]["users"]
      $scope.vui_stats_computed.metrics.validations_per_user[week] = $scope.vui_stats_raw.stats_by_week[week]["validations"]/$scope.vui_stats_raw.stats_by_week[week]["users"]
    }
    console.log($scope.vui_stats_computed.metrics)
    console.group('Prepare VUI Stats')
  }

  $scope.refresh_vui_stats = function refresh_vui_stats (argument) {
    console.group('Refresh VUI Graph')
    $http.get('http://boomboard.rboomerang.com/api/vui').
        success(function(data, status, headers, config) {
          console.log(data)
          if ("error" in data){
            console.error("[BoomBoard] VUI API Failed")
          }
          $scope.vui_stats_raw = data.result
          $scope.vui_stats_computed={}
          prepare_stats_graph_data()
          draw_vui_graph()
          $scope.vui_stats_computed.metrics = { "total_validations":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                        "total_clients":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                        "total_users":{"week-0":0, "week-1":0, "week-2":0, "week-3":0,},
                                                        "validations_per_user":{"week-0":0.0, "week-1":0.0, "week-2":0.0, "week-3":0.0,},
                                                      }
          prepare_stats_data()
          prepare_stats_pie_data()
          draw_vui_clients_graph()

        }).
        error(function(data, status, headers, config) {
          console.error(data)
        });
    console.groupEnd('Refresh VUI Graph')
    $timeout(refresh_vui_stats, 180000); // run every 3 min
  }

  $scope.refresh_vui_stats()

}])

// Date Time Controller
.controller('twitter_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
  $scope.tickInterval = 1000 //ms
  var tick = function() {
      $('iframe').css("height","300px");
      $('iframe').css("margin-left","8%");
      $('iframe').contents().find('div.root').css("backgroundColor","#001C33");
      $('iframe').contents().find('div.timeline-header').css("display","none");
      $('iframe').contents().find('div.stream').css("height","300px");
      $scope.tickInterval += 100
      $timeout(tick, $scope.tickInterval); // reset the timer
  }
  // Start the timer
  tick()
}]);