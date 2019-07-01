# Molecule Property Prediction

This is a Kaggle competetion [dataset](https://www.kaggle.com/c/champs-scalar-coupling) which still ongoing. 

My target is to use the property of the molecule to predict the magnetic interaction(the scalar coupling constant) between two atoms in a molecule.

## Predictors

This is a typical relational dataset. The train and test file contains the pairs relation of atoms in different molecules. The major information has:

- molecule_name: the id of each molecule
- atom_index: the index of atom which is unique in each molecule
- type: the coupling type between two atoms pair
- x, y, z: the spatial position of each atom
- atom: the element of the atom

These are basically all the information I have.

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
