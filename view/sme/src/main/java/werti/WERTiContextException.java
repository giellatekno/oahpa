package werti;

public final class WERTiContextException extends Exception {
	private static String spam(final String message) {
		return "WERTiContext found a problem: "+message;
	}

	// first 6 digits of sha1sum of java source file
	static final long serialVersionUID = 0xd4f21;

	/**
	 * @see Exception#Exception(String)
	 */
	public WERTiContextException(String message) {
		super(spam(message));
	}

	/**
	 * @see Exception#Exception(String,Throwable)
	 */
	public WERTiContextException(String message, Throwable cause) {
		super(spam(message), cause);
	}

	/**
	 * @see Exception#Exception(Throwable)
	 */
	public WERTiContextException(Throwable cause) {
		super(cause);
	}

	public static WERTiContextException ioe(String path) {
		return new WERTiContextException("Could not access "+path);
	}

	public static WERTiContextException ioe(String path, Throwable e) {
		return new WERTiContextException("Could not access "+path,e);
	}
}
