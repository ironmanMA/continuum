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
			{{Test}}

	<ul class="gNow" id="col1">
		<li ng-repeat="card in uiJSON">
			<div class="card">
			<div style="float:left; padding:5px" >
				<img ng-src="assets/images/{{card.site}}.png" style="max-width: 75px;">
			</div>
			<div style="margin-left:100px" >
				<p class="card-title">{{card.title}}</p>
				<p>{{card.info}}</p>
				<p class="url"><a href="{{card.link}}">learn more</a></p>
			</div>
			</div>
		</li>
	</ul>

		</div>
	</body>
</html>