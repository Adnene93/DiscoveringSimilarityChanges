'''
Created on 2 mars 2017

@author: Adnene
'''
def flattenThemesTree(themes):
    arrNew=[]
    for x in themes :
        s= x.split('.')
        
        for i in range(len(s)) :
            sub=''
            for j in range(i+1):
                sub+=s[j]+'.'
            sub=sub[:-1]
            if sub not in arrNew :
                arrNew.append(sub)
    arrNew.append('')
    arrNew.sort()
    return arrNew

def parent_tag(t):
    if len(t)==0:
        return None
    parent='.'.join(t.split('.')[:-1])
    return parent


def all_parents_tag(t): #PARENTS + SELF
    v=t.split('.')
    all_parents=set(['']) | set(['.'.join(v[0:i+1]) for i in range(len(v))])
    return all_parents

def all_parents_tag_exclusive(t): #PARENTS without SELF
    if (t==''):
        return set()
    v=t.split('.')
    all_parents=set(['']) | set(['.'.join(v[0:i+1]) for i in range(len(v)-1)])
    return all_parents

def tree_theme(themes):
    flat=flattenThemesTree(themes)
    ret_map={};
    for x in flat:
        parent_x=parent_tag(x)
        all_parents=all_parents_tag(x)
        ret_map[x]={'parent':parent_x,'children':[],'right_borthers':[],'all_parents':all_parents,'all_parents_exclusive':all_parents-{x}}
        if parent_x is not None:
            ret_map[parent_x]['children'].append(x)
        
    for x,y in ret_map.iteritems():
        if y['parent'] is not None:
            brothers=ret_map[y['parent']]['children']
            y['right_borthers']=brothers[brothers.index(x)+1:]
    return ret_map



def get_theme_from_value(v):
    space_index=v.find(' ')
    if space_index>0:
        return v[:space_index]
    return v

def get_label_from_value(v):
    space_index=v.find(' ')
    if space_index>0:
        return v[space_index+1:]
    return v

def get_domain_from_dataset_theme(distinct_values):
    distinct_themes_without_label=set()
    labelmap={}
    for v in distinct_values:
        theme_v=get_theme_from_value(v)
        label_v=get_label_from_value(v)
        labelmap[theme_v]=label_v
        distinct_themes_without_label |= {theme_v}
    tree_of_themes=tree_theme(distinct_themes_without_label)
    for key in tree_of_themes:
        labelmap[key]=labelmap.get(key,'-')
    #print labelmap
    return tree_of_themes,labelmap

def get_starting_pattern_theme(tree):
    starting_pattern=['']
    starting_refinement=0
    default_widthmax=float('inf')
    return starting_pattern,starting_refinement,default_widthmax


def value_to_yield_themes(tree,pattern,refinement_index,widthmax=0):
    return None if (refinement_index<len(pattern)-1) and pattern[refinement_index] in tree[pattern[refinement_index+1]]['all_parents']  else pattern

def children_themes_flag(tree,pattern,refinement_index=None,widthmax=float('inf')):
    len_p=len(pattern)
    refin_index_is_not_last=refinement_index+1<len_p 
    p_refinindex_1=pattern[refinement_index+1] if refin_index_is_not_last else None
    if len_p<=widthmax:
        if refinement_index is None:
            refinement_index=len_p
        last_t=pattern[refinement_index]
        actual=tree[last_t]
        parent=actual['parent']
        for c in actual['children']:
            if refin_index_is_not_last and c>=p_refinindex_1:
                continue
            actual_child=pattern[:]
            actual_child[refinement_index]=c
            yield actual_child,refinement_index
        if len_p<widthmax:
            brothers_and_uncles=[br for par in actual['all_parents'] for br in tree[par]['right_borthers'] if not (refin_index_is_not_last and br>=p_refinindex_1)]
            for b in brothers_and_uncles:
                actual_child=pattern[:]
                actual_child.insert(refinement_index+1,b)
                yield actual_child,refinement_index+1


