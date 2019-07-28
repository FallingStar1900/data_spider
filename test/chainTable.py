import os
import sys

class Node:

    def __init__(self, data, pnext=None):
        self.data = data
        self._next = pnext

    def __repr__(self):
        return str(self.data)

class ChainData:

    def __init__(self):
        self.head = None
        self.length = 0

    def isEmpty(self):
        return (self.length == 0)

    def append_tail(self, dataOrNode):
        item = None
        if isinstance(dataOrNode, Node):
            item = dataOrNode
        else:
            item = Node(dataOrNode)

        # 如果self.head=None false ,not self.head = not false = true
        if not self.head:
            self.head = item
            self.length = self.length + 1
        else:
            node = self.head
            while node._next:
                node = node._next
            node._next = item
            self.length = self.length + 1

    def append_head(self, dataOrNode):
        item = None
        if isinstance(dataOrNode, Node):
            item = dataOrNode
        else:
            item = Node(dataOrNode)

        if not self.head:
            self.head = item
            self.length += 1
        else:
            tmp = self.head
            item._next = tmp
            self.head = item
            self.length += 1

    def deleteData(self, data):
        if self.isEmpty():
            print("the chainTable is empty")
            return
        if not data:
            print("dataOrNode is None")
            return
        # 只有一个节点的情况
        if self.head._next is None:
            self.head = None
            self.length -= 1
            return
        # 有多个节点的情况
        node = self.head
        prev = self.head
        while node:
            if node.data == data:
                prev._next = node._next
                self.length -= 1
                return
            else:
                prev = node
                node = node._next

    def deleteNode(self, index):
        if self.isEmpty():
            return
        if index <0 or index > int(self.length):
            print("index is invalid")
            return
        if index == 0:
            self.head = self.head._next
            self.length -= 1
            return
        node = self.head
        prev = self.head
        j = 1
        while node._next and j < index:
            prev = node
            node = node._next
            j = j + 1
        if j == index:
            prev._next = node._next
            self.length -= 1

    def updateData(self, srcData, orgData):
        if self.isEmpty():
            print("the chainTable is empty")
            return
        node = self.head
        if node.data == srcData:
            node.data = orgData
            return
        while node._next:
            node = node._next
            if node.data == srcData:
                node.data = orgData
                return

    def updateIndexData(self, index, data):
        if self.isEmpty():
            print("is empty")
            return

        if index > self.length or index <= 0:
            print("index is invalid")
            return
        j = 1
        node = self.head
        while j < index and node._next:
            node = node._next
            j = j + 1

        if j == index:
            node.data = data
            return

    def getNodeData(self, index):
        if self.isEmpty() or index <=0 or index > self.length:
            print("is invalid")
            return
        j = 1
        node = self.head
        while node._next and j < index:
            node = node._next
            j = j + 1

        if j == index:
            return node.data

    def getNodeIndex(self, data):
        if self.isEmpty():
            print("is invalid")
            return
        node = self.head
        j = 1
        while node:
            if node.data == data:
                return j
            node = node._next
            j = j + 1
        if j > self.length:
            print("no found")
            return

    def insert(self, index, dataOrNode):
        if self.isEmpty():
            print("is empty")
            return
        if index <= 0 or self.length <index or dataOrNode == "" or dataOrNode is None:
            print("is invalid")
            return
        j = 1
        if isinstance(dataOrNode, Node):
            item = dataOrNode
        else:
            item = Node(dataOrNode)

        if index == 1:
            item._next = self.head
            self.head = item
            self.length += 1
            return
        node = self.head
        prev = self.head
        while node._next and j < index:
                prev = node
                node = node._next
                j = j + 1
        if j == index:
            prev._next = item
            item._next = node
            self.length += 1

    def __repr__(self):
        if self.isEmpty():
            return "chainTable is empty"
        node = self.head
        nlist = ''
        while node:
            nlist = nlist + str(node.data) + ' '
            node = node._next
        return nlist

    def reverseChainTable(self, chainNode):
        if chainNode.isEmpty():
            print("the chain is empty")
            return
        if chainNode.length == 1:
            print("only one node ,not need reverse")
            return
        plast = None
        node = chainNode.head
        while node:
            tmp = node._next
            node._next = plast
            plast = node
            node = tmp
        return plast

    def merge2chainTable(self, pHead1, pHead2):
        if pHead1 is None and pHead2 is None:
            print("chain is empty")
            return
        tmpnode = Node(0)
        pnew = tmpnode
        while pHead1 and pHead2:
            if pHead1.data <= pHead2.data:
                pnew._next = pHead1
                pHead1 = pHead1._next
            else:
                pnew._next = pHead2
                pHead2 = pHead2._next
            pnew = pnew._next
        if pHead1 is not None:
            pnew._next = pHead1
        if pHead2 is not None:
            pnew._next = pHead2
        return tmpnode._next

    def merge2chainTable1(self, pHead1, pHead2):
        if pHead1 is None and pHead2 is None:
            print("is empty")
            return None
        if pHead1 is None:
            return pHead2
        if pHead2 is None:
            return pHead1
        if pHead1.data <= pHead2.data:
            pre = pHead1
            pre._next = self.merge2chainTable1(pHead1._next, pHead2)
        else:
            pre = pHead2
            pre._next = self.merge2chainTable1(pHead1, pHead2._next)
        return pre

    def findCommonNode(self, pHead1, pHead2):
        if pHead1 is None or pHead2 is None:
            return None
        node1 = pHead1._next
        node2 = pHead2._next
        if node1.data == node2.data:
            return node1
        length1 = 0
        length2 = 0
        while node1:
            length1 += 1
            node1 = node1._next
        while node2:
            length2 += 1
            node2 = node2._next
        node1 = pHead1
        node2 = pHead2

        if length1 >= length2:
            div = length1 - length2
            while div > 0:
                node1 = node1._next
                div = div - 1
        else:
            div = length2 - length1
            while div > 0:
                node2 = node2._next
                div = div - 1
        while node1.data != node2.data and node1 is not None and node2 is not None:
            node1 = node1._next
            node2 = node2._next
        if node1 is None or node2 is None:
            return None
        else:
            return node1.data

    #判断一个链表是否有环或者环的入口
    def EntryNodeOfLoop(self, pHead):
        if pHead is None or pHead.next is None or pHead.next.next is None:
            return None
        p1 = pHead.next
        p2 = pHead.next.next
        while p1 != p2:
            if p1 is not None and p2 is not None:
                p1 = p1.next
                p2 = p2.next.next
            else:
                return None
        #return p1
        p2 = pHead
        while p1 != p2:
            if p1.next == p2:
                return p2
            p1 = p1.next
            p2 = p2.next
        return p1

    def deleteDuplication(self, pHead):
        if pHead is None:
            return pHead
        a = []
        b = set()
        p = pHead
        while p:
            if p.val not in a:
                a.append(p.val)
            else:
                b.add(p.val)
            p = p.next
        p = pHead
        tmp = []
        while p:
            if p.val in b:
                p = p.next
                continue
            else:
                tmp.append(p)
            p = p.next
        if not len(tmp):
            return None
        pHead = tmp[0]
        i = 0
        j = len(tmp)-1
        while i<j:
            tmp[i].next = tmp[i+1]
            tmp[i+1].next = None
            i = i + 1
        return pHead


