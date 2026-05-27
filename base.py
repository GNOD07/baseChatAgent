# python的基本语法
# 与js对比学习，方便理解

## 1. 变量、数据类型与f-string
print("1. 变量、数据类型与f-string")
# JS: let name = 'Alice';
name = 'Alice'  # Python中变量不需要声明类型，直接赋值即可
age = 30  # Python中的数据类型包括字符串、整数、浮点数等
is_student = True  # 布尔类型

# Python中的f-string用于格式化字符串，类似于JS中的模板字符串 `My name is ${name}, I am ${age} years old.`
print(f'My name is {name}, I am {age} years old.')

## 2. 循环与判断
print("\n2. 循环与判断")
# 记住一点：Python 用冒号 : 和缩进来表示代码块。
# JS：for(let i = 0; i < 5; i++) { console.log(i); }
# python 中的 range(5) 相当于生成一个[0, 1, 2, 3, 4]的序列
for i in range(3):  # Python中的for循环使用range函数生成序列
    print(i)

count = 0
total = 0
while count < 5:
    total += count
    count += 1
    # if count == 4:
    #     print("跳出循环，count=4了")
    #     break  # break语句用于跳出循环，类似于JS中的break
    #     print("这行代码永远不会执行，因为break已经跳出循环了")
    if count == 2:
        print("跳过count=2的情况")
        continue  # continue语句用于跳过当前循环的剩余部分，直接进入下一次循环，类似于JS中的continue
        print("这行代码永远不会执行，因为continue已经跳过了当前循环的剩余部分了")
    print("当前count =", count, "total =", total)  # 在循环中打印当前的count和total值
else:
    print("循环结束，total =", total)  # while循环也可以有else块，在循环正常结束时执行,如果循环是通过break跳出的，则不会执行else块

# JS: if (age > 18) { console.log('Adult'); } else { console.log('Minor'); }
if age > 18:  # Python中的if语句使用冒号和缩进来定义代码块
    print('Adult')
else:
    print('Minor')

## 3. 函数与字典
print("\n3. 函数与字典Dict")
# python里和JSON对象叫字典，使用花括号 {} 定义，键值对之间用冒号 : 分隔
# 函数定义用def关键字，类似于JS中的function
# JS: function get_agent_info(name, version = 1.0) { return { name: name, version: version }; }
def get_agent_info(name, version=1.0):
    return {"name": name, "version": version}  # 返回一个字典

agent = get_agent_info("DeepSeek Agent", 2.0)

print(agent["version"])  # 访问字典中的值，类似于JS中的对象属性访问 agent.version

## 4. 类
print("\n4. 类")
# Python中的类定义使用class关键字，类似于JS中的class
# Python 官方（PEP 8）推荐的命名规范是 大驼峰命名法（PascalCase / CapWords）。也就是说，类名的每个单词首字母都要大写，并且单词之间不使用下划线分隔。
# python中的class与JS的class核心差异：
## 所有实例方法（包括构造函数）的第一个参数必须是 self（相当于 JS 里的 this，但必须显式写出来）。
## 构造函数叫 __init__（前后各两个下划线），创建对象时自动调用。

# JS: class Agent { constructor(name) { this.name = name; } getName() { return this.name; } }
# 4.1 构造函数 __init__ 和实例方法
print("4.1 构造函数 __init__ 和实例方法")
class MyAgent:
    # 类属性，所有实例共享
    default_model = "DeepSeek"
    
    # 构造函数，创建实例时自动调用
    def __init__(self, name, api_key):
        # self参数是Python中类方法的约定，表示实例本身，类似于JS中的this
        self.name = name  # 实例属性，每个实例独有
        self._api_key = api_key # 私有属性，约定俗成以单下划线开头，不能在类外直接访问修改
        self.memory = []  # 用于存储对话历史的实例属性
    
    # 实例方法，必须包含self参数
    def chat(self, message):
        self.memory.append(message) # 将消息存储到实例的memory属性中
        print(f"{self.name} 正在思考...{message}")
        return f"{self.name} 回复: {message[::-1]}"  # 简单地返回消息的反转作为回复

# 使用class
agent = MyAgent("qwen-max", "secret_api_key")
print(agent.default_model)
agent._api_key = "new_api_key"  #
print(agent._api_key)  # 虽然是私有属性，但在Python中仍然可以访问（不推荐）
print(agent.chat("Hello, Agent!"))

