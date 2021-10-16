"""phy_tree.py

Class to Visualize the Phylogenetic Relationships/Connections in the Data 

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO 
                  -- ALL RIGHTS RESERVED 
        
        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code 
        (10/16/2021)

"""


import networkx as nx
import matplotlib.pyplot as plt

# Have some way of vizually differenting diffrent parts of the tree
DEFAULT_T_NODE_COLOR = 'black'
DEFAULT_FAM_COLOR = 'red'
DEFAULT_SPECIES_COLOR = 'green'
DEFAULT_CONN_COLOR = 'blue'

DEFAULT_GRAPH = nx.Graph()


class Trunk:
    """
        Phylogenetic Family Data Composing the Main Stem of the Phylogenetic Tree. 
        The Tree Class is a class which takes in the Trunk Class as a parameter from which 
        it constructs the tree from a DataFrame Provided. 

        attr :: self.graph - The networkx.Graph Object Representing the Phylogenetic Tree's Structure 
        attr :: self.all_fams - The Main Butterfly and Moth Families comprising our data 
        attr :: self.traversal_nodes - The nodes in the Graph objects which are not families, species nodes but seperation nodes between the 
                                        families at the time of divergence. Essentially the nodes that represent a common ancestor not reflected in the data provided.
    """

    def __init__(self, Graph=DEFAULT_GRAPH):
        """ Trunk Constructor    
            ~ This is all HardCoded in to avoid any mistakes in the phylogenetic relationships between the diffrent families in the DataSet.
        """
        self.all_fams = [
            'lycaenidae',
            'nymphalidae',
            'zyganidae',
            'saturniidae',
            'papilionidae',
            'hesperiidae',
            'uraniidae',
            'pieridae'
        ]
        self.graph = self.mk_tree_trunk(Graph)
        self.traversal_nodes = [i for i in list(
            self.graph.nodes) if i not in self.all_fams]

    def mk_tree_trunk(self, G):
        """ Constructs Phylogentic Tree of our ButteryFly and Moths in terms of families.
        """
        # mk the root and the diff connectors
        G.add_node('r')
        G.add_node('t0')
        G.add_node('t1')
        G.add_node('t2')
        G.add_node('t3')
        G.add_node('t4')
        G.add_node('t5')
        # Add The families in our data as nodes in a graph
        for fam in self.all_fams:
            G.add_node(fam)
        # connect connectors to fam to mk Trunk
        G.add_edge('r', 'zyganidae')
        G.add_edge('r', 't0')
        G.add_edge('t0', 't1')
        G.add_edge('t0', 't2')
        G.add_edge('t2', 'saturniidae')
        G.add_edge('t2', 'uraniidae')
        G.add_edge('t1', 'papilionidae')
        G.add_edge('t1', 't3')
        G.add_edge('t3', 'hesperiidae')
        G.add_edge('t3', 't4')
        G.add_edge('t4', 't5')
        G.add_edge('t4', 'pieridae')
        G.add_edge('t5', 'lycaenidae')
        G.add_edge('t5', 'nymphalidae')
        return G


stem = Trunk()


def draw_tree(Tree):
    """ Draws Phylogenetic Tree

        Inputs:
            ('networkx.classes.graph.Graph' Object Class) - 'Tree' : The Graph Object Representing Phylogenetic Relationships
        Outputs:
            (None) - Plots Graph Object 
    """
    # Draw the Kamada Kawaii
    nx.draw_kamada_kawai(Tree, with_labels=1)
    plt.axis('off')
    plt.show()
    plt.clf()
    return


def pos_nodes(Tree):
    """ Returns Position of Nodes comprising the Phylogenetic Tree

        Inputs:
            ('networkx.classes.graph.Graph' Object Class) - 'Tree' : The Graph Object Representing Phylogenetic Relationships
        Outputs:
            (Dictionary) - Dictionary mapping node names to their planar co-ordinates i.e {'pieridae' : [0.1678,-0.801]}
    """
    return nx.kamada_kawai_layout(Tree, dim=2)


