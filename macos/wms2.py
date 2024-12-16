# -*- coding: utf-8 -*-
"""
Created on Wed May 31 01:03:53 2023

@author: Roshaan Abbas Jaffery
"""

import numpy as np 
import pandas as pd

import re,sys, os
import pyomo.environ as pe

from sklearn.preprocessing import OrdinalEncoder
import sqlite3
import warnings
import logging

logging.getLogger('pyomo.core').setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

script_dir = os.path.dirname(sys.argv[0])
database_folder = os.path.join(script_dir, 'databases')
db2_path = os.path.join(database_folder, 'db2.db')

input_pathh = sys.argv[1]
sheet1h_entry = sys.argv[2]
len_limit = int(sys.argv[3])
box_limit = int(sys.argv[4])
# len_limit = 290
# box_limit = 3




df_put = pd.read_excel(input_pathh , sheet_name=sheet1h_entry)
# df_put = pd.read_excel(r'/Users/roshaanabbasjaffery/Downloads/Test2.xlsx' , sheet_name='Sheet1')
 
df_put = df_put[["Palet Numarası","Müşteri","Palet\nBoy" ,'Nihai İstif Yükekliği\n(cm)','Palet\nEn',"Malzeme kısa metni", "Sevkiyat Tarihi"]].values

df_put = pd.DataFrame(df_put, columns=['Palet','Customer',"Length","Height","Width","Material","Out date"])


encoder = OrdinalEncoder()


df_put['Customer_Inc'] = df_put['Customer'] + '_' + df_put['Out date'].dt.strftime('%Y-%m-%d')

df_put['Customer'] = encoder.fit_transform(df_put[['Customer_Inc']])

conn = sqlite3.connect(db2_path)
query = 'SELECT * FROM Product'
column_names = ['Length', 'Width',"Height" ,'Product']
dfkeys = pd.read_sql_query(query, conn)
dfkeys.columns = column_names
conn.close()
prod_keys = dfkeys.set_index(['Length', 'Width','Height'])['Product'].to_dict()


def get_key(row):
    dimensions = (row['Length'], row['Width'],row["Height"])
    return prod_keys.get(dimensions, '')

df_put['Product'] = df_put.apply(get_key, axis=1)


matrix = {}
orderM = []
lk = []
hk = []
for _, row in df_put.iterrows():
    
    customer = row['Customer']
    product = row['Product']
    out_date = row['Out date'].strftime('%Y-%m-%d')
    orderM.append([row["Palet"], out_date])

    

    # Check if the customer is already in the matrix
    if customer not in matrix:
        matrix[customer] = {}
    
    # Check if the product is already in the matrix for the current customer
    if product not in matrix[customer]:
        matrix[customer][product] = 0
    
    # Increment the count for the current customer and product
    matrix[customer][product] += 1
product_types = df_put['Product'].unique()

# Create an empty dictionary to store the column indices for each product
product_indices = {}

# Assign column indices to each product type
for index, product in enumerate(product_types):
    product_indices[product] = index

# Create a numpy array with shape (number of customers, 106) filled with zeros
AIX0 = np.zeros((len(matrix),241))

# Iterate over the customers and their products in the matrix dictionary
for customer_index, (customer, products) in enumerate(matrix.items()):
    for product, count in products.items():
        # Get the column index for the current product
        column_index = product_indices[product]
        
        # Assign the count to the corresponding cell in AIX0
        AIX0[customer_index, column_index] = count

# Convert the dataframe to a numpy array
orderM = np.array(orderM)


conn  = sqlite3.connect(db2_path)
query0 = "SELECT * FROM Distance"
Dist = np.array(pd.read_sql_query(query0, conn)).reshape(11700,1)
query1 = "SELECT * FROM Turnover"
Tk = np.array(pd.read_sql_query(query1, conn)).flatten()

cursor = conn.cursor()
cursor.execute("SELECT * FROM WSC")
rows = cursor.fetchall()
wsc = np.array(rows)


query2 = "SELECT Length, Height FROM Dims"

df = pd.read_sql_query(query2, conn)

lk = df['Length'].tolist()
hk = df['Height'].tolist()

conn.close()

p = np.sum(AIX0,axis = 0).astype(int)
Aix = np.random.randint(2, size=(Dist.shape[0],wsc.shape[1]))
Aix[Aix ==0] = 1
AIX = np.matmul(Aix, wsc)
AIX = (AIX*Tk)/Dist

AIX1 = np.array(AIX).reshape(Dist.shape[0],wsc.shape[1])


conn = sqlite3.connect(db2_path)
query = "SELECT * FROM Locations"
locs_df = pd.read_sql_query(query,conn)
locs = set(locs_df['Position'])
# print(len(locs))
conn.close()
loc = []
for i in range(Dist.shape[0]):
    loc.append(i)
