import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_current_plane(plane_size=(1000, 1000), J = 1., print_allowed = False):
    """
    :plane_size: tuple, 电流平面的大小
    :J: float, 电流的大小
    :print_allowed: bool, 是否打印细节
    :return: int, 电流平面分布
    """
    plane = np.zeros(plane_size)
    #第几个边作为入口
    #规定1、2、3, 4分别代表左边界、上边界、右边界、下边界
    enter_param_1 = np.random.randint(low=0, high=4, size=1)[0]+1
    #这条边第几个点
    if enter_param_1 == 1 or enter_param_1 == 3:
        enter_param_2 = np.random.randint(low=0, high=plane_size[1], size=1)[0]
    else:
        enter_param_2 = np.random.randint(low=0, high=plane_size[0], size=1)[0]
    
    #确定起点位置
    if enter_param_1 == 1:
        current_pos = [0, enter_param_2]
    elif enter_param_1 == 2:
        current_pos = [enter_param_2, plane_size[1]-1]
    elif enter_param_1 == 3:
        current_pos = [plane_size[0]-1, enter_param_2]
    else:
        current_pos = [enter_param_2, 0]
    
    #规定1、2、3、4分别代表左边界、上边界、右边界、下边界
    #规定1、2、3、4分别代表右、下、左、上， 5、6、7、8代表右下、左下、左上、右上   
    #调用递归函数
    plane = current_move(plane, current_pos, next_move = enter_param_1, platform_size = plane_size,print_allowed = print_allowed)
    
    current_tensor = np.zeros(plane_size+(2,))
    print(current_tensor.shape)
    
    sqrt2 = np.sqrt(2)
    cur2tensor = {
        0 : [ 0     ,      0 ],
        1 : [ 1     ,      0 ],
        2 : [ 0     ,     -1 ],
        3 : [-1     ,      0 ],
        4 : [ 0     ,      1 ],
        5 : [ sqrt2 , -sqrt2 ],
        6 : [-sqrt2 , -sqrt2 ],
        7 : [-sqrt2 ,  sqrt2 ],
        8 : [ sqrt2 ,  sqrt2 ]
    }
    
    for i in range(plane_size[0]):
        for j in range(plane_size[1]):
            current_tensor[i, j] = J*cur2tensor[plane[i, j]]
            
    return current_tensor, plane

def current_move(platform, current_pos, next_move, platform_size,print_allowed = False):
    #决定步数
    step = np.random.randint(low=0, high=min(platform_size), size=1)[0] + 1
    
    move = {
        1 : "右",
        2 : "下",
        3 : "左",
        4 : "上",
        5 : "右下",
        6 : "左下",
        7 : "左上",
        8 : "右上"
    }
    
    if print_allowed:
        print(f"当前的位置为{current_pos}")
        print(f"当前的方向为{move[next_move]}")
        print(f"当前的步数为{step}")
    
    #如果没有走出去，则决定下一个方向
    #使用字典规定合法移动
    allowed_motion = {
        1 : [2, 4, 5, 8],
        2 : [1 ,3, 5, 6],
        3 : [2, 4, 6, 7],
        4 : [1, 3, 7, 8],
        5 : [1, 2],
        6 : [2, 3],
        7 : [3, 4],
        8 : [4, 1]
    }
    next_state_move = random.choice(allowed_motion[next_move])
        
    #当前移动是右
    if next_move == 1:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0]+1, current_pos[1]
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
    #当前移动是下
    elif next_move == 2:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0], current_pos[1]-1
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
    #当前移动是左
    elif next_move == 3:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0]-1, current_pos[1]
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
                
     #当前移动是上
    elif next_move == 4:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0], current_pos[1]+1
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
            
    #当前移动是右下         
    elif next_move == 5:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0]+1, current_pos[1]-1
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
                
    #当前移动是左下  
    elif next_move == 6:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0]-1, current_pos[1]-1
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
                
    #当前行动是左上
    elif next_move == 7:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0]-1, current_pos[1]+1
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
                
    #当前行动是右上          
    elif next_move == 8:
        for ii in range(step):
            if current_pos[0] < 0 or current_pos[1] < 0:
                return platform
            try:
                if platform[current_pos[0], current_pos[1]] != 0:
                    return platform
                platform[current_pos[0], current_pos[1]] = next_move
                current_pos[0], current_pos[1] = current_pos[0]+1, current_pos[1]+1
                if print_allowed:
                    print(f"第{ii+1}步为{current_pos}")
            except IndexError:
                return platform
            
                
    #递归
    return current_move(platform, current_pos, next_state_move, platform_size)

