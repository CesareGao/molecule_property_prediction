# Molecule Property Prediction

This is a Kaggle competetion [dataset](https://www.kaggle.com/c/champs-scalar-coupling) which still ongoing. 

## Predictors

This is a typical relational dataset. The train and test file contains the pairs relation of atoms in different molecules. The major information has:

- molecule_name: the id of each molecule
- atom_index: the index of atom which is unique in each molecule
- type: the coupling type between two atoms pair
- x, y, z: the spatial position of each atom
- atom: the element of the atom

These are basically all the information I have.

## Motivation

My target is to use the property of the molecule to predict the magnetic interaction(the scalar coupling constant) between two atoms in a molecule. This property is really hard to measure as the there is no clear way to just look at and calculate the coupling constant. It always be hard when it comes to large molucule with many atoms. So if I can predict it, according to the structure of molecule, it will be really helpful for give a first look at a new material.

The predictors is quite domain related. So maybe we could use a small social network group(for example, FaceBook) to indicate the molecule.

Molecule | FaceBook Group
------------------ | ---------------------
molecule name | unique group name
atom index | each person's id in the group
what kind of atom | the social title of each person
hidden atom | who joined the group but with unpublic personal infos even could be a net police
spatial position of each atom | the group title of each person
coupling type | the social titles of each pair of group members and their relation(stranger, friends, enemy)
distance between atoms | how close each pair of group members look like
coupling constant(our target) | how truly close are the relations among each pair of group members

I want to analyze the small graph problems, figure out a way to quantify the effect of a graph to each node and predict the relation among each nodes pair.

## Method

Use these less-predictor data to predict the scalar coupling constant of atom paris in different molecules.

1. Convert the molecule data into a graph.
1. Find the influence of the molecule structure to each atom pair and send the information from graph back to the data table.
1. Use the extrated structure data to build a machine learning model.
1. Model evaluation and selection, try to use deep learning if possible.

## Main problem

- limited information from the dataset. How to performe a informational data mining?
- How to summarize structure data of differenmt molecule structure?
- If to return a quantified information, how to set the value of each column?
- As the dataset owner only concern about the coupling constant between certain element of atom. There are some missing train data of other element. How to fill the missing atom and relation data, and evaluate their influence.

## Some ideas to try

- Use Pregel to build graph model and count the influence of the molecule structure
- Use pagerank algorithms to evaluate the contrubution of the molecule structure
- take the volume of the molecule into acount
- Use k-means to set the initial contribution of coupling and modified this with a feedback
- Set all the unknown atom with same initial value
