'''
Created on 3 mars 2017

@author: Adnene
'''


import cProfile
import pstats
from time import time

from ENUMERATORS_ATTRIBUTES.enumerator_attribute_nominal import children_nominal, \
    value_to_yield_nominal, get_domain_from_dataset_nominal, \
    get_starting_pattern_nominal, closure_continueFrom_nominal, \
    pattern_cover_object_nominal, closed_nominal, respect_order_nominal, \
    object_value_for_index_nominal, pattern_cover_object_nominal_index, \
    closed_nominal_index, equality_nominal
from ENUMERATORS_ATTRIBUTES.enumerator_attribute_numeric import children_numeric, \
    value_to_yield_numeric, get_domain_from_dataset_numeric, \
    get_starting_pattern_numeric, closure_continueFrom_numeric, \
    pattern_cover_object_numeric, closed_numeric, respect_order_numeric, \
    object_value_for_index_numeric, pattern_cover_object_numeric_index, \
    closed_numeric_index, equality_numeric, index_correspondant_to_numeric, compute_full_support_numeric
from ENUMERATORS_ATTRIBUTES.enumerator_attribute_simple import children_simple, \
    value_to_yield_simple, get_domain_from_dataset_simple, \
    get_starting_pattern_simple, closure_continueFrom_simple, \
    pattern_cover_object_simple, pattern_cover_object_simple_index, \
    closed_simple, closed_simple_index, respect_order_simple, \
    object_value_for_index_simple, equality_simple, index_correspondant_to_simple, compute_full_support_simple
from ENUMERATORS_ATTRIBUTES.enumerator_attribute_themes import children_themes, \
    value_to_yield_themes, get_domain_from_dataset_theme, \
    get_starting_pattern_theme, closure_continueFrom_themes, \
    pattern_cover_object_themes, closed_themes, respect_order_themes, \
    object_value_for_index_themes, pattern_cover_object_themes_index, \
    closed_themes_index, equality_themes, closure_continueFrom_themes_new, index_correspondant_to_themes, compute_full_support_themes



POSSIBLE_ENUMERATOR_CHILDREN={
    'simple':children_simple,
    'numeric':children_numeric,
    'nominal':children_nominal,
    'themes':children_themes
};

POSSIBLE_ENUMERATOR_VALUE_TO_YIELD={
    'simple':value_to_yield_simple,
    'numeric':value_to_yield_numeric,
    'nominal':value_to_yield_nominal,
    'themes':value_to_yield_themes
};

POSSIBLE_ENUMERATOR_GET_DOMAIN_FROM_DATASET={
    'simple':get_domain_from_dataset_simple,
    'numeric':get_domain_from_dataset_numeric,
    'nominal':get_domain_from_dataset_nominal,
    'themes':get_domain_from_dataset_theme
}; 


POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN={
    'simple':get_starting_pattern_simple,
    'numeric':get_starting_pattern_numeric,
    'nominal':get_starting_pattern_nominal,
    'themes':get_starting_pattern_theme
}; 

POSSIBLE_ENUMERATOR_CONTINUE_FROM={
    'simple':closure_continueFrom_simple,
    'numeric':closure_continueFrom_numeric,
    'nominal':closure_continueFrom_nominal,
    'themes':closure_continueFrom_themes_new
};

POSSIBLE_ENUMERATOR_COVER_OBJECT={
    'simple':pattern_cover_object_simple,
    'numeric':pattern_cover_object_numeric,
    'nominal':pattern_cover_object_nominal,
    'themes':pattern_cover_object_themes
};

POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX={
    'simple':pattern_cover_object_simple_index,
    'numeric':pattern_cover_object_numeric_index,
    'nominal':pattern_cover_object_nominal_index,
    'themes':pattern_cover_object_themes_index
};


POSSIBLE_ENUMERATOR_CLOSED={
    'simple':closed_simple,
    'numeric':closed_numeric,
    'nominal':closed_nominal,
    'themes':closed_themes
};

POSSIBLE_ENUMERATOR_CLOSED_INDEX={
    'simple':closed_simple_index,
    'numeric':closed_numeric_index,
    'nominal':closed_nominal_index,
    'themes':closed_themes_index
};



