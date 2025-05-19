class BSTNode:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.parent = None
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.size = 0
        self.root = None

    #cause:xNode changes after each "insert_help function" call & for creating recursive func
    #so I have two func for inserting (insert() & insert_help())
    def insert(self, id, name):
        newNode = BSTNode(id, name)
        #If BSTtree is empty
        if self.isEmptyBST():
            self.root = newNode
            self.size += 1
        else:
            #to find the place of a new node in the tree & inserting
            self.insert_help(self.root, newNode)

    def insert_help(self, xNode, newNode):
        if newNode.id < xNode.id:
            if xNode.left is None:
                #inserting
                xNode.left = newNode
                newNode.parent = xNode
                #used for sizeBST function
                self.size += 1
            else:
                self.insert_help(xNode.left, newNode)
        else:
            if xNode.right is None:
                #inserting
                xNode.right = newNode
                newNode.parent = xNode
                #used for sizeBST function
                self.size += 1
            else:
                self.insert_help(xNode.right, newNode)

    #cause:xNode changes after each "search_help function" call & for creating recursive func
    #so I have two func for searching too (search() & search_help())
    def search(self, id):
        return self.search_help(self.root, id)

    def search_help(self, xNode, id):
        #If it's found
        if xNode is None or xNode.id == id:
            return xNode
        #searching
        if id < xNode.id:
            return self.search_help(xNode.left, id)
        else:
            return self.search_help(xNode.right, id)
            
    def transplant(self, pastNode, newNude):
        if pastNode.parent is None:
            self.root = newNude
        elif pastNode == pastNode.parent.left:
            pastNode.parent.left = newNude
        else:
            pastNode.parent.right = newNude
        if newNude is not None:
            newNude.parent = pastNode.parent

    def delete(self, id):
        node = self.search(id)
        if node is None:
            return
        #node with just a right child or without child
        if node.left is None:
            self.transplant(node, node.right)
        #node with just a left child
        elif node.right is None:
            self.transplant(node, node.left)
        #node with two children
        else:
            #minimum member in node's right children
            minInRight = self.tree_minimum(node.right)
            #If minInRight is'nt a child of node
            if minInRight.parent != node:
                self.transplant(minInRight, minInRight.right)
                minInRight.right = node.right
                minInRight.right.parent = minInRight
            #If minInRight is a child of node
            self.transplant(node, minInRight)
            minInRight.left = node.left
            minInRight.left.parent = minInRight
        #delete node with this id in MaxHeap too
        nodeMaxHeap = MaxHeap()
        nodeMaxHeap.delete(id)
        self.size -= 1

    def tree_minimum(self, node):
        while node and node.left is not None:
            node = node.left
        return node
    
    #VLR
    def pre_order(self):
        self.pre_order_help(self.root)

    def pre_order_help(self, node):
        if node is not None:
            print(f"Name: {node.name}, ID: {node.id}")
            self.pre_order_help(node.left)
            self.pre_order_help(node.right)

    def isEmptyBST(self):
        return self.root is None

    def sizeBST(self):
        return self.size
    #tamam bst
        
class HeapNode:
    def __init__(self, id, priority):
        self.id = id
        self.priority = priority

class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def insert(self, id, priority):
        newNode = HeapNode(id, priority)
        #add a new node
        self.heap.append(newNode)
        #sorting
        index = len(self.heap) - 1
        while index > 0:
            parentIndex = (index - 1) // 2
            if self.heap[index].priority > self.heap[parentIndex].priority:
                #swap newnode with its parent
                self.heap[index], self.heap[parentIndex] = self.heap[parentIndex], self.heap[index]
                index = parentIndex
            #sorted
            else:
                break
    
    def delete(self, id):
        for i in range(len(self.heap)):
            #node is found
            if self.heap[i].id == id:
                #replace it with last node
                self.heap[i] = self.heap[-1]
                #remove the last node
                self.heap.pop()
                #If i < len(self.heap) then it means maybe heap is'nt sort so I should check it
                if i < len(self.heap):
                    #sorting
                    self.maxHeapify(i)
                return
        #If node with this id is'nt exist
        print(f"node with id:{id} is'nt found!")
    
    def maxHeapify(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        #If left exist and its data bigger than largest data
        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left
        #If right exist and its data bigger than largest data
        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right
        if largest != index:
            #swap for srting
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            #sorting
            self.maxHeapify(largest)

    def extract_max(self):
        if self.isEmptyHeap():
            print("heap underflow")
            return None
        else:
            #save the node id for delete in BST too
            idBST = self.heap[0].id
            bstD = BST()
            bstD.delete(idBST)
            maxNode = self.heap[0]
            #remove the last of member and save it in lastNode
            lastNode = self.heap.pop()
            self.heap[0] = lastNode
            self.maxHeapify(0)
        return maxNode

    def increasePriority(self, id, newpriority):
        #find node's index with this id
        for i in range(len(self.heap)):
            if self.heap[i].id == id:
                index = i
            else:
                index = -1
        if index == -1:
            print("id is'nt found!")
            return
        #save the found index priority
        lastpriority = self.heap[index].priority
        if newpriority < lastpriority:
            print("new priority must be bigger than the last priority!")
            return
        #If newpriority >= lastpriority:
        #change the priority
        self.heap[index] = (self.heap[index].id, newpriority)
        #sorting
        self.maxHeapify(index)

    def printHeap(self):
        if self.isEmptyHeap():
            print("heap is empty")
            return
        for node in self.heap:
            print(f"Priority: {node.priority}, id: {node.id}")
            
    def isEmptyHeap(self):
        return len(self.heap) == 0
    
    def size(self):
        return len(self.heap)


bst = BST()
bst.insert(6, "mariwo")
bst.insert(11, "sepehr")
bst.insert(14, "jina")
bst.insert(9, "mhmd")
bst.insert(3, "mobina")
bst.insert(5, "poya")

maxheap = MaxHeap()
maxheap.insert(6, 18)
maxheap.insert(11, 84)
maxheap.insert(14, 20)
maxheap.insert(9, 58)
maxheap.insert(3, 36)
maxheap.insert(5, 25)

#print bst and heap
print("preorderBST:")
bst.pre_order()
print("\nHeap:")
maxheap.printHeap()

#searching in bst
node = bst.search(9)
if node:
    print(f"\nsearching id {9} :\nName: {node.name}, ID: {node.id}")
else:
    print("\nnode is'nt exist!")

#deleting in bst
node = bst.search(5)
if node:
    Name = node.name
bst.delete(5)
maxheap.delete(5)
if node:
    print(f"\nThe node with name {node.name} and ID 5 was successfully deleted!")
else:
    print("\nnode with id=5 is not exist!")

#print bst and heap
print("\npreorderBST:")
bst.pre_order()
print("\nHeap:")
maxheap.printHeap()

#extract max from heap
maxNode = maxheap.extract_max()
print(f"\nExtracted max: id: {maxNode.id}, Priority: {maxNode.priority}")
bst.delete(maxNode.id)

#print bst and heap
print("\npreorderBST:")
bst.pre_order()
print("\nHeap:")
maxheap.printHeap()

#increase priority
# print("\nincrease priority id = 3 to newpriority = 78")
# maxheap.increasePriority(3, 78)

#print bst and heap
# print("\npreorderBST:")
# bst.pre_order()
# print("\nHeap:")
# maxheap.printHeap()

#delete from heap
maxheap.delete(14)
print("\nnode with id = 14 is deleted in maxheap")

#print bst and heap
print("\npreorderBST:")
bst.pre_order()
print("\nHeap:")
maxheap.printHeap()
