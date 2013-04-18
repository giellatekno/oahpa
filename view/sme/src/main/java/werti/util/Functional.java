package werti.util;

import java.util.Collection;
import java.util.LinkedList;
import java.util.List;

/* Reminds functional programming. */
public class Functional {
	public static <T> Collection<T> filter(Collection<T> l, Predicate<T> p) {
		final Collection<T> rl = new LinkedList<T>();
		for (T t:l) { if (p.check(t)) rl.add(t); }
		return rl;
	}

	public static <A,B> List<B> map(Collection<A> l, Function<A,B> f) {
		final List<B> rl = new LinkedList<B>();
		for (final A a:l) { rl.add(f.apply(a)); }
		return rl;
	}

	public interface Function<A,B> { public B apply(A a); }
	public interface Predicate<T> { public boolean check(T t); }
}