POSSIBLE_ENUMERATOR_RESPECT_ORDER={
    'simple':respect_order_simple,
    'numeric':respect_order_numeric,
    'nominal':respect_order_nominal,
    'themes':respect_order_themes
};

POSSIBLE_ENUMERATOR_INDEX_OBJECT_VALUES={
    'simple':object_value_for_index_simple,
    'numeric':object_value_for_index_numeric,
    'nominal':object_value_for_index_nominal,
    'themes':object_value_for_index_themes
};

POSSIBLE_ENUMERATOR_EQUALITY={
    'simple':equality_simple,
    'numeric':equality_numeric,
    'nominal':equality_nominal,
    'themes':equality_themes    
};

POSSIBLE_INDEXES_PER_ATTRIBUTES={
    'simple':index_correspondant_to_simple,
    'numeric':index_correspondant_to_numeric,
    'themes':index_correspondant_to_themes
}

POSSIBLE_FULL_SUPPORT_COMPUTING={
    'simple':compute_full_support_simple,
    'numeric':compute_full_support_numeric,
    'themes':compute_full_support_themes,
    
    
}


def value_to_yield_complex(attributes,refinement_index):
    pattren_to_yield=[]
    pattren_to_yield_append=pattren_to_yield.append
    for i in range(len(attributes)):
        attribute_to_refin_Yielded=attributes[i]['pattern_yielded']
#         actual_attribute_type=attribute_to_refin['type']
#         actual_attribute_domain=attribute_to_refin['domain']
#         actual_attribute_refinement_index=attribute_to_refin['refinement_index']
#         actual_attribute_widthmax=attribute_to_refin['widthmax']
#         actual_attribute_pattern=attribute_to_refin['pattern']
#         attribute_pattern_to_yield=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_attribute_pattern,actual_attribute_refinement_index,actual_attribute_widthmax)
#         
        if attribute_to_refin_Yielded is None :
            return None
        pattren_to_yield_append(attribute_to_refin_Yielded)
    return pattren_to_yield


def label_attributes(attributes):
    return [[attr['labelmap'].get(x,x) for x in attr['pattern_yielded']] for attr in attributes]


