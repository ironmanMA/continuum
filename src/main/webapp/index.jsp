<%@page import="com.boomerang.google.auth.GoogleAuthHelper"%>
<%@page import="com.boomerang.config.AppConfigUtil"%>
<%@page import="java.io.*, java.util.Date, java.util.Enumeration" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>

<%
	AppConfigUtil configuration = new AppConfigUtil();
	final int date_number =  (int) new Date().getTime();
	final String login_page = "/dashboard/index.jsp?v="+date_number;
	final String home_page = "/dashboard/home.jsp?v="+date_number;
	final String logout_page = "/dashboard/logout.jsp?v="+date_number;
	final String profile_page = "/dashboard";
	final GoogleAuthHelper helper = new GoogleAuthHelper();

	/*
	 * The GoogleAuthHelper handles all the heavy lifting, and contains all "secrets"
	 * required for constructing a google login url.
	 */
	if (request.getParameter("code") == null || request.getParameter("state") == null) {
		;
	} else if (request.getParameter("code") != null && request.getParameter("state") != null && request.getParameter("state").equals(session.getAttribute("state"))) {

		session.removeAttribute("state");
		session.setAttribute("json",helper.getUserInfoJson(request.getParameter("code")));
		session.setAttribute("authorized","true");
		session.setAttribute("date_string", "?v="+date_number);
		String json_check = session.getAttribute("json").toString().replaceAll("(\r\n|\n)","");
		if( !json_check.contains("@boomerangcommerce.com") ){
			response.sendRedirect( logout_page );
		}
	}

      try
      {
         if( (session.getAttribute("authorized").equals("true") )){

            response.sendRedirect( home_page );
        }
      }
      catch(Exception e)
      {
            session.removeAttribute("authorized");
      }
 %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
<html >
  <head>
    <meta charset="UTF-8">
    <meta name="google" value="notranslate">
    <title>BoomBoard | Operations Dashboard</title>
    <link rel="stylesheet" href="assets/css/3P/bootstrap/css/bootstrap.css">
    <script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
    <script src="assets/js/3P/bootstrap/js/bootstrap.js"></script>
<style>
/*@import url(http://fonts.googleapis.com/css?family=Arvo:400);*/
@import url(http://fonts.googleapis.com/css?family=Work+Sans:100,600);

body, html {
  padding: 0;
  margin: 0;
}

h1 {
  font-size: 4em;
  color: white;
  font-family: 'Work Sans', serif;
  letter-spacing: 2px;
  pointer-events: none;
  font-weight: 100;
  position: absolute;
  top: 30%;
  left: 0;
  right: 0;
  text-align: center;
}
.cust-tooltip + .tooltip > .tooltip-inner {
	background-color: rgba(30, 71, 105, 0.54);
	font-family: 'Work Sans', serif;
	color: #448fda;
	font-weight: bold;
}

.login-button{
    color: #448fda;
    font-family: 'Work Sans', serif;
    font-weight: 100;
    position: absolute;
    top: 55%;
    width: 100px;
    margin-left: 50%;
    left: -50px;
    right: 0;
    background-color: rgba(0, 28, 51, 0.5);
}

.login-button:hover{
	border-color: #448fda;
	font-family: 'Work Sans', serif;
	background-color: rgba(0, 28, 51, 0.5);
	color: #448fda;
}
</style>
</head>

<body>

<h1>BOOMBOARD</h1>
<a type="button"
			class="login-button btn btn-default btn-lg cust-tooltip"
			data-toggle="tooltip"
			href="<%out.println(helper.buildLoginUrl());session.setAttribute("state", helper.getStateToken());%>"
			data-placement="right"
			title="use only @boomerangcommerce.com email-id">
			Login</a>

<!-- credits to http://s.codepen.io/awendland/debug/XJExGv? -->
<canvas></canvas>

<script>
$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	})

var canvas = document.querySelector("canvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
var ctx = canvas.getContext("2d");

var TAU = 2 * Math.PI;

times = [];
function loop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  update();
  draw();
  requestAnimationFrame(loop);
}

function Ball (startX, startY, startVelX, startVelY) {
  this.x = startX || Math.random() * canvas.width;
  this.y = startY || Math.random() * canvas.height;
  this.vel = {
    x: startVelX || Math.random() * 2 - 1,
    y: startVelY || Math.random() * 2 - 1
  };
  this.update = function(canvas) {
    if (this.x > canvas.width + 50 || this.x < -50) {
      this.vel.x = -this.vel.x;
    }
    if (this.y > canvas.height + 50 || this.y < -50) {
      this.vel.y = -this.vel.y;
    }
    this.x += this.vel.x;
    this.y += this.vel.y;
  };
  this.draw = function(ctx, can) {
    ctx.beginPath();
    ctx.globalAlpha = .4;
    ctx.fillStyle = '#448fda';
    ctx.arc((0.5 + this.x) | 0, (0.5 + this.y) | 0, 3, 0, TAU, false);
    ctx.fill();
  }
}

var balls = [];
for (var i = 0; i < canvas.width * canvas.height / (65*65); i++) {
  balls.push(new Ball(Math.random() * canvas.width, Math.random() * canvas.height));
}

var lastTime = Date.now();
function update() {
  var diff = Date.now() - lastTime;
  for (var frame = 0; frame * 16.6667 < diff; frame++) {
    for (var index = 0; index < balls.length; index++) {
      balls[index].update(canvas);
    }
  }
  lastTime = Date.now();
}
var mouseX = -1e9, mouseY = -1e9;
document.addEventListener('mousemove', function(event) {
  mouseX = event.clientX;
  mouseY = event.clientY;
});

function distMouse(ball) {
  return Math.hypot(ball.x - mouseX, ball.y - mouseY);
}

function draw() {
  ctx.globalAlpha=1;
  ctx.fillStyle = '#001c33';
  ctx.fillRect(0,0,canvas.width, canvas.height);
  for (var index = 0; index < balls.length; index++) {
    var ball = balls[index];
    ball.draw(ctx, canvas);
    ctx.beginPath();
    for (var index2 = balls.length - 1; index2 > index; index2 += -1) {
      var ball2 = balls[index2];
      var dist = Math.hypot(ball.x - ball2.x, ball.y - ball2.y);
        if (dist < 100) {
          ctx.strokeStyle = "#448fda";
          ctx.globalAlpha = 1 - (dist > 100 ? .8 : dist / 150);
          ctx.lineWidth = "2px";
          ctx.moveTo((0.5 + ball.x) | 0, (0.5 + ball.y) | 0);
          ctx.lineTo((0.5 + ball2.x) | 0, (0.5 + ball2.y) | 0);
        }
    }
    ctx.stroke();
  }
}

// Start
loop();
</script>
  </body>
</html>