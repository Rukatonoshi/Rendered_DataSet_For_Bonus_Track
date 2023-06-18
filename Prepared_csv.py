import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

dir_path = os.path.dirname(os.path.realpath(__file__))
file = dir_path + '//Dataset-Unicauca-Version2-87Atts.csv'

data = pd.read_csv(file)
print(f'Num of Rows: {data.shape[0]}\nNum of Columns: {data.shape[1]}')
#print(data.head())

# filtering the classes which have more than 10000 rows (occurrences)
freq_protocol = data['ProtocolName'].value_counts()
requiredProtocolName = []
for key, value in freq_protocol.items():
    if (value >= 10000):
        requiredProtocolName.append(key)

print(requiredProtocolName)

#forming dataset from the random 10000 data from the requiredProtocolName
listofDataFrames = []
for protocol in requiredProtocolName:
    listofDataFrames.append(pd.DataFrame(data[data['ProtocolName'] == protocol].sample(n = 10000)))

sampledData = pd.concat(listofDataFrames)
print(sampledData.shape)

# taking random rows and shuffling the dataframe
data = sampledData.sample(frac=1, random_state=1).reset_index()

# remove the rows that contains NULL values
data.dropna(inplace=True)
data.dropna(axis='columns')
data.reset_index(drop=True, inplace=True)

# remove columns which contains zeroes in the data
data = data.loc[:, (data != 0).any(axis=0)]
print(data.shape)

print(data['ProtocolName'])

# converting the protocol name (target column) to required format (int)
# using LabelEncoder function from sklearn.preprocession library
encoder = LabelEncoder().fit(data['ProtocolName'])
data['ProtocolName'] = encoder.transform(data['ProtocolName'])
values = encoder.inverse_transform(data['ProtocolName'])
target_column = data['ProtocolName']

# mapping the encoded value
encoded_target_column = {}
for i in range(len(data['ProtocolName'])):
    encoded_target_column[data['ProtocolName'][i]] = values[i]
print(encoded_target_column)

dataset = data.drop(['Flow.ID','Source.IP','Label', 'Timestamp','Destination.IP', 'Source.Port', 'Destination.Port', 'Protocol'], axis=1)
print(dataset.shape)

# write rendered dataframe to csv file
dataset.to_csv(dir_path+'//rendered_dataset.csv')
