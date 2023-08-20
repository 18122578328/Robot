import matplotlib.pyplot as plt

def show(final_Xk_zz,IP_LIST):
    i=0
    x = []      #x坐标数组，n个
    y = []      #y坐标数组，n个
    z = []      #角度数组，n个
    while i< len(IP_LIST):   #i<finzl_Xk_zz的行数
        x.append(final_Xk_zz[3*i,0])
        y.append(final_Xk_zz[3*i+1,0])
        z.append(final_Xk_zz[3*i+2,0])
        i+=1
    plt.scatter(x,y,marker='.')
    plt.xlim([-10,10])
    plt.ylim([-10,10])
    for i in range(len(x)):
        plt.annotate(round(z[i],2),xy=(x[i],y[i]),xytext=(x[i],y[i]))
    plt.show()