def check_fd(inp, attr):
    if '->' not in inp:
        return None
    
    elements = inp.upper().replace(' ', '')
    elements = elements.split('->')

    x = elements[0].split(',')
    y = elements[1].split(',')
    for e in x:
        if e not in attr:
            print(f'invalid FD: attribute {e} not in relational table')
            return None
    for e in y:
        if e not in attr:
            print(f'invalid FD: attribute {e} not in relational table')
            return None
    
    return (set(x), set(y))

def compute_closure(x, y, func_depts):
    closure = set(x)
    closure.update(y)
    changed = True
    while changed:
        changed = False
        for dep in func_depts:
            if dep[0].issubset(closure) and not dep[1].issubset(closure):
                closure.update(dep[1])
                changed = True
    return closure

def is_superkey(closure, attributes):
    if attributes.issubset(closure):
        return True
    return False

def check_nontrivial(fd):
    if fd[1].issubset(fd[0]):
        return False
    return True

def infer_fds(fds, attr):
    new_fds = []

    for fd in fds:
        if fd[0].issubset(attr) and fd[1].issubset(attr) and check_nontrivial(fd):
            new_fds.append(fd)
        elif fd[0].issubset(attr):
            diff = fd[1].intersection(attr)
            if diff!=set() and check_nontrivial((fd[0], diff)):
               new_fds.append((fd[0], diff))
        elif fd[1].issubset(attr):
            for f in fds:
                if fd[0].issubset(f[1]) and f[0].issubset(attr) and check_nontrivial((f[0], fd[1])):
                    new_fds.append((f[0], fd[1]))
                    break
        else:
            diff_r = fd[1].intersection(attr)
            if diff_r!=set():
                for f in fds:
                    if fd[0].issubset(f[1]) and f[0].issubset(attr) and check_nontrivial((f[0], diff_r)):
                        new_fds.append((f[0], diff_r))
                        break
    return new_fds

def get_bcnf_string(bcnf):
    result = []
    for item in bcnf:
        result.append(str(item))

    return ', '.join(result)

def bcnf(attributes, functional_dependencies):
    curr_relations = []
    curr_relations.append((attributes, functional_dependencies))
    bcnf_relations = []

    while curr_relations:
        relation = curr_relations.pop(0)
        attr = relation[0]
        fds = relation[1]
        isBCNF = True
        # print(f'relation: {attr}, fds: {fds}')

        for fd in fds:
            # Get closure
            closure = compute_closure(fd[0], fd[1], fds)

            # Check if the closure is not a superkey
            if not is_superkey(closure, attr):
                isBCNF=False

                new_relation = fd[0].union(fd[1])
                new_fds = infer_fds(fds, new_relation)
                curr_relations.append((new_relation, new_fds))

                other_relation = attr.difference(new_relation)
                other_relation.update(fd[0])
                other_fds = infer_fds(fds, other_relation)
                curr_relations.append((other_relation, other_fds))
                x = ','.join(fd[0])
                y = ','.join(fd[1])
                print(f'Decompose: {attr} by {x} -> {y} into {new_relation} and {other_relation}')
                break

        if isBCNF: 
            bcnf_relations.append(attr)

    return bcnf_relations


print('Welcome the the BCNF decomposer! Please enter the information in the following format:\n')
print('1. list of attributes in the relation of interest, ie {A, B, C, D, E}')
print('2. list of functional dependencies, one per line.')
print('     - The left- and right-hand sides of the dependency (separated by ->) must specify valid attributes')
print('declared by the first line, separated by commas, ie A -> C')
print('Enter "done" when finished.\n')

inp = input("Relation Attributes: ")
attr = inp.replace(' ', '').replace('{', '').replace('}', '').upper().split(',')
attributes = set(attr)
functional_dependencies = []
done = False

while not done:
    inp = input('Functional Dependency: ')
    if inp == 'done':
        done = True
    else:
        result = check_fd(inp, attr)
        if result is not None:
            functional_dependencies.append(result)
        else:
            print()

bcnf_result = bcnf(attributes, functional_dependencies)
string = get_bcnf_string(bcnf_result)
print("BCNF: ", string)