def generate_current_field(current_field_size=(10, 10, 10), *args, **kwargs):
    """
    current_field_size: tuple, 电流张量的大小。
    接下来可以输入多个参数，代表有多少个电流平面。可以输入(1,5)，代表J大小为1，所处平面的z=5,也可以输入5，默认J=1，z=5。
    返回的是电流分布张量
    """
    J_field = np.zeros(current_field_size + (3,))
    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2:      
            J_field[:,:,arg[1],:2],_ = generate_current_plane((current_field_size[0],current_field_size[1]), arg[0])
        elif isinstance(arg, int):
            J_field[:,:,arg,:2],_ = generate_current_plane((current_field_size[0],current_field_size[1]))
        else:
            print("J平面要求的格式错误")
    return J_field
        


def calculate_magnetic_field(J, dx=1, dy=1, dz=1):
    mu0 = 4 * np.pi * 1e-7  # 真空中的磁导率

    # 获取电流密度张量的大小
    nx, ny, nz, _ = J.shape

    # 初始化磁场分布张量H，初始值为零
    B = np.zeros((nx, ny, nz, 3))

    # 创建网格的坐标矩阵
    x, y, z = np.arange(nx), np.arange(ny), np.arange(nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # 对电流密度张量的每个元素计算其对每个点的磁场贡献
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                # 从所有网格点到电流元素 (i, j, k) 的矢量差矩阵
                r_vec_x = (X - i) * dx
                r_vec_y = (Y - j) * dy
                r_vec_z = (Z - k) * dz

                # 计算距离矢量的大小，应对距离为0的情形防止除0
                r_mag = np.sqrt(r_vec_x**2 + r_vec_y**2 + r_vec_z**2)
                r_mag[i, j, k] = np.inf  # 自身点距离设为无穷大，忽略自身对磁场的贡献

                # 电流密度在点(i, j, k)的分量
                dJ = J[i, j, k, :][np.newaxis, np.newaxis, np.newaxis, :]

                # 利用比奥-萨伐尔定律计算磁场，利用广播规则来避免循环计算
                cross_prod = np.cross(dJ, np.stack((r_vec_x, r_vec_y, r_vec_z), axis=-1))
                dB = cross_prod * mu0 / (4 * np.pi * r_mag[..., np.newaxis]**3)

                B += dB

    return B



def plot_vectors_plane(J = None, J_z=5, B = None, B_z=5):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    try:
        for i in range(J.shape[0]):
            for j in range(J.shape[1]):
                ax.quiver(i, j, J_z, J[i, j, J_z, 0], J[i, j, J_z, 1], J[i, j, J_z, 2], color="red")
    except AttributeError :
        pass

    try:
        for i in range(B.shape[0]):
            for j in range(B.shape[1]):
                ax.quiver(i, j, B_z, B[i, j, B_z, 0], B[i, j, B_z, 1], B[i, j, B_z, 2], length=10000000, color="blue")
    except AttributeError :
        pass

    plt.show()
    
import matplotlib.pyplot as plt

def plot_vectors_tensor(J = None, B = None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    try:
        for i in range(J.shape[0]):
            for j in range(J.shape[1]):
                for k in range(J.shape[2]):
                    ax.quiver(i,j ,k , J[i,j,k,0], J[i,j,k,1], J[i,j,k,2], color = "red")
    except AttributeError:
        pass

    try:
        for i in range(B.shape[0]):
            for j in range(B.shape[1]):
                for k in range(B.shape[2]):
                    ax.quiver(i, j,k, B[i,j,k,0], B[i,j,k,1] ,B[i,j,k,2], length=10000000 , color = "blue")
    except AttributeError:
        pass

    plt.show()