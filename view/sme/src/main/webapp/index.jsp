<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<%@page import="java.io.File"%>
<%@page import="java.net.URLEncoder"%>
<%@page import="werti.server.Activities"%>
<%@page import="werti.util.ActivitiesSessionLoader"%><html xmlns="http://www.w3.org/1999/xhtml">
<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
		<link type="text/css" href="/WERTisme/werti.css" rel="stylesheet" />
		<title>Welcome to VIEW</title>
</head>
<body>
<div id="topcontainer">
		<div id="header">
			
		</div>
		<div id="navbar">
			<ul>
			    <li><a href="/WERTisme/index.jsp?content=home">Home</a></li>
				<li><a href="/WERTisme/index.jsp?content=about">About VIEW</a></li>
				<!--<li><a href="/WERTisme/index.jsp?content=intro">Getting Started</a></li> -->
				<li><a href="/WERTisme/index.jsp?content=activities">Topics and Activities</a>
					<ul>
						<%
						
						// load activities into/from session
						Activities acts = ActivitiesSessionLoader.createActivitiesInSession(request);

						for (String basename : acts) {
							String displayName = acts.getActivity(basename).getName();
							out.println("<li><a href=\"/WERTisme/index.jsp?content=activity-help&amp;activity=" + URLEncoder.encode(basename, "UTF-8")  + "\">" + displayName + "</a></li>");
						}
						%>
					</ul>
				</li>
				<!-- <li><a href="/WERTisme/index.jsp?content=firefox-extension">Firefox Extension</a></li> -->
			</ul>
			<% 
			String content = request.getParameter("content");
			String blurb = "";
			if (content == null || content.equals("home")) {
			    blurb = "<!--<p id=\"blurb\"><b>VIEWsme</b> is an " + 
			            "ICALL system designed to provide supplementary language learning activities using " +
			            "authentic North Saami texts selected by the learner.</p>-->";
			}
			out.println(blurb);
            %>
		</div>
		<div id="main">
			<% 			
			if (content == null) {
				content = "tmpl/home.jsp";
			} else {
				content = "tmpl/" + content + ".jsp";
			}
			%>
			<jsp:include page="<%= content %>" />
		</div>

		<div id="footer"></div>
		</div>
</body>
</html>
