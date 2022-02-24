#lang racket


;; 空环境
(define env0 '())

;; 扩展环境：压栈
(define ext-env
    (lambda (x v env)
        (cons `(,x . ,v) env)))


;; 查找环境值
(define lookup
    (lambda (x env)
        ;; env中查找p
        ;; 找到：返回p关于x的v
        ;; 没找到：返回#f
        (let ([p (assq x env)])
            (cond 
                [(not p) #f]
                [else (cdr p)]))))

;; 闭包：实现 lexical scope
;; Q: 为何闭包可以实现 lexical scope呢？
;; A: 闭包的结构包括，f 函数定义、env 环境值
;;    定义被解释时，创建闭包，实际上就是记录了定义时的env环境
;;    这与lexical的定义契合 q.e.d
;;    推测出，struct创建传递了值而不是引用
(struct Closure(f env))

;; 解释
(define interp
    (lambda (exp env)
        (match exp                                  ;分支匹配：表达式的两种情况
            
            [(? symbol? x)                          ;是符号，解析环境的符号
                (let ([v (lookup x env)])
                    (cond
                        [(not v)
                         (error "undefined variable" x)]
                        [else v]))]


            [(? number? x) x]                       ; 是数字，直接返回
            
            [`(let ([,x ,e1]) ,e2)                  ; 变量绑定
              (let ([v1 (interp e1 env)]) 
                    (interp e2 (ext-env x v1 env)))] ;解右值


            [`(lambda (,x) ,e)                      ; 是函数，返回一个闭包，记录了函数定义时的环境
                (Closure exp env)]                                    

            [`(,e1 ,e2)                             ; 函数调用
                (let ([v1 (interp e1 env)]          ; 计算函数的值（即一个闭包）
                      [v2 (interp e2 env)])         ; 计算参数值
                ;; 求解函数定义
                (match v1
                    ;; 到达函数定义，解释执行函数
                    ;; 假如这里传入env 而不是 env-save
                    ;; 我们的R2就变成了 Dynamic Scoping
                    [(Closure `(lambda (,x) ,e) env-save)
                     (interp e (ext-env x v2 env-save))]        ;lexical环境内插入我们传递的实际参数
                ))
            ]                                      


            [`(,op ,e1 ,e2)                         ;是运算, 匹配提取操作符op和两个操作数e1,e2
                (let ([v1 (interp e1 env)]                   ; 递归调用 interp 自己，得到 e1 的值
                    [v2 (interp e2 env)])                  ; 递归调用 interp 自己，得到 e2 的值
                (match op                            ; 分支匹配：操作符 op 的 4 种情况
                   ['+ (+ v1 v2)]                     ; 如果是加号，输出结果为 (+ v1 v2)
                   ['- (- v1 v2)]                     ; 如果是减号，乘号，除号，相似的处理
                   ['* (* v1 v2)]
                   ['/ (/ v1 v2)]))])))



(define r2
    (lambda (exp)
        (interp exp env0)))


;; ------------------tests-------------------------
(r2 '(+ 1 2))
;; => 3

(r2 '(* 2 3))
;; => 6

(r2 '(* 2 (+ 3 4)))
;; => 14

(r2 '(* (+ 1 2) (+ 3 4)))
;; => 21

(r2 '((lambda (x) (* 2 x)) 3))
;; => 6

(r2
'(let ([x 2])
   (let ([f (lambda (y) (* x y))])
     (f 3))))
;; => 6

(r2
'(let ([x 2])
   (let ([f (lambda (y) (* x y))])
     (let ([x 4])
       (f 3)))))
;; => 6
