package werti.uima.ae.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

import org.apache.uima.analysis_engine.AnalysisEngineProcessException;

/**
 * A wrapper around the external morphg program, which is used to
 * generate base forms of verbs for the gerunds topic.
 * 
 * @author Niels Ott?
 * @author Adriane Boyd
 *
 */
public class Morphg {	
	private String morphgLoc;
	private String morphgVerbstemLoc;
	
	public Morphg(String execLoc, String verbstemLoc) {
		morphgLoc = execLoc;
		morphgVerbstemLoc = verbstemLoc;
	}

	/**
	 * 
	 * @param tokenList
	 * @return a string of tab-separated morphg output
	 * @throws AnalysisEngineProcessException 
	 */
	public String process(String input) throws AnalysisEngineProcessException { 		
		// build argument list
		ArrayList<String> argList = new ArrayList<String>();
		argList.add(morphgLoc);
		argList.add("-f");
		argList.add(morphgVerbstemLoc);

		// obtain process
		ProcessBuilder builder = new ProcessBuilder(argList);
		String output = "";
		try {
			Process process = builder.start();

			// get input and output streams (are they internally buffered??)
			BufferedWriter tomorphg =  new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
			BufferedReader frommorphg = new BufferedReader(new InputStreamReader(process.getInputStream()));

			tomorphg.write(input);
			tomorphg.close();
			output = frommorphg.readLine();
			frommorphg.close();
		} catch (IOException e) {
			throw new AnalysisEngineProcessException(e);
		}
		
		return output;
	}
}
