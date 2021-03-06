# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
# Ergasia 2 : Sxediasi & Xrisi Vaseon Dedomenon , June 2020 
# Revisited By: Aggelos Psimitis-Christodoulopoulos (2019513) / Stylianos Alexis (2019502)
# Metaptyxiako HA
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
from itertools import chain

def connection():
    ''' Use this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def classify_review(reviewid):
    
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    sql = """SELECT r.text 
             FROM reviews r 
             WHERE r.review_id = '"""+reviewid+"'"""

    try:
    	cur.execute(sql)
    	results = cur.fetchall()
    	#text from review with id equal to the function's parameter
    	text_review = results

    except:
    	print("error")
    
    sql= """SELECT b.name 
    	    FROM business b, reviews r 
    	    WHERE b.business_id = r.business_id AND r.review_id = '"""+reviewid+"'"""

    try:
    	cur.execute(sql)
    	results = cur.fetchall()
    	#business's name of review with id equal to the function's parameter
    	business_name = results
    except:
    	print("error")

    sql = "SELECT * FROM posterms"

    try:
    	cur.execute(sql)
    	#positive terms from data base
    	posTerms = cur.fetchall()
    except:
    	print("error")

    sql = "SELECT * FROM negterms"

    try:
    	cur.execute(sql)
    	#negative terms from data base
    	negTerms = cur.fetchall()
    except:
    	print("error")

    #divide review text in tuples which contain 1,2 and 3 words respectively
    text = text_review[0][0].split()
    text_one_word = extract_NGrams(text, 1)
    text_two_word = extract_NGrams(text, 2)
    text_three_word = extract_NGrams(text, 3)
    
    #join 2 or 3 separate words into 1 string in order to compare with positive/negative strings with 2 or 3 words respectively
    for item in text_two_word:
    	item[0]=' '.join(word for word in item)
    for item in text_three_word:
    	item[0]=' '.join(word for word in item)

    #positive/negative terms counter
    posCount = 0
    negCount = 0
   
    posTerms_threeWords_list = []
    #count positive terms with 3 words
    for x in posTerms:
    	for y in text_three_word:
    		if y[0]==x[0]:
    		    posCount = posCount+3
    		    #put terms with 3 words counted as positive to a list
    		    posTerms_threeWords_list.append(y)
   
    negTerms_threeWords_list = []
    #count negative terms with 3 words
    for x in negTerms:
    	for y in text_three_word:
    		if y[0]==x[0]:
    		    negCount = negCount+3
    		    #put terms with 3 words counted as negative to a list
    		    negTerms_threeWords_list.append(y)

    posTerms_twoWords_list = []
    #count positive terms with 2 words
    for x in posTerms:
    	for y in text_two_word:
    		if y[0]==x[0]:
    			posCount=posCount+2
    			#put terms with 2 words counted as positive to a list
    			posTerms_twoWords_list.append(y)

    negTerms_twoWords_list = []
    #count negative terms with 2 words
    for x in negTerms:
    	for y in text_two_word:
    		if y[0]==x[0]:
    			negCount=negCount+2
    			#put terms with 2 words counted as negative to a list
    			negTerms_twoWords_list.append(y)

    posTerms_oneWord_list = []
    #count positive terms with 1 words
    for x in posTerms:
    	for y in text_one_word:
    		if y[0]==x[0]:
    			posCount=posCount+1
    			#put terms with 1 word counted as positive to a list
    			posTerms_oneWord_list.append(y)
    

    negTerms_oneWord_list = []
    #count negative terms with 1 words
    for x in negTerms:
    	for y in text_one_word:
    		if y[0]==x[0]:
    			negCount=negCount+1
    			#put terms with 1 words counted as negative to a list
    			negTerms_oneWord_list.append(y)

    #check if any counted positive term with 2 words is a substring of a counted positive term with 3 words
    for x in posTerms_threeWords_list:
        for y in posTerms_twoWords_list:
            if isSubstring(y[0],x[0])==1:
            	#reduce counter because we doublecounted
                posCount=posCount-2	

    #check if any counted positive term with 1 word is a substring of a counted positive term with 2 words
    for x in posTerms_twoWords_list:
        for y in posTerms_oneWord_list:
            if isSubstring(y[0],x[0])==1:
            	#reduce counter because we doublecounted
                posCount=posCount-1
    
    #check if any counted negative term with 2 words is a substring of a counted negative term with 3 words
    for x in negTerms_threeWords_list:
        for y in negTerms_twoWords_list:
            if isSubstring(y[0],x[0])==1:
            	#reduce counter because we doublecounted
                negCount=negCount-2	

    #check if any counted negative term with 1 word is a substring of a counted negative term with 2 words
    for x in negTerms_twoWords_list:
        for y in negTerms_oneWord_list:
            if isSubstring(y[0],x[0])==1:
            	#reduce counter because we doublecounted
                negCount=negCount-1			

    if posCount>negCount:
    	result = "Positive"
    elif posCount<negCount:
    	result = "Negative"
    else:
    	result = "Neutral"

    return [("Business Name","Review"),(business_name[0][0],result)]

#geekforgeeks: https://www.geeksforgeeks.org/check-string-substring-another/
def isSubstring(s1, s2): 
    M = len(s1) 
    N = len(s2) 
  
    # A loop to slide pat[] one by one  
    for i in range(N - M + 1): 
  
        # For current index i, 
        # check for pattern match  
        for j in range(M): 
            if (s2[i + j] != s1[j]): 
                break
              
        if j + 1 == M : 
            return 1 
  
    return -1
#https://programminghistorian.org/en/lessons/keywords-in-context-using-n-grams
def extract_NGrams(wordlist, n):
    return [wordlist[i:i+n] for i in range(len(wordlist)-(n-1))]




def updatezipcode(business_id,zipcode):
    
   # Create a new connection
    
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    sql = """SELECT b.business_id 
             FROM business b 
             WHERE b.business_id = '"""+business_id+"'"""

    try:
        cur.execute(sql)
        business = cur.fetchall()
        if cur.rowcount == 0:
            return [("no such business exists",)]

    except:
        print("error")

    sql = """UPDATE business b 
             SET b.zip_code = """+zipcode+"""
             WHERE b.business_id = '"""+business_id+"'""" 
    
    try:
        cur.execute(sql)
    except:
        con.rollback()
        print("error")

    con.commit()

    sql = """SELECT b.zip_code 
             FROM business b 
             WHERE b.business_id ='"""+business_id+"'"""

    try:
        cur.execute(sql)
        new_zipcode = cur.fetchall()
    except:
        print("error")

    return [("business","new zipcode"),(business[0][0],new_zipcode[0][0])]
    

def selectTopNbusinesses(category_id,n):

    # Create a new connection
    
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    sql = """ SELECT distinct(b.business_id), COUNT(pn.positive) 
              FROM business b, reviews r, reviews_pos_neg pn, business_category bc, category c
              WHERE b.business_id = r.business_id AND r.review_id = pn.review_id AND pn.positive = true 
              AND bc.business_id = b.business_id AND bc.category_id = c.category_id AND c.category_id = """+category_id+"""
              GROUP BY b.business_id
              ORDER BY COUNT(pn.positive) DESC
              LIMIT """+n+""""""

    try:
    	cur.execute(sql)
    	#businesses in category given by the function's parameter, sorted by number of positive reviews
    	results=cur.fetchall()
    except:
    	return("error in querry result")

    n=int(n)
    m = len(results)
    if n>m:
    	k=m
    else:
    	k=n	
    
    results_list=[]
    #create new tuple
    new_results = ("business id","# of positive reviews")
    #put tuple into a list to properly display the results
    results_list.append(new_results)
    for x in range(k):
    	new_results=(results[x][0],results[x][1])
    	results_list.append(new_results)
    
    return results_list

def traceUserInfuence(userId,depth):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    strUserId = str(userId)
    sql = """ SELECT distinct f.friend_id 
              FROM user u, friends f, reviews r1, reviews r2
              WHERE r1.user_id = u.user_id AND r2.user_id = f.friend_id AND r1.business_id = r2.business_id 
              AND r1.date<r2.date AND f.user_id = u.user_id AND u.user_id = '"""+strUserId+"'""""
              GROUP BY r1.business_id"""

    try:
    	cur.execute(sql)
        #user's friends influenced directly by user
    	directFriends = cur.fetchall()
    except:
    	print("error)")
     
    intDepth = int(depth) 

    #auxilliary list of lists to store friends of each user's direct friend
    dummyLists = [[] for i in range(intDepth+1)]

    #put friends that are influenced directly by the user in a list                 
    directFriendsList = []
    for x in directFriends:
        directFriendsList.append(x[0])
        dummyLists[1].append(x[0])

    l = len(directFriendsList)

    #create a tuple and then a list to properly display the results 
    listTuple = ("Influenced explicitly","Influenced implicitly")
    finalList = []
    finalList.append(listTuple)

    if intDepth>1:
        #put users that are influenced indirectly into a separate list
        indirectFriendsList = []
        for i in range(intDepth):
            for item in dummyLists[i]:   
                sql = """ SELECT distinct f.friend_id 
                          FROM user u, friends f, reviews r1, reviews r2
                          WHERE r1.user_id = u.user_id AND r2.user_id = f.friend_id AND r1.business_id = r2.business_id 
                          AND r1.date<r2.date AND f.user_id = u.user_id AND u.user_id = '"""+item+"'""""
                          GROUP BY r1.business_id"""
                try:
                    cur.execute(sql)
                    results = cur.fetchall()
                except:
                    print("error")
                for x in results:
                    indirectFriendsList.append(x[0])
                    dummyLists[i+1].append(x[0])

        k = len(indirectFriendsList)
        if k>l:
            for i in range(k):
                if i<l:
                    listTuple = (directFriendsList[i], indirectFriendsList[i])
                else:
                    listTuple = ((), indirectFriendsList[i])
                finalList.append(listTuple)
        else:
            for i in range(l):
                if i<k :
                    listTuple = (directFriendsList[i], indirectFriendsList[i])
                else:
                    listTuple = (directFriendsList[i], ())
                finalList.append(listTuple)
    else:
        #if depth = 1 simply put the results from the first querry into the final list
        for i in range(l):
            listTuple = (directFriendsList[i],())
            finalList.append(listTuple)

    
    return finalList

    