def pattern_over_attributes(attributes,pattern):
    newattributes=attributes[:]
    for i in range(len(attributes)):
        newattributes[i]=newattributes[i].copy()
        newattributes[i]['pattern']=pattern[i]
        newattributes[i]['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[newattributes[i]['type']](newattributes[i]['domain'],newattributes[i]['pattern'],newattributes[i]['refinement_index'],newattributes[i]['widthmax'])
    return newattributes


def children_complex_flag(attributes,refinement_index):
    
    attribute_to_refin=attributes[refinement_index]
    
    actual_attribute_type=attribute_to_refin['type']
    actual_attribute_domain=attribute_to_refin['domain']
    actual_attribute_refinement_index=attribute_to_refin['refinement_index']
    actual_attribute_widthmax=attribute_to_refin['widthmax']
    actual_pattern=attribute_to_refin['pattern']
    actual_continue_from=POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_pattern,actual_pattern,actual_attribute_refinement_index)
    for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax):
        attributes_child=attributes[:]
        attributes_child[refinement_index]=attributes_child[refinement_index].copy()
        attributes_child[refinement_index]['pattern']=actual_child
        attributes_child[refinement_index]['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
        #POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_child,actual_child,actual_attribute_refinement_index)
        attributes_child[refinement_index]['refinement_index']=actual_refin
        yield attributes_child
        
def children_complex(attributes,refinement_index):
    for i in range(refinement_index,len(attributes)):
        for child_complex in children_complex_flag(attributes,i):
            yield child_complex,i
            
            
def init_attributes_complex(dataset,attributes):
    for attr in attributes:
        attr['domain']=set()
        attr['refinement_index']=0
        
        
    for o in dataset:
        for attr in attributes:
            o_attr_value=o[attr['name']]
            attr['domain'] |=  {o_attr_value} if not hasattr(o_attr_value, '__iter__') else {v for v in o_attr_value}
    for attr in attributes:
        old_width_max=attr.get('widthmax',None)
        attr['domain'],attr['labelmap']=POSSIBLE_ENUMERATOR_GET_DOMAIN_FROM_DATASET[attr['type']](attr['domain'])
        
        attr['pattern'],attr['refinement_index'],attr['widthmax']=POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN[attr['type']](attr['domain'])
        attr['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[attr['type']](attr['domain'],attr['pattern'],attr['refinement_index'],attr['widthmax'])
        if old_width_max is not None:
            attr['widthmax']=old_width_max
        attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr['type']](attr['domain'],attr['pattern'],attr['pattern'],attr['refinement_index'])
    return attributes


def create_index_complex(dataset,attributes):
    index=[]
    index_append=index.append
    for o in dataset:
        o_index={}
        for attr in attributes:
            name=attr['name']
            typeAttr=attr['type']
            domain=attr['domain']
            o_index[name]=POSSIBLE_ENUMERATOR_INDEX_OBJECT_VALUES[typeAttr](domain,o,name)
        index_append(o_index)
    
    for attr in attributes:
        #if attr['type'] in {'numeric','themes'}: 
            POSSIBLE_INDEXES_PER_ATTRIBUTES[attr['type']](attr,index)
    ############################################################################"
#     for attr in attributes:
#         attr_name=attr['name']
#         attr_type=attr['type']
#         attr_domain=attr['domain']
#         attr_refinement_index=attr['refinement_index']
#         if attr_type=='numeric':
#             indexe_attr={k:set() for k in attr_domain}
#             for i in xrange(len(dataset)):
#                 indexe_attr[dataset[i][attr_name]]|={i}
#                 #attr_pattern=[dataset[i][attr_name],dataset[i][attr_name]]
#                 #if POSSIBLE_ENUMERATOR_COVER_OBJECT[attr_type](attr_domain,attr_pattern,attr_refinement_index,dataset[i][attr_name],attr_name):
#             print  indexe_attr   
    return index    


def enumerator_complex(attributes,refinement_index):
    yielded_pattern=value_to_yield_complex(attributes,refinement_index)
    if yielded_pattern is not None:
        yield attributes,yielded_pattern
    for child,refin_child in children_complex(attributes,refinement_index):
        
        for child_attribute,child_pattern_yielded in enumerator_complex(child,refin_child):
            yield child_attribute,child_pattern_yielded




def enumerator_complex_from_dataset(dataset,attributes):
    attributes=init_attributes_complex(dataset,attributes)
    for c in enumerator_complex(attributes,0):
        yield c
        


def compute_support_complex(attributes,dataset):
    support=[]
    support_append=support.append
    for obj in dataset:
        is_obj_covered=True
        for attr in attributes:
            attr_name=attr['name']
            attr_type=attr['type']
            attr_domain=attr['domain']
            attr_refinement_index=attr['refinement_index']
            attr_widthmax=attr['widthmax']
            attr_pattern=attr['pattern']
            is_obj_covered=POSSIBLE_ENUMERATOR_COVER_OBJECT[attr_type](attr_domain,attr_pattern,attr_refinement_index,obj,attr_name)
            if not is_obj_covered:
                break
        
        if not is_obj_covered:
            continue
        support_append(obj)
    return support



def get_attr_infos(attributes):
    return [(attr['name'],POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr['type']],set(attr['pattern'])) for attr in attributes]

def compute_support_complex_index(attributes,dataset,datasetIndices,allIndexes,refinement_index,wholeDataset=[],threshold=0):
    support=[]
    support_append=support.append
    indices=[]
    indices_append=indices.append
    #if len(attributes)>1: print attributes[1]['pattern']
    len_datasetIndices=len(datasetIndices)
    #v_ind=0
    if False :
        attr_infos=[(attr['name'],POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr['type']],attr['pattern']) for attr in attributes[refinement_index:]]
        
        for v_ind in range(len_datasetIndices):
            obj=dataset[v_ind]
            ind_obj=datasetIndices[v_ind]
            all_index_ind_obj=allIndexes[ind_obj]
            is_obj_covered=True
            for name,cover_fun_index,set_pattern in attr_infos:
                is_obj_covered=cover_fun_index(set_pattern,all_index_ind_obj,name)
                #POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr_type](attr_domain,attr_pattern,attr_refinement_index,allIndexes[ind_obj],attr_name))
                if not is_obj_covered:
                    len_datasetIndices-=1
                    if len_datasetIndices<threshold:
                        return support,indices 
                    break
            
            if is_obj_covered:
                support_append(obj)
                indices_append(ind_obj)
        #v_ind+=1
    
    else :
        
        attr_ref=attributes[refinement_index]
        indices=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_ref['type']](datasetIndices,attr_ref)
        if len(indices)<threshold:
            return [],[]
        support=[wholeDataset[inds] for inds in indices]
        
