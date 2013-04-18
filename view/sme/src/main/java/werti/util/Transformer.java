package werti.util;

import java.util.LinkedList;
import java.util.List;

public class Transformer {

	public static <A> List<? extends A> applyRules(A a, List<Transformation<A>> rules) {
		List<A> items = new LinkedList<A>();
		items.add(a); //initial seed
		for (final Transformation<A> r:rules) {
			for (A i:items) {
				items.addAll(r.apply(i));
			}
		}
		return items;
	}
}
