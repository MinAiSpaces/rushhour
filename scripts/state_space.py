def func2(n):
    x = 0

    for i in range(n + 1):
        x += func1(i)

    return x


def func1(n):
    x = 0

    for i in range(n + 1):
        x += 1 + i

    return x


def main():
    n = 8

    for i in range(n + 1):
        print('vrije plekken:', i)
        print('met 2 autos:', func1(i))
        print('met 3 autos:', func2(i))
        print()


if __name__ == '__main__':
    main()