#         indices=datasetIndices#.copy()
#         enum_attrs=(attr for attr in attributes[refinement_index:])
#         attr_1=next(enum_attrs)
#         indices=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_1['type']](indices,attr_1)
#         if len(indices)<threshold:
#             return [],[]
#         for attr in enum_attrs:
#             attr_type=attr['type']
#             indices&=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_type](indices,attr)
#             #print attr['pattern'], indices
#             if len(indices)<threshold:
#                 return [],[]
#         support=[wholeDataset[inds] for inds in indices]
        
        
        
#         for v_ind in range(len_datasetIndices):
#             if datasetIndices[v_ind] in indices:
#                 indices_append(datasetIndices[v_ind])
#                 support_append(dataset[v_ind])
        #support = [dataset[ind] for ind in indices]
    
    
    return support,indices

def compute_support_complex_index_for_cbo(attributes,dataset,datasetIndices,allIndexes,refinement_index):
    support=[]
    support_append=support.append
    indices=[]
    indices_append=indices.append
    values_per_attr=[]
    range_len_attributes=range(len(attributes))
    for k in range_len_attributes:
        values_per_attr.append([])
    
    attr_infos=[(attr['name'],POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr['type']],attr['pattern']) for attr in attributes[refinement_index:]]
    
    #v_ind=0
    for v_ind in range(len(datasetIndices)):
        obj=dataset[v_ind]
        ind_obj=datasetIndices[v_ind]
        is_obj_covered=True
        for name,cover_fun_index,set_pattern in attr_infos:
            is_obj_covered=cover_fun_index(set_pattern,allIndexes[ind_obj],name)
            #POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr_type](attr_domain,attr_pattern,attr_refinement_index,allIndexes[ind_obj],attr_name))
            if not is_obj_covered:
                break
        
        if is_obj_covered:
            support_append(obj)
            indices_append(ind_obj)
            for a_ind in range_len_attributes:
                name=attributes[a_ind]['name']
                values_per_attr[a_ind].append(allIndexes[ind_obj][name])
        #v_ind+=1
    #print values_per_attr[0],attributes[0]['name']
    return support,indices,values_per_attr

def closed_complex(attributes,support):
    closed=[]
    for attr in attributes:
        attr_name=attr['name']
        attr_type=attr['type']
        attr_domain=attr['domain']
        closed_attr=POSSIBLE_ENUMERATOR_CLOSED[attr_type](attr_domain,[item[attr_name] for item in support])
        closed.append(closed_attr)
    return closed



def closed_complex_index(attributes,support,datasetIndices,allIndexes):
    closed=[]
    closed_append=closed.append
    a_ind=0
    

    for attr in attributes:
        attr_name=attr['name']
        attr_type=attr['type']
        attr_domain=attr['domain']
        #attr_dist=attr['distinct']
        closed_attr=POSSIBLE_ENUMERATOR_CLOSED_INDEX[attr_type](attr_domain,[allIndexes[ind][attr_name] for ind in datasetIndices])
        #closed_attr=POSSIBLE_ENUMERATOR_CLOSED_INDEX[attr_type](attr_domain,attr_dist)
        
        #closed_attr=POSSIBLE_ENUMERATOR_CLOSED_INDEX[attr_type](attr_domain,attrValues[a_ind])
        closed_append(closed_attr)
        a_ind+=1
    return closed

