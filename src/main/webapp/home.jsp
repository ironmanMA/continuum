<%@page import='com.boomerang.config.AppConfigUtil'%>
<%@page import='java.io.*, java.util.Date, java.util.Enumeration'%>
<%@page contentType='text/html' pageEncoding='UTF-8'%>

<%
  final String login_page = "/dashboard/index.jsp";
  final String home_page = "/dashboard/home.jsp";
  final String logout_page = "/dashboard/logout.jsp";
  final String profile_page = "/dashboard";
  final String date_number_string = ""+session.getAttribute("date_string");

      try
      {
        if( !session.getAttribute("authorized").equals("true") ){
              response.sendRedirect( logout_page );
        }
      }
      catch(Exception e)
      {
            session.removeAttribute("authorized");
              response.sendRedirect( logout_page );
      }
      AppConfigUtil configuration = new AppConfigUtil();
 %>

<html ng-app="boomboard">
<head>
	<title>BoomBoard | Operations Dashboard</title>

	<link rel="stylesheet" href="assets/css/3P/bootstrap/css/bootstrap.css">
	<link rel="stylesheet" href="assets/css/main.css<%out.print(date_number_string);%>">
	<link rel="stylesheet" href="assets/css/widget-style.css<%out.print(date_number_string);%>">

	<script src="assets/js/jQuery.js"></script>
  <script src="assets/js/numeral.js"></script>
	<script src="assets/js/angular.js"></script>
	<script src="assets/js/main_ctrl.js<%out.print(date_number_string);%>" ></script>
	<script src="assets/js/highcharts.js" ></script>
	<script src="assets/js/dark-arvo.js" ></script>
  <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>

  <style type="text/css">
    ::-webkit-scrollbar {
        width: 3px;
    }
    ::-webkit-scrollbar-track {
        background-color: #001C33;
        border-left: 2px solid #001C33;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #173B58;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: #112C42;
    }
  </style>

</head>
<body style="background-color:#001C33; color: white;">

