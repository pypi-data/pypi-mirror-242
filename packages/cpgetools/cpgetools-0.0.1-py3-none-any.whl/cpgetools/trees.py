import graphviz
def root(A):
    if A!=[]:
        return str(A[0])
def left_child(A):
    if A!=[]:
        return A[1]
def right_child(A):
    if A!=[]:
        return A[2]
def is_empty(A):
    return A==[]
    
def draw_tree(A,title):
    #Parcour en largeur
    dot = graphviz.Digraph(title,comment='A binary tree',node_attr={'color': '#FFB6C1', 'style': 'filled'})
    Tree_Dot=dict()#permet de donner une correpo,dance entre les nodes de A et les labels de Dot
    file=[(A,-1)]
    i=0
    while file!=[]:
        T,i_pere=file.pop(0)
        dot.node(str(i),str(root(T)))
        if i!=0:
            dot.edge(str(i_pere),str(i))
        Tree_Dot[root(T)]=i
        gauche=left_child(T)
        droit=right_child(T)
        if gauche!=[]:
            file.append((gauche,i)) 
        if droit!=[]:
            file.append((droit,i))
        i+=1
    dot.attr(label=title)
    dot.attr(fontsize='20')
    return dot,Tree_Dot

def animate_secuence(Tree,sequence,titel="a sequence"):
    dot,Tree_Dot=draw_tree(Tree,titel)
    dot.attr(label=titel)
    dot.attr(fontsize='20')
    yield dot
    sequence2=[]
    i=0
    while True:
        i=i%len(sequence)
        node=sequence[i]
        sequence2.append(node)
        #dot.node("#sequence#",titel+"\n=["+"\n".join(sequence2)+"]",shape="rectangle")
        dot.attr(label=titel+"=\n["+"  ".join(sequence[:i+1])+"]",shape="rectangle")
        dot.node(str(Tree_Dot[node]),color="red")
        yield dot
        dot.node(str(Tree_Dot[node]),color="lightblue")
        i+=1


testTree=["+",["*",[4,[],[]],[5,[],[]]],["/",[6,[],[]],[7,[],[]]]]