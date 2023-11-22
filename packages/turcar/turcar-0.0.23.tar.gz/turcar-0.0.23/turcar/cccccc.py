import itertools


def print_combinations(people):
    result = []  # 用于存储所有可能的过河方案
    left_bank = set(people)  # 左岸的初始情况
    right_bank = set()  # 右岸的初始情况
    boat = set()  # 船上的初始情况

    def is_valid(path):
        if ('妈妈' in path and ('爸爸' in path or '路人' in path or '哥哥' in path)) or (
                '爸爸' in path and ('妹妹' in path or '妈妈' in path)) or (
                '哥哥' in path and ('妹妹' in path or '妈妈' in path or '路人' in path)) or (
                '妹妹' in path and ('爸爸' in path or '哥哥' in path)) or (
                '路人' in path and ('妈妈' in path or '哥哥' in path)):
            return False
        return True

    # 定义一个名为cross的内部函数，用于模拟每次过河的情况
    def cross(river, path=[], right_river=set()):
        # 如果左岸和船上都没有人，则表示所有人都已经成功过河，将当前路径加入结果中
        if not river and not boat:
            result.append(path)
            return
        # 返回左岸,从船上下来一个人
        if boat:
            print("回来： ", boat)
            left_bank.update(boat)  # 船上的人到达左岸
            right_bank.difference_update(boat)  # 船上的人从右岸移除
            path = path + [boat]
            river.update(boat)
            print("左边： ", river)
        # 遍历所有可能的过桥方式，即从左岸选取两个人或者一个人，或者从船上下来一个人
        for pair in itertools.combinations(river, 2):
            a, b = pair
            if is_valid([a, b]):
                # print([a, b])
                print("is_valid左边:", river)
                new_river = river - {a, b}  # 更新左岸的情况
                right_river.update({a, b})  # 更新右岸的情况
                print(new_river)
                print("is_valid左边new_river:", new_river)
                new_path = path + [(a, b)]  # 更新过河组合
                print("过河组合: ", new_path)

                # 遍历所有可能的装载方式，即带着两个人过河、带着一个人过河、或者空船过河
                for load in (a,), (b,):

                    # print(load)
                    # 检查当前装载方式是否合法，即所有要过河的人都在左岸，且左岸剩余的人数不会因为此次过河而造成左岸人数少于右岸
                    # if all(x in river for x in load) and len(left_bank) - len(load) >= len(right_bank) - len(load):
                    # left_bank.difference_update(load)  # 船上的人从左岸移除
                    # right_bank.update(load)  # 船上的人到达右岸
                    if len(load) == 1 and load[0] != "妹妹":
                        boat.clear()
                        boat.update(load)
                        cross(new_river, new_path, right_river)
                        left_bank.update(load)
                        right_bank.difference_update(load)

    cross(left_bank)
    print("结束")
    print(result)
    for i, step in enumerate(result):
        print(f"Step {i + 1}: {step}")


people = ['妈妈', '爸爸', '哥哥', '妹妹', '路人']
print_combinations(people)
