def valid_fd(inn, relation):
    if '->' not in inn:
        return None
    
    fd = inn.replace(' ', '').split('->')

    left = fd[0].split(',')
    right = fd[1].split(',')
    for l in left:
        if l not in relation:
            print('error, make sure FD is in the relation')
            return None
    for r in right:
        if r not in relation:
            print('error, make sure FD is in the relation')
            return None
    
    return (set(left), set(right))

def get_closure(left, right, fn_dp):
    closure = set(left)
    closure.update(right)
    keep_going = True

    while keep_going:
        keep_going = False
        for d in fn_dp:
            if d[0].issubset(closure):
                if not d[1].issubset(closure):
                    closure.update(d[1])
                    keep_going = True
    return closure

def infer_fds(fn_dp, rel):
    rel_fd = []

    for d in fn_dp:
        if d[0].issubset(rel) and d[1].issubset(rel):
            if not d[0].issubset(d[1]):
                rel_fd.append(d)
        else:
            diff_r = d[1].intersection(rel)
            if diff_r!=set():
                for f in fn_dp:
                    if d[0].issubset(f[1]) and f[0].issubset(rel):
                        if not f[0].issubset(diff_r):
                            rel_fd.append((f[0], diff_r))
                            break
    return rel_fd

def bcnf(rels, fncl_deps):
    curr = [(rels, fncl_deps)]
    bcnfs = []

    while curr:
        rel = curr.pop(0)
        attributes = rel[0]
        f_d = rel[1]
        check_bcnf = True

        for f in f_d:
            closure = get_closure(f[0], f[1], f_d)

            if not attributes.issubset(closure):
                check_bcnf = False

                relation = f[0].union(f[1])
                new_fds = infer_fds(f_d, relation)
                curr.append((relation, new_fds))

                relation2 = attributes.difference(relation)
                relation2.update(f[0])
                other_fds = infer_fds(f_d, relation2)
                curr.append((relation2, other_fds))
                left = ','.join(f[0])
                right = ','.join(f[1])
                print(f'Decompose: {attributes} by {left} -> {right} into {relation} and {relation2}')
                break

        if check_bcnf: 
            bcnfs.append(attributes)

    return bcnfs

inn = input("Enter your relation (ie {A, B, C}): ")
relation = set(inn[1:len(inn)-1].replace(' ', '').split(','))
func_deps = []

while True:
    inn = input('Enter your FD (ie A -> B, C) or "complete" if no more: ')
    if inn == 'complete':
        break
    else:
        valid = valid_fd(inn, list(relation))
        if valid is not None:
            func_deps.append(valid)
        else:
            print()

decomp = bcnf(relation, func_deps)

list = []
for rel in decomp:
    list.append(str(rel))
result=', '.join(list)

print("Decomposed Relations: ", result)