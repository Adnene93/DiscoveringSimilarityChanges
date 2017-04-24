# DiscoveringSimilarityChanges
This repository depict the materials concerning the paper : Flash point : Discovering exceptional pairwise behaviors in votes or ratings data. The repository contains :
1. **PaDMiV** : The project scripts used to generate qualitative and performance experiments
2. **Datasets** : the datasets Movielens (Script) and EPD8 (European parliament Dataset - *8th mandate*) 
3. **Tags of EPD** : contains the details of the tree of tags concerning the dataset EPD8
4. **Qualitative XP** : a set of qualitative experiments and examples of scripts that can be used to reproduce the qualitative experiments results
5. **Performance XP** : a set of performance experiments and examples of scripts that can be used to reproduce the  performance experiments results

## 1.  PaDMiV ##

Contains the method (DSC - Discovering Similarities Changes) method scripts and other scripts usefuls to print figures, filtering files ... It contains mainly the two scripts : 

**./main.py** : used to generate qualitative results
**./mainPerf.py** : used to generate performance experiments



## 2.  Datasets ##

The datasets directory contains the following files : 

+ **/transformMovielens.py** : In order to generate the movielens dataset that is usable by our project. Please run the following steps :
    + Download the movielens100K dataset from the following url : `https://grouplens.org/datasets/movielens/100k/`
    + put the script  **/transformMovielens.py** onto the downloaded directory and execute it
    + The scripts returns this file ***movielens_dataset.csv*** that is ready to use by our scripts
+ **/EPD8.csv** : Contains the records of roll call votes during the 8th mandate (last update 17-10-2016). This file is a result of post processing json files downloaded from `parltrack.euwiki.org`

### 3.  Tags of EPD  ###

The excel file provides details of all the tags by which a ballot can be tagged. This file provide a mapping of tags hierarchical ID with their corresponding labels.


