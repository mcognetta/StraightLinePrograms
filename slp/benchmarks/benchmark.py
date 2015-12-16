'''
benchmark testing
'''

import time
import slp.core.nodes as nodes

def n_choose_k(n,k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def naive_expansion(x=3,y=5,n=2**5):
    sum = 0
    for i in range(n+1):
        sum += n_choose_k(n,i)*x**(n-i)*y**i
    return sum

def naive_multiplication(x=3,y=5,n=2**13):
    result = 1
    for i in range(n):
        result *= (x+y)
    return result

def slp_expansion(x=3,y=5,n=8):
    v_x = nodes.variable_node()
    v_y = nodes.variable_node()

    g_0 = nodes.sum_node(v_x,v_y)
    g_1 = nodes.product_node(g_0,g_0) #(x+y)^2
    g_2 = nodes.product_node(g_1,g_1) # ^4
    g_3 = nodes.product_node(g_2,g_2) # ^8
    g_4 = nodes.product_node(g_3,g_3) # ^16
    g_5 = nodes.product_node(g_4,g_4) # ^32
    g_6 = nodes.product_node(g_5,g_5) # 64
    g_7 = nodes.product_node(g_6,g_6) # 128
    g_8 = nodes.product_node(g_7,g_7) # 256
    g_9 = nodes.product_node(g_8,g_8) # 512
    g_10 = nodes.product_node(g_9,g_9) # 1024
    g_11 = nodes.product_node(g_10,g_10) # 2048
    g_12 = nodes.product_node(g_11,g_11) # 4096
    g_13 = nodes.product_node(g_12,g_12) # 8192
    g_14 = nodes.product_node(g_13,g_13) # 16384

    eval_list = {}
    eval_list[v_x] = x
    eval_list[v_y] = y
    output = nodes.output_node([g_13])
    return output.evaluate(eval_list)

s = time.time()
#naive_expansion()
slp_expansion()
#naive_multiplication()
e = time.time()

print(e-s)