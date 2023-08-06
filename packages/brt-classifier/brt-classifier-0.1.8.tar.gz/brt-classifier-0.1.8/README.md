# Tree classifications

This repository contains classifications of some of the problems on rooted binary trees.

## Usage

**To generage a new problem file:**

```
python -m brt_classifier generate <label-count>
```

where "label-count" is 2 or 3 will generate `problems/problems-temp.json` that contains all non-isomorphic, non-redundant problems. Moreover, it will classify some of those problems that can be automatically classified.

**To classify problems** in e.g. file `problems/3labels.json`:

```
python -m brt_classifier classify problems/3labels.json
```

Add a flag `-w` at the end, if you want the classification result's changes to persist

**To find out problems's complexity** e.g. for problem {121, 212}:

```
python -m brt_classifier find 121 212
```

Change the constraints at the end of the command to search for a different problem.

**To print statistics on a problem file** e.g. file `problems/3labels.json`:

```
python -m brt_classifier statistics problems/3labels.json
```

## Notation

_The following notation explanation is about 2-label setting, but can be trivially extended to a setting with > 2 labels_

We list the problems using sets of allowed restrictions. Since the tree is always binary, we’ll use _xyz_ as a shorthand for “if a node has a label _y_, then it must have 1 child with label _x_ and one child with label _z_”. E.g. _{ 121, 212 }_ means that if a node has label 2, it must have both children with label 1, and if a node has a label 1, it must have both children with label 2. Another example, _{112, 212, 122}_ means “if a node has label 1, it can either have children with labels 1 and 2 (i.e. children with different labels) or both children with labels 2; if a node has label 2, it must have children with 2 different labels (1, 2)”

## Problems

Note that we only consider problems that are non-isomorphic. E.g. { 112, 121 } and { 122, 212 } are isomorphic as we can just map ones to twos and twos to ones in the former instance to get to the latter one.

Besides, we also reduce the number of problems by eliminating redundant constraints wherever possible. E.g. {111, 112, 212} is in essence the same problem as {111} since 2s are never allowed to be a "parent" node. Similarly, {112, 212} is the same as {} (i.e. nothing is allowed) since 2 can never be used as a parent node so we can safely remove both 112 and 212.

### 2 labels

Most of the problems were rather trivial to classify. Lower and upper bound justifications for a not-so-trivial problem {121, 112} can be found here in [the docs folder](https://github.com/AleksTeresh/tree-classifications/tree/master/docs).

{112, 122} is O(1)-time solvable: each node simply tells one of its children "you will be 1" and the other one "you will be 2". Since {112, 122} is O(1)-time solvable then any problems that are relaxations of it are O(1)-time solvable too. Thus, {112, 212, 122} and {121, 112, 212, 122} were classified as O(1) solvable too.
