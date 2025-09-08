# 创建了一个类
class Car:
    # 属性
    def __init__(self, Brand, Color):
        self.Brand = Brand  # 实例属性
        self.Color = Color

    # 类方法
    def CarBrand(self):
        print(f'Your car brand is {self.Brand}')

    def CarCorlor(self):
        print(f'Your car color is {self.Color}')

# 创建了对象/实例化
mycar = Car('lbjn', 'red')
yourcar = Car('bc', 'yellow')

# 调用方法
mycar.CarBrand()
yourcar.CarCorlor()

# 访问属性
print(yourcar.Color)