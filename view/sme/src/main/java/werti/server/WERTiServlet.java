package werti.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Locale;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.lang.StringEscapeUtils;
import org.apache.log4j.Logger;
import org.apache.uima.jcas.JCas;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Node;
import org.jsoup.nodes.Document;
import org.openid4java.OpenIDException;
import org.openid4java.consumer.ConsumerException;
import org.openid4java.consumer.ConsumerManager;
import org.openid4java.discovery.DiscoveryException;
import org.openid4java.discovery.DiscoveryInformation;
import org.openid4java.discovery.Identifier;
import org.openid4java.message.AuthRequest;
import org.openid4java.message.MessageException;

import werti.WERTiContext;
import werti.WERTiContext.WERTiContextException;
import werti.util.ActivitiesSessionLoader;
import werti.util.HTMLEnhancer;
import werti.util.HTMLUtils;
import werti.util.JSONEnhancer;
import werti.util.PageHandler;
import werti.util.PostRequest;
import werti.util.PracticeHandler;

import com.google.gson.Gson;

import weka.core.Instances;
import weka.filters.Filter;

/**
 * The server side implementation of the WERTi service.
 *
 * This is where the work is coordinated. The rough outline of the procedure is as follows:
 *
 * <ul>
 * <li>We take a request via the doGet() (web form) or doPost() (add-on) methods.</li>
 * <li>For web form requests, the HTML source of the URL is fetched and spans of text are
 * identified.</li>
 * <li>The document is processed in UIMA, invoking the pre- and postprocessors for the current
 * topic.</li>
 * <li>Afterwards, we take the resulting CAS and insert enhancement annotations
 * (<tt>WERTi</tt>-<tt>&lt;span&gt;</tt>s) according to the target annotations from the
 * postprocessor.</li>
 *
 * @author Aleksandar Dimitrov
 * @author Adriane Boyd
 */
public class WERTiServlet extends HttpServlet {
	private static final Logger log =
		Logger.getLogger(WERTiServlet.class);

	public static WERTiContext context;
	
	// maximum amount of of ms to wait for a web-page to load
	private static final int MAX_WAIT = 1000 * 10; // 10 seconds

	public static final long serialVersionUID = 10;
	
	public static final Set<String> supportedVersions = new HashSet<String>(Arrays.asList("0.10"));

	private Processors processors;
	
	public static OpenIDConsumer openidConsumer = null;

	public void init(ServletConfig config) throws ServletException {
		super.init(config);
		log.warn("Initializing servlet.");
		// initialise servletcontext
		try {
			WERTiContext.init(config);
		} catch (WERTiContextException wce) {
			log.fatal("Context failed to initialize.");
			log.fatal(wce);
		}
	}

	public void destroy() {
		// no-op
	}

	/* (non-Javadoc)
     * @see javax.servlet.http.HttpServlet#doGet(javax.servlet.http.HttpServletRequest, javax.servlet.http.HttpServletResponse)
     */
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
	throws ServletException, IOException {

		long startTime = System.currentTimeMillis();
		log.debug("received GET request");
		req.setCharacterEncoding("UTF-8");
		resp.setCharacterEncoding("UTF-8");

		// OpenID verification request
		if ("true".equals(req.getParameter("openid_return"))) {
			if (openidConsumer == null) {
				String openidReturnToUrl = getOpenIDReturnToUrl(req);
				openidConsumer = new OpenIDConsumer(openidReturnToUrl, this);
			}

			Identifier verified = openidConsumer.verifyResponse(req);
			if (verified != null) {
				resp.sendRedirect(getServletBaseUrl(req) + "/openid/return.jsp?openid.identity=" + verified.getIdentifier());
			}
			else {
				resp.sendRedirect(getServletBaseUrl(req) + "/openid/verification-failed.jsp");
			}

			return;
		}
		
		String url = req.getParameter("url");
		String activity = req.getParameter("activity");
		String lang = req.getParameter("language");
		if (lang == null) {
			lang = "en";
		}

		ActivityConfiguration config = loadActivitiesAndProcessors(req, activity); //track this

		// merge config with request parameters
		mergeConfigParams(config, req);

		URL u = new URL(url);
		Document htmlDoc;
		try {
			htmlDoc = Jsoup.parse(u, MAX_WAIT);
		} catch (IOException ioe) {
			throw new ServletException("Webpage retrieval failed.");
		}

		HTMLUtils.markTextNodes(htmlDoc, htmlDoc.body());

		// TODO: potentially modify jsoup to return unescaped text so that this hack 
		//       can be removed
		String htmlString = spansToETags(htmlDoc, HTMLUtils.className, false);

		PageHandler ph = new PageHandler(processors, activity, htmlString, lang);
		JCas cas;
		cas = ph.process();
		
		if (cas != null) {
			HTMLEnhancer ge = new HTMLEnhancer(cas);
			String result = ge.enhance(activity, u.toString(), req, config, getServletContext().getServletContextName());

			log.info("Web (" + (System.currentTimeMillis() - startTime) + "): " + req.getParameter("language") + ",  " + activity + ", " + req.getParameter("client.enhancement") + ", " + url + ", " + cas.getDocumentLanguage());
			
			try { // to write to the response stream
				resp.setContentType("text/html");
				final PrintWriter out = resp.getWriter();
				out.write(result);
				out.close();
			} catch (IOException ioe) {
				log.error("Failed to write to temporary file");
				throw new ServletException("", ioe);
			}
		} else {
			throw new ServletException("The selected language/topic/activity combination is not currently available.");
		}
	}
	
