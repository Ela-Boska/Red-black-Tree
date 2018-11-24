import queue
import pdb
Black = 'Black'
Red = 'Red'

class node():
    def __init__(self,key,value=None):
        self.key = key
        self.value = value
        self.p = None
        self.left = None
        self.right = None
        self.color = None
    
    def __repr__(self):
        return '{}:{}'.format(self.key, self.color)



class RBTree():
    def __init__(self, root = None):
        self.root = root
        
    def mid(self):
        def _mid(x):
            if x == None:
                return []
            else:
                return _mid(x.left) + [x] + _mid(x.right)
        return _mid(self.root)

    def pre(self):
        def _pre(x):
            if x == None:
                return []
            else:
                return [x] + _pre(x.left) + _pre(x.right)
    
    def __call__(self,key):
        return self.find(key)

    @property
    def height(self):
        def _height(x):
            if x==None:
                return 0
            else:
                return max(_height(x.left)+1,_height(x.right)+1)
        return _height(self.root)

    @property
    def min_height(self):
        def min_height(x):
            if x==None:
                return 0
            else:
                return min(min_height(x.left)+1,min_height(x.right)+1)
        return min_height(self.root)

    def find(self,key):
        x = self.root
        while x==None or x.key != key:
            if x == None:
                return None
            if x.key > key:
                x = x.left
            else:
                x = x.right
        return x

    def print(self):
        assert self.height <6, 'The height is out of range!'
        length = 8
        unit = length + 2
        height = self.height
        xs = [[None,0] for x in range(2**height)]
        def plug(a, coor):
            if a == None:
                return
            xs[coor][0] = a
            plug(a.left,coor*2)
            plug(a.right,coor*2+1)
        plug(self.root,1)
        for i in range(len(xs)//2,len(xs)):
            xs[i][1] = i - len(xs)//2
        for h in range(height-1,0,-1):
            for j in range(2**(h-1),2**h):
                xs[j][1] = (xs[2*j][1] + xs[2*j+1][1])/2
        for h in range(1,1+height):
            print(' '*int(xs[2**(h-1)][1]*unit),end='')
            for j in range(2**(h-1),2**h):
                if xs[j][0] == None:
                    print(' '*unit, end='')
                else:
                    print('{:10}'.format(str(xs[j][0])),end='')
                if j+1<2**h:
                    print(' '*int(unit * (xs[j+1][1]-xs[j][1]-1)), end='')
            print()


    def add(self,a):
        if not isinstance(a,node):
            a = node(a)
        if self.root == None:
            self.root = a
            a.color = Black
        else:
            a.color = Red
            x = self.root
            while True:
                if x.key > a.key:
                    if x.left == None:
                        x.left = a
                        a.p = x
                        break
                    else:
                        x = x.left
                elif x.key < a.key:
                    if x.right == None:
                        x.right = a
                        a.p = x
                        break
                    else:
                        x = x.right

            add_fix(self,a)

    def delete(self,z):
        if not isinstance(z,node):
            z = self.find(z)
            if z == None:
                raise ValueError('key not find')
        def _delete(T, x):
            if x.left == None and x.right == None:
                if x == T.root:
                    T.root = None
                    del x
                elif x.color == Red:
                    if x.p.left == x:
                        x.p.left = None
                    else:
                        x.p.right = None
                    del x
                else:
                    p = x.p
                    if p.left == x:
                        p.left = None
                        del x
                        del_fix(self, p, True)
                    else:
                        p.right = None
                        del x
                        del_fix(self, p, False)
                    
            elif x.left == None:
                if x != T.root:
                    if x.p.left == x:
                        x.p.left = x.right
                    else:
                        x.p.right = x.right
                    x.right.p = x.p
                    x.right.color = Black
                else:
                    T.root = x.right
                    x.right.color = Black
                del x
            elif x.right == None:
                if x != T.root:
                    if x.p.left == x:
                        x.p.left = x.left
                    else:
                        x.p.right = x.left
                    x.left.p = x.p
                    x.left.color = Black
                else:
                    T.root = x.left
                    x.left.color = Black
                del x
            else:
                temp = successor(x)
                x.key = temp.key
                x.value = temp.value
                _delete(T, temp)
        _delete(self, z)


def lr(T, a):
    r = a.right
    a.right = r.left
    if r.left != None:
        r.left.p = a
    r.p = a.p
    if a.p == None:
        T.root = r
    elif a == a.p.left:
        a.p.left = r
    else:
        a.p.right = r
    a.p = r
    r.left = a
        

def rr(T, a):
    r = a.left
    a.left = r.right
    if r.right != None:
        r.right.p = a
    r.p = a.p
    if a.p == None:
        T.root = r
    elif a == a.p.right:
        a.p.right = r
    else:
        a.p.left = r
    a.p = r
    r.right = a

def add_fix(T, a):
    while a.p != None and a.p.color == Red:
        if a.p == a.p.p.left:
            y = a.p.p.right
            if y != None and y.color == Red:
                a.p.p.color = Red
                a.p.color = Black
                y.color = Black
                a = a.p.p
            else:
                if a.p.right == a:
                    a = a.p
                    lr(T, a)
                a.p.color = Black
                a.p.p.color = Red
                rr(T, a.p.p)

            
        
        else:
            y = a.p.p.left
            if y != None and y.color == Red:
                a.p.p.color = Red
                a.p.color = Black
                y.color = Black
                a = a.p.p
            else:
                if a.p.left == a:
                    a = a.p
                    rr(T, a)
                a.p.color = Black
                a.p.p.color = Red
                lr(T, a.p.p)
        T.root.color = Black
    
def successor(z):
    if z.right == None:
        raise ValueError(r"This node doesn't have right child!")
    ans = z.right
    while ans.left != None:
        ans = ans.left
    return ans

def del_fix(T, z, del_left):
    if not del_left:
        bro = z.left
        if bro.color == Black:
            if z.color == Red:
                if color(bro.right) == Black and color(bro.left) == Black:
                    bro.color = Red
                    z.color = Black
                elif color(bro.left) == Black:
                    z.color = Black
                    lr(T, bro)
                    rr(T,z)
                elif color(bro.right) == Black:
                    bro.color = Red
                    z.color = Black
                    bro.left.color = Black
                    rr(T, z)
                else:
                    bro.color = Red
                    bro.left.color = Black
                    z.color = Black
                    rr(T,z)
            else:   # z:black
                if color(bro.right) == Black and color(bro.left) == Black:
                    bro.color = Red
                    if z != T.root:
                        if z.p.left == z:
                            del_fix(T, z.p, True)
                        else:
                            del_fix(T, z.p, False)
                elif color(bro.left) == Black:
                     bro.right.color = Black
                     lr(T, bro)
                     rr(T, z)
                elif color(bro.right) == Black:
                    bro.left.color = Black
                    rr(T, z)
                else:
                    bro.left.color = Black
                    rr(T, z)
        else:                                   # bro:Red & parent:Black
            z.color = Red
            bro.color = Black
            rr(T, z)
            del_fix(T, z, False)
    else:
        bro = z.right
        if bro.color == Black:
            if z.color == Red:  
                if color(bro.right) == Black and color(bro.left) == Black:
                    bro.color = Red
                    z.color = Black
                elif color(bro.right) == Black:
                    z.color = Black
                    rr(T, bro)
                    lr(T,z)
                elif color(bro.left) == Black:
                    bro.color = Red
                    z.color = Black
                    bro.right.color = Black
                    lr(T, z)
                else:
                    bro.color = Red
                    bro.right.color = Black
                    z.color = Black
                    lr(T,z)
            else:   # z:black
                if color(bro.right) == Black and color(bro.left) == Black:
                    bro.color = Red
                    if z != T.root:
                        if z.p.left == z:
                            del_fix(T, z.p, True)
                        else:
                            del_fix(T, z.p, False)
                elif color(bro.right) == Black:
                     bro.left.color = Black
                     rr(T, bro)
                     lr(T, z)
                elif color(bro.left) == Black:
                    bro.right.color = Black
                    lr(T, z)
                else:
                    bro.right.color = Black
                    lr(T, z)
        else:                                   # bro:Red & parent:Black
            z.color = Red
            bro.color = Black
            lr(T, z)
            del_fix(T, z, True)

def black_count(Tree):
    root = Tree.root
    def _black_count(x):
        if x == None:
            return 1
        else:
            l_count = _black_count(x.left)
            r_count = _black_count(x.right)
            if not l_count or not r_count:
                return False
            if l_count != r_count:
                return False
            else:
                if x.color == Black:
                    return l_count + 1
                else:
                    return l_count
    return _black_count(root)

def node_check(Tree):
    root = Tree.root
    def _node_check(x):
        if x == None:
            return Black
        else:
            left_check = _node_check(x.left)
            if not left_check:
                print(str(x)+'.left is wrong!')
                return False
            right_check = _node_check(x.right)
            if not right_check:
                print(str(x)+'.right is wrong!')
                return False
            if x.color == Red:
                if left_check == Red or right_check == Red:
                    print(x, 'is wrong !')
                    return False
                return Red
            else:
                return x.color
    return _node_check(root)
            

def certificate(Tree , verbose = True):
    black_num = black_count(Tree)
    node_valid = node_check(Tree)
    if verbose:
        if not black_num:
            print('The number of black nodes varies!')
        else:
            print('The depth of black nodes is {}'.format(black_num))
        if node_valid:
            print('The nodes are valid.')
        else:
            print('The nodes are not valid!')
    return bool(black_num) and bool(node_valid)
    
def color(x):
    if x == None:
        return Black
    else:
        return x.color