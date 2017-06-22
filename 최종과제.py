import sys
sys.setrecursionlimit(200000000)

k=[]
class RBtree:
    def __init__(self):
        self.__NIL = [0, True, None, None, None]
        self.__root = self.__NIL
        self.blackheight = 1
        self.currentbh = 0


    def __key_node(self, key):
        node = self.__root
        while node[0] != key and node != self.__NIL:
            if key < node[0]:
                node = node[3]
            else:
                node = node[4]
        return node

    def __minimum(self, node):
        while node[3] != self.__NIL: node = node[3]
        return node

    def __lrotate(self, x):
        y = x[4]
        y[2] = x[2]  # 1
        if y[2] == self.__NIL:  # 2
            self.__root = y
        elif y[2][3] == x:
            y[2][3] = y
        else:
            y[2][4] = y
        x[4] = y[3]  # 3
        if x[4] is not self.__NIL: x[4][2] = x
        y[3] = x  # 5
        x[2] = y  # 6

    def __rrotate(self, y):
        x = y[3]
        x[2] = y[2]
        if x[2] == self.__NIL:
            self.__root = x
        elif x[2][3] == y:
            x[2][3] = x
        else:
            x[2][4] = x
        y[3] = x[4]
        if y[3] is not self.__NIL: y[3][2] = y
        x[4] = y
        y[2] = x

    def __insert_fixup(self, node):
        nodep = node[2]
        if nodep[1]:
            self.__root[1] = True
            return
        nodepp = nodep[2]
        if nodep == nodepp[3]:
            nodeuncle = nodepp[4]
            if nodeuncle[1] == False:
                nodep[1] = nodeuncle[1] = True
                nodepp[1] = False
                return self.__insert_fixup(nodepp)
            if node == nodep[4]:
                self.__lrotate(nodep)
                self.__rrotate(nodepp)
                node[1] = True
                nodepp[1] = False
                return
            self.__rrotate(nodepp)
            nodep[1] = True
            nodepp[1] = False
        else:
            nodeuncle = nodepp[3]
            if nodeuncle[1] == False:
                nodep[1] = nodeuncle[1] = True
                nodepp[1] = False
                return self.__insert_fixup(nodepp)
            if node == nodep[3]:
                self.__rrotate(nodep)
                nodep = node
            self.__lrotate(nodepp)
            nodep[1] = True
            nodepp[1] = False

    def __transplant(self, u, v):
        if u is self.__root:
            self.__root = v
        elif u == u[2][3]:
            u[2][3] = v
        else:
            u[2][4] = v
        v[2] = u[2]

    def __delete_fixup(self, x):
        if not x[1] or x is self.__root:
            x[1] = True
            return
        xp = x[2]
        if x == xp[3]:
            w = xp[4]
            if w[4][1] == False:
                self.__lrotate(xp)
                w[1] = xp[1]
                xp[1] = w[4][1] = True
                return
            if w[3][1] == False:
                self.__rrotate(w)
                xp[4][1] = True
                w[1] = False
                return self.__delete_fixup(x)
            if not w[1]:
                self.__lrotate(xp)
                xp[1] = False
                w[1] = True
                return self.__delete_fixup(x)
        else:
            w = xp[3]
            if not w[3][1]:
                self.__rrotate(xp)
                w[1] = xp[1]
                xp[1] = w[3][1] = True
                return
            if not w[4][1]:
                self.__lrotate(w)
                w[1] = False
                xp[3][1] = True
                return self.__delete_fixup(x)
            if not w[1]:
                self.__rrotate(xp)
                xp[1] = False
                w[1] = True
                return self.__delete_fixup(x)
        w[1] = False
        self.__delete_fixup(xp)

    def __delete_node(self, node):
        if node[3] is self.__NIL:
            self.__transplant(node, node[4])
            if node[1]: return self.__delete_fixup(node[4])
            return
        if node[4] is self.__NIL:
            self.__transplant(node, node[3])
            if node[1]: return self.__delete_fixup(node[3])
            return
        newnode = self.__minimum(node[4])
        node[0] = newnode[0]
        self.__delete_node(newnode)


    def insert(self, key):
        node = self.__root
        if node == self.__NIL:
            self.__root = [key, True, self.__NIL, self.__NIL, self.__NIL]
            return
        while node != self.__NIL:
            nodep = node
            if key < node[0]:
                node = node[3]
            else:
                node = node[4]
        if key < nodep[0]:
            nodep[3] = [key, False, nodep, self.__NIL, self.__NIL]
            self.__insert_fixup(nodep[3])
        else:
            nodep[4] = [key, False, nodep, self.__NIL, self.__NIL]
            self.__insert_fixup(nodep[4])

    def delete(self, key):
        node = self.__key_node(key)
        if node is self.__NIL:return -1
        self.__delete_node(node)

    def exists(self, key):
        node = self.__key_node(key)
        if node != self.__NIL:
            print(key, 'exists.')
            self.__printnode(node)
            return
        else:
            print(key, 'does not exist.')


    ls = lambda self: self.inorder_tree_walk()

    def inorder_tree_walk(self, node=None):
        if node == None: node = self.__root
        if node != self.__NIL:
            self.inorder_tree_walk(node[3])
            k.append(node[0])
            self.inorder_tree_walk(node[4])

    def depthls(self, node=None, depth=-1):
        if node is None: node = self.__root
        depth += 1
        if node != self.__NIL:
            self.depthls(node[3], depth)
            print('Depth:', depth, '  key:', node[0], '  colour:', node[1] and 'black' or 'red')
            self.depthls(node[4], depth)






    printnode = lambda self, key: self.__printnode(self.__key_node(key))

    def __printnode(self, node):
        if node is self.__NIL:
            print('node does not exist.')
            return
        print('node key:', node[0])
        print('node colour:', node[1] and 'black' or 'red')
        if node[2] != self.__NIL:
            print('node parent key:', node[2][0])
            print('node parent colour:', node[2][1] and 'black' or 'red')
        if node[3] != self.__NIL:
            print('node left child key:', node[3][0])
            print('node left child colour:', node[3][1] and 'black' or 'red')
        if node[4] != self.__NIL:
            print('node right child key:', node[4][0])
            print('node right child colour:', node[4][1] and 'black' or 'red')

    def isbalance(self):
        self._update_blackheight()
        self.currentbh = 0
        self._checkbalance(self.__root)

    def _update_blackheight(self):
        self.blackheight = 1
        node = self.__root
        while node[3] is not self.__NIL:
            node = node[3]
            if node[1]: self.blackheight += 1
        print('bh=', self.blackheight)


    def _checkbalance(self, node):
        if node != self.__NIL:
            if node[1] : self.currentbh += 1
            self._checkbalance(node[3])
            self._checkbalance(node[4])
            if node[1]: self.currentbh -= 1
        else:
            if self.currentbh != self.blackheight:
                print('Tree not balanced! Current blackheight is', self.currentbh, 'whereas Blackheight is', self.blackheight)



