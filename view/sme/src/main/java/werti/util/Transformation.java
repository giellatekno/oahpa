package werti.util;

import java.util.List;

public interface Transformation<A> {

	/**
	 * Non-deterministic application.
	 *
	 * @param a Transformation parameter.
	 * @return A list of results. Empty if no result.
	 */
	public List<A> apply(A a);

	/**
	 * Checks for preconditions.
	 *
	 * @param a The parameter that is to be checked.
	 * @return {@code true} if {@code a} does meet the
	 * precondition, {@code false} otherwise.
	 */
	public boolean meetsPrecondition(A a);
}
