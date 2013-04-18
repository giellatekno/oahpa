<%@ page isErrorPage="true" %>

<h1>Server Error</h1>
 
<div class="text">

<p>
Sorry, we ran into a problem processing your request!
</p>

<blockquote>
<%= (exception == null) ? "" : exception.getMessage() %>
</blockquote>

</div>
