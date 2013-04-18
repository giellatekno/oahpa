<h1>Feedback</h1>

<div class="text">

<p>Please use this form to send us feedback or report problems with VIEW.</p>

<p>All fields are optional, but a URL that demonstrates the problem is helpful for any bug reports.</p>

<%@page import="net.tanesha.recaptcha.ReCaptcha"%>
<%@page import="net.tanesha.recaptcha.ReCaptchaFactory"%>
<%@page import="net.tanesha.recaptcha.ReCaptchaResponse"%>

<div style="margins: 10px; padding: 10px;">
<form action="sendfeedback.jsp" method="post">
<table>
<tr>
<td>Email:</td>
<td><input type="text" name="from" size="40"/></td>
</tr>
<tr>
<td>URL:</td>
<td><input type="text" name="url" size="40"/></td>
</tr>
<tr>
<td style="vertical-align: top;">Message:</td>
<td><textarea name="message" cols="50" rows="10"></textarea></td>
</tr>

<tr>
<td colspan="2">

<div align="center">
<%
        // create recaptcha without <noscript> tags
        ReCaptcha captcha = ReCaptchaFactory.newReCaptcha("6LcoXLsSAAAAABg1BSPjWXmmPCJ3nnxSC5SKXkp9", "6LcoXLsSAAAAANcyuPl2aUpkQP0ZwRoDMvvjci5D", false);
        String captchaScript = captcha.createRecaptchaHtml(request.getParameter("error"), null);
        
        out.print(captchaScript);
%>

<input type="submit" value="Send"/>
</div>
</td>
</tr>
</table>
</form>
</div>

</div>
