"""phy_tree.py
Class to Visulize the Phylogenetic Relationships/Connections in the Data 

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO 
                  -- ALL RIGHTS RESERVED 
        
        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code 
        (09/01/2021)

"""

import networkx as nx
import scale_data as data 
import matplotlib.pyplot as plt


class Trunk:
    def __init__(self):
        self.graph = self.mk_tree_trunk()
        self.all_fams = [
            'lycaenidae', 'nymphalidae',
            'zyganidae', 'saturniidae',
            'papilionidae', 'hesperiidae',
            'uraniidae', 'pieridae']
        self.traversal_nodes = [i for i in list(
            self.graph.nodes) if i not in self.all_fams]

    def mk_tree_trunk(self):
        G = nx.Graph()

        G.add_node('r')
        G.add_node('t0')
        G.add_node('t1')
        G.add_node('t2')
        G.add_node('t3')
        G.add_node('t4')
        G.add_node('t5')

        G.add_node('zyganidae')
        G.add_node('lycaenidae')
        G.add_node('nymphalidae')
        G.add_node('saturniidae')
        G.add_node('papilionidae')
        G.add_node('hesperiidae')
        G.add_node('pieridae')
        G.add_node('uraniidae')

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


global stem
stem = Trunk()


class Tree:
    def __init__(self, df, trunk=stem):
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
        self.fill_tree()
        self.simplify_once()
        show_tree(self)
        return

    def fill_tree(self):
        # init
        self.tree = self.trunk
        # Get the depth of the Hierarchy you want to Itterate over
        hierarchy, count = list(self.df.columns[1:5]),0
        while count < (len(hierarchy) - 1):
            # Get the corresponding Data to the Current lvl in the tree
            lvl = hierarchy[count]
            nodes = [i for i in set(self.df[lvl].values)]
            # 
            for p_node in nodes:
                node_df = self.df.loc[self.df[lvl] == p_node]
                sub_lvl = hierarchy[count + 1]
                children = [i for i in set(node_df[sub_lvl].values)]

                # ADD SUBFAMILY NODE AND CONNECT TO EXISTING TRUNK FAMILY NODE BY EDGE
                if p_node != '' and count == 0:
                    self.tree.add_node(p_node)  # ++ NODE
                    fams = list(
                        set(self.df.loc[self.df[lvl] == p_node]['family'].values))
                    if len(fams) == 1 and fams[0] != '':
                        self.tree.add_edge(fams[0], p_node)  # ++ EDGE

                grand_lvl = hierarchy[count - 1]
                for child in children:

                    # ADD NODE TO GRANDPARENT IF PARENT IS VOID
                    if p_node == '' and child != '':
                        grandparent = list(
                            self.df.loc[self.df[sub_lvl] == child][grand_lvl].values)[0]
                        if grandparent != '':
                            # ++ CHILD <-> GPARENT EDGE
                            self.tree.add_edge(child, grandparent)
                        else:
                            pass
                    if child == '':
                        dsub_lvl = hierarchy[count + 2]
                        gchildren = list(
                            self.df.loc[self.df[lvl] == p_node][dsub_lvl].values)
                        comp = list(
                            self.df.loc[self.df[sub_lvl] == child][dsub_lvl].values)
                        gr_children = [i for i in gchildren if i in comp]

                        # IF THE CHILD IS VOID BUT PARENT IS NOT CONNECT PARENT TO GRANDCHILD
                        for granchild in gr_children:
                            if granchild != '' and p_node != '':
                                # ++ G_CHILD <-> PARENT  EDGE
                                self.tree.add_edge(granchild, p_node)
                            else:
                                pass

                    else:
                        # ADD CHILD TO PARENT NODE
                        self.tree.add_node(child)  # ++ CHILD NODE
                        if p_node != '':
                            # ++ PARENT <-> CHILD EDGE
                            self.tree.add_edge(p_node, child)
                        else:
                            pass
            count += 1

        # Remove Manually Constructed Family Nodes which don't appear in our data
        all_famis = [i for i in set(self.df.family.values) if i != '']
        to_remove = [i for i in self.trunk_fams if i not in all_famis]

        for node in to_remove:
            if node in list(self.tree.nodes):
                self.tree.remove_node(node)

        return self.tree

    def simplify_once(self):

        g = self.tree

        d_dict = g.degree
        nodes = list(g.nodes)
        adj_dict = dict(g.adj)

        reducables = [i for i in nodes if d_dict[i] == 2]
        leaves = [i for i in nodes if d_dict[i] == 1]
        conns = [i for i in nodes if d_dict[i] > 2]

        # initilize a dictionary to connect leaves to their LCA
        d = {}

        for l in leaves:
            # Create a Deapth first search list from a leaf
            search_list = list(nx.dfs_preorder_nodes(g, l))

            # Pointer to list to itterate
            j = 0
            cnode = None
            while cnode not in conns:
                cnode = search_list[j]
                j += 1
            else:
                if l not in d.keys():
                    d[l] = cnode

        for c in conns:
            # Deapth First Search  itterator
            search_list = list(nx.dfs_preorder_nodes(g, c))
            j = 0
            x = search_list[j]
            while x not in conns or c == x:
                j += 1
                x = search_list[j]
            else:
                d[c] = x

        # They are by def. reducable having only 2 edges
        for r in reducables:
            g.remove_node(r)

        for k, v in d.items():
            g.add_edge(k, v)

        for l in leaves:
            if l in self.t_nodes:
                if l != 'r':
                    g.remove_node(l)

        self.tree = g

        return self.tree


def pos_nodes(Tree):
    # Vizual Layout
    return nx.kamada_kawai_layout(Tree.tree, dim=2)


def set_node_atts(Tree, p, nodes, color='red', size=700):
    nx.draw_networkx_nodes(Tree.tree, p, nodelist=nodes,node_color=color, node_size=size)


def draw_tree(Tree):
    # Draw the Kamada Kawaii
    nx.draw_kamada_kawai(self.tree, with_labels=1)
    plt.axis('off')
    plt.show()
    return
