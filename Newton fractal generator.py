import sympy as sym
from PIL import Image

z = sym.Symbol('z')
iterations = 0
epsilon = 5
colors = ["red", "blue", "green"]
dim = 101
func = z ** 3 - 2 * z + 2


def roots(func):
    list = []
    for i in sym.solveset(func):
        list.append(sym.N(i, epsilon))
    return list


def newtonsMethod(z_0, func, roots):
    global iterations
    z_1 = z_0
    if z_1 in roots:
        it = iterations
        iterations = 0
        return z_1, it
    z_1 = sym.N(z_0 - (func.subs(z, z_0) / sym.diff(func).subs(z, z_0)), epsilon, chop=1e-8)
    iterations += 1
    if iterations == 30:
        iterations = 0
        return 'n', z_1
    return newtonsMethod(z_1, func, roots)


def map(x, y):
    nx = x / (dim - 1)
    ny = y / (dim - 1)
    px = -1 + -((dim - 1) / 2) + nx * 2 * ((dim - 1) / 2)
    py = (dim - 1) / 2 + ny * -2 * ((dim - 1) / 2)
    return int(px), int(py)


def drawFractal(func):
    img = Image.new('RGB', (dim, dim), "black")  # create a new black image
    pixels = img.load()  # create the pixel map2
    print(roots(func))
    start = int(-((dim - 1) / 2))
    end = int(((dim - 1) / 2) + 1)
    count = 0

    for i in range(start, end):  # for every col:
        for j in range(start, end):  # For every row
            real = map(i, j)[0]
            imag = map(i, j)[1]
            root = newtonsMethod(complex(i / 100, j / 100), func, roots(func))
            count += 1
            print(round(count / (dim * dim) * 100), "%")
            if root[0] == roots(func)[0]:
                # print("(",i,",",j,") blue:",root[0])
                pixels[real, imag] = (0, 0, 255)
            elif root[0] == roots(func)[1]:
                # print("(" , i , "," , j , ") red:" , root[0])
                pixels[real, imag] = (255, 0, 0)
            elif root[0] == roots(func)[2]:
                # print("(" , i , "," , j , ") green:" , root[0])
                pixels[real, imag] = (0, 255, 0)
            elif root[0] == 'n':
                # print("(" ,i, "," ,j, ") no root:", root[1])
                continue

    img.show()


# print(newtonsMethod(complex(0,1),(z**3-2*z+2),roots(z**3-2*z+2)))

drawFractal(func)
