window.name = "Continuum";
angular.module('continuum',
  [
    // 'ngAnimate',
    ])
// AWS Controller
.controller('continuum_ctrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
  //globals
	$scope.welcome = "AWS"

	function jsonForUI (json) {
		// body...
		uiJSON = {}
		if(json["movies"].length >0){
			// movie template
			title = json["movies"][0]
			uiJSON = [
				{
					"site": "imdb",
					"title": title.toUpperCase()+" Movie",
					"info": " 8.5/10 rating",
					"link": "http://www.imdb.com/find?q="+title.toLowerCase()
				},
				{
					"site": "youtube",
					"title": title.toUpperCase()+" Video",
					"info": " >10 millions of views on this",
					"link": "https://www.youtube.com/results?search_query="+title.toLowerCase()
				},
				{
					"site": "bookmyshow",
					"title": "Tickets for "+title.toUpperCase(),
					"info": "tickets running out, book fast",
					"link": "https://in.bookmyshow.com/bengaluru/movies/"+title.toLowerCase()
				}
				]
		}else if(json["places"].length >0){
			// places template
			title = json["places"][0]
			// $http({
			// 	method: 'GET',
			// 	url: 'https://api.forecast.io/forecast/572137b8258bed98f73cbbb7760e9117/12.933548,77.621243',
			// }).success(function(data){
			// 	console.log(data);
			// }).error(function(data){
			// 	alert(data);
			// });

			uiJSON = [
				{
					"site": "weather",
					"title": "22°C "+title.toUpperCase(),
					"info": " Right time to Headout ",
					"link": "https://weather.com/weather/today"
				},
				{
					"site": "headout",
					"title": "Attractions in "+title.toUpperCase(),
					"info": "49 amazing things to do",
					"link": "https://www.headout.com/tours/dubai"+title.toLowerCase()+"?tags=attraction&categoryId=107"
				},
				{
					"site": "facebook",
					"title": "Your friends are ... ",
					"info": "84 live events in this place",
					"link": "https://www.facebook.com/search/events/?q="+title.toLowerCase()
				}
				]
		}else if(json["food"].length >0){
			// food template
			title = json["food"][0]
			uiJSON = [
				{
					"site": "zomato",
					"title": "Let's eat "+title.toUpperCase(),
					"info": "26 amazing restaurants are available",
					"link": "https://www.zomato.com/bangalore/restaurants?q="+title.toLowerCase()
				},
				{
					"site": "spoonacular",
					"title": "Cook "+title.toUpperCase(),
					"info": "amazing recipes, ready in 35 minutes!!!",
					"link": "https://spoonacular.com/"+title.toLowerCase()
				},
				{
					"site": "swiggy",
					"title": "Deliver "+title.toUpperCase(),
					"info": "get it delivered within 20 minutes!!!",
					"link": "https://www.swiggy.com"
				}
				]
		}else{
			// nothing
			// bol gaand mari
			uiJSON = []
		}

		return uiJSON
	}

	function tokenParse (params){
		front_user = params.split('&_geoLat_=')[0]
		front_geoLat = params.split('&_geoLon_=')[0]
		front_geoLon = params.split('&_text_=')[0]
		front_text = params
		// find userName
		userName = front_user.split('_user_=')[1]
		// find geolocation
		geoLat = front_geoLat.split('&_geoLat_=')[1]
		geoLon = front_geoLon.split('&_geoLon_=')[1]
		// find text
		text = front_text.split('&_text_=')[1]
		return {
			"userName" : userName,
			"geoLocation" : geoLat+","+geoLon,
			"text" : text
		}
	}

	$scope.start = function start (argument) {
		// body...
		$scope.Test = window.location.href;
		// http://continuum.rboomerang.com:8080/continuum?user=gaurav&geoLat=12.9&geoLon=77.6&text=uhello%20%23%24%25%24%20guaejfi%20sfudhsuail%20cindrella%20revenant%20%20jksgfuh832hfr8u%20f8yf8vrjh%20pizza%20koramangala%20biryani

		// http://continuum.rboomerang.com:8080/continuum?_user_=gaurav&_geoLat_=12.9&_geoLon_=77.6&_text_=uhello #$%$ guaejfi sfudhsuail cindrella revenant  jksgfuh832hfr8u f8yf8vrjh pizza koramangala biryani

		// $scope.json = {
		// 				"userName":"gaurav",
		// 				"geoLocation":"12.933548, 77.621243",
		// 				"movies":["revenant","Hotel Transylvania"],//"revenant","Hotel Transylvania"
		// 				"places":[],//"koramangala","trolltunga"
		// 				"food":[]//"crepes","dinner"
		// 				}
		tokens = tokenParse(window.location.href.split('continuum/')[1])
// 		{"userName":"Gaurav",
// "geoLocation": "12.933548, 77.621243", "text": "uhello #$%$ guaejfi sfudhsuail cindrella revenant  jksgfuh832hfr8u f8yf8vrjh pizza koramangala biryani"}
		var dataObj = {
				userName : tokens["userName"],
				geoLocation : tokens["geoLocation"],
				text : tokens["text"]
		};
		console.log($scope.Test)
		console.log(dataObj)
		var res = $http.post('//continuum.rboomerang.com:8080/continuumcore/highterms', dataObj);
		res.success(function(data, status, headers, config) {
			$scope.message = data;
			$scope.uiJSON = jsonForUI(data)
		});
		res.error(function(data, status, headers, config) {
			console.log( "failure message: " + JSON.stringify({data: data}));
		});
		// $scope.uiJSON = jsonForUI($scope.json)
		// $scope.apply()
	}

	$scope.start()

	$scope.Test = window.location.href;

}])