def search():
        f = open("input.txt", 'r')
        rbt = RBtree()
        lines = f.readlines()
        for i in lines:
            if int(i) > 0:
                rbt.insert(int(i))
            elif int(i) < 0:
                i = abs(int(i))
                rbt.delete(int(i))
            else:
                rbt.inorder_tree_walk()
        f.close()

        g = open("search.txt", 'r')
        h = open("output.txt", 'w')
        lines=g.readlines()
        lines_t=[]
        for ii in lines:
            lines_t.append(ii[:-1])
        for i in lines_t:
            i=int(i)
            if i is 0:
                print('')
            else:
                if i in k:
                    i_index=k.index(i)
                    ip=i_index-1
                    ipv=k[ip]
                    a = max(k)
                    if i_index is k.index(a):
                        inev='NIL'
                    else:
                        ine=i_index+1
                        inev=k[ine]
                    if i_index is 0:
                        ipv='NIL'
                    h.write(str(ipv))
                    h.write(' ')
                    h.write(str(i))
                    h.write(' ')
                    h.write(str(inev))
                    h.write('\n')

                else:
                        ipv=i
                        inev=i
                        while ipv not in k:
                            ipv=int(ipv)-1
                            if ipv<= 0:
                                ipv='NIL'
                                break
                        while inev not in k:
                            inev=int(inev)+1
                            if int(inev)>max(k):
                                inev='NIL'
                                break
                        h.write(str(ipv))
                        h.write(' ')
                        h.write('NIL' )
                        h.write(' ')
                        h.write(str(inev))
                        h.write('\n')
        g.close()
        h.close()

        u= open('output.txt', 'r')
        lines=u.readlines()
        for i in lines:
            print(i)
        u.close()

search()