	/**
	 * Annotate according to the topic/activity/text provided in a JSON PostRequestObject.
	 * 
	 * @param req the servlet request
	 * @param resp the servlet response
	 */
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		
		long startTime = System.currentTimeMillis();
		log.debug("received POST request");
		
		// read request in as string
		// (gson.fromJson() seems unhappy with req.getReader() as its first argument, don't know why)
		String line;
		String requestString = "";
		BufferedReader reader = req.getReader();
		while((line = reader.readLine()) != null) {
			requestString += line;
		}

		// parse this string into an object
		Gson gson = new Gson();
		PostRequest requestInfo = gson.fromJson(requestString, PostRequest.class);

		// check if this version is supported
		if (!supportedVersions.contains(requestInfo.version)) {
			resp.sendError(490);
			log.info("Add-on, version conflict (" + (System.currentTimeMillis() - startTime) + "): " + requestInfo.topic + ", " + requestInfo.activity + ", " + requestInfo.url);
			return;
		}
		
		// if this is an OpenID authentication request, handle it separately
		if (requestInfo.type.matches("openid-authentication")) {
			String userSuppliedIdentifier = requestInfo.url;
			// TODO do something with this info
			log.debug("requestInfo.document: " + requestInfo.document);
			if (openidConsumer == null) {
				String openidReturnToUrl = getOpenIDReturnToUrl(req);
				openidConsumer = new OpenIDConsumer(openidReturnToUrl, this);
			}
			openidConsumer.authRequest(userSuppliedIdentifier, req, resp);
			return;
		}

		String lang = requestInfo.language;
		if (lang == null) {
			lang = "en";
		}

		ActivityConfiguration config = loadActivitiesAndProcessors(req, requestInfo.topic);
		
		// check if the requested topic exists
		if (config == null) {
			resp.sendError(491);
			log.info("Add-on, topic doesn't exist (" + (System.currentTimeMillis() - startTime) + "): " + lang + ", " + requestInfo.topic + ", " + requestInfo.activity + ", " + requestInfo.url);
			return;
		}
		
		// check if the language-topic combination exists
		if (config.getPreDesc(lang) == null || config.getPostDesc(lang) == null) {
			resp.sendError(492);
			log.info("Add-on, topic doesn't exist for language ("  + (System.currentTimeMillis() - startTime) + "): " + lang + ", " + requestInfo.topic + ", " + requestInfo.activity + ", " + requestInfo.url);
			return;
		}
		
		/* // disallow passives
		if (requestInfo.topic.equals("Passives")) {
			resp.sendError(491);
			return;
		}*/

		// set enhancement type
		config.setClientValue(lang, "enhancement", requestInfo.activity);
		
		// extract the wertiview spans from the document
		Document doc = Jsoup.parse(requestInfo.document);  
		String htmlString = spansToETags(doc, "wertiview", true);
		
		String result = "";
		
		// handling each type of request
		if (requestInfo.type.matches("practice")) {
			PracticeHandler ph = new PracticeHandler(requestInfo);
			result = ph.process();
		} else { // should be a "page" request
			
			PageHandler ph = new PageHandler(processors, requestInfo.topic, htmlString, lang);
			JCas cas;
			cas = ph.process();

			JSONEnhancer pe = new JSONEnhancer(cas, requestInfo.activity);
			result = pe.enhance();
			
			log.info("Add-on (" + (System.currentTimeMillis() - startTime) + "): " + requestInfo.language + ", " + requestInfo.topic + ", " + requestInfo.activity + ", " + requestInfo.url + ", " + cas.getDocumentLanguage());
		}	

