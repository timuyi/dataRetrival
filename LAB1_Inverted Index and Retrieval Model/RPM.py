"""
后缀表达式
ReversePolishNotation 将运算符写在操作数之后
解决带括号的表达式问题

此函数返回 操作项与操作的列表
"""

def RPM(expression,operator):  
    result = []             # 结果
    stack = []              # 模拟栈
    for item in expression: 
        if item not in operator:      # 如果当前item不是操作符则直接加入
            result.append(item)
            while len(stack) and stack[len(stack)-1] == "not":#最后一个是not要弹出
                stack.pop()
                result.append("not")
                
        else:                     # 如果当前字符为一切其他操作符
            if len(stack) == 0:   # 如果栈空，直接入栈
                stack.append(item)
            elif item == ')':     #右括号弹出 直到遇到左括号或栈空
                pop_item = stack.pop()
                while len(stack) and pop_item != '(':
                    result.append(pop_item)
                    pop_item = stack.pop()
                #栈不空再弹一个
                if len(stack):
                    pop_item = stack.pop()
                    result.append(pop_item)
            else:#除(之外均要弹出一个运算符号 且不能弹出（   not也不可弹出
                if stack[len(stack)-1]!="(" and item!="(" and item!="not":
                    pop_item = stack.pop()
                    result.append(pop_item)
                stack.append(item)

    # 表达式遍历完了，但是栈中还有操作符不满足弹出条件，把栈中的东西全部弹出
    while stack:
        result.append(stack.pop())
    return result
    # 返回字符串
    #return "".join(result)

if __name__ == "__main__":
    expression = ["a","and","b","and","not","(","c","or","d",")"]
    expression = ["ari","and","(","rand","or","rand",")"]
    #expression = ["a","and","not","(","not","ari",")"]
    #expression = ["not","not","ari",")"]
    operator = ["and","or","not","(",")"]
    print(RPM(expression,operator))
