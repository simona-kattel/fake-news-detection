import pandas as pd 
import numpy as np 
fake= pd.read_csv("fake.csv")
real=pd.read_csv("real.csv")

#data cleaning 
   #in data cleaning we load the dataset , see if the dataset is really loaded with the help of head or samples then we label the 
   # data for example here fake will be labled as 0 and real as 1 and remove the rows that we dont need  in our project 
   #and only the rows and coloms that we will use and then again check the now data by using head or samples and then we can movve to 
   #data preprocessing this is the basic load method of data cleaning

    
fake.sample(5)
real.sample(5)  #gives 5 radom data rows from the dataset 


fake['model'] = 0
real['model'] = 1 # labeling the data 0 for fake and 1 for real


fake.head()
real.head() #gives the first 5 rows of the dataset

