from random import randint

data = {
    'F3'    : [],
    'FC5'   : [],
    'AF3'   : [],
    'F7'    : [],
    'T7'    : [],
    'P7'    : [],
    'O1'    : [],
    'O2'    : [],
    'P8'    : [],
    'T8'    : [],
    'F8'    : [],
    'AF4'   : [],
    'FC6'   : [],
    'F4'    : []
}

# for key, val in sorted(data.iteritems()):
#     print key
#     if key is not 'F3' and key is not 'F7' :
#         for i in range(10) : val.append(randint(0,100))
#     # print val

# data[:] = [val.append(randint(0,100)) for key, val in data.iteritems()]

# data['F3'].append(randint(0,100))

print data
