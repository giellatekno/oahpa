package werti.util;

import java.io.File;
import java.io.IOException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import werti.server.Activities;

/**
 * Helper class for loading a fresh {@link Activities} registry
 * into the web session. 
 * 
 * @author Niels Ott
 * @version $Id: ActivitiesSessionLoader.java 731 2010-11-05 12:55:06Z adriane@SFS.UNI-TUEBINGEN.DE $
 */
public class ActivitiesSessionLoader {
	
	public static Activities createActivitiesInSession(HttpServletRequest req) throws IOException {
		// try to obtain the activities from the session
		HttpSession session = req.getSession();
		Activities acts = (Activities)session.getAttribute(Activities.ATT_NAME);

		// if this doesn't work out, create the activities
		if ( acts == null ) {
			acts = new Activities(new File(session.getServletContext().getRealPath("/activities")));
			session.setAttribute(Activities.ATT_NAME, acts);
		}
		
		return acts;		
	}
}
