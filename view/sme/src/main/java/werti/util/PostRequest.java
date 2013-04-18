package werti.util;

/**
 * Corresponds to the structure of the JSON AJAX requests 
 * sent by the add-on.
 * 
 * @author Adriane Boyd
 */
public class PostRequest {
	public String type;
	public String url;
	public String language;
	public String topic;
	public String activity;
	public String document;
	public String version;
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("PostRequest(");
		sb.append("\n  type = ");
		sb.append(this.type);
		sb.append("\n  url = ");
		sb.append(this.url);
		sb.append("\n  language = ");
		sb.append(this.language);
		sb.append("\n  topic = ");
		sb.append(this.topic);
		sb.append("\n  activity = ");
		sb.append(this.activity);
		sb.append("\n  document = ");
		sb.append(this.document);
		sb.append("\n  version = ");
		sb.append(this.version);
		sb.append("\n)");
		return sb.toString();
	}
}