def enumerator_complex_config(attributes,refinement_index,config):
    yielded_pattern=value_to_yield_complex(attributes,refinement_index)
    config_new=config.copy()
    if yielded_pattern is not None:
        yield yielded_pattern,attributes,config_new
    if config_new['flag']:
        for child,refin_child in children_complex(attributes,refinement_index):
            for child_pattern_yielded,child_attribute,child_config in enumerator_complex_config(child,refin_child,config_new):
                yield child_pattern_yielded,child_attribute,child_config
    

def enumerator_complex_from_dataset_config(dataset,attributes):
    attributes=init_attributes_complex(dataset,attributes)
    count=0
    config={'support':dataset,'flag':True}
    
    closed_patterns=[]
    
    for pattern_to_yield,e_attributes,e_config in enumerator_complex_config(attributes,0,config):
        e_config['support']=compute_support_complex(e_attributes, e_config['support'])
        count+=1
        if len(e_config['support'])==0:
            e_config['flag']=False
        else:
            pattern_to_yield,label_attributes(e_attributes),e_config
#             closed=closed_complex(e_attributes,e_config['support'])
#             closed_attr=pattern_over_attributes(e_attributes,closed)
#             closed_yield=value_to_yield_complex(closed_attr, 0)
#             if closed_yield not in closed_patterns:
#                 closed_patterns.append(closed_yield)
#                 yield closed,e_config
    print count
    


def respect_order_complex(attr_p1,attr_p2,refinement_index):
    p1=[atr['pattern'] for atr in attr_p1]
    p2=[atr['pattern'] for atr in attr_p2]
    
    p1_types=[atr['type'] for atr in attr_p1]
    
    for i in range(0,refinement_index):
        if not POSSIBLE_ENUMERATOR_EQUALITY[p1_types[i]](p1[i],p2[i]):
            return False
    
    p1_refin=attr_p1[refinement_index]['pattern']
    p2_refin=attr_p2[refinement_index]['pattern']
    refinement_refin=attr_p1[refinement_index]['refinement_index']
    type_refin=attr_p1[refinement_index]['type']
    
    return POSSIBLE_ENUMERATOR_RESPECT_ORDER[type_refin](p1_refin,p2_refin,refinement_refin)


def closure_continueFrom_complex(attr_pattern_input,attr_closed_input,refinement_index):
    attr_continue_from=attr_pattern_input[:]
    
    for i in range(refinement_index,len(attr_pattern_input)):
        attr_continue_from[i]=attr_continue_from[i].copy()
        attr=attr_continue_from[i]
        attr_type=attr['type']
        attr_domain=attr['domain']
        attr_refinement_index=attr['refinement_index']
        attr_pattern=attr['pattern']
        attr_closed=attr_closed_input[i]['pattern']
        attr['pattern']=attr_closed
        #attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr_type](attr_domain,attr_pattern,attr_closed,attr_refinement_index)
        actual_attr_continue_from=attr['continue_from']
        if i==refinement_index:
            attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr_type](attr_domain,attr_pattern,attr_closed,attr_refinement_index)
        else :
            attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr_type](attr_domain,actual_attr_continue_from,attr_closed,attr_refinement_index)
    return attr_continue_from

def attr_to_pattern(attributes):
    return [atr['pattern'] for atr in attributes]




