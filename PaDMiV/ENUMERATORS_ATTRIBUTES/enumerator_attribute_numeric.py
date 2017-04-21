'''
Created on 1 mars 2017

@author: Adnene
'''

def get_domain_from_dataset_numeric(distinct_values):
    return sorted(distinct_values),{}

def get_starting_pattern_numeric(domain):
    starting_pattern=domain[:]
    starting_refinement=0
    default_widthmax=0
    return starting_pattern,starting_refinement,default_widthmax



def value_to_yield_numeric(domain,pattern,refinement_index=0,widthmax=0):
    returned=None
    if (len(pattern)>=1):
        returned=[pattern[0],pattern[-1]]
    return returned

def children_numeric(domain,pattern,refinement_index=0,widthmax=0):
    if len(pattern)>1:
        arr_left=pattern[1:]
        arr_right=pattern[:-1]
        possible_children=[[arr_left,arr_right],[0,1]]

        for k in range(refinement_index,2):
            if possible_children[0][k][-1]-possible_children[0][k][0]>=widthmax:
                yield possible_children[0][k],possible_children[1][k]



def enumerator_numeric(domain,pattern,refinement_index=0,widthmax=0):
    yielded_pattern=value_to_yield_numeric(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_numeric(domain,pattern,refinement_index,widthmax):
        for child_pattern in enumerator_numeric(domain,child,refin_child,widthmax):
            yield child_pattern


def pattern_cover_object_numeric(domain,pattern,refinement_index,record,attribute):
    #x=record[attribute]
    return pattern[0] <= record[attribute] <= pattern[-1]

def pattern_cover_object_numeric_index(pattern,record,attribute):
    return pattern[0] <= record[attribute] <= pattern[-1]
    #return record[attribute] in pattern

def object_value_for_index_numeric(domain,record,attribute):
    return record[attribute]   

    

def infimum_numeric(domain,p1,p2):
    return sorted(set(p1)|set(p2))

def closed_numeric(domain,list_patterns):
    #print list_patterns
    list_set_patterns = [{item} for item in list_patterns]
    clos=sorted(reduce(set.union,list_set_patterns))
    res=domain[domain.index(clos[0]):domain.index(clos[-1])+1]
    return res

def closed_numeric_index(domain,list_patterns):
    clos=sorted(set(list_patterns))
    res=domain[domain.index(clos[0]):domain.index(clos[-1])+1]
    return res

def respect_order_numeric(p1,p2,refinement_index):
    return False if refinement_index==1 and p1[0]<>p2[0] else True




def closure_continueFrom_numeric(domain,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    return closed


def equality_numeric(p1,p2):
    return p1==p2