def convert_indices_to_coords(idx_list, dim0, dim1, dim2, dim3):
    coords_list = []
    for idx in idx_list:
        l = (idx // (dim0 * dim1 * dim2)) + 1
        k = ((idx // (dim0 * dim1)) % dim2) + 1
        j = ((idx // dim0) % dim1) + 1
        i = (idx % dim0) + 1
        coords_list.append((i, j, k, l))
    
    return coords_list

dim0, dim1, dim2, dim3 = 2,45, 13, 10
coords_list = convert_indices_to_coords(loc, dim0, dim1, dim2, dim3)

f_s = set()
l_s = set()
for i in range(0, Dist.shape[0], Dist.shape[0]//10):
    for j in range(i, i+90):
        if j < Dist.shape[0] and j in locs:
            f_s.add(j)

    for j in range(i+1008, i+1170):
        if j < Dist.shape[0] and j in locs:
            l_s.add(j)



alloc_out = []
optp = [] 

K = range(0,wsc.shape[1])
R = pe.Set(initialize = sorted(locs))

model = pe.ConcreteModel()




model.x = pe.Var(R, K, within = pe.Binary)

model.c1 = pe.ConstraintList()
for k in K:
    lhs1 = sum(model.x[r, k] for r in R)
    rhs1 = p[k]
    model.c1.add(lhs1 == rhs1)

model.c2 = pe.ConstraintList()
for r in R:
    lhs2 = sum(model.x[r, k] for k in K)
    rhs2 = box_limit
    model.c2.add(lhs2 <= rhs2)

model.c3 = pe.ConstraintList()
for r in R:
    lhs3 = sum((model.x[r, k]*lk[k]) for k in K)  
    rhs3 = len_limit
    model.c3.add(lhs3 <= rhs3)

model.c4 = pe.ConstraintList()
for k in K:
    if hk[k] < 145:
        lhs4 = sum(model.x[r, k] for r in f_s if r in R)
        rhs4 = p[k]
        model.c4.add(lhs4 == rhs4)

model.c6 = pe.ConstraintList()
for k in K:
    if hk[k] > 210:
        lhs6 = sum(model.x[r, k] for r in l_s if r in R)
        rhs6 = p[k]
        model.c6.add(lhs6 == rhs6)

model.c7 = pe.ConstraintList()
for k in K:
    if lk[k] > 145:
        lhs7 = sum(model.x[r,k] for r in range(9360,11700) if r in R)
        rhs7 = p[k]
        model.c7.add(lhs7==rhs7) 

model.obj = pe.Objective(
    expr=pe.summation(AIX1, model.x),
    sense=pe.maximize)

solver = pe.SolverFactory('cbc', executable = '/usr/local/bin/cbc')
results  = solver.solve(model)




r_counts = {}
for r in R:
    for k in K: 
        if model.x[r,k].value > 0:
            
            line = f"x[{r},{k}] = {model.x[r,k].value}"
            alloc_out.append(line)
            
            line2 = f"Ürün {k+1} {coords_list[r][3]}. Sıra {coords_list[r][1]}. Sutün {coords_list[r][2]}. Raf seviyesi {coords_list[r][0]}. Derinlik’e yerleştirilmelidir"
            print(line2)
            optp.append(line2)

            if r in r_counts:
                r_counts[r] += 1
            else:
                r_counts[r] = 1
for r in R:
    if r_counts.get(r, 0) >= 2:
        locs.remove(r)                

# end_time = time.time()
# runtime = end_time - start_time
# print(runtime)    
for i in range(len(optp)):
    replace = str(orderM[i][0])
# Find the index of the word 'price' in the string
    num = re.search(r'\d+', optp[i])

# Check if a number was found
    if num:
    # Replace the number with the replacement value
        optp[i] = optp[i].replace(num.group(), replace, 1)
        print(optp[i])
data_list = optp
pkey  = []
# Insert data into the table
for data_str in data_list:
    # Extract the number after "Product"
    product_number = int(data_str.split('Ürün ')[1].split(' ')[0])
    pkey.append(product_number)

alloc_out = [str(x) for x in alloc_out]
pos = []
x_vals = np.zeros((11700,241))
for item in alloc_out:
    row, col, value = map(float, item.split('[')[1].split(']')[0].split(',') + [item.split('=')[1]])
    x_vals[int(row)][int(col)] = value
    if value:
        pos.append(int(row))
data_list = optp
product_number  = []
allocs_str = []

for data_str in data_list:
    product_number.append(int(data_str.split('Ürün ')[1].split(' ')[0]))
    allocs_str.append(data_str)

orderM = pd.DataFrame(orderM, columns=["ID",'Out'])
# orderM[''] = orderM['id'].astype(int)

conn = sqlite3.connect(db2_path)
df_locs = pd.DataFrame(locs,columns = ["Position"])
df_locs.to_sql("Locations", conn,if_exists='replace',index = False)

cols ,res = ['ID','Allocation','Position'],[product_number, allocs_str, pos]

data = {col: val for col, val in zip(cols, res)}
res = pd.DataFrame(data)


df_pick = pd.concat([orderM, res], axis=1)
df_pick = df_pick.loc[:, ~df_pick.columns.duplicated()].dropna()

df_pick.to_sql("Product_placed", conn, if_exists='append',index = False)
conn.close()
