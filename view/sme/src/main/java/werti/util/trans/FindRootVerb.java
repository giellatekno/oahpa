package werti.util.trans;

/*import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.jgrapht.DirectedGraph;

import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DirectedSubgraph;

import org.jgrapht.traverse.DepthFirstIterator;

import werti.uima.ae.PassiveSentenceConverter;

import werti.uima.types.annot.Token;

import werti.util.Transformation;*/

public class FindRootVerb { /*<A extends DirectedGraph<Token,PassiveSentenceConverter.RelationshipEdge>> implements Transformation<A> {

	//public List<DirectedGraph<Token,PassiveSentenceConverter.RelationshipEdge>> apply(A g) {
	public List<A> apply(A g) {
		final Set<Token> ts = g.vertexSet();
		final List<DirectedGraph<Token,PassiveSentenceConverter.RelationshipEdge>> r =
			new ArrayList<DirectedGraph<Token,PassiveSentenceConverter.RelationshipEdge>>();

		for (final Token t:ts) {
			if (t.getTag().matches("^V.*") && g.incomingEdgesOf(t).size() == 0) {
				r.add(getSubgraph(g,t));
			}
		}
		return (List<A>)r;
	}

	private DirectedGraph<Token,PassiveSentenceConverter.RelationshipEdge> getSubgraph(A g, Token root) {
		final DepthFirstIterator<Token,PassiveSentenceConverter.RelationshipEdge> it =
			new DepthFirstIterator<Token,PassiveSentenceConverter.RelationshipEdge>(g,root);
		final Set<Token> subgraphVertices = new HashSet<Token>();
		final Set<PassiveSentenceConverter.RelationshipEdge> subgraphEdges =
			new HashSet<PassiveSentenceConverter.RelationshipEdge>();

		while (it.hasNext()) { subgraphVertices.add(it.next()); }
		for (final Token t:subgraphVertices) {
			subgraphEdges.addAll(g.outgoingEdgesOf(t));
		}
		return new DirectedSubgraph<Token,PassiveSentenceConverter.RelationshipEdge>(g,subgraphVertices, subgraphEdges);
	}

	public boolean meetsPrecondition(A g) {
		return true;
	}*/
}
