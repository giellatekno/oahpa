package werti.server;

import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.TreeMap;

/**
 * Find activity specifications for all active activities.
 * 
 * @author Niels Ott?
 * @author Adriane Boyd
 *
 */
public class Activities implements Iterable<String> {

	public static final String ATT_NAME = "werti.activities";
	
	private TreeMap<String, ActivityConfiguration> configMap;
	private Set<String> ignoredActivities;
    
	public Activities(File actDir) throws IOException {
		configMap = new TreeMap<String, ActivityConfiguration>();
		
		ignoredActivities = new HashSet<String>();
		ignoredActivities.add("Conditionals");
		
		for (File f : actDir.listFiles()) {
			if (f.isDirectory() && !ignoredActivities.contains(f.getName())) {
				configMap.put(f.getName(), new ActivityConfiguration(
						new File(f.getAbsolutePath() + File.separator + "activity.xml")));
			}
		}
	}

	public Iterator<String> iterator() {
		return configMap.keySet().iterator();
	}
	
	public ActivityConfiguration getActivity(String key) {
		return configMap.get(key);
	}
	
}
