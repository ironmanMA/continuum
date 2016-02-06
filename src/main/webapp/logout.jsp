<%@page contentType="text/html" pageEncoding="UTF-8"%>

<%
	final String login_page = "/dashboard/index.jsp";
	final String home_page = "/dashboard/home.jsp";
	final String logout_page = "/dashboard/logout.jsp";
	final String profile_page = "/dashboard";
	session.removeAttribute("authorized");
	session.removeAttribute("json");
	session.removeAttribute("date_string");
	response.sendRedirect( login_page );
 %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>BoomBoard</title>

</head>
<body>

</body>
</html>
