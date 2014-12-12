#-*- coding: utf-8 -*-
import pandas
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import sqlite3
import os
import csv
import matplotlib.pyplot as plt
import math

#amelioration : faire une PCA par exemple :-) avant la Logit
#separer la classe '1' en classes '4' et classes '5'

from GetFinalDB import finalSep
from constructUserIded import primaryCat
#~ df = pandas.read_csv('../FinalSimpleDB.txt',sep = ';')
#~ if not os.exist('../FinalSimpleDB.db3') :
con = sqlite3.connect('../FinalSimpleDB.db3')
#~ name = """idCust text, idProd text,date numeric, ratingReview integer, avgRating real, wAvgRating real,  nbReview integer, 
			#~ nbHelpful integer, salesrank integer, %othervariables%""".replace("%othervariables%",','.join(["catCust"+str(i)+" integer" for i in range(1,len(primaryCat)+1)]))
#~ nbVariables = len(names.split(','))
#~ command = """create table if not exists DbSql (%names%);""".replace("%names%",names)
#~ print command

for year in [ i for i in range(1998,2004)] :
	regr = linear_model.LinearRegression()
	regrLasso = linear_model.Lasso(alpha = 10.,max_iter = 1e6,tol = 1e-3)
	randomForest = RandomForestClassifier(n_estimators = 30,n_jobs = 4)
	Logit = linear_model.LogisticRegression()
	beginTrain = str(year)+"-01-01"
	endTrain = str(year+1)+"-12-31"
	beginTest = str(year+2)+"-01-01"
	endTest = str(year+2)+"-12-31"
	commandTrain = """SELECT * FROM DbSql where (date(date) between date(\"%beginTrain%\") and date(\"%endTrain%\"))""".replace("%beginTrain%",beginTrain).replace("%endTrain%",endTrain)
	commandTest = """SELECT * FROM DbSql where (date(date) between date(\"%beginTest%\") and date(\"%endTest%\"))""".replace("%beginTest%",beginTest).replace("%endTest%",endTest)
	print "Extract database"
	dfTrain = pandas.read_sql(commandTrain,con)
	dfTest = pandas.read_sql(commandTest,con)
	
	
	dfTrain["Apetance"] = (dfTrain["ratingReview"]/4).astype('int')
	dfTest["Apetance"] = (dfTest["ratingReview"]/4).astype('int')
	varPredicted = "Apetance"
	
	print "Training Models"
	#~ regr.fit(dfTrain.ix[:,4:-1],dfTrain["ratingReview"])
	randomForest.fit(dfTrain.ix[:,4:-1],dfTrain[varPredicted])
	#~ regrLasso.fit(dfTrain.ix[:,4:-1],dfTrain["ratingReview"])
	Logit.fit(dfTrain.ix[:,4:-1],dfTrain[varPredicted])
	print "Predict Result"
	#~ predLin = regr.predict(dfTest.ix[:,4:-1])
	predRF = randomForest.predict(dfTest.ix[:,4:-1])
	predLogit = Logit.predict(dfTest.ix[:,4:-1])
	#~ predLasso = regrLasso.predict(dfTest.ix[:,4:-1])
	
	
	#~ print("Error linear model for %d : %f" % (year,np.sqrt(np.mean((predLin - dfTest[varPredicted])*(predLin - dfTest[varPredicted])))))
	#~ print("Error random forest for %d : %f" % (year,np.sqrt(np.mean((predRF - dfTest[varPredicted])*(predRF - dfTest[varPredicted])))))
	#~ print("Error Lasso for %d : %f" % (year,np.sqrt(np.mean((predLasso - dfTest[varPredicted])*(predLasso - dfTest[varPredicted])))))
	#~ predLin = predLin.astype('int')
	predRF = predRF.astype('int')
	predLogit = predLogit.astype('int')
	#~ print pandas.crosstab(dfTest[varPredicted],predLin)
	print pandas.crosstab(dfTest[varPredicted],predRF)
	print pandas.crosstab(dfTest[varPredicted],predLogit)
	#~ break
	
	
	#~ print 'Coefficients (%d) : ' % year, regr.coef_
	
	#~ plt.plot(dfTest["idCust"],dfTest["ratingReview"])
	#~ plt.plot(dfTest["idCust"], regr.predict(dfTest.ix[:,4:]),color = "blue")
	#~ plt.show()
	
	
	#~ print dfTrain.shape
	#~ print dfTest.shape
	#~ print "_____________________"





#~ command = """SELECT count(*), date  FROM DbSql where date(date) >= date(\"1995-01-01\") group by date """.replace("%beginDate%",beginDate).replace("%endDate%",endDate)
#~ print command
#~ df = pandas.read_sql(command,con)

#~ print df.head
#~ print df.shape

#~ plt.figure()
#~ df.plot(kind = 'bar')
#~ plt.show()
#~ con.close()
#~ con.execute(command)

#~ print "the data base is created"
#~ csvReader = csv.reader(open('../FinalSimpleDB.txt'), delimiter=';')
#~ print "Let's insert !"
#~ for row in csvReader:
	#~ print row
	#~ command = """insert into DbSql (%%names%%) values (%dots%)""".replace('%%names%%',names.replace('integer','').replace('numeric','').replace('real','').replace('text','')).replace('%dots%',','.join(['?' for i in range(1,nbVariables+1)]))
	#~ print command
	#~ con.execute(command, row)

#~ con.execute(command)
#~ con.execute(""".separator '%sep%'
			#~ .import \"../FinalSimpleDB.txt\" DbSql """.replace("%sep%",finalSep))
#~ command = """load data local infile  \"../FinalSimpleDB.txt\" into table DbSql fields terminated by \"%sep%\" lines terminated by \"\r\n\"; """.replace("%sep%",finalSep)

#~ create table DbSql(idCust text, idProd text,date numeric, ratingReview integer, avgRating real, wAvgRating real,  nbReview integer, nbHelpful integer, salesrank integer, catCust1 integer,catCust2 integer,catCust3 integer,catCust4 integer,catCust5 integer,catCust6 integer,catCust7 integer,catCust8 integer,catCust9 integer,catCust10 integer,catCust11 integer,catCust12 integer,catCust13 integer,catCust14 integer);
