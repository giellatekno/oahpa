package werti.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.io.IOException;

import org.apache.uima.analysis_engine.AnalysisEngine;

import org.apache.uima.jcas.JCas;

import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.resource.ResourceSpecifier;

import org.apache.uima.UIMAFramework;

import org.apache.uima.util.InvalidXMLException;
import org.apache.uima.util.XMLInputSource;

public class RunDriver {
	private static void exit(final String m) {
		System.err.println("Fatal: "+m);
		System.exit(1);
	}

	private static void exit(final String m, final Throwable t) {
		System.err.println(t.getStackTrace());
		exit(m);
	}

	public static void main(final String[] args) throws Exception {
		if (args[0] == null) { exit("Please provide one or more descriptor files"); }

		final BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
		final StringBuffer   s = new StringBuffer();

		while (r.ready()) {
			s.append(r.readLine());
		}

		for (final String desc:args) {
			final RunDriver a = new RunDriver(desc);
			a.process(s.toString());
		}
	}

	private final AnalysisEngine ae;
	private static JCas cas;

	private RunDriver(final String desc) throws Exception {
		final XMLInputSource in      = new XMLInputSource(desc);
		final ResourceSpecifier spec =
			UIMAFramework.getXMLParser().parseResourceSpecifier(in);
		this.ae  = UIMAFramework.produceAnalysisEngine(spec);
		if (RunDriver.cas == null) { RunDriver.cas = ae.newJCas(); }
	}

	private void process(final String s) {
		assert(RunDriver.cas !=null);
		RunDriver.cas.setDocumentText(s);
	}
}
