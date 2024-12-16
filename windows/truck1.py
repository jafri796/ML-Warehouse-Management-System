# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 21:03:17 2023

@author: Roshaan Abbas Jaffery
"""

# import pyomo.environ as pe

from mayavi import mlab
import sys
import random
import itertools
import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
  # Replace 'tr_TR.utf8' with the appropriate Turkish locale identifier for your system
sys.stdout.reconfigure(encoding='utf-8')
input_path = sys.argv[1]
sheet1_entry = sys.argv[2]
v_int = int(sys.argv[3])
w_int = int(sys.argv[4])
truck_int  = []
for i in range(3):
    truck_int.append(int(sys.argv[i+5]))

# # read the Excel file and storing data for
# v_item here
df = pd.read_excel(input_path, sheet_name=sheet1_entry, header = 1)
# df = pd.read_excel(r"/Users/roshaanabbasjaffery/Downloads/code/1212 (1).xlsx", sheet_name= 'Sayfa1', header  = 1)
df = df.iloc[:,:17]
df = df.dropna()
# print(df)


df=df[['Palet Brüt Ağr','Palet Boy','Palet En','Palet Yükseklik','Film Eni (mm)']]
df = df.apply(pd.to_numeric, errors='coerce').dropna()
np_truck = df.to_numpy()
np_truck[:,3] = 125
np_truck
v_item = np.zeros((np_truck.shape[0]))
w = np.zeros((np_truck.shape[0]))
s_ird = np.zeros((np_truck.shape[0],2,3))
lbl = []


for i in range(np_truck.shape[0]):
  lbl.append(np_truck[i,4])
  v_item[i] = (np_truck[i,1]*np_truck[i,2]*np_truck[i,3]/10**3)
  w[i] = np_truck[i,0]
  for j in range(2):
    for k in range(3):
      if j ==0:
        s_ird[i,j,0] = np_truck[i,1]
        s_ird[i,j,1] = np_truck[i,2]
        s_ird[i,j,2] = np_truck[i,3]
      else:
        s_ird[i,j,0] = np_truck[i,2]
        s_ird[i,j,1] = np_truck[i,1]
        s_ird[i,j,2] = np_truck[i,3]
        
v_item = np.array(v_item).astype(int)
w = np.array(w).astype(int)
s_ird = np.array(s_ird).astype(int).reshape(w.shape[0],2,3)

# v_truck = 84864
# s_truck = [240, 1360, 260]
# w_lim = 18000 
# # w_int  = w_lim



v_truck = v_int
s_truck = truck_int
w_lim = w_int  



if np.sum(w) > w_lim:
    
    print("Ağırlık Limiti aşıldı.")
    print()
    
    weight_excess = np.sum(w) - w_lim
    
    
            
    print(f" {weight_excess} kg ağırlığında ürünü dosyadan kaldırın ve tekrar deneyin")
    print()
else: 
    model = cp_model.CpModel()
    
    I = range(0, w.shape[0])  #indexing through 10 items ??????it should be 54 tho
    
    R = range(0,2) #indexing through two rotations
    
    D = range(0, 3) #indexing through three dimensions 
    
    # not sure about this one -ö
    
    
     
    #zeynep fixing bugs
    # v_item = [int(v) for v in v_item]
    
    
    
    #what do we do about this -ö
    #we delete this -z
    ## for epoch in range()
    #solver = pywraplp.Solver.CreateSolver('SCIP')
    
    x = {}
    rot = {}
    y_plus = {}
    y_minus = {}
    up = {}
    um = {}
    u = {}
    A = {}
    B = {}
    c = {}
    
    
    
    #  x[(i, j)] = model.NewBoolVar('x[{}][{}]')
    
    for i in I:
        x[(i)] = model.NewBoolVar('x[{}]'.format(i))
        A[(i)] = model.NewBoolVar( 'A[{}]'.format(i))
        B[(i)] = model.NewBoolVar( 'B[{}]'.format(i))
        for j in I:
            for d in D:
                if i < j:
                    y_plus[(i,j,d)] = model.NewBoolVar('y_plus[{}][{}][{}]' .format(i, j, d))
                    y_minus[(i,j,d)] = model.NewBoolVar('y_minus[{}][{}][{}]' .format(i, j, d))
                    
    for i in I:
        for r in R:
            rot[(i,r)] = model.NewBoolVar('rot[{}][{}]' .format(i, r))
    
    for i in I:
        for d in D:
            c[(i, d)] = model.NewIntVar(0, 10**9, 'c[{}][{}]' .format(i, d))
            
    for i in I:
        for j in I:   
            if i < j:
                up[(i,j)] = model.NewBoolVar( 'up[{}][{}]'.format(i, j))
                um[(i,j)] = model.NewBoolVar( 'um[{}][{}]'.format(i, j))
                u[(i,j)] = model.NewBoolVar( 'u[{}][{}]' .format(i, j))
    #Constraints
    
    # Constraint 1
    for i in I:
        model.Add(sum(v_item[i] * x[i] for i in I) <= v_truck)
    
    # Constraint 2
    for i in I:
        for d in D:
            model.Add(c[i, d] <= x[i] * s_truck[d])
    
    #Constraint 3
    for i in I:
        model.Add(sum(rot[i, r] for r in R) == x[i])
    
    # Constraint 4
    for i in I:
        for d in D:
           model.Add(c[i, d] + sum(rot[i, r] * s_ird[i, r, d] for r in R) <= s_truck[d])
    
    # Constraint 5
    for i in I:
        for j in I:
            if i < j:
                for d in D:
                    model.Add(c[i, d] + sum(s_ird[i, r, d] * rot[i, r] for r in R) - s_truck[d] * (1 - y_plus[i, j, d]) <= c[j, d])
    
    # Constraint 6
    for i in I:
        for j in I:
            if i < j:
                for d in D:
                    model.Add(c[j, d] + sum(s_ird[j, r, d] * rot[j, r] for r in R) - s_truck[d] * (1 - y_minus[i, j, d]) <= c[i, d])
    
    # Constraint 7
    for i in I:
        for j in I:
            if i < j:
                for d in D:
                    lhs7 = x[i] + x[j] - 1
                    rhs7 = sum(y_plus[i, j, d] + y_minus[i, j, d] for d in D)
                    model.Add(lhs7 <= rhs7)
    
    # Constraint 8
    for i in I:
        for j in I:
            for d in D:
                if i < j:
           
                    model.Add(y_plus[i, j, d] <= x[j])
    
    # Constraint 9
    for i in I:
        for j in I:
            for d in D:
                if i < j:
                
                    model.Add(y_minus[i, j, d] <= x[i])
    
    # Constraint 10
    model.Add(sum(x[i]*w[i] for i in I)<= w_lim)
    
    # Constraint 11
    for i in I:
        for j in I:
            if i < j:
                lhs11 = up[i, j]
                rhs11 = y_plus[i, j, 2] + (1 - y_minus[i, j, 2]) + (1 - y_minus[i, j, 1]) + (1 - y_minus[i, j, 0]) + (1 - y_plus[i, j, 0]) + (1 - y_plus[i, j, 1]) - 5
                model.Add(lhs11 >= rhs11)
    
    # Constraint 12
    for i in I:
        for j in I:
            if i < j:
                lhs12 = up[i, j]
                rhs12 = y_plus[i, j, 2]
                model.Add(lhs12 <= rhs12)
    #13
    for i in I:
        for j in I:
            if i<j:
                lhs13 = up[i, j]
                rhs13 = 1 - y_minus[i, j, 2]
                model.Add(lhs13 <= rhs13)
    
    #14
    for i in I:
        for j in I:
            if i<j:
                lhs14 = up[i, j]
                rhs14 = 1 - y_minus[i, j, 1]
                model.Add(lhs14 <= rhs14)
    # Constraint 15: x -
    for i in I:
        for j in I:
            if i<j:
                lhs15 = up[i, j]
                rhs15 = 1 - y_minus[i, j, 0]
                model.Add(lhs15 <= rhs15)
    
    # Constraint 16: x +
    for i in I:
        for j in I:
            if i<j:
                lhs16 = up[i, j]
                rhs16 = 1 - y_plus[i, j, 0]
                model.Add(lhs16 <= rhs16)
    
    # Constraint 17: y +
    for i in I:
        for j in I:
            if i<j:
                lhs17 = up[i, j]
                rhs17 = 1 - y_plus[i, j, 1]
                model.Add(lhs17 <= rhs17)
    
    # Constraint 18:
    for i in I:
        for j in I:
            if i<j:
                lhs18 = um[i, j]
                rhs18 = y_minus[i, j, 2] + (1 - y_plus[i, j, 2]) + (1 - y_minus[i, j, 1]) + (1 - y_minus[i, j, 0]) + (1 - y_plus[i, j, 0]) + (1 - y_plus[i, j, 1]) - 5
                model.Add(lhs18 >= rhs18)
    
    # Constraint 19:
    for i in I:
        for j in I:
            if i<j:
                lhs19 = um[i, j]
                rhs19 = y_minus[i, j, 2]
                model.Add(lhs19 <= rhs19)
    
    # Constraint 20:
    for i in I:
        for j in I:
            if i<j:
                lhs20 = um[i, j]
                rhs20 = 1 - y_plus[i, j, 2]
                model.Add(lhs20 <= rhs20)
    
    # Constraint 21:
    for i in I:
        for j in I:
            if i<j:
                lhs21 = um[i, j]
                rhs21 = 1 - y_minus[i, j, 1]
                model.Add(lhs21 <= rhs21)
    
    # Constraint 22:
    for i in I:
        for j in I:
            if i<j:
                lhs22 = um[i, j]
                rhs22 = 1 - y_minus[i, j, 0]
                model.Add(lhs22 <= rhs22)
    #23
    for i in I:
        for j in I:
            if i < j:
                model.Add(um[i, j] <= 1 - y_plus[i, j, 0])
    
    for i in I:
        for j in I:
            if i < j:
                model.Add(um[i, j] <= 1 - y_plus[i, j, 1])
    
    for i in I:
        for j in I:
            if i < j:
                model.Add(u[i, j] == um[i, j] + up[i, j])
                # model.Add(u[i,j]<=um[i,j])
                # model.Add(u[i,j]<=up[i,j])
    
    
    # ups i did it again
    for i in I:
        for j in I:
            if i < j:
                model.Add(c[i, 0]+20 >= c[j, 0] - s_truck[0] * (1 - u[i, j]))
    
    # for i in I:
    #     for j in I:
    #         if i < j:
    #             model.Add(c[i, 1]+20 >= c[j, 0] - s_truck[1] * (1 - u[i, j]))
    
    # for i in I:
    #     for j in I:
    #         if i < j:
    #             lhs26 = c[i, 0] + sum(rot[i, r] * s_ird[i, r, 0] for r in R)+20
    #             rhs26 = c[j, 0] + sum(rot[j, r] * s_ird[j, r, 0] for r in R) + s_truck[0] * (1 - u[i, j])
    #             model.Add(lhs26 <= rhs26)
    
    # for i in I:
    #     for j in I:
    #         if i < j:
    #             lhs27 = c[i, 0] + sum(rot[i, r] * s_ird[i, r, 0] for r in R) -20
    #             rhs27 = c[j, 0] + sum(rot[j, r] * s_ird[j, r, 0] for r in R) + s_truck[0] * (1 - u[i, j])
    #             model.Add(lhs27 <= rhs27)
    
    for i in I:
        for j in I:
            if i < j:
                lhs27 = c[i, 1] + sum(rot[i, r] * s_ird[i, r, 1] for r in R) -20
                rhs27 = c[j, 1] + sum(rot[j, r] * s_ird[j, r, 1] for r in R) + s_truck[1] * (1 - u[i, j])
                model.Add(lhs27 <= rhs27)
    
    for i in I:
        for j in I:
            if i < j:
                lh1 = rot[i, 0] - rot[j, 0]
                lh2 = rot[j, 0] - rot[i, 0]
                lh3 = rot[i, 1] - rot[j, 1]
                lh4 = rot[j, 1] - rot[i, 1]
                rh = 1 - u[i, j]
                model.Add(lh1 <= rh)
                model.Add(lh2 <= rh)
                model.Add(lh3 <= rh)
                model.Add(lh4 <= rh)
    
    for i in I:
        lhs29 = c[i, 1]
        rhs29 = 350 - s_truck[1] * A[i]
        model.Add(lhs29 >= rhs29)
    
    for i in I:
        model.Add(B[i] <= A[i])
    
    for i in I:
        model.Add(B[i] <= x[i])
    
    for i in I:
        model.Add(B[i] <= A[i] + x[i] - 1)
    
    lhs33 = sum(B[i] * w[i] for i in I)  
    rhs33 = 4500
    model.Add(lhs33 <= rhs33)
    
    #dunno what to do about these -ö
    #
    # obj = model.NewIntVar(0, 10**9, "Objective Function")
    # model.Add(obj == sum(v_item[i] * x[i] for i in I))
    model.Maximize(sum(v_item[i]*x[i] for i in I))  
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    #     # print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
    # else:
    #     print('No solution found.')
    # if status == cp_model.FEASIBLE:
    #     print('x =', [solver.Value(x[i]) for i in I])
    #     print('Objective function value =', solver.Value(obj))
    # else:
    #     print('No solution found.')
    
    
    
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
      
        # print(f"c[{i+1},{1}] = {solver.Value(c[i,0])} \t c[{i+1},{2}] = {solver.Value(c[i,1])} \t c[{i+1},{3}] = {solver.Value(c[i,2])}")
        print("Ürünleri sırasıyla sol köşeden yerleştirmeye başlayın:")
        print()
        # print('Objective function value =', solver.Value(obj))
    else:
        print('No solution found.')
        
    
    
    x_val = []
    y_val = []
    z_val = []
    sizes_x = []
    sizes_y = []
    sizes_z = []
    
    for i in I:
        if solver.Value(x[i]) != 0:
            x_val.append(solver.Value(c[i, 0]))
            y_val.append(solver.Value(c[i, 1]))
            z_val.append(solver.Value(c[i, 2]))
            for r in R:
                if solver.Value(rot[i, r]):
                    sizes_x.append(s_ird[i, r, 0])
                    sizes_y.append(s_ird[i, r, 1])
                    sizes_z.append(s_ird[i, r, 2])
    x, y, z = [], [], []
    for i in range(len(x_val)):
        xi = np.linspace(x_val[i], x_val[i]+sizes_x[i]/1.1)
        yi = np.linspace(y_val[i], y_val[i]+sizes_y[i]/1.1)
        zi = np.linspace(z_val[i], z_val[i]+sizes_z[i]/1.1)
        xi, yi, zi = np.meshgrid(xi, yi, zi, indexing='ij')
        x.append(xi.ravel())
        y.append(yi.ravel())
        z.append(zi.ravel())
    fig, ax = plt.subplots(figsize=(8, 6))
    # ax.axis('off')
    # Scatter plot with markers and labels
    ax.scatter(y_val, x_val)
    ax.set_xlim(-100,s_truck[1])
    ax.set_ylim(-20,s_truck[0])
    for i, label in enumerate(x_val):
        if z_val[i] > 125:
            ax.text(y_val[i], x_val[i]+20, lbl[i], fontsize=10, color='blue',
                    ha='center', va='center')
        else:
            ax.text(y_val[i], x_val[i]+10, lbl[i], fontsize=10, color='red',
                    ha='center', va='center')
            
    red_patch = mpatches.Patch(color='red', label='Üst')
    blue_patch = mpatches.Patch(color='blue', label='Alt')
    ax.legend(handles=[red_patch, blue_patch], loc='upper right')
    # Set labels for the axes
    ax.set_xlabel('Y-axis')
    ax.set_ylabel('X-axis')
    # plt.show()
    fig.savefig('plot.png')
    
    
    colors = list(itertools.product([i / 10 for i in range(11)], repeat=3))
    
    random.shuffle(colors)
    fig = mlab.figure(size=(800, 600))
     
    
    # create boxes using points3d
    for i in range(len(x_val)):
        
        max_size = max(sizes_x + sizes_y + sizes_z)
        
        mlab.points3d(x[i], y[i], z[i], mode='cube', scale_factor= 2, color = colors[i])
        text_list_below = []
        text_list_above = []
    # with open('Results.txt', 'w') as f:
        
        for i in range(len(x_val)):
            max_size = max(sizes_x + sizes_y + sizes_z)
            if z_val[i]>=125:
                text_x = x_val[i]+3*max_size
                text_y = y_val[i]+0.5*(max_size)
                text_z = z_val[i] +0.5*max_size
                text = f' {lbl[i]} \n' 
                text_p = lbl[i]
                text_list_above.append((text_p, text_x, text_y, text_z))
            else:
                text_x = -1*(x_val[i]+1.25*max_size)
                text_y = y_val[i]+0.5*(max_size)
                text_z = z_val[i]
                text = f' {lbl[i]} \n'
                text_p = lbl[i]
                text_list_below.append((text_p, text_x, text_y, text_z))
            mlab.text3d(text_x, text_y, text_z, str(text), scale=(20,20, 20), color=(0, 0, 1))
    sorted_text_list_below = sorted(text_list_below, key=lambda x: (x[1], x[2], x[3]))       
    sorted_text_list_above = sorted(text_list_above, key=lambda x: (x[1], x[2], x[3]))       
            
    text_sequence_below = '------'.join(map(lambda x: str(x[0]), sorted_text_list_below))
    
    print("Aşağı:")
    print()
    print(text_sequence_below)
    print()
    # Create the text_sequence for above 125
    text_sequence_above = '------'.join(map(lambda x: str(x[0]), sorted_text_list_above))
    print("Üstte: ")
    print()
    print(text_sequence_above)
        
    fig.scene.disable_render = False # Super duper trick    
    
        # Add a text3d object for the number
    # show figure
    mlab.outline(extent=[0, s_truck[0], 0, s_truck[1], 0, s_truck[2]])
    mlab.outline.color = (1, 0, 0) 
    # Add a grid to the plot
    # mlab.view(distance='auto')
    # mlab.savefig('truck_plot.png')  # Specify the desired file name and extension
    mlab.show()
    # Close the Mayavi figure
    # mlab.close()
