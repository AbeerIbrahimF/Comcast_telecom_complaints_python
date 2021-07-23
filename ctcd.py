import pandas as pd 
import matplotlib.pyplot as plt


#1-Import data into Python environment.
df = pd.read_csv('/Users/Abeer/Downloads/Comcast_telecom_complaints_data.csv')
df.head()

#Check for Null
df.isnull().sum()
df.info()


#2-Provide the trend chart for the number of complaints at monthly and daily granularity levels.

#Convert col Date_month_year data type to date 
df['Date_month_year'] = pd.to_datetime(df['Date_month_year'])
df['Month'] = df['Date_month_year'].dt.month
df['Day'] = df['Date_month_year'].dt.day_name()

#Monthly
Month = df.groupby([df['Month']]).agg({'count'}).sort_values(by='Month')
Month['Ticket #'].plot(kind='line')

#Daily
Day = df.groupby([df['Day']]).agg({'count'})
Day['Ticket #'].plot(kind='line')


#3-Provide a table with the frequency of complaint types.
complaints = pd.DataFrame({'index':range(df.shape[0])})
df['Customer Complaint'] = df['Customer Complaint'].str.lower()
complaints['Internet'] = df['Customer Complaint'].str.extract("(internet)")
complaints['Network'] = df['Customer Complaint'].str.extract("(network)")
complaints['bills'] = df['Customer Complaint'].str.extract("(billing)")
complaints['charges'] = df['Customer Complaint'].str.extract("(charges)")
complaints['email'] = df['Customer Complaint'].str.extract("(email)")
complaints['data_cap'] = df['Customer Complaint'].str.extract("(data capacity)")
complaints_freq= complaints.notnull().sum().sort_values(ascending=False)
print(complaints_freq)


#4-Create a new categorical variable with value as Open and Closed. 
df.loc[df.Status=='Solved','Status']='Closed'
df.loc[df.Status=='Pending','Status']='Open'
df['Status'].value_counts()

#5-Provide state wise status of complaints in a stacked bar chart.
comp_st=pd.crosstab(df.State,df.Status)
comp_st.plot(kind='bar',figsize=(15,10),stacked=True)

#6-Provide the percentage of complaints resolved till date, which were received through the Internet and customer care calls.
st = df.groupby(['Status']).size()
st_per = st/st.sum()*100
st_per

resolved_percent = df.groupby(['Received Via','Status']).size().unstack()
resolved_percent['resolved'] = resolved_percent['Closed']/resolved_percent['Closed'].sum()*100
resolved_percent