# 4.2 封装与属性装饰器@property
print("\n4.2 封装与属性装饰器@property")
# 在前端，如果你想拦截对某个属性的赋值或读取，可能会用 Object.defineProperty 或 Vue 的 computed。Python 里用的是 @property。这在处理 API Key、敏感数据校验时极其有用。

class SecureAgent:
    def __init__(self, api_key):
        self._api_key = api_key  # 内部真实存储的变量
    
    @property
    def api_key(self):
        # 当外部执行 agent.api_key 时，实际上调用的是这个方法
        return self._api_key[:4]+ "****"  # 通过@property装饰器定义的属性访问器，允许我们在访问时添加逻辑, 对外隐藏真实的key值
    @api_key.setter
    def api_key(self, new_key):
        # 当外部执行 agent.api_key = "new_key" 时，实际上调用的是这个方法
        if len(new_key) < 8:
            raise ValueError("API Key must be at least 8 characters long.")
        self._api_key = new_key

secure_agent = SecureAgent("my_secret_api_key")
print(secure_agent.api_key)  # 输出: my_s****，隐藏了真实的API Key
secure_agent.api_key = "new_secure_key"  # 更新API Key，触发setter方法
print(secure_agent.api_key)  # 输出: new_****，再次隐藏了真实的API Key
# secure_agent.api_key = "short"  # 这行会抛出 ValueError，因为新API Key长度不足8个字符

# 4.3 继承与super()
print("\n4.3 继承与super()")
# 当你需要定制一个特定功能的 Agent 时，不需要重写整个类，直接继承即可。super() 用来调用父类的方法（类似 JS 的 super()）。

#父类
class BaseAgent:
    def __init__(self, name):
        self.name = name
    def chat(self, message):
        return f"父类 {self.name} 回复: {message}"

#子类继承父类
class CodingAgent(BaseAgent):
    def __init__(self, name, language):
        super().__init__(name) # 调用父类的构造函数，初始化name属性
        self.language = language  # 子类特有的属性
    # 方法重写
    def chat(self, message):
        base_chat = super().chat(message)  # 调用父类的chat方法，获取基础回复
        return f"子类 {base_chat} (使用{self.language}编写代码)"  # 在父类回复的基础上添加子类特有的信息

coding_agent = CodingAgent("CodeMaster", "Python")
print(coding_agent.chat("Write a function to add two numbers."))

# 4.4 多态
print("\n4.4 多态")
# 多态是面向对象编程的核心特性之一。即同一个方法（或接口），在不同的对象身上，会表现出完全不同的行为。
# 4.4.1 继承+方法重写实现多态（最经典的多态）
print("4.4.1 继承+方法重写实现多态（最经典的多态）")

# 父类，定义一个统一的“执行任务”接口
class FatherAgent:
    def execute(self):
        print("父类执行任务")

class CoderAgent(FatherAgent):
    def execute(self):
        print("CoderAgent 正在编写代码...")

class DrawAgent(FatherAgent):
    def execute(self):
        print("DrawAgent 正在绘制图像...")

# 创建不同类型的Agent实例
coder = CoderAgent()
drawer = DrawAgent()

def run_agent(agent):
    agent.execute()  # 无论传入的是哪个子类实例，都能正确调用对应的execute方法

run_agent(coder)  # 输出: CoderAgent 正在编写代码...
run_agent(drawer) # 输出: DrawAgent 正在绘制图像...

# 4.4.2 duck typing实现多态（Python独有的多态）
print("\n4.4.2 duck typing实现多态（Python独有的多态）")
# Python 是一门动态语言，它比 Java 等静态语言更灵活。Python 奉行“鸭子类型”（Duck Typing）原则：“如果它走起来像鸭子，叫起来也像鸭子，那它就是一只鸭子。”
# 这意味着，在 Python 里实现多态，甚至不需要继承同一个父类。只要不同的类里都有同名的方法（比如都有 execute），你就可以把它们当成同一种东西来调用。

class Dog:
    def speak(self):
        print("Woof!")
class Cat:
    def speak(self):
        print("Meow!")

def animal_speak(animal):
    animal.speak()  # 只要传入的对象有speak方法，就能调用，无需关心它是什么类型

dog = Dog()
cat = Cat()
animal_speak(dog)  # 输出: Woof!
animal_speak(cat)  # 输出: Meow!