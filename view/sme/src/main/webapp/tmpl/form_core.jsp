<%
String activity = request.getParameter("activity");
%>

<div class="text">

<div class="activityForm">


<h3 class="activityFormH3">Try it out:</h3>

<!-- <p>
This form lets you get an idea of what WERTi can do, but it may have trouble accessing or displaying
some pages.  For the best results, use the  
<a href="index.jsp?content=firefox-extension">WERTi firefox extension</a>.
</p> -->

<p> Practise North Saami grammar on the web pages that you choose yourself. </p>

<form class="activityForm" target="_blank" method="get" action="WERTiServlet" name="activityForm">

<input type="hidden" name="activity" value="<%= activity %>" />
<input type="hidden" name="language" value="en" />

<b>URL:</b> <input type="text" name="url" class="urlInput" />
<p />
<b>Activity type:</b>

<label><input type="radio" name="client.enhancement" value="colorize" checked="checked" />Colorize</label>
<label><input type="radio" name="client.enhancement" value="click" />Click</label>
<label><input type="radio" name="client.enhancement" value="mc" />Multiple Choice</label>
<label><input type="radio" name="client.enhancement" value="cloze" />Practice</label>

<br /><br />

<input type="submit" value="Go!" class="activityFormSubmit" /> (opens in a new window)
</form>

<!--
<p>Some example sites with colorizing:</p>

<ul>
<li><a target="_blank" href="/WERTisme/WERTiServlet?activity=<%= activity %>&url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FComputer-assisted_language_learning&client.enhancement=colorize">Wikipedia</a> (computer-assisted language learning)</li>
<li><a target="_blank" href="/WERTisme/WERTiServlet?activity=<%= activity %>&url=http%3A%2F%2Fwww.guardian.co.uk%2Fenvironment%2Fgreen-living-blog%2F2009%2Foct%2F29%2Fcar-free-cities-neighbourhoods&client.enhancement=colorize">The Guardian</a> (car-free cities)</li>
<li><a target="_blank" href="/WERTisme/WERTiServlet?activity=<%= activity %>&url=http%3A%2F%2Fpublicliterature.org%2Fbooks%2Femma%2F&client.enhancement=colorize">Public Literature</a> (Emma by Jane Austen)</li>
</ul>
-->
<p>
</p>


</div>

</div>