if __name__ == "__main__":
    chainTable = ChainData()
    for i in [1,1,2,3,3,4,5,5]:
        chainTable.append_tail(i)
    print(chainTable)
    node = chainTable.deleteDuplication(chainTable.head)
    print(node.data)
    '''
    chainTable1 = ChainData()
    for j in [2,4,6,8]:
        chainTable1.append_tail(j)
    print(chainTable1)
    mergeTable = ChainData()
    new_head = mergeTable.merge2chainTable1(chainTable.head, chainTable1.head)
    node = new_head
    nlist = ''
    while node:
        nlist = nlist + str(node.data) + ' '
        node = node._next
    print(nlist)

    
    last = chainTable.reverseChainTable(chainTable)
    node = last
    nlist = ''
    while node:
        nlist = nlist + str(node.data) + ' '
        node = node._next
    print(nlist)   
    nodes = Node(555)
    chainTable.insert(4, nodes)
    print(chainTable)
    chainTable.insert(3,222)
    print(chainTable)
    index = chainTable.getNodeIndex(14)
    print(index)
    data = chainTable.getNodeData(19)
    print(data)
    chainTable.updateIndexData(3, 222)
    print(chainTable)
    chainTable.updateData(12, 111)
    print(chainTable)
    print(chainTable)
    chainTable.deleteData(3)
    print(chainTable)
    chainTable.deleteData(1)
    print(chainTable)
    '''