def children_themes(tree,p_from,refinement_index=None,widthmax=float('inf')):
    for p in p_from:
        len_p=len(p)
        for new_refin in range(refinement_index,len_p):
            if new_refin>0 and p[new_refin-1] in tree[p[new_refin]]['all_parents']:#(isParent(p[new_refin-1],p[new_refin]) or p[new_refin-1]==p[new_refin]):
                break
            for c,refin_child in children_themes_flag(tree,p,new_refin,widthmax):
                yield c,refin_child 
                

def enumerator_themes(domain,pattern,refinement_index,widthmax):
    yielded_pattern=value_to_yield_themes(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_themes(domain,closure_continueFrom_themes(domain, pattern, pattern, refinement_index),refinement_index,widthmax):
        for child_pattern in enumerator_themes(domain,child,refin_child,widthmax):
            yield child_pattern

          
def maximum_tree(tree,set_tag):
    return sorted(set_tag-{tag_parent for tag in set_tag for tag_parent in tree[tag]['all_parents_exclusive']})


def pattern_cover_object_themes(tree,pattern,refinement_index,record,attribute):
    return set(pattern) <= {par for x in record[attribute] for par in tree[x]['all_parents']}



def pattern_cover_object_themes_index(pattern,record,attribute):
    return set(pattern) <= record[attribute]
#{par for x in record[attribute] for par in tree[x]['all_parents']}

def object_value_for_index_themes(tree,record,attribute):
    return {par for x in record[attribute] for par in tree[get_theme_from_value(x)]['all_parents']}

def infimum_themes(tree,p1,p2):
    toRet=set()
    if p1<>p2:
        toRet=set(maximum_tree(tree,{par for x in p1 for par in tree[x]['all_parents']} & {par for x in p2 for par in tree[x]['all_parents']}))
    else :
        toRet=set(maximum_tree(tree,set(p1)))
    return sorted(toRet)


def closed_themes(tree,list_patterns):
    list_patterns_new=[{par for x in pat for par in tree[x]['all_parents']} for pat in list_patterns]
    #list_set_patterns = map(set,list_patterns)
    return maximum_tree(tree, reduce(set.intersection,list_patterns_new))



def closed_themes_index(tree,list_patterns):
    list_pattern_new=set.intersection(*list_patterns)
    return maximum_tree(tree, list_pattern_new)


def respect_order_themes(p1,p2,refinement_index):
    if p1==p2:
        return True
    range_len_min_comp=reversed(range(refinement_index))
    res=True
    
    if (p1[refinement_index]>p2[refinement_index]):
        return False
    
    for i in range_len_min_comp:
        res&=(p1[i]==p2[i])
        if not res:
            return res
    return True





def closure_continueFrom_themes(tree,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    ref_in_closed=closed[refinement_index]
    ref_in_p=pattern[refinement_index]
    new_pattern=closed[:]
    if ref_in_p<ref_in_closed:
        new_pattern.insert(refinement_index,ref_in_p)
    
    if new_pattern==closed:
        return [new_pattern]
    else :
        return [new_pattern,closed]
    
def closure_continueFrom_themes_new(tree,patternArray,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    ret=[];ret_extend=ret.extend;
    if type(patternArray[0]) is not list:
        ret_extend(closure_continueFrom_themes(tree,patternArray,closed,refinement_index))
        ret_new=ret
    else :
        for pattern in patternArray:
            ret_extend(closure_continueFrom_themes(tree,pattern,closed,refinement_index))
    
        ret_set={tuple(x) for x in ret}
        ret_sorted=[sorted(s) for s in ret_set]
        ret_refs=[(ret_sorted[i][refinement_index],ret_sorted[i],len(ret_sorted[i])) for i in range(len(ret_sorted))]
    
            
        ret_refs_dict={}
        for refin,pat,length_pat in ret_refs:
            if length_pat not in ret_refs_dict:
                ret_refs_dict[length_pat]=[]
            ret_refs_dict[length_pat].append((refin,pat))
        
        ret_new=[min(ret_refs_dict[k],key=lambda x : x[0])[1] for k in ret_refs_dict]

    return ret_new

    
def equality_themes(p1,p2):
    return p1==p2