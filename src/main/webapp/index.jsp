<%@page import='java.io.*, java.util.Date, java.util.Enumeration'%>
<%@page contentType='text/html' pageEncoding='UTF-8'%>

<%
  final String date_number_string = "?v="+(int) new Date().getTime();;
 %>

 <html ng-app="continuum">
 	<link rel="stylesheet" href="assets/css/3P/bootstrap/css/bootstrap.css">
 	<link rel="stylesheet" href="assets/css/main.css<%out.print(date_number_string);%>">
	<script src="assets/js/jQuery.js"></script>
	<script src="assets/js/numeral.js"></script>
	<script src="assets/js/angular.js"></script>
	<script src="assets/js/main_ctrl.js<%out.print(date_number_string);%>" ></script>

<body>
	<div ng-controller="continuum_ctrl" >
			<!-- {{Test}} -->

	<ul class="gNow" id="col1">

		<li ng-if="uiJSON==null || uiJSON.length < 1">
			<div class="card">
			<div style="float:left; padding:5px" >
				<img ng-src="assets/images/weather.png" style="max-width: 75px;">
			</div>
			<div style="margin-left:100px" >
				<p class="card-title">22°C in Koramangla</p>
				<p class="card-info">Headout and enjoy the pleasnt weather</p>
				<p class="url"><a target="_blank" href="https://weather.com/weather/today">learn more</a></p>
			</div>
			</div>
		</li>

		<li ng-if="uiJSON==null || uiJSON.length < 1">
			<div class="card">
			<div style="float:left; padding:5px" >
				<img ng-src="assets/images/pvr.png" style="max-width: 60px;">
			</div>
			<div style="margin-left:100px" >
				<p class="card-title">Head to PVR</p>
				<p class="card-info">Hurry up tickets are running out</p>
				<p class="url"><a target="_blank" href="http://www.pvrcinemas.com/">book now</a></p>
			</div>
			</div>
		</li>

		<li ng-repeat="card in uiJSON" ng-if="uiJSON.length >= 1">
			<div class="card">
			<div style="float:left; padding:5px" >
				<img ng-src="assets/images/{{card.site}}.png" style="max-width: 60px;">
			</div>
			<div style="margin-left:100px" >
				<p class="card-title">{{card.title}}</p>
				<p class="card-info">{{card.info}}</p>
				<p class="url"><a target="_blank" href="{{card.link}}">{{card.action_text}}</a></p>
			</div>
			</div>
		</li>
	</ul>

		</div>
	</body>
</html>