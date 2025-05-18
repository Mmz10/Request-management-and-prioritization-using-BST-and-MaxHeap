class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.left = None
        self.right = None
        self.parent = None

class BST:
    def __init__(self):
        self.root = None

    def Insert(self, id, name):
        newNode = Node(id, name)
        if self.root is None:
            self.root = newNode
            return
        x = self.root
        while True:
            if id < x.id:
                if x.left is None:
                    x.left = newNode
                    newNode.parent = x
                    return
                x = x.left
            elif id > x.id:
                if x.right is None:
                    x.right = newNode
                    newNode.parent = x
                    return
                x = x.right
            # dr sort tekrari bodne id:
            else:
                return

    def search(self, id):
        x = self.root
        if x is None or x.id == x:
            return x
        if id < x.id:
            return search(x.left, id)
        else:
            return search(x.right, id)

    def Transplant(self, p, n):
        if p.parent is None:
            self.root = n
        elif p == p.parent.left:
            p.parent.left = n
        else:
            p.parent.right = n
        if n is not None:
            p.parent = n.parent
            
    def FindMin(self, x):
        while x.left is not None:
            x = x.left
        return x
    
    def delete(self, id):
        n = self.search(id)
        if n is None:
            print('not found!')
            return
        # n without child
        if n.left is None and n.right is None:
            # n = root
            if n.parent is None:
                self.root = None
            else:
                # n = left child
                if n.parent.left == n:
                    n.parent.left = None
                # n = right child
                else:
                    n.parent.right = None
        # n with one child
        # with left child
        elif n.left is None:
            Transplant(self, id, id.right)
        #with right child
        elif n.right is None:
            Transplant(self, id, id.left)
        # n with two child
        else:
            y = FindMin(id.right)
            if y.parent != id:
                Transplant(self, y, y.right)
                y.right = id.right
                y.right.parent = y
            Transplant(self, id, y)
            y.left = id.left
            y.left.parent = y

    def PrintIN(self, x):
        if x is not None:
            self.Print(x.left)
            print(f'ID: {x.id}, Name: {x.name}')
            self.Print(x.right)