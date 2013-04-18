	<% 
		String activity = request.getParameter("activity");
		if (activity != null) {
			String help = "/activities/" + activity + "/help.jsp";
			String form = "form.jsp";
	%>
			<jsp:include page="<%= help %>" />
			<hr />
			<jsp:include page="<%= form %>" />
	<%
		} else {
			out.println("Please choose a topic from the menu bar on the left.");
		}
	%>