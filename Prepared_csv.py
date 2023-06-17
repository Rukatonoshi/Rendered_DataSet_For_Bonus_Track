import numpy as np
import pandas as pd

import os
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

# write rendered dataframe to csv file
data.to_csv(dir_path+'//rendered_dataset.csv')
