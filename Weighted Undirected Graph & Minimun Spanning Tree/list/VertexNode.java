/* VertexNode.java */

package list;

public class VertexNode extends ListNode{

    protected EdgeList edges;
    protected VertexNode prev;
    protected VertexNode next;

    
    /**
     *  VertexNode() constructor.
     *  @param vertex the application representation of the vertex.
     *  @param l the list that this node belongs to.
     *  @param p the node previous to this node.
     *  @param n the node following this node.
     */
    public VertexNode(Object vertex, VertexList l, VertexNode p, VertexNode n){
    	item = vertex;
    	edges = new EdgeList();
    	myList = l;
    	prev = p;
    	next = n;
    }

    public EdgeList getEdges(){
        return edges;
    }

    /**
     *  next() returns the node following this node.  If this node is invalid,
     *  throws an exception.
     *
     *  @return the node following this node.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public VertexNode next() throws InvalidNodeException{
    	if(!isValidNode()){
            throw new InvalidNodeException("next() called on invalid node");
    	}
    	return next;
    }

    /**
     *  prev() returns the node preceding this node.  If this node is invalid,
     *  throws an exception.
     *
     *  @param node the node whose predecessor is sought.
     *  @return the node preceding this node.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public VertexNode prev() throws InvalidNodeException{
    	if(!isValidNode()){
            throw new InvalidNodeException("prev() called on invalid node");
    	}
    	return prev;
    }
    
    /**
     *  insertAfter() inserts an item immediately following this node.  If this
     *  node is invalid, throws an exception.
     *
     *  @param item the item to be inserted.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public void insertAfter(Object vertex) throws InvalidNodeException{
    	if(!isValidNode()){
            throw new InvalidNodeException("insertAfter() called on invalid node");
    	}
    	VertexNode nodeAfter = ((VertexList)myList).newNode(vertex, ((VertexList)myList), this, next);
    	next = nodeAfter;
    	next.next.prev = nodeAfter;
    	myList.size++;
    }

    /**
     *  insertBefore() inserts an item immediately preceding this node.  If this
     *  node is invalid, throws an exception.
     *
     *  @param item the item to be inserted.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public void insertBefore(Object vertex) throws InvalidNodeException{
        if (!isValidNode()) {
            throw new InvalidNodeException("insertBefore() called on invalid node");
        }
        VertexNode nodeBefore = ((VertexList)myList).newNode(vertex, ((VertexList)myList), prev, this);
        prev = nodeBefore;
        prev.prev.next = nodeBefore;
        myList.size++;
    }

    /**
     *  remove() removes this node from its VertexList.  If this node is invalid,
     *  throws an exception.
     *
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public void remove() throws InvalidNodeException {
        if (!isValidNode()) {
            throw new InvalidNodeException("remove() called on invalid node");
        }
        next.prev = prev;
        prev.next = next;
        myList.size--;
        myList = null;
        next = null;
        prev = null;
    }

}
