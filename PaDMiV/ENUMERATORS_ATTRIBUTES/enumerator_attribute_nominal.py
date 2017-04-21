'''
Created on 1 mars 2017

@author: Adnene
'''
from operator import is_not
from functools import partial

def get_domain_from_dataset_nominal(distinct_values):
    return sorted(distinct_values),{}

def get_starting_pattern_nominal(domain):
    starting_pattern=domain[:]
    starting_refinement=0
    default_widthmax=0
    return starting_pattern,starting_refinement,default_widthmax

def value_to_yield_nominal(domain,pattern,refinement_index,widthmax):
    returned=filter(partial(is_not, None), pattern)    
    return returned if len(returned) else None


def children_nominal(domain,pattern,refinement_index,widthmax=0):
    
    for i in range(refinement_index,len(domain)):
        if pattern[i] is None:
            continue
        possible_child=pattern[:]
        possible_child[i]=None
        yield possible_child,i+1
        


        
        
        
def enumerator_nominal(domain,pattern,refinement_index,widthmax=0):
    yielded_pattern=value_to_yield_nominal(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_nominal(domain,pattern,refinement_index,widthmax):
        for child_pattern in enumerator_nominal(domain,child,refin_child,widthmax):
            yield child_pattern
            
def pattern_cover_object_nominal(domain,pattern,refinement_index,record,attribute):
    return record[attribute] in pattern

def pattern_cover_object_nominal_index(pattern,record,attribute):
    return record[attribute] in pattern

def object_value_for_index_nominal(domain,record,attribute):
    return record[attribute]   




def infimum_nominal(domain,p1,p2):
    return sorted(set(p1)|set(p2))

def closed_nominal(domain,list_patterns):
    list_set_patterns = [{item} for item in list_patterns]
    clos=reduce(set.union,list_set_patterns)
    res=domain[:]
    for k in range(len(res)):
        if res[k] not in clos:
            res[k]=None
    return res

def closed_nominal_index(domain,list_patterns):
    list_set_patterns = [{item} for item in list_patterns]
    clos=reduce(set.union,list_set_patterns)
    res=domain[:]
    for k in range(len(res)):
        if res[k] not in clos:
            res[k]=None
    return res

def respect_order_nominal(p1,p2,refinement_index):
    return False if any(p1[i]<>p2[i] for i in range(0,refinement_index)) else True

def closure_continueFrom_nominal(domain,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    return closed

def equality_nominal(p1,p2):
    return p1==p2