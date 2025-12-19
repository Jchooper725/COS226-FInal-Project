class BTreeNode:
    def __init__(self, t, leaf=False, parent=None):
        self.t = t
        self.leaf = leaf
        self.parent = parent
        self.keys = []        # each element is [key, data]
        self.children = []

    def search(self, k):
        """Search for a key k (first element of pair)"""
        i = 0
        while i < len(self.keys) and k > self.keys[i][0]:
            i += 1

        if i < len(self.keys) and self.keys[i][0] == k:
            return self.keys[i]   # return the [key, data] pair

        if self.leaf:
            return None

        return self.children[i].search(k)


class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def insert(self, pair):
        """
        Insert a [key, data] pair
        The key is pair[0]
        """
        key = pair[0]
        root = self.root

        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root)
            root.parent = new_root
            self.root = new_root
            self.split_child(new_root, 0)

        self.insert_non_full(self.root, pair)

    def split_child(self, parent, i):
        t = self.t
        node = parent.children[i]
        new_node = BTreeNode(t, leaf=node.leaf, parent=parent)

        # Move middle key up
        parent.keys.insert(i, node.keys[t - 1])
        parent.children.insert(i + 1, new_node)

        # Split keys
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]

        # Split children
        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]
            for child in new_node.children:
                child.parent = new_node

    def insert_non_full(self, node, pair):
        i = len(node.keys) - 1
        key = pair[0]

        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = pair
        else:
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == 2 * self.t - 1:
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1

            node.children[i].parent = node
            self.insert_non_full(node.children[i], pair)

    def traverse(self, node=None, level=0):
        if node is None:
            node = self.root

        parent_keys = [k[0] for k in node.parent.keys] if node.parent else None
        print(f"Level {level} | Keys: {[k for k in node.keys]} | Parent keys: {parent_keys}")

        for child in node.children:
            self.traverse(child, level + 1)