def children_complex_flag_cbo(attributes,refinement_index):
    
    attribute_to_refin=attributes[refinement_index]
    
    actual_attribute_type=attribute_to_refin['type']
    actual_attribute_domain=attribute_to_refin['domain']
    actual_attribute_refinement_index=attribute_to_refin['refinement_index']
    actual_attribute_widthmax=attribute_to_refin['widthmax']
    #actual_continue_from=attribute_to_refin['pattern']
    actual_continue_from=attribute_to_refin['continue_from']
    for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax):
        attributes_child=attributes[:]
        attributes_child[refinement_index]=attributes_child[refinement_index].copy()
        attributes_child_refinement_index=attributes_child[refinement_index]
        attributes_child_refinement_index['pattern']=actual_child
        attributes_child_refinement_index['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
        attributes_child_refinement_index['refinement_index']=actual_refin
        yield attributes_child
        
def children_complex_cbo(attributes,refinement_index):
    for i in range(refinement_index,len(attributes)):
        for child_complex in children_complex_flag_cbo(attributes,i):
            yield child_complex,i

def enumerator_complex_cbo(attributes,refinement_index,config):
    yielded_pattern=value_to_yield_complex(attributes,refinement_index)
    if yielded_pattern is not None:
        yield yielded_pattern,attributes,config
        
        for child,refin_child in children_complex_cbo(attributes,refinement_index):
            config_child=config.copy()
            config_child['support']=compute_support_complex(child,config_child['support'])
            if len(config_child['support'])>0:
                closed=closed_complex(child,config_child['support'])
                attributeClosed=pattern_over_attributes(child, closed)
                if respect_order_complex(child, attributeClosed, refin_child):
                    continue_from=closure_continueFrom_complex(child, attributeClosed, refin_child)
                    for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo(continue_from,refin_child,config_child):
                        yield child_pattern_yielded,child_attribute,child_config

def enumerator_complex_cbo_init(dataset,attributes):
    attributes=init_attributes_complex(dataset,attributes)
    count=0
    config={'support':dataset,'flag':True}
    
    closedinit=closed_complex(attributes,config['support'])
    attributeClosed=pattern_over_attributes(attributes, closedinit)
    attr_continue_from=closure_continueFrom_complex(attributes,attributeClosed,0)
    for pattern_to_yield,e_attributes,e_config in enumerator_complex_cbo(attr_continue_from,0,config):
        yield pattern_to_yield,e_config['support']


def enumerator_complex_cbo_new(attributes,refinement_index,config,wholeDataset,threshold=0,verbose=False):
    yielded_pattern=value_to_yield_complex(attributes,refinement_index)
    config_new=config.copy()

    if yielded_pattern is not None: 
        config_new['nb_visited'][0]+=1
        if verbose and config_new['nb_visited'][0]%1000==0:
            print config_new['nb_visited'][0],config_new['nb_visited'][1],config_new['nb_visited'][2]
        config_new['support'],config_new['indices']=compute_support_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index,wholeDataset,threshold)
        if len(config_new['support'])>=threshold:
            if len(config_new['support'])==threshold:
                config_new['flag']=False
            closed=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'])
            config_new['nb_visited'][1]+=1
            attributeClosed=pattern_over_attributes(attributes, closed)
            #print value_to_yield_complex(attributes,refinement_index)
            #print value_to_yield_complex(attributeClosed,refinement_index)
            
            if respect_order_complex(attributes, attributeClosed, refinement_index):
                continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
                config_new['nb_visited'][2]+=1
                yield value_to_yield_complex(attributeClosed,refinement_index),attributeClosed,config_new
            else :
                config_new['flag']=False
        else :
            config_new['flag']=False
    else :
        continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index)
    
    if config_new['flag']:
        for child,refin_child in children_complex_cbo(continue_from,refinement_index):
            for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new(child,refin_child,config_new,wholeDataset,threshold,verbose):
                yield child_pattern_yielded,child_attribute,child_config


def enumerator_complex_cbo_new_bfs(arr_attributes,arr_refinement_index,confs,threshold=0,lvl=0,verbose=False):
    arr_cont_config=[];
    arr_cont_config_append=arr_cont_config.append
    for attributes,refinement_index,config in zip(arr_attributes,arr_refinement_index,confs):
        yielded_pattern=value_to_yield_complex(attributes,refinement_index)
        config_new=config.copy()
        
        if yielded_pattern is not None: 
            #print yielded_pattern,lvl,config_new.get('lvl',0)
            config_new['nb_visited'][0]+=1
            if verbose and config_new['nb_visited'][0]%100==0:
                print config_new['nb_visited'][0],config_new['nb_visited'][1]
            config_new['support'],config_new['indices']=compute_support_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index,threshold)
            if len(config_new['support'])>=threshold:
                closed=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'])
                attributeClosed=pattern_over_attributes(attributes, closed)
                if respect_order_complex(attributes, attributeClosed, refinement_index):
                    continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
                    config_new['nb_visited'][1]+=1
                    yield value_to_yield_complex(attributeClosed,refinement_index),attributeClosed,config_new
                else :
                    config_new['flag']=False
            else :
                config_new['flag']=False
        else :
            continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index)
        if config_new['flag']:
            arr_cont_config_append((continue_from,config_new,refinement_index))
            config_new['lvl']=lvl+1
    c=[];c_append=c.append
    r=[];r_append=r.append
    confs=[];confs_append=confs.append
    
    for cont_from,conf_new,refin_refin in arr_cont_config:
        for child,refin_child in children_complex_cbo(cont_from,refin_refin):
            c_append(child)
            r_append(refin_child)
            confs_append(conf_new)
    if len(c)>0:
        for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_bfs(c,r,confs,threshold,lvl+1,verbose):
            yield child_pattern_yielded,child_attribute,child_config            
                        

        