<div class="row">
  <div id="aws_cost_curr_stats" class="col-xs-9" ng-controller="aws_ctrl" style="background-color: #04213A;">
    <div class="panel" style="border-radius: 0px; background-color: #001C33;">
      <div class="panel-heading" style="padding: 5px;">
        <h3 class="panel-title" style="font-size: 20px; font-weight: 100;">AWS Costs</h3>
      </div>
      <div class="panel-body" style="padding: 5px;">
        <div class="row text-center">
          <!-- show current stats -->

          <div class="col-xs-3" >
            <!-- total costs -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(aws_data_raw.predicted_costs["total"], '$0,0.00', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <span ng-style="{ 'color' : adjust_numerics(aws_data_computed.costs_diff['total'], '0.00%', 0).color}">
                {{adjust_numerics(aws_data_computed.costs_diff['total'], '0.00%', 0).symbol}} {{adjust_numerics(aws_data_computed.costs_diff['total'], '0.00%', 0).value}}
              </span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> TOTAL
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- ec2 costs -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(aws_data_raw.predicted_costs["ec2"], '$0,0.00', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <span ng-style="{ 'color' : adjust_numerics(aws_data_computed.costs_diff['ec2'], '0.00%', 0).color}">
                {{adjust_numerics(aws_data_computed.costs_diff['ec2'], '0.00%', 0).symbol}} {{adjust_numerics(aws_data_computed.costs_diff['ec2'], '0.00%', 0).value}}
              </span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#74CF7C">&#9679;</span> EC2
            </span>
          </div>
          <div class="col-xs-3" >
            <!-- rds costs -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(aws_data_raw.predicted_costs["rds"], '$0,0.00', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <span ng-style="{ 'color' : adjust_numerics(aws_data_computed.costs_diff['rds'], '0.00%', 0).color }">
                {{adjust_numerics(aws_data_computed.costs_diff['rds'], '0.00%', 0).symbol}} {{adjust_numerics(aws_data_computed.costs_diff['rds'], '0.00%', 0).value}}
              </span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#D47863">&#9679;</span> RDS
            </span>
          </div>
          <div class="col-xs-3" >
            <!-- untagged costs -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(aws_data_computed.infra_costs["total"]["untagged"]["predicted_costs"], '$0,0.00', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <span ng-style="{ 'color' : adjust_numerics(aws_data_computed.infra_costs['total']['untagged']['diff_costs'], '0.00%', 0).color }">
                {{adjust_numerics(aws_data_computed.infra_costs['total']['untagged']['diff_costs'], '0.00%', 0).symbol}} {{adjust_numerics(aws_data_computed.infra_costs['total']['untagged']['diff_costs'], '0.00%', 0).value}}
              </span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#A3D6DC">&#9679;</span> UNTAGGED
            </span>
          </div>
        </div>

        <div class="row" style="max-height: 200px">
          <div class="col-xs-12" >
            <div class="row" >
              <div id="aws_cost_graph" class="col-xs-5" style="height: 200px">
                <!-- plot graph for costs -->
              </div>
              <div class="col-xs-3" style="height: 200px">
                <div class="row" >
                  <div class="col-xs-6" style="padding: 10px; font-size: 1.5em; color: #A0A0A0;" >
                    This Month
                  </div>

                  <!-- <div class="col-xs-6" >
                    <span class="aws-curr-cost" >
                      {{adjust_numerics(aws_data_computed.costs_this_month['total'], '$0,0.00', 0).value}}
                    </span>
                    <br>
                    <span class="aws-facet-name" >
                      <span style="color:#207378">&#9679;</span> TOTAL
                    </span>
                  </div> -->

                </div>
                <!-- plot curr stats -->
                <div class="row" >
                  <div class="col-xs-6" >
                    <span class="aws-curr-cost" >
                      {{adjust_numerics(aws_data_computed.costs_this_month['ec2'], '$0,0.00', 0).value}}
                    </span>
                    <br>
                    <span class="aws-facet-name" >
                      <span style="color:#207378">&#9679;</span> EC2
                    </span>
                  </div>

                  <div class="col-xs-6" >
                    <span class="aws-curr-cost" >
                      {{adjust_numerics(aws_data_computed.costs_this_month['rds'], '$0,0.00', 0).value}}
                    </span>
                    <br>
                    <span class="aws-facet-name" >
                      <span style="color:#207378">&#9679;</span> RDS
                    </span>
                  </div>

                  <div class="col-xs-6" >
                    <span class="aws-curr-cost" >
                      {{adjust_numerics(aws_data_computed.costs_this_month['redshift'], '$0,0.00', 0).value}}
                    </span>
                    <br>
                    <span class="aws-facet-name" >
                      <span style="color:#207378">&#9679;</span> REDSHIFT
                    </span>
                  </div>

                  <div class="col-xs-6" >
                    <span class="aws-curr-cost" >
                      {{adjust_numerics(aws_data_computed.costs_this_month['emr'], '$0,0.00', 0).value}}
                    </span>
                    <br>
                    <span class="aws-facet-name" >
                      <span style="color:#207378">&#9679;</span> EMR
                    </span>
                  </div>

                </div>
              </div>
              <div id="aws_system_cost_graph" class="col-xs-4" style="height: 200px">
                <!-- plot pie graph for costs -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="curr_date_time" class="col-xs-3" ng-controller="date_time_ctrl" style=" background-color: #04213A; height: 330px;">
    <div class="panel" style="border-radius: 0px; background-color: #001C33;">
      <div class="panel-heading" style="padding: 5px; text-align: left;">
        <h3 class="panel-title" style="font-size: 20px; font-weight: 100;">Time</h3>
      </div>
      <div class="panel-body" style="padding: 20px; text-align: left;">
        <div class="row" >
          <div class="col-xs-12" style="color:#A0A0A0; font-size: 5em;font-weight: 100; font-weight: bold;">
            <!-- week day -->
            {{timer.weekday}}
          </div>
        </div>
        <div class="row" >
          <div class="col-xs-12" style="color:#A0A0A0;font-size: 4em;font-weight: 100;">
            <!-- time with day, month -->
            {{timer.day}}, {{timer.month}}
          </div>
        </div>
        <div class="row" >
          <div class="col-xs-12" style="color:white;font-size: 2.5em;font-weight: 100;">
            <!-- time with hh:mm -->
            {{timer.time_24}}
          </div>
        </div>
      </div>
    </div>
    {{welcome}}
  </div>
</div>

<div class="row" ng-if="true" >
  <div id="boombar_stats" class="col-xs-6" ng-controller="boombar_ctrl" style="background-color: #04213A;">
    <div class="panel" style="border-radius: 0px; background-color: #001C33;">
      <div class="panel-heading" style="padding: 5px; text-align: left;">
        <h3 class="panel-title" style="font-size: 20px; font-weight: 100;">Boombar</h3>
      </div>
      <div class="panel-body">
        <div class="row text-center">
          <!-- metric snippets daalo idhar -->
          <div class="col-xs-3" >
            <!-- total hits this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(boombar_stats_computed.total_hits['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((boombar_stats_computed.total_hits['week-1']-boombar_stats_computed.total_hits['week-2'])/boombar_stats_computed.total_hits['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((boombar_stats_computed.total_hits['week-1']-boombar_stats_computed.total_hits['week-2'])/boombar_stats_computed.total_hits['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((boombar_stats_computed.total_hits['week-1']-boombar_stats_computed.total_hits['week-2'])/boombar_stats_computed.total_hits['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> TOTAL
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total user-NB + inc/dec -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(boombar_stats_computed.expand_action['week-1']['conversion']/100, '00.00%', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((boombar_stats_computed.expand_action['week-1']['conversion']-boombar_stats_computed.expand_action['week-2']['conversion'])/boombar_stats_computed.expand_action['week-2']['conversion'], '0.00%', 0).color }">
                {{adjust_numerics((boombar_stats_computed.expand_action['week-1']['conversion']-boombar_stats_computed.expand_action['week-2']['conversion'])/boombar_stats_computed.expand_action['week-2']['conversion'], '0.00%', 0).symbol}} 
                {{adjust_numerics((boombar_stats_computed.expand_action['week-1']['conversion']-boombar_stats_computed.expand_action['week-2']['conversion'])/boombar_stats_computed.expand_action['week-2']['conversion'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> EXPAND
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total clients used + inc/dec -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(boombar_stats_computed.total_clients['week-1'].length, '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((boombar_stats_computed.total_clients['week-1'].length-boombar_stats_computed.total_clients['week-2'].length)/boombar_stats_computed.total_clients['week-2'].length, '0.00%', 0).color }">
                {{adjust_numerics((boombar_stats_computed.total_clients['week-1'].length-boombar_stats_computed.total_clients['week-2'].length)/boombar_stats_computed.total_clients['week-2'].length, '0.00%', 0).symbol}} {{adjust_numerics((boombar_stats_computed.total_clients['week-1'].length-boombar_stats_computed.total_clients['week-2'].length)/boombar_stats_computed.total_clients['week-2'].length, '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> CLIENTS
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total uniq users used + inc/dec -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(boombar_stats_computed.total_clients['week-1'].length, '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((boombar_stats_computed.unique_nb_users['week-1'].length-boombar_stats_computed.unique_nb_users['week-2'].length)/boombar_stats_computed.unique_nb_users['week-2'].length, '0.00%', 0).color }">
                {{adjust_numerics((boombar_stats_computed.unique_nb_users['week-1'].length-boombar_stats_computed.unique_nb_users['week-2'].length)/boombar_stats_computed.unique_nb_users['week-2'].length, '0.00%', 0).symbol}} {{adjust_numerics((boombar_stats_computed.unique_nb_users['week-1'].length-boombar_stats_computed.unique_nb_users['week-2'].length)/boombar_stats_computed.unique_nb_users['week-2'].length, '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> USERS
            </span>
          </div>
        </div>
        <div class="row">
          <!-- graph dalo idhar -->
          <div id="boombar_stats_graph" class="col-xs-5" style="height: 200px">
          </div>
          <div class="col-xs-3" style="height: 200px;">
            <!-- Curr Stats -->
            <div class="row" style="padding: 10px; font-size: 1.5em; color: #A0A0A0;" >
              This Week
            </div>
            <div class="row" >
              <div class="col-xs-6" >
                <!-- total hits this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(boombar_stats_computed.total_hits['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> TOTAL
                </span>
              </div>
              <div class="col-xs-6" >
                <!-- total user-NB + inc/dec -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(boombar_stats_computed.expand_action['week-0']['conversion']/100, '00.00%', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> EXPAND
                </span>
              </div>
              <div class="col-xs-6" >
                <!-- total clients used + inc/dec -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(boombar_stats_computed.total_clients['week-1'].length, '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> CLIENTS
                </span>
              </div>
              <div class="col-xs-6" >
                <!-- total uniq users used + inc/dec -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(boombar_stats_computed.total_clients['week-1'].length, '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> USERS
                </span>
              </div>
            </div>
          </div>
          <div id="boombar_clients_graph" class="col-xs-4" style="height: 200px;">
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="code_commit_stats" class="col-xs-6" ng-controller="code_commit_ctrl" style="background-color: #04213A;">
    <div class="panel" style="border-radius: 0px; background-color: #001C33;">
      <div class="panel-heading" style="padding: 5px; text-align: left;">
        <h3 class="panel-title" style="font-size: 20px; font-weight: 100;">Code Commits</h3>
      </div>
      <div class="panel-body">
        <div class="row text-center">

          <div class="col-xs-3" >
            <!-- total commits this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(code_commit_stats_computed.metrics.total_commits['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((code_commit_stats_computed.metrics.total_commits['week-1']-code_commit_stats_computed.metrics.total_commits['week-2'])/code_commit_stats_computed.metrics.total_commits['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((code_commit_stats_computed.metrics.total_commits['week-1']-code_commit_stats_computed.metrics.total_commits['week-2'])/code_commit_stats_computed.metrics.total_commits['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((code_commit_stats_computed.metrics.total_commits['week-1']-code_commit_stats_computed.metrics.total_commits['week-2'])/code_commit_stats_computed.metrics.total_commits['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> TOTAL
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total users this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(code_commit_stats_computed.metrics.total_users['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((code_commit_stats_computed.metrics.total_users['week-1']-code_commit_stats_computed.metrics.total_users['week-2'])/code_commit_stats_computed.metrics.total_users['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((code_commit_stats_computed.metrics.total_users['week-1']-code_commit_stats_computed.metrics.total_users['week-2'])/code_commit_stats_computed.metrics.total_users['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((code_commit_stats_computed.metrics.total_users['week-1']-code_commit_stats_computed.metrics.total_users['week-2'])/code_commit_stats_computed.metrics.total_users['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> USERS
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total Repos this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(code_commit_stats_computed.metrics.total_repos['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((code_commit_stats_computed.metrics.total_repos['week-1']-code_commit_stats_computed.metrics.total_repos['week-2'])/code_commit_stats_computed.metrics.total_repos['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((code_commit_stats_computed.metrics.total_repos['week-1']-code_commit_stats_computed.metrics.total_repos['week-2'])/code_commit_stats_computed.metrics.total_repos['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((code_commit_stats_computed.metrics.total_repos['week-1']-code_commit_stats_computed.metrics.total_repos['week-2'])/code_commit_stats_computed.metrics.total_repos['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> REPOS
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total code speed this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(code_commit_stats_computed.metrics.commit_per_user['week-1'], '0.00', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((code_commit_stats_computed.metrics.commit_per_user['week-1']-code_commit_stats_computed.metrics.commit_per_user['week-2'])/code_commit_stats_computed.metrics.commit_per_user['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((code_commit_stats_computed.metrics.commit_per_user['week-1']-code_commit_stats_computed.metrics.commit_per_user['week-2'])/code_commit_stats_computed.metrics.commit_per_user['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((code_commit_stats_computed.metrics.commit_per_user['week-1']-code_commit_stats_computed.metrics.commit_per_user['week-2'])/code_commit_stats_computed.metrics.commit_per_user['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> CODE SPEED
            </span>
          </div>

        </div>
        <div class="row">
          <div id="code_commit_stats_graph" class="col-xs-7" style="height: 200px">
          </div>
          <div class="col-xs-5" style="height: 200px">
            <!-- this weeks stats -->
            <div class="row" style="padding: 10px; font-size: 1.5em; color: #A0A0A0;" >
              This Week
            </div>
            <div class="row" >
              <div class="col-xs-6" >
                <!-- total hits this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(code_commit_stats_computed.metrics.total_commits['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> TOTAL
                </span>
              </div>

              <div class="col-xs-6" >
                <!-- total users this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(code_commit_stats_computed.metrics.total_users['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> USERS
                </span>
              </div>

              <div class="col-xs-6" >
                <!-- total Repos this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(code_commit_stats_computed.metrics.total_repos['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> REPOS
                </span>
              </div>

              <div class="col-xs-6" >
                <!-- total code speed this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(code_commit_stats_computed.metrics.commit_per_user['week-0'], '0.00', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> CODE SPEED
                </span>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>

<div class="row" ng-if="true" >
  <div id="vui_stats" class="col-xs-8" ng-controller="vui_ctrl">
    <div class="panel" style="border-radius: 0px; background-color: #001C33;">
      <div class="panel-heading" style="padding: 5px; text-align: left;">
        <h3 class="panel-title" style="font-size: 20px; font-weight: 100;">VUI</h3>
      </div>
      <div class="panel-body">
        <div class="row text-center">

          <div class="col-xs-3" >
            <!-- total hits this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(vui_stats_computed.metrics.total_validations['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((vui_stats_computed.metrics.total_validations['week-1']-vui_stats_computed.metrics.total_validations['week-2'])/vui_stats_computed.metrics.total_validations['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((vui_stats_computed.metrics.total_validations['week-1']-vui_stats_computed.metrics.total_validations['week-2'])/vui_stats_computed.metrics.total_validations['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((vui_stats_computed.metrics.total_validations['week-1']-vui_stats_computed.metrics.total_validations['week-2'])/vui_stats_computed.metrics.total_validations['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> TOTAL
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total hits this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(vui_stats_computed.metrics.total_users['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((vui_stats_computed.metrics.total_users['week-1']-vui_stats_computed.metrics.total_users['week-2'])/vui_stats_computed.metrics.total_users['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((vui_stats_computed.metrics.total_users['week-1']-vui_stats_computed.metrics.total_users['week-2'])/vui_stats_computed.metrics.total_users['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((vui_stats_computed.metrics.total_users['week-1']-vui_stats_computed.metrics.total_users['week-2'])/vui_stats_computed.metrics.total_users['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> USERS
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total hits this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(vui_stats_computed.metrics.total_clients['week-1'], '0,0', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((vui_stats_computed.metrics.total_clients['week-1']-vui_stats_computed.metrics.total_clients['week-2'])/vui_stats_computed.metrics.total_clients['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((vui_stats_computed.metrics.total_clients['week-1']-vui_stats_computed.metrics.total_clients['week-2'])/vui_stats_computed.metrics.total_clients['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((vui_stats_computed.metrics.total_clients['week-1']-vui_stats_computed.metrics.total_clients['week-2'])/vui_stats_computed.metrics.total_clients['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> CLIENTS
            </span>
          </div>

          <div class="col-xs-3" >
            <!-- total hits this week -->
            <span class="aws-curr-cost" >
              {{adjust_numerics(vui_stats_computed.metrics.validations_per_user['week-1'], '0.00', 0).value}}
            </span>
            <br>
            <span class="aws-diff-cost" >
              <!-- up -->
              <span ng-style="{ 'color' : adjust_numerics((vui_stats_computed.metrics.validations_per_user['week-1']-vui_stats_computed.metrics.validations_per_user['week-2'])/vui_stats_computed.metrics.validations_per_user['week-2'], '0.00%', 0).color }">
                {{adjust_numerics((vui_stats_computed.metrics.validations_per_user['week-1']-vui_stats_computed.metrics.validations_per_user['week-2'])/vui_stats_computed.metrics.validations_per_user['week-2'], '0.00%', 0).symbol}} {{adjust_numerics((vui_stats_computed.metrics.validations_per_user['week-1']-vui_stats_computed.metrics.validations_per_user['week-2'])/vui_stats_computed.metrics.validations_per_user['week-2'], '0.00%', 0).value}}</span>
            </span>
            <span class="aws-facet-name" >
              <span style="color:#207378">&#9679;</span> WORK SPEED
            </span>
          </div>

        </div>
        <div class="row">
          <div id="vui_stats_graph" class="col-xs-5" style="height: 200px">
          </div>
          <div class="col-xs-3" style="height: 200px">
            <div class="row" style="padding: 10px; font-size: 1.5em; color: #A0A0A0;" >
              This Week
            </div>
            <div class="row">

              <div class="col-xs-6" >
                <!-- total hits this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(vui_stats_computed.metrics.total_validations['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> TOTAL
                </span>
              </div>

              <div class="col-xs-6" >
                <!-- total users this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(vui_stats_computed.metrics.total_users['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> USERS
                </span>
              </div>

              <div class="col-xs-6" >
                <!-- total Repos this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(vui_stats_computed.metrics.total_clients['week-0'], '0,0', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> CLIENTS
                </span>
              </div>

              <div class="col-xs-6" >
                <!-- total code speed this week -->
                <span class="aws-curr-cost" >
                  {{adjust_numerics(vui_stats_computed.metrics.validations_per_user['week-0'], '0.00', 0).value}}
                </span>
                <br>
                <span class="aws-facet-name" >
                  <span style="color:#207378">&#9679;</span> WORK SPEED
                </span>
              </div>

            </div>
          </div>
          <div id="vui_clients_graph" class="col-xs-4" style="height: 200px">
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="twitter_feed" class="col-xs-4" ng-controller="twitter_ctrl" style="background-color: #04213A;">
    <div class="panel" style="border-radius: 0px; background-color: #001C33;">
      <div class="panel-heading" style="padding: 5px; text-align: left;">
        <h3 class="panel-title" style="font-size: 20px; font-weight: 100;">Twitter Feed</h3>
      </div>
      <div class="panel-body">
        <div class="row" ng-if="true" >
          <a class="twitter-timeline" href="https://twitter.com/IronMan_MA/lists/boomerangcommerce" data-widget-id="637670810992275456">Tweets from https://twitter.com/IronMan_MA/lists/boomerangcommerce</a>
        </div>
      </div>
    </div>
  </div>
</div>

</body>
</html>