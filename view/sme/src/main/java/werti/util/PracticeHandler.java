package werti.util;

import org.apache.log4j.Logger;

/**
 * Methods needed for processing practice response.
 * 
 * @author Adriane Boyd
 *
 */
public class PracticeHandler {
	private static final Logger log =
		Logger.getLogger(PracticeHandler.class);
	
	private PostRequest requestInfo;
	
	public PracticeHandler(PostRequest aRequestInfo) {
		requestInfo = aRequestInfo;
	}
	
	public String process() {
		return "";
	}
}
