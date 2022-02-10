'''
Author: XPectuer
LastEditor: XPectuer
'''
'''
URL: http://www.yinwang.org/blog-cn/2012/08/01/interpreter
Author: XPectuer
LastEditor: XPectuer
'''
import R2_error as r2e
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
    def __init__(self, val:chr='$'):        
        self.val = val 
        self.children = []

ast_nil = AST_Node()

# TODO: - [x] make it generic 
# TODO: - [ ] enable raising syntax error 
# TODO: - [ ] enable multiple digital calc
def parse(input: str)-> AST_Node:
    ptr = root = AST_Node()
    stack = Stack()

    for idx, c in enumerate(input):
        if c != ' ':
            if c == '(':
                cc = input[idx+1] 
                ptr.children.append(AST_Node(cc))
                stack.push(ptr)
                ptr = ptr.children[-1]


            elif c == ')':
                ptr = stack.pop()

            elif c in {'+','-','*','/'}:  
                ptr.val = c

            else:  
                ptr.children.append(AST_Node(val=c))        

    return root.children[0]
    


'''
                - +
                -- 1 2
                - +
                -- 3 4
           

'''

def pre_order_test(root: AST_Node, i: int): 
    for j in range(i):
        print('=>',end='')
    if root.val == -1: 
        print('(')
    else:
        print(root.val)
    if len(root.children) == 0:
        return
    for e in root.children:
        pre_order_test(e,i+1) 

    #print(')')    


'''
练习1:
这个练习是这样：写出一个函数，名叫tree-sum，它对二叉树进行“求和”，把所有节点里的数加在一起，返回它们的和。
举个例子，(tree-sum '((1 2) (3 4)))，执行后应该返回 10。
注意：这是一颗二叉树，所以不会含有长度超过 2 的子树，你不需要考虑像 ((1 2) (3 4 5)) 这类情况。
需要考虑的例子是像这样：(1 2)，(1 (2 3)), ((1 2) 3) ((1 2) (3 4))，……

TODO:
思考题：这个例子只能处理一位数计算，能否将其扩展到多位数？
'''


def calculate(root: AST_Node) -> chr:
    if root.val in {'+','-','*','/'}:
        opr = root.val
        op1 = int(calculate(root.children[0]))
        op2 = int(calculate(root.children[1]))
 
        if opr == '+': return op1 + op2 
        elif opr == '-': return op1 - op2 
        elif opr == '*': return op1 * op2 
        elif opr == '/': return op1 / op2
        else:
            raise r2e.R2SyntaxError()
    
    else:    
        return root.val 



if __name__ == '__main__':
    inputs = ["(+ (+ 1 2) (+ 3 4))",
                "(+ 1 (* 2 3))",
                "(+ (+ 1 2) 3)",
                "(+ 1 2)"]

    for input in inputs:
        print('=======[{}]========'.format(input))
        root = parse(input)
        #pre_order_test(root,0)
        print("result:", calculate(root))