def set_node_attributes(Tree, nodes, color='red', size=700):
    """ Changes the 'nodes' in the 'Tree' Graph to have 'color' and have a diameter 'size'

        Inputs:
            ('networkx.classes.graph.Graph' Object Class) - 'Tree': The Graph object 
            (List of Strings) - 'nodes': The nodes in the Graph whose attributes you want to set
            (String) - 'color' : The Color of the nodes in the Graph
            (Int) - 'size' : The Diameter of the nodes in the Graph
        Outputs:
            (None) - Alters the Graph Object
    """
    poses = pos_nodes(Tree)
    nx.draw_networkx_nodes(Tree, poses, nodelist=nodes,
                           node_color=color, node_size=size)


class Tree:
    """
        The Phylogenetic Tree Object representing the 'relatedness' of diffrent species in our study

        attr :: 'self.trunk' : The 'Trunk' Object Class from which we fill out the rest of the tree given the input params
        attr :: 'self.trunk_fams' : All The diffrent families in the Trunk Graph
        attr :: 'self.t_nodes' : The name of the traversal nodes in the Trunk Graph
        attr :: 'self.df' : A DataFrame from our study containing the species samples to fill out the rest of the Tree
        attr :: 'self.tree' : The Graph Object of the Phylogenetic Tree of the Data 'self.df'
    """

    def __init__(self, df, trunk=stem):
        """
            Tree Class Constructor: 
                Creates a Graph representation of the Phylogenetic Data from our study

            param :: 'df' - Pandas.DataFrame Type Object Class of our Scale Data 
            param :: 'trunk' - The networkx.Graph object representing the family phylogony of our diffrent families 
        """
        # Constructor Data
        self.trunk = trunk.graph                # Manual Graph
        self.trunk_fams = trunk.all_fams        # Families in DB
        self.t_nodes = trunk.traversal_nodes    # Traversal Nodes
        # Construction Params
        self.df = df                            # Scale Data
        # init
        self.tree = None
        self.complete()

    def complete(self):
        """ Fills Graph Object out given the input parameters into the class 
        """
        self.fill_tree()                    # This fills out the trunk with DataFrame Phylogeny
        self.simplify_totally()             # Simplify's our Relationships to LCA's only
        # Add some visual flair to make this easier on the eyes
        self.add_node_color()
        draw_tree(self.tree)                # Represent our Phylogony

    def fill_tree(self):
        """ Fills The Tree Graph Structure outwardly from the Stem itterating over the 
            DataFrame inputted as a parameter in the constructor 
        """
        # void inputs
        voids = ['', 'nan', None]
        # init
        self.tree = self.trunk
        # Get the depth of the Hierarchy you want to Itterate over
        hierarchy, count = list(self.df.columns[1:5]), 0
        while count < (len(hierarchy) - 1):
            # Get the corresponding Data to the Current lvl in the tree
            lvl = hierarchy[count]
            nodes = [i for i in set(self.df[lvl].values)]
            print('0- ', lvl, nodes)
            for p_node in nodes:
                node_df = self.df.loc[self.df[lvl] == p_node]
                sub_lvl = hierarchy[count + 1]
                children = [i for i in set(node_df[sub_lvl].values)]

                # ADD SUBFAMILY NODE AND CONNECT TO EXISTING TRUNK FAMILY NODE BY EDGE
                if p_node not in voids and count == 0:
                    self.tree.add_node(p_node)  # ++ NODE
                    fams = list(
                        set(self.df.loc[self.df[lvl] == p_node]['family'].values))
                    if len(fams) == 1 and fams[0] not in voids:
                        self.tree.add_edge(fams[0], p_node)  # ++ EDGE

                grand_lvl = hierarchy[count - 1]
                for child in children:

                    # ADD NODE TO GRANDPARENT IF PARENT IS VOID
                    if p_node in voids and child not in voids:
                        grandparent = list(
                            self.df.loc[self.df[sub_lvl] == child][grand_lvl].values)[0]
                        if grandparent not in voids:
                            # ++ CHILD <-> GPARENT EDGE
                            self.tree.add_edge(child, grandparent)
                        else:
                            pass
                    if child in voids:
                        dsub_lvl = hierarchy[count + 2]
                        gchildren = list(
                            self.df.loc[self.df[lvl] == p_node][dsub_lvl].values)
                        comp = list(
                            self.df.loc[self.df[sub_lvl] == child][dsub_lvl].values)
                        gr_children = [i for i in gchildren if i in comp]

                        # IF THE CHILD IS VOID BUT PARENT IS NOT CONNECT PARENT TO GRANDCHILD
                        for granchild in gr_children:
                            if granchild not in voids and p_node not in voids:
                                # ++ G_CHILD <-> PARENT  EDGE
                                self.tree.add_edge(granchild, p_node)
                            else:
                                pass

                    else:
                        # ADD CHILD TO PARENT NODE
                        self.tree.add_node(child)  # ++ CHILD NODE
                        if p_node not in voids:
                            # ++ PARENT <-> CHILD EDGE
                            self.tree.add_edge(p_node, child)
                        else:
                            pass
            count += 1

        # Remove Manually Constructed Family Nodes which don't appear in our data
        all_famis = [i for i in set(
            self.df.family.values) if i not in voids]
        to_remove = [i for i in self.trunk_fams if i not in all_famis]
        for node in to_remove:
            if node in list(self.tree.nodes):
                self.tree.remove_node(node)

    def remove_nodes(self, nodes):
        """ Removes the nodes listed from the Phylogentic Tree
        """
        for node in nodes:
            self.tree.remove_node(node)
        return

    def reduce_nodes(self, nodes):
        """ Reduces the nodes listed from the Phylogentic Tree
                i.e : Removes itself and connects the only other two adjacent nodes to each other 
        """
        d_adj = self.tree.adj
        for node in nodes:
            # get the keys of the value in the adjacency dictionary
            to_connect = list(d_adj[node].keys())
            assert len(
                to_connect) == 2, 'Reducible Node by definition only has two edges'
            # Remove the node
            self.remove_nodes([node])
            # Connect the two nodes that need to be
            self.tree.add_edge(to_connect[0], to_connect[1])

    def simplify_once(self):
        """ Simplify The given Graph 'G' to remove reducible nodes in the Graph. 
        """
        # Get nodes and how many connections they each have
        d_dict, nodes = self.tree.degree, list(self.tree.nodes)
        # remove reducable Nodes & Leaves of the Tree
        reducable_nodes, leaves = [i for i in nodes if d_dict[i] == 2 and i not in self.trunk_fams], [
            i for i in nodes if d_dict[i] == 1]
        # Reduce Appropriate Nodes
        self.reduce_nodes(reducable_nodes)
        # remove any transitionary nodes that may have stuck around after a prune
        self.remove_nodes(
            [i for i in leaves if i in self.t_nodes and i != 'r'])

    def simplify_totally(self):
        """ Simplify the phylogenetic tree to the point it can't be simplified any further 
        """
        tree, next_tree = 0, 1
        while tree != next_tree:
            tree = self.tree
            self.simplify_once()
            next_tree = self.tree
            self.simplify_once()
        else:
            return

    def add_node_color(self):
        """ Changes the Node attributes to be more visually interesting
        """
        # Get nodes and how many connections they each have
        d_dict, nodes = self.tree.degree, list(self.tree.nodes)
        species = [i for i in nodes if d_dict[i] == 1 and i != 'r']
        families = [i for i in nodes if i in self.trunk_fams]
        trans = [i for i in nodes if i in self.t_nodes]
        # Throwaway to just do a quick group exclusion
        th_ = []
        th_.extend(species)
        th_.extend(families)
        th_.extend(trans)
        # get anything that's a subfamily ect
        conns = [i for i in nodes if i not in set(th_)]
        set_node_attributes(self.tree, nodes=species,
                            color=DEFAULT_SPECIES_COLOR)
        set_node_attributes(self.tree, nodes=families, color=DEFAULT_FAM_COLOR)
        set_node_attributes(self.tree, nodes=trans, color=DEFAULT_T_NODE_COLOR)
        set_node_attributes(self.tree, nodes=conns, color=DEFAULT_CONN_COLOR)
