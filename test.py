def nuke(n):
    a = []
    for i in range(10):
        if (n > 1):
            a.append(nuke(n-1))
        else:
            a.append(i)
    return a


x = {}

x['y'] = 'z'

y = x['1']

print(y)