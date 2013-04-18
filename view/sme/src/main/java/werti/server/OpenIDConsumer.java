package werti.server;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import org.apache.log4j.Logger;
import org.omg.CORBA_2_3.portable.OutputStream;
import org.openid4java.consumer.*;
import org.openid4java.discovery.*;
import org.openid4java.message.*;
import org.openid4java.OpenIDException;

public class OpenIDConsumer extends HttpServlet {

	private static final long serialVersionUID = 3784831295129116629L;

	private static final Logger log = Logger.getLogger(OpenIDConsumer.class);

	public ConsumerManager manager;
	public String returnToUrl;
	public WERTiServlet wertiServlet;

	public OpenIDConsumer(String returnToUrl, WERTiServlet wertiServlet) {
		// instantiate a ConsumerManager object
		try {
			this.manager = new ConsumerManager();
		} catch (ConsumerException ce) {
			// TODO Auto-generated catch block
			ce.printStackTrace();
		}

		// configure the return_to URL where your application will receive
		// the authentication responses from the OpenID provider
		this.returnToUrl = returnToUrl;
		
		this.wertiServlet = wertiServlet;
	}

	/** 
	 * placing the authentication request 
	 */
	@SuppressWarnings("unchecked")
	public String authRequest(String userSuppliedIdentifier, 
			HttpServletRequest httpReq, HttpServletResponse httpResp)
			throws IOException {

		try {
			// perform discovery on the user-supplied identifier
			List<DiscoveryInformation> discoveries = this.manager.discover(userSuppliedIdentifier);

			// attempt to associate with the OpenID provider
			// and retrieve one service endpoint for authentication
			DiscoveryInformation discovered = this.manager.associate(discoveries);

			// store the discovery information in the user's session
			httpReq.getSession().setAttribute("openid-disc", discovered);

			// obtain a AuthRequest message to be sent to the OpenID provider
			AuthRequest authReq = this.manager.authenticate(discovered, this.returnToUrl);

			String destUrlWithCgi = authReq.getDestinationUrl(true);
			//if (!discovered.isVersion2() || 
			//		destUrlWithCgi.getBytes().length < 2048) {
			if (!discovered.isVersion2()) {
				// Option 1: GET HTTP-redirect to the OpenID Provider endpoint
				// The only method supported in OpenID 1.x
				// redirect-URL usually limited ~2048 bytes
				httpResp.sendRedirect(destUrlWithCgi);
				return null;
			}
			else {
				// Option 2: HTML FORM Redirection (Allows payloads >2048 bytes)

				// the JSP puts together a form with lots of hidden <input>s 
				// and submits it to the OpenID Provider using the POST method
				RequestDispatcher dispatcher = this.wertiServlet.getServletContext().getRequestDispatcher("/openid/formredirection.jsp");
				// these attributes can be read out in the JSP
				httpReq.setAttribute("OPEndpoint", authReq.getOPEndpoint());
				httpReq.setAttribute("parameterMap", authReq.getParameterMap());
				try {
					dispatcher.forward(httpReq, httpResp);
					log.debug("sent to the client a page that redirects to the OP");
				}
				catch (ServletException se) {
					// TODO Auto-generated catch block
					se.printStackTrace();
				}
			}
		}
		catch (OpenIDException e) {
			// present error to the user
		}

		return null;
	}

	/** 
	 * processing the authentication response 
	 */
	public Identifier verifyResponse(HttpServletRequest httpReq) {
		try {
			// extract the parameters from the authentication response
			// (which comes in as a HTTP request from the OpenID provider)
			ParameterList response = new ParameterList(httpReq.getParameterMap());

			// retrieve the previously stored discovery information
			DiscoveryInformation discovered = (DiscoveryInformation) httpReq.getSession().getAttribute("openid-disc");

			// extract the receiving URL from the HTTP request
			StringBuffer receivingURL = httpReq.getRequestURL();
			String queryString = httpReq.getQueryString();
			if (queryString != null && queryString.length() > 0) {
				receivingURL.append("?").append(httpReq.getQueryString());
			}

			// verify the response; ConsumerManager needs to be the same
			// instance used to place the authentication request
			VerificationResult verification = this.manager.verify(receivingURL.toString(), response, discovered);

			// examine the verification result and extract the verified identifier
			Identifier verified = verification.getVerifiedId();
			return verified;  // success
		}
		catch (OpenIDException e) {
			// present error to the user
		}

		return null;
	}
}