		try { // to write to the response stream
			//Locale locale = new Locale("se-NO", "");
			resp.setContentType("text/plain"); // charset=UTF-8");
			final PrintWriter out = resp.getWriter();
			//final PrintWriter out = new PrintWriter(new OutputStreamWriter(resp.getOutputStream(), "UTF8"), true);
			out.write(result);
			out.close();
		} catch (IOException ioe) {
			log.error("Error writing to response stream");
			throw new ServletException("", ioe);
		}
	}
	
	/**
	 * load the activity.xml files for all topics. Initialize the pre- and 
	 * postprocessors for each.
	 * @param req the HTTP request
	 * @param topicName the topic chosen by the user
	 * @return the configuration of the activity chosen by the user
	 */
	private ActivityConfiguration loadActivitiesAndProcessors(HttpServletRequest req, 
			String topicName) throws IOException, ServletException {

		// load activities from/into session
		Activities acts = ActivitiesSessionLoader.createActivitiesInSession(req);
		ActivityConfiguration config = acts.getActivity(topicName);

		// load processors if necessary
		loadProcessors(acts); // track this
		
		return config;
	}
	
	/**
	 * replace all <span class="wertiview"> tags with <e> tags. Copy the 
	 * wertiview IDs if there are any. Turn the HTML character entities inside 
	 * the spans/e-tags into unicode characters.
	 * @param doc the result of a Jsoup parse
	 * @param className the name of the class of the relevant spans
	 * @param haveIds whether the wertiview spans have IDs in the wertiviewid attribute
	 * @return the <html> node as a string
	 */
	private String spansToETags(Document doc, String className, boolean haveIds) {
		// find all added spans using the class name and replace everything inside 
		// the <e> tokens with unescaped unicode characters
		String htmlString = doc.html();
		Pattern enhancePatt = Pattern.compile("<span class=\"[^\"]*" + className + "[^\"]*\"( wertiviewid=\"([^\"]*)\")?>(.*?)</span>", Pattern.DOTALL);
		Matcher enhanceMatcher = enhancePatt.matcher(htmlString);
		while (enhanceMatcher.find()) {
			htmlString = htmlString.replace(enhanceMatcher.group(3), StringEscapeUtils.unescapeHtml(enhanceMatcher.group(3)));
		}

		// replace these spans with <e> tags for use in normal pipeline
		if (haveIds) {
			htmlString = htmlString.replaceAll(enhancePatt.toString(), "<e id=\"$2\">$3</e>");
		}
		else {
			htmlString = htmlString.replaceAll(enhancePatt.toString(), "<e>$3</e>");
		}

		return htmlString;
	}
	
	@SuppressWarnings("unchecked")
	private void mergeConfigParams(ActivityConfiguration config, HttpServletRequest req) {
		Enumeration<String> paramNames = req.getParameterNames();
		String lang = req.getParameter("language");
		while (paramNames.hasMoreElements()) {
			String key = paramNames.nextElement();
			boolean worked = false;
			boolean isConfigParam = false;
			String value = req.getParameter(key);

			if (key.startsWith(ActivityConfiguration.CLIENT_PREFIX)) {
				worked = config.setClientValue(lang, key.substring(ActivityConfiguration.CLIENT_PREFIX.length()+1), value);
				isConfigParam = true;
			} else if (key.startsWith(ActivityConfiguration.PRE_PREFIX)) {
				worked = config.setServerPreValue(lang, key.substring(ActivityConfiguration.PRE_PREFIX.length()+1), value);
				isConfigParam = true;
			} else if (key.startsWith(ActivityConfiguration.POST_PREFIX)) {
				worked = config.setServerPostValue(lang, key.substring(ActivityConfiguration.POST_PREFIX.length()+1), value);
				isConfigParam = true;
			}

			if (isConfigParam) {
				if (worked) {
					log.debug("Successfully set config param: " + key + " to:" + value);
				} else {
					log.debug("Access denied for config param: " + key);
				}
			}
		}
	}
	
	/**
	 * If the processors haven't been loaded, load them.
	 * 
	 * @param acts the list of activities
	 * @throws IOException
	 * @throws ServletException
	 */
	private void loadProcessors(Activities acts) throws IOException, ServletException {
		if (processors == null) {
			long startTime = System.currentTimeMillis();
			processors = new Processors(acts);
			log.info("Loaded all UIMA processors (" + (System.currentTimeMillis() - startTime) + ")");
		}
	}
	
	private static String getServletBaseUrl(HttpServletRequest req) {
		String baseUrl = req.getScheme() + "://" + req.getServerName() + ":" + req.getServerPort() + req.getContextPath();
		return baseUrl;
	}
	
	private static String getOpenIDReturnToUrl(HttpServletRequest req) {
		String baseUrl = getServletBaseUrl(req);
		String openidReturnToUrl = baseUrl + "/VIEW?openid_return=true";
		return openidReturnToUrl;
	}
}
