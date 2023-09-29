BCNF Decomposer Program
Cynthia France, CS 316 Fall 2023


RUNNING THE PROGRAM
- Compile the python script and run (download bcnf.py and click the run button)
- Follow the prompts given in the command line


INPUT REQUIREMENTS
Relation Attributes: 
- attributes should be comma separated
- surround the attributes in curly braces ({})
- example: {A, B, C, D, E}

Functional Dependency:
- one FD per line
- the left and right sides of the dependency should be separated by an arrow (->)
- each side of the dependency should be comma separated
- elements on each side of the dependency should appear in the relational attribute defined earlier
- when finished with the FDs, enter "done"
- example: A -> C


AFTER INPUTS
- after "done" is input, the program decomposes to bcnf, printing each decomposition step
    - Decompose: {'D', 'C', 'A', 'F', 'E', 'B'} by A -> D,C into {'D', 'C', 'A'} and {'A', 'F', 'E', 'B'}
- at the end, the program gives the decompositions in the following form: 
    - BCNF: {'D', 'C', 'A'}, {'E', 'B'}, {'A', 'F', 'B'}


EXAMPLE RUN
The following is an exmaple of what you should see when running the program. Please note, the user inputs are
what follows after the prompts "Relational Attributes:" and "Functional Dependency:"

--- bcnf decomposition start ---

Welcome the the BCNF decomposer! Please enter the information in the following format:

1. list of attributes in the relation of interest, ie {A, B, C, D, E}
2. list of functional dependencies, one per line.
     - The left- and right-hand sides of the dependency (separated by ->) must specify valid attributes
declared by the first line, separated by commas, ie A -> C
Enter "done" when finished.

Relation Attributes: {A, B, C, D, E, F}
Functional Dependency: A->C,D
Functional Dependency: B->E
Functional Dependency: A,E->F
Functional Dependency: done
Decompose: {'D', 'C', 'A', 'F', 'E', 'B'} by A -> D,C into {'D', 'C', 'A'} and {'A', 'F', 'E', 'B'}
Decompose: {'A', 'F', 'E', 'B'} by B -> E into {'E', 'B'} and {'A', 'F', 'B'}
BCNF:  {'D', 'C', 'A'}, {'E', 'B'}, {'A', 'F', 'B'}

--- bcnf decomposition end ---