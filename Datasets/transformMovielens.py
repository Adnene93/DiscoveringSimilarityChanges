import csv

def readCSVwithHeader(source,selectedHeader=None,numberHeader=None,arrayHeader=None,delimiter='\t',flag_header_exceed=False,has_header=True,skip=False):
    results=[]
    header=[]
    
    with open(source, 'rb') as csvfile:
        
        readfile = csv.reader(csvfile, delimiter=delimiter)
        if not has_header:
            header=selectedHeader
        else :
            header=next(readfile)[:-1] if flag_header_exceed else next(readfile)
        if skip :

            header=selectedHeader
            next(readfile)
        #selectedHeader=selectedHeader if selectedHeader is not None else header
        
        range_header=range(len(header))
        
        if numberHeader is None and arrayHeader is None  :
            if selectedHeader is None:
                results=[{header[i]:row[i] for i in range_header} for row in readfile]
            else :
                results=[{header[i]:row[i] for i in range_header if header[i] in selectedHeader} for row in readfile]
        else :
            numberHeader=numberHeader if numberHeader is not None else []
            arrayHeader=arrayHeader if arrayHeader is not None else []
            if selectedHeader is None:
                results=[{header[i]:float(row[i]) if header[i] in numberHeader else eval(row[i]) if header[i] in arrayHeader else row[i] for i in range_header} for row in readfile] 
            else :
                results=[{header[i]:float(row[i]) if header[i] in numberHeader else eval(row[i]) if header[i] in arrayHeader else row[i] for i in range_header if header[i] in selectedHeader} for row in readfile]

        
    return results,header

def writeCSVwithHeader(data,destination,selectedHeader=None,delimiter='\t'):
    header=selectedHeader if selectedHeader is not None else data[0].keys()
    with open(destination, 'wb') as f:
        writer2 = csv.writer(f,delimiter='\t')
        writer2.writerow(header)
        for elem in iter(data):
            row=[]
            for i in range(len(header)):
                row.append(elem[header[i]])
            writer2.writerow(row)



moviesGenres=['Unknown','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery','Romance','SciFi','Thriller','War','Western']
nbHeader=['movieID','Unknown','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery','Romance','SciFi','Thriller','War','Western']
agesDiscret=['G0-10','G10-20','G20-30','G30-40','G40-50','G50-60','G60-70','G70-80','G80-90','G90-100']

moviesGenresMap={
    'Unknown':0,'Action':1,'Adventure':2,'Animation':3,'Children':4,'Comedy':5,'Crime':6,'Documentary':7,'Drama':8,'Fantasy':9,'FilmNoir':10,'Horror':11,'Musical':12,'Mystery':13,'Romance':14,'SciFi':15,
    'Thriller':16,'War':17,'Western':18
}

agesmap={
    (0,17):'teenagers',
    (18,34):'young',
    (35,55):'middle-age',
    (56,100):'old'
}
#userid | itemid | rating | timestamp
items,headerItem=readCSVwithHeader('u.item',selectedHeader=['movieID','movieTitle','releaseDate','videoRD','IMDBURL','Unknown','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery','Romance','SciFi','Thriller','War','Western'],delimiter='|',flag_header_exceed=True,has_header=False,skip=True)
users,headerUser=readCSVwithHeader('u.user',selectedHeader=['userid','age','gender','occupation','zipcode'],delimiter='|',flag_header_exceed=True,has_header=False)
reviews,headerReviews=readCSVwithHeader('u.data',selectedHeader=['userid','movieID','Rating','Timestamp'],delimiter='\t',flag_header_exceed=True,has_header=False,skip=False)
newDataset=[]


moviesMapping={}
usersMapping={}

for row in items:
    moviesMapping[row['movieID']]=row

for row in users:
    usersMapping[row['userid']]=row
    #raw_input('...')

newDataset=[]
for row in reviews:
    new_row=row.copy()
    new_row.update(moviesMapping[new_row['movieID']])
    new_row.update(usersMapping[new_row['userid']])
    new_row['releaseDate']=new_row['releaseDate'][7:]
    for key in moviesGenresMap:
        new_row[key]=int(new_row[key])
    newDataset.append(new_row)
    #print row
    #raw_input('....')
#writeCSVwithHeader(newDataset,'RANDmovielens100k.csv',selectedHeader=['movieID','movieTitle','releaseDate','IMDBURL','Unknown','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery','Romance','SciFi','Thriller','War','Western','userid','age','gender','occupation','zipcode','Timestamp','Rating'])


#dataset,header=readCSVwithHeader('RANDmovielens100k.csv',numberHeader=nbHeader,delimiter='\t')
dataset=newDataset[:]
newDataset=[]
for row in dataset :

    row['genres']=[str(moviesGenresMap[k])+' '+k for k in moviesGenres if row[k]==1]
    age_group=''
    for cond,group_slice in agesmap.iteritems():
        if int(row['age']) >= cond[0] and  int(row['age']) <= cond[1]:
            age_group=group_slice
            break

    row['ageGroup']=age_group
    for k in moviesGenres:
        del row[k]
    if row['releaseDate']=='':
        continue
    newDataset.append(row)

dataset=sorted(newDataset,key=lambda x : x['movieID'])

for row in dataset:
    row['movieID']=str(int(row['movieID']))

writeCSVwithHeader(dataset,'movielens_dataset.csv',selectedHeader=['movieID','movieTitle','releaseDate','genres','IMDBURL','userid','age','ageGroup','gender','occupation','zipcode','Timestamp','Rating'])


































# newDataset=[]
# for row in dataset :

#     row['genres']=[str(moviesGenresMap[k])+' '+k for k in moviesGenres if row[k]==1]
#     age_group=''
#     for cond,group_slice in agesmap.iteritems():
#         if int(row['age']) >= cond[0] and  int(row['age']) <= cond[1]:
#             age_group=group_slice
#             break

#     row['ageGroup']=age_group
#     for k in moviesGenres:
#         del row[k]
#     if row['releaseDate']=='':
#         continue
#     newDataset.append(row)

# dataset=sorted(newDataset,key=lambda x : x['movieID'])

# for row in dataset:
#     row['movieID']=str(int(row['movieID']))

# writeCSVwithHeader(dataset,'movielens100YearsTrNew.csv',selectedHeader=['movieID','movieTitle','releaseDate','genres','IMDBURL','userid','age','ageGroup','gender','occupation','zipcode','Timestamp','Rating'])
