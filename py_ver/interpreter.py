'''
URL: http://www.yinwang.org/blog-cn/2012/08/01/interpreter
Author: XPectuer
LastEditor: XPectuer
'''

from ast import AST
from re import X

class Stack():
    
    def __init__(self, array=[] , length=0, cap=0):        
        self._array = array
    
    def push(self, val):
        self._array.append(val)

    def pop(self):
        val = self._array[-1]
        self._array = self._array[:-1] 
        return val

    def top(self):
        return self._array[-1]
    
    def empty(self):
        return len(self._array)==0

    def length(self):
        return len(self._array)
    


class AST_Node():
    # -1 == +
    def __init__(self, val=-1):        
        self.val = val 
        self.children = []

ast_nil = AST_Node()

def make_AST(input: str)-> AST_Node:
    ptr = root = AST_Node()
    stack = Stack()

    for c in input:
        if c != ' ':
            if c == '(':
                # push stk
                ptr.children.append(AST_Node())
                stack.push(ptr)
                ptr = ptr.children[-1]
            elif c == ')':
                ptr = stack.pop()
            else:  
                ptr.children.append(AST_Node(val=int(c)))        
    return root.children[0]
    


'''
                - +
                -- 1 2
                - +
                -- 3 4
           

'''

def pre_order_test(root: AST_Node, i: int): 
    for j in range(i):
        print('-',end='')
    if root.val == -1: 
        print('(')
    else:
        print(root.val)
    if len(root.children) == 0:
        return
    for e in root.children:
        pre_order_test(e,i+1) 

    print(')')    


'''
练习1:
这个练习是这样：写出一个函数，名叫tree-sum，它对二叉树进行“求和”，把所有节点里的数加在一起，返回它们的和。
举个例子，(tree-sum '((1 2) (3 4)))，执行后应该返回 10。
注意：这是一颗二叉树，所以不会含有长度超过 2 的子树，你不需要考虑像 ((1 2) (3 4 5)) 这类情况。
需要考虑的例子是像这样：(1 2)，(1 (2 3)), ((1 2) 3) ((1 2) (3 4))，……
'''


def tree_sum(root: AST_Node) -> int:

    if root.val == -1:
        op1 = tree_sum(root.children[0])
        op2 = tree_sum(root.children[1])
        return op1 + op2 
    else:    
        return root.val 



if __name__ == '__main__':
    inputs = ["((1 2) (3 4))",
                "(1 (2 3))",
                "((1 2) 3)",
                "(1 2)"]

    for input in inputs:
        root = make_AST(input)
        # pre_order_test(root,0)
        print(input,":",tree_sum(root))