# def enumerator_complex_cbo_init_new(dataset,attributes):
#     attributes=init_attributes_complex(dataset,attributes)
#     count=0
#     
#     #print create_index_complex(dataset, attributes);
#     config={'support':dataset,'flag':True,'indices':range(len(dataset)),'allindex':create_index_complex(dataset, attributes)}
#     
#     for pattern_to_yield,e_attributes,e_config in enumerator_complex_cbo_new(attributes,0,config):
#         count+=1
# #         if len(e_config['support'])<0:
# #             e_config['flag']=False
# #         else:
#         yield pattern_to_yield,e_config
#     print '------------',count,'--------------'
'''
'attributes = [
    {
        'name':'name_column',
        'type':'type_attribute'
    }
]
'''



def enumerator_complex_config_all(attributes,refinement_index,config):
    yielded_pattern=value_to_yield_complex(attributes,refinement_index)
    config_new=config.copy()
    config_new['refinement']=refinement_index
    if yielded_pattern is not None:
        yield yielded_pattern,attributes,config_new
    if config_new['flag']:
        for child,refin_child in children_complex(attributes,refinement_index):
            for child_pattern_yielded,child_attribute,child_config in enumerator_complex_config_all(child,refin_child,config_new):
                yield child_pattern_yielded,child_attribute,child_config
                
def enumerator_complex_from_dataset_new_config(dataset,attributes,config_init={},objet_id_attribute='id',threshold=1,verbose=False):
    attributes=init_attributes_complex(dataset,attributes)
    visited=set()
    count=0
    count2=0
    config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0]}
    config.update(config_init)
    for pattern_to_yield,e_attributes,e_config in enumerator_complex_config_all(attributes,0,config):
        count+=1
        e_config['support'],e_config['indices']=compute_support_complex_index(e_attributes,e_config['support'],e_config['indices'],e_config['allindex'],e_config['refinement'],wholeDataset=dataset,threshold=threshold)
        if verbose and count%1000==0:
            print count,count2
        #e_config['support']=compute_support_complex(e_attributes, e_config['support'])
        if len(e_config['support'])<threshold:
            e_config['flag']=False
            
        else:
                
#             actual_id=tuple(sorted(x[objet_id_attribute] for x in e_config['support']))
#             if actual_id in visited:
#                 continue
#             else:
#                 visited|={actual_id}
                count2+=1
                #count2+=1
                e_config['nb_visited']=[count,count2]
                yield pattern_to_yield,label_attributes(e_attributes),e_config
    if verbose :
        print '------------',count,count2,'--------------'
                
def enumerator_complex_cbo_init_new_config(dataset,attributes,config_init={},threshold=1,verbose=False,bfs=False):
#     pr = cProfile.Profile()
#     pr.enable()
    timing=0
    st=time()
    attributes=init_attributes_complex(dataset,attributes)
    
    config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0,0]}
    config.update(config_init)
    timing+=time()-st
    #st=time()
    if not bfs :
        enum=enumerator_complex_cbo_new(attributes,0,config,dataset,threshold,verbose)
    else :
        enum=enumerator_complex_cbo_new_bfs([attributes],[0],[config],threshold,0,verbose)
        
    for pattern_to_yield,e_attributes,e_config in enum:
        #timing+=time()-st
        yield pattern_to_yield,label_attributes(e_attributes),e_config
        #st=time()
    if verbose :
        print '--------ENUMERATOR----------',e_config['nb_visited'],'----------ENUMERATOR-----------'
#     pr.disable()
#     ps = pstats.Stats(pr)
#     ps.sort_stats('cumulative').print_stats(100)