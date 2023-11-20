from copy import deepcopy

deno_list = ['1','2','3']
deno_list2 = deepcopy(deno_list)

deno_list2.pop('1')

print(deno_list)
print(deno_list2)