
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t              # Minimum degree
        self.leaf = leaf        # Is true when node is leaf
        self.keys = []          # Keys in node
        self.children = []      # Child pointers

    def search(self, k):
        i = 0
        while i < len(self.keys) and k > self.keys[i]:
            i += 1
        if i < len(self.keys) and self.keys[i] == k:
            return self
        if self.leaf:
            return None
        return self.children[i].search(k)

    def split_child(self, i, y):
        t = self.t
        z = BTreeNode(t, y.leaf)
        mid_key = y.keys[t - 1]

        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        self.children.insert(i + 1, z)
        self.keys.insert(i, mid_key)

    def insert_non_full(self, k):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and k < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
        else:
            while i >= 0 and k < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i, self.children[i])
                if k > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(k)

    # -------- Deletion helpers --------
    def remove(self, k):
        idx = self.find_key(k)

        if idx < len(self.keys) and self.keys[idx] == k:
            if self.leaf:
                self.keys.pop(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            if self.leaf:
                return
            flag = idx == len(self.keys)
            if len(self.children[idx].keys) < self.t:
                self.fill(idx)
            if flag and idx > len(self.keys):
                self.children[idx - 1].remove(k)
            else:
                self.children[idx].remove(k)

    def find_key(self, k):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < k:
            idx += 1
        return idx

    def remove_from_non_leaf(self, idx):
        k = self.keys[idx]
        if len(self.children[idx].keys) >= self.t:
            pred = self.get_pred(idx)
            self.keys[idx] = pred
            self.children[idx].remove(pred)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ = self.get_succ(idx)
            self.keys[idx] = succ
            self.children[idx + 1].remove(succ)
        else:
            self.merge(idx)
            self.children[idx].remove(k)

    def get_pred(self, idx):
        cur = self.children[idx]
        while not cur.leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def get_succ(self, idx):
        cur = self.children[idx + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]

        child.keys.insert(0, self.keys[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys.pop(idx))
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        self.children.pop(idx + 1)


class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def search(self, k):
        return self.root.search(k)

    def insert(self, k):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, leaf=False)
            s.children.append(r)
            self.root = s
            s.split_child(0, r)
            s.insert_non_full(k)
        else:
            r.insert_non_full(k)

    def traverse(self, node=None, level=0):
        if node is None:
            node = self.root

        print("Level", level, " ", len(node.keys), "keys:", node.keys)
        if not node.leaf:
            for child in node.children:
                self.traverse(child, level + 1)


