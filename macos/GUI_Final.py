# -*- coding: utf-8 -*-
"""
@author: Roshaan Abbas Jaffery
"""
import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkmacosx import Button
import platform
import subprocess
import pandas as pd
import datetime
import os
import sys
from tkinter import ttk
import webbrowser
from tkinter import scrolledtext






script_dir = os.path.dirname(sys.argv[0])
database_folder = os.path.join(script_dir, 'databases')

db1_path = os.path.join(database_folder, 'db1.db')
# db1_path = "databases/db1.db"

db2_path = os.path.join(database_folder, 'db2.db')
# db2_path = "databases/db2.db"

figures_folder = os.path.join(script_dir, 'Figures')

Main_Page = os.path.join(figures_folder, 'Main_page.png')
WMS_Menu = os.path.join(figures_folder, 'WMS_Menu.png')
WMS_submenu = os.path.join(figures_folder, 'WMS_submenu.png')
truck_menu = os.path.join(figures_folder, 'truck_menu.png')
truck_output = os.path.join(figures_folder, 'truck_output.png')



truck1_path = os.path.join(script_dir,  'truck1.py')
truck2_path = os.path.join(script_dir,  'truck2.py')
wms1_path = os.path.join(script_dir,  'wms1.py')
wms2_path = os.path.join(script_dir, 'wms2.py')







class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("1000x700")
        self.master = master
        self.pack_propagate(0)
        self.input_pathm = None
        self.sheet_b_entry = 3
        self.sheet_l_entry = 290
        self.input_pathh= None
        self.input_patht = None
        self.image = None
        self.check_var = True
        self.create_main_menu()
        
   
       
    
       
    def create_main_menu(self):
        self.master.title("Main Menu")
        self.pack(fill=tk.BOTH, expand=1)
        
        bg_image = tk.PhotoImage(file=Main_Page)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.pack(padx = 0, pady = 0, expand= True)
        
        if (platform.system() == 'Darwin'):    
            wms_button = Button(self, text="AS/RS Depo Yönetim Sistemi", bg= '#AE2D39', command=self.create_wms_menu,
                               font= ("inter",26), fg = 'white', borderwidth = 3, relief = "flat")
            wms_button.place(relx=0.5, rely=0.60, anchor=tk.CENTER, relwidth = 0.38)
            truck_button = Button(self, text="Araç Yükleme Optimizasyonu", command=self.create_truck_menu,
                                     font= ("inter",26),bg = '#AE2D39', fg = 'white', borderwidth = 3, relief = 'flat')
            truck_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
            manual_button = Button(self, text="Kullanıcı Kılavuzu", command=self.open_pdf,
                                     font= ("inter",26),bg = '#AE2D39', fg = 'white', borderwidth = 3, relief = 'flat')
            manual_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER, relwidth = 0.38)
        else:
            wms_button = Button(self, text="AS/RS Depo Yönetim Sistemi", bg= '#AE2D39', command=self.create_wms_menu,
                               font= ("inter",20), fg = 'white', borderwidth = 3, relief = "flat")
            wms_button.place(relx=0.5, rely=0.60, anchor=tk.CENTER, relwidth = 0.38)
            
            truck_button = Button(self, text="Araç Yükleme Optimizasyonu", command=self.create_truck_menu,
                                     font= ("inter",20),bg = '#AE2D39', fg = 'white', borderwidth = 3, relief = tk.FLAT)
            truck_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER, relwidth = 0.38)
            
        
            manual_button = Button(self, text="Kullanıcı Kılavuzu", command=self.open_pdf,
                                     font= ("inter",20),bg = '#AE2D39', fg = 'white', borderwidth = 3, relief = tk.FLAT)
            manual_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER, relwidth = 0.38)
            
        
        wms_button.lift()
    
        
        truck_button.lift()
        
        
        manual_button.lift()
        

    def select_input_file_mamul(self):
        # Define file types for file dialog
        file_types = [('Excel Files', '*.xlsx'), ('CSV Files', '*.csv')]
        self.input_pathm = filedialog.askopenfilename(filetypes=file_types)
        
        # self.create_mamul_menu.tkraise()  # show the calling menu again
        # self.create_mamul_menu.focus_set()  # set the focus on the calling menu
        return self.input_pathm
        # Prompt user to select input file
            
    
    def select_input_file_hammade(self):
        # Define file types for file dialog
        file_types = [('Excel Files', '*.xlsx'), ('CSV Files', '*.csv')]
        
        # Prompt user to select input file
        self.input_pathh = filedialog.askopenfilename(filetypes=file_types)
        
        # self.create_hammade_menu.tkraise()  # show the calling menu again
        # self.create_hammade_menu.focus_set()  # set the focus on the calling menu
        return self.input_pathh
        
    
    def select_input_file_truck(self):
        # Define file types for file dialog
        file_types = [('Excel Files', '*.xlsx'), ('CSV Files', '*.csv')]
        
        # Prompt user to select input file
        self.input_patht = filedialog.askopenfilename(filetypes=file_types)
       
        # self.create_truck_menu.tkraise()  # show the calling menu again
        # self.create_truck_menu.focus_set()  # set the focus on the calling menu
        return self.input_patht
        
        
    
        
    def create_wms_menu(self):
        self.master.title("WMS Menu")
        self.clear_frame()
        
        bg_image = tk.PhotoImage(file=WMS_Menu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


    # Bind the resize_image function to the window resize event

        
        

        if (platform.system() == 'Darwin'):
            mamul_button = Button(self, text="Mamül- Yarı Mamül", command=self.create_mamul_menu,
                                     font= ("inter",26),fg = 'white',bg = '#AE2D39')
            mamul_button.place(relx = 0.05, rely = 0.45,relwidth = 0.3225)
            hammade_button = Button(self, text="Hammade - Ambalaj", command=self.create_hammade_menu,
                                       font= ("inter",26),fg = 'white',bg = '#AE2D39')
            hammade_button.place(relx = 0.05, rely = 0.53, relwidth= 0.3225)      
            layout_button = Button(self, text="Depo Yerleşimini Değiştir", command=self.create_layout_menu,
                                       font= ("inter",26),fg = 'white',bg = '#AE2D39')
            layout_button.place(relx = 0.05, rely = 0.61)      
            go_back_button = Button(self, text="Geri Dön", command=self.go_back,
                                       font= ("inter",20),fg = 'white',bg = '#AE2D39')
            go_back_button.place(relx = 0.47, rely = 0.92)    
        else:
            
            mamul_button = Button(self, text="Mamül- Yarı Mamül", command=self.create_mamul_menu,
                                     font= ("inter",20),fg = 'white',bg = '#AE2D39')
            mamul_button.place(relx = 0.05, rely = 0.45,relwidth = 0.37)
            
            hammade_button = Button(self, text="Hammade - Ambalaj", command=self.create_hammade_menu,
                                       font= ("inter",20),fg = 'white',bg = '#AE2D39')
            hammade_button.place(relx = 0.05, rely = 0.53, relwidth= 0.37)      
            
            layout_button = Button(self, text="Depo Yerleşimini Değiştir", command=self.create_layout_menu,
                                       font= ("inter",20),fg = 'white',bg = '#AE2D39')
            layout_button.place(relx = 0.05, rely = 0.61,relwidth = 0.37)      
            
            go_back_button = Button(self, text="Geri Dön", command=self.go_back,
                                       font= ("inter",16),fg = 'white',bg = '#AE2D39')
            go_back_button.place(relx = 0.45, rely = 0.92)    

        
        mamul_button.lift()
        
        
        hammade_button.lift()                       
        
        
        layout_button.lift()                       
        
        
        go_back_button.lift()
        
        
    def create_mamul_menu(self):
        self.master.title("Mamul Menu")
        self.clear_frame()
        
        bg_image = tk.PhotoImage(file= WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        main_label = tk.Label(self, text = "Yerleştirme Menüsü", font = ('inter', 32, 'bold'), bg = '#FAFAFA', fg = '#AE2D39')
        main_label.place(relx = 0.5, rely = 0.10, anchor = tk.CENTER)
        
        len_limit = str(self.sheet_l_entry)
        box_limit = str(self.sheet_b_entry)
        
        if (platform.system() == 'Darwin'):
            input_button = Button(self, text="Kullanılacak Dosya", command=self.select_input_file_mamul
                                     ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            input_button.place(relx = 0.5, rely = 0.2, anchor = tk.CENTER)

            allocate_button = Button(self, text="Yerleştir", command=lambda: self.run_mamul_script(sheet1m_entry, len_limit, box_limit)
                                        ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            allocate_button.place(relx = 0.5, rely =0.48, anchor = tk.CENTER, relwidth = 0.155)
            pickm_button = Button(self, text="Ürün Çıkar", command= self.create_pick_mamul_menu
                                        ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            pickm_button.place(relx = 0.5,rely = 0.54, anchor = tk.CENTER, relwidth = 0.155)
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_wms,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.6, anchor = tk.CENTER, relwidth = 0.155)
        else:
            input_button = Button(self, text="Kullanılacak Dosya", command=self.select_input_file_mamul
                                     ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            input_button.place(relx = 0.5, rely = 0.2, anchor = tk.CENTER, relwidth=0.2)
            
            allocate_button = Button(self, text="Yerleştir",
                                        command=lambda: self.run_mamul_script(sheet1m_entry,len_limit, box_limit)
                                        ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            allocate_button.place(relx = 0.5, rely =0.48, anchor = tk.CENTER, relwidth = 0.18)
            pickm_button = Button(self, text= "Ürün Çıkar", command= self.create_pick_mamul_menu
                                             ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            pickm_button.place(relx = 0.5,rely = 0.54, anchor = tk.CENTER, relwidth = 0.18)                             
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_wms
                                      ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.6, anchor = tk.CENTER, relwidth = 0.18)
            
            
                
        sheet1_label = tk.Label(self, text="Dosya Adı:", font= ("inter",16),fg = '#AE2D39',bg = '#FAFAFA')
        sheet1_label.place(relx = 0.5, rely = 0.28, anchor = tk.CENTER)
        
        sheet1m_entry = tk.Entry(self)
        sheet1m_entry.place(relx = 0.5, rely = 0.33, anchor = tk.CENTER)
        sheet1m_entry = sheet1m_entry
        
        
        
        
        
        
        
        
    
    def create_layout_menu(self):
        self.master.title("Layout Menu")
        self.clear_frame()
        bg_image = tk.PhotoImage(file= WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        main_label = tk.Label(self, text = "Depo Planı Ayarları", font = ('inter', 32, 'bold'), bg = '#FAFAFA', fg = '#AE2D39')
        main_label.place(relx = 0.5, rely = 0.10, anchor = tk.CENTER)
        
        sheet1_label = tk.Label(self, text="Hücre Uzunluğu:", font= ("inter",20,'bold'),fg = '#AE2D39',bg = '#FAFAFA')
        sheet1_label.place(relx = 0.38, rely = 0.25, anchor = tk.CENTER)
        sheet2_label = tk.Label(self, text="Hücre Limiti:",font= ("inter",20,'bold'),fg = '#AE2D39',bg = '#FAFAFA')
        sheet2_label.place(relx = 0.362, rely =0.35, anchor = tk.CENTER)
        
        sheet1_entry = tk.Entry(self)
        # sheet1_entry.insert(tk.END, sheet1_entry.default_value)
        sheet1_entry.place(relx = 0.60, rely = 0.255, anchor = tk.CENTER)
    
        

        sheet2_entry = tk.Entry(self)
        # sheet2_entry.insert(tk.END, sheet2_entry.default_value)
        sheet2_entry.place(relx = 0.6, rely =0.355, anchor = tk.CENTER)
        def update_default_values():
            # Retrieve the current values from the entry widgets
            current_value1 = sheet1_entry.get()
            current_value2 = sheet2_entry.get()
            
            # Update the default values of the entry widgets
            self.sheet_l_entry = current_value1
            self.sheet_b_entry = current_value2
            # print(sheet1_entry.default_value)

        def reset_to_default():
            self.sheet_l_entry = 290  
            self.sheet_b_entry = 3

            # Set the entry widget values to their default values
            sheet1_entry.delete(0, tk.END)
            sheet1_entry.insert(tk.END, self.sheet_l_entry)
            
            sheet2_entry.delete(0, tk.END)
            sheet2_entry.insert(tk.END, self.sheet_b_entry)
            # print(sheet1_entry.default_value)

        
        sheet1_entry.insert(tk.END, self.sheet_l_entry)
        sheet2_entry.insert(tk.END, self.sheet_b_entry)

        
        if (platform.system() == 'Darwin'):
            update_button = Button(self, text="Güncelle", command=update_default_values,font= ("inter",18),bg = '#AE2D39',fg = '#FAFAFA')
            update_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth = 0.155)


            reset_button = Button(self, text="Eski Haline Dön", command=reset_to_default,font= ("inter",18),bg = '#AE2D39',fg = '#FAFAFA')
            reset_button.place(relx=0.5, rely=0.56, anchor=tk.CENTER, relwidth = 0.155)
            
            go_back_button = Button(self, text="Geri dön", command=self.go_back_wms,font= ("inter",18),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx=0.5, rely=0.62, anchor=tk.CENTER, relwidth = 0.155)
            
        
        else:
            update_button = Button(self, text="Güncelle", command=update_default_values,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            update_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth = 0.18)


            reset_button = Button(self, text="Eski Haline Dön", command=reset_to_default,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            reset_button.place(relx=0.5, rely=0.56, anchor=tk.CENTER,relwidth = 0.18)
        
            go_back_button = Button(self, text="Geri dön", command=self.go_back_wms,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx=0.5, rely=0.62, anchor=tk.CENTER,relwidth = 0.18)
        

        
    def create_hammade_menu(self):
        self.master.title("Hammade Menu")
        self.clear_frame()
        bg_image = tk.PhotoImage(file=WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        main_label = tk.Label(self, text = "Yerleştirme Menüsü", font = ('inter', 32, 'bold'), bg = '#FAFAFA', fg = '#AE2D39')
        main_label.place(relx = 0.5, rely = 0.10, anchor = tk.CENTER)
        
        len_limit = str(self.sheet_l_entry)
        box_limit = str(self.sheet_b_entry)
        
        if (platform.system() == 'Darwin'):
            
            input_button = Button(self, text="Kullanılacak Dosya", command=self.select_input_file_hammade
                                     ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            input_button.place(relx = 0.5, rely = 0.2, anchor = tk.CENTER)
            allocate_button = Button(self, text="Yerleştir", command=lambda: self.run_hammade_script(sheet1h_entry, len_limit, box_limit)
                                        ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            allocate_button.place(relx = 0.5, rely =0.48, anchor = tk.CENTER, relwidth = 0.155)
            pickh_button = Button(self, text="Ürün Çıkar", command= self.create_pick_hammade_menu
                                        ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            
            pickh_button.place(relx = 0.5,rely = 0.54, anchor = tk.CENTER, relwidth = 0.155)
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_wms
                                           ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.6, anchor = tk.CENTER,relwidth = 0.155)
        else:
            
            input_button = Button(self, text="Kullanılacak Dosya", command=self.select_input_file_hammade
                                     ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            input_button.place(relx = 0.5, rely = 0.2, anchor = tk.CENTER, relwidth = 0.2)
            
            allocate_button = Button(self, text="Yerleştir", command=lambda: self.run_hammade_script(sheet1h_entry, len_limit, box_limit)
                                        ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            allocate_button.place(relx = 0.5, rely =0.48, anchor = tk.CENTER, relwidth = 0.18)
            
            pickh_button = Button(self, text="Ürün Çıkar", command= self.create_pick_hammade_menu
                                        ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            pickh_button.place(relx = 0.5,rely = 0.54, anchor = tk.CENTER, relwidth = 0.18)
            
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_wms
                                       ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.6, anchor = tk.CENTER,relwidth = 0.18)
            
        
        
        sheet1_label = tk.Label(self, text="Dosya Adı:", font= ("inter",16),fg = '#AE2D39',bg = '#FAFAFA')
        sheet1_label.place(relx = 0.5, rely = 0.28, anchor = tk.CENTER)
        
        sheet1h_entry = tk.Entry(self,  bg = "#FAFAFA")
        sheet1h_entry.place(relx = 0.5, rely = 0.33, anchor = tk.CENTER)
        sheet1h_entry = sheet1h_entry
        
        
        
        
        
       

    def  create_pick_mamul_menu(self):
        
        self.master.title("Pick Order Menu")
        self.clear_frame()
        bg_image = tk.PhotoImage(file= WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        
        
        conn = sqlite3.connect(db1_path)
        query = "SELECT ID , Out FROM Product_placed"
        pick_cust_m = pd.read_sql(query,conn)
        conn.close()
        

        
        pick_label = tk.Label(self, text  ="Ürün Çıkış Menüsü", font = ('inter',32, 'bold'),fg = '#AE2D39',bg = '#FAFAFA' )
        pick_label.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)
        style = ttk.Style()
        style.configure('Custom.Treeview', font=('inter', 16))
        treeview = ttk.Treeview(self, name='treeview',columns=['Palet ID','Sevkiyat Tarihi'],show='headings', style='Custom.Treeview')

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=treeview.yview)

        columns=['Palet ID','Sevkiyat Tarihi']

        treeview.configure(yscrollcommand=scrollbar.set)
        for col in columns:
            treeview.heading(col, text = col, anchor ='center')
            treeview.column(col,anchor = 'center')
        # for col in pick_cust_m.columns:
        #     # treeview.heading(col, text=col, anchor="center")
        #     treeview.column(col, anchor="center")
        
        for _, row in pick_cust_m.iterrows():
            treeview.insert("", "end", values=row.tolist())
            
        treeview.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=500, height = 300)
        
        ship_label = tk.Label(self, text = "Sevkiyat Tarihi Seç: ", font = ('inter',16),fg = '#AE2D39',bg = '#FAFAFA')
        ship_label.place(relx = 0.4, rely = 0.664, anchor = tk.CENTER)
        
        
        
        # cust_label = tk.Label(self, text = "Customer: ", font = ('inter',16),fg = '#AE2D39',bg = '#FAFAFA')
        # cust_label.place(relx = 0.4, rely = 0.75, anchor = tk.CENTER)
        
        # cust_entry = tk.Entry(self, )
        # cust_entry.place(relx = 0.5, rely =0.74)
        # cust_entry = cust_entry
        # Define a function to update the DataFrame when a button is clicked
        def update_dataframe(ship_entry):
            
            date = str(ship_entry.get())
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            
            conn =sqlite3.connect(db1_path)
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT Position FROM Product_placed WHERE Out = ?", (date,))
            positions = cursor.fetchall()
            cursor.execute("SELECT Allocation FROM Product_placed WHERE Out = ?",(date,))
            res_alloc = cursor.fetchall()
            res_alloc = [row[0] for row in res_alloc]  # Extract the first element of each row
            res_alloc = [item.replace("'", "") for item in res_alloc]

            cursor.execute("DELETE FROM Product_placed WHERE Out = ?", (date,))
            
            
            
            for position in positions:
                cursor.execute("INSERT INTO Locations (Position) VALUES (?)", (position[0],))

            conn.commit()
            
            query = "SELECT ID , Out FROM Product_placed"
            pick_cust_m = pd.read_sql(query,conn)

            conn.close()
            
            alloc_win  = tk.Toplevel(self)

            alloc_win.title("Positions")
            alloc_win.geometry("600x400")
            
            scrolled_text = scrolledtext.ScrolledText(alloc_win, font = ('inter', 12),fg = '#AE2D39',bg = '#ECEDEE')
            scrolled_text.place(relx=0.0, rely=0 ,relwidth=1,relheight=0.5)

            for row in res_alloc:
                scrolled_text.insert(tk.END, f"{row}\n")
                
            
            
            conn = sqlite3.connect(db1_path)
            query = "SELECT ID , Out FROM Product_placed"
            pick_cust_m = pd.read_sql(query,conn)
            conn.close()
            
            style.configure('Custom.Treeview', font=('inter', 16))
            old_treeview = self.nametowidget('treeview')
            old_treeview.destroy()
            new_treeview = ttk.Treeview(self, columns=['Palet ID','Sevkiyat Tarihi'],name  = 'treeview', show='headings', style='Custom.Treeview')
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=new_treeview.yview)
            columns=['Palet ID','Sevkiyat Tarihi']
            for col in columns:
                new_treeview.heading(col, text=col, anchor = 'center')
                new_treeview.column(col,anchor = 'center')
            
            for _, row in pick_cust_m.iterrows():
                new_treeview.insert("", "end", values=row.tolist())
        
            # remove the old treeview widget and add the new one
            
            new_treeview.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=500, height = 300)
            
            if (platform.system()) =="Darwin":
                scrollbar.place(relx=0.735, rely=0.221, height=275)
                close_button = Button(alloc_win, text="Çıkış", command=lambda: close_window(alloc_win)
                                         ,font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
                close_button.place(relx = 0.35, rely = 0.8, anchor = tk.CENTER, relwidth = 0.23)
                
                get_text_button = Button(alloc_win, text="Metne Aktar", command=lambda: get_text(res_alloc)
                                         ,font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
                get_text_button.place(relx = 0.60, rely = 0.8,anchor = tk.CENTER)
            else:
                scrollbar.place(relx=0.73, rely=0.221, height=275)
                close_button = Button(alloc_win, text="Çıkış", command=lambda: close_window(alloc_win)
                                         ,font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
                close_button.place(relx = 0.35, rely = 0.8, anchor = tk.CENTER, relwidth = 0.23)
                get_text_button = Button(alloc_win, text="Metne Aktar", command=lambda: get_text(res_alloc)
                                         ,font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
                get_text_button.place(relx = 0.60, rely = 0.8,anchor = tk.CENTER)
            
            

                    
        
        if (platform.system() == 'Darwin'):
            scrollbar.place(relx=0.735, rely=0.221, height=275)
            pick_button_m = Button(self, text='Ürün Çıkar', command=lambda: update_dataframe(ship_entry),
                                      font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
            pick_button_m.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER, relwidth=0.12)
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_mamul
                                        ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.86, anchor = tk.CENTER, relwidth=0.12)
        
        else:
            scrollbar.place(relx=0.73, rely=0.221, height=275)
            pick_button_m = Button(self, text='Ürün Çıkar', command=lambda: update_dataframe(ship_entry),
                                      font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
            pick_button_m.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER, relwidth=0.12)
            
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_mamul
                                        ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.86, anchor = tk.CENTER, relwidth=0.12)
            
        
       
        # ship_entry = DateEntry(self, width=12, background='#FAFAFA', foreground='#AE2D39', date_pattern='yyyy-mm-dd')
        ship_entry = tk.Entry(self)
        ship_entry.place(relx=0.5, rely=0.65)
        ship_entry.lift()
        
        def get_text(res_alloc):
           with open('Ürün_Çıkar.txt', 'w') as file:
               for item in res_alloc:
                   file.write(str(item) + '\n')

                
        def close_window(win):
            win.destroy()
        
    
    def  create_pick_hammade_menu(self):
        
        self.master.title("Pick Order Menu")
        self.clear_frame()
        bg_image = tk.PhotoImage(file= WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        
        conn = sqlite3.connect(db2_path)
        query = "SELECT ID , Out FROM Product_placed"
        pick_cust_m = pd.read_sql(query,conn)
        conn.close()
        

        
        pick_label = tk.Label(self, text  ="Ürün Çıkış Menüsü", font = ('inter',32, 'bold'),fg = '#AE2D39',bg = '#FAFAFA' )
        pick_label.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)
        style = ttk.Style()
        style.configure('Custom.Treeview', font=('inter', 16))
        treeview = ttk.Treeview(self, name='treeview',columns=['Palet ID','Sevkiyat Tarihi'],show='headings', style='Custom.Treeview')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=treeview.yview)

        columns=['Palet ID','Sevkiyat Tarihi']

        treeview.configure(yscrollcommand=scrollbar.set)
        for col in columns:
            treeview.heading(col, text = col, anchor ='center')
            treeview.column(col,anchor = 'center')
        # for col in pick_cust_m.columns:
        #     # treeview.heading(col, text=col, anchor="center")
        #     treeview.column(col, anchor="center")
        
        for _, row in pick_cust_m.iterrows():
            treeview.insert("", "end", values=row.tolist())
            
        treeview.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=500, height = 300)
        
        
        
        ship_label = tk.Label(self, text = "Sevkiyat Tarihi Seç: ", font = ('inter',16),fg = '#AE2D39',bg = '#FAFAFA')
        ship_label.place(relx = 0.4, rely = 0.664, anchor = tk.CENTER)
        # Define a function to update the DataFrame when a button is clicked
        def update_dataframe(ship_entry):
            
            date = str(ship_entry.get())
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            
            conn =sqlite3.connect(db2_path)
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT Position FROM Product_placed WHERE Out = ?", (date,))
            positions = cursor.fetchall()
            cursor.execute("SELECT Allocation FROM Product_placed WHERE Out = ?",(date,))
            res_alloc = cursor.fetchall()
            res_alloc = [row[0] for row in res_alloc]  # Extract the first element of each row
            res_alloc = [item.replace("'", "") for item in res_alloc]

            cursor.execute("DELETE FROM Product_placed WHERE Out = ?", (date,))
            
            
            
            for position in positions:
                cursor.execute("INSERT INTO Locations (Position) VALUES (?)", (position[0],))

            conn.commit()
            
            query = "SELECT ID , Out FROM Product_placed"
            pick_cust_m = pd.read_sql(query,conn)

            conn.close()
            
            alloc_win  = tk.Toplevel(self)

            alloc_win.title("Positions")
            alloc_win.geometry("600x400")
            
            scrolled_text = scrolledtext.ScrolledText(alloc_win, font = ('inter', 12),fg = '#AE2D39',bg = '#ECEDEE')
            scrolled_text.place(relx=0.0, rely=0 ,relwidth=1,relheight=0.5)

            for row in res_alloc:
                scrolled_text.insert(tk.END, f"{row}\n")
                
            
            
            conn = sqlite3.connect(db2_path)
            query = "SELECT ID , Out FROM Product_placed"
            pick_cust_m = pd.read_sql(query,conn)
            conn.close()
            
            style.configure('Custom.Treeview', font=('inter', 16))
            old_treeview = self.nametowidget('treeview')
            old_treeview.destroy()
            new_treeview = ttk.Treeview(self, columns=['Palet ID','Sevkiyat Tarihi'],name  = 'treeview', show='headings', style='Custom.Treeview')
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=new_treeview.yview)
            columns=['Palet ID','Sevkiyat Tarihi']
            for col in columns:
                new_treeview.heading(col, text=col, anchor = 'center')
                new_treeview.column(col,anchor = 'center')
            
            for _, row in pick_cust_m.iterrows():
                new_treeview.insert("", "end", values=row.tolist())
        
            # remove the old treeview widget and add the new one
            
            new_treeview.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=500, height = 300)
            
            
            if (platform.system()) =="Darwin":
                scrollbar.place(relx=0.735, rely=0.221, height=275)
                close_button = Button(alloc_win, text="Çıkış", command=lambda: close_window(alloc_win)
                                         ,font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
                close_button.place(relx = 0.35, rely = 0.8, anchor = tk.CENTER, relwidth = 0.23)
                
                get_text_button = Button(alloc_win, text="Metne Aktar", command=lambda: get_text(res_alloc)
                                         ,font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
                get_text_button.place(relx = 0.60, rely = 0.8,anchor = tk.CENTER)
            else:
                scrollbar.place(relx=0.73, rely=0.221, height=275)
                close_button = Button(alloc_win, text="Çıkış", command=lambda: close_window(alloc_win)
                                         ,font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
                close_button.place(relx = 0.35, rely = 0.8, anchor = tk.CENTER, relwidth = 0.23)
                
                get_text_button = Button(alloc_win, text="Metne Aktar", command=lambda: get_text(res_alloc)
                                         ,font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
                get_text_button.place(relx = 0.60, rely = 0.8,anchor = tk.CENTER)
    
           
            
                    
        
        if (platform.system() == 'Darwin'):
            scrollbar.place(relx=0.735, rely=0.221, height=275)
            
            pick_button_m = Button(self, text='Ürün Çıkar', command=lambda: update_dataframe(ship_entry),
                                      font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
            pick_button_m.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER, relwidth=0.12)
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_mamul
                                        ,font= ("inter",20),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.86, anchor = tk.CENTER, relwidth=0.12)
        
        else:
            scrollbar.place(relx=0.73, rely=0.221, height=275)
            pick_button_m = Button(self, text='Ürün Çıkar', command=lambda: update_dataframe(ship_entry),
                                      font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
            pick_button_m.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER, relwidth=0.155)
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_mamul
                                        ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            go_back_button.place(relx = 0.5, rely =0.86, anchor = tk.CENTER, relwidth=0.155)
            
       
        
        ship_entry = tk.Entry(self)
        # ship_entry = DateEntry(self, width=12, background='#FAFAFA', foreground='#AE2D39', date_pattern='yyyy-mm-dd')
        ship_entry.place(relx=0.5, rely=0.65)
        ship_entry.lift()
        
        def get_text(res_alloc):
           with open('Ürün_Çıkar.txt', 'w') as file:
               for item in res_alloc:
                   file.write(str(item) + '\n')

                
        def close_window(win):
            win.destroy()
        
    
    def create_truck_menu(self):
        self.master.title("Truck Menu")
        self.clear_frame()
        
        bg_image = tk.PhotoImage(file= truck_menu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        
        # label2 = tk.Label(self, text = "Truck Space Optimization", font = ('inter',45), fg = '#AE2D39', bg ='#D0E7F6')
        # label2.place(relx = 0.50, rely = 0.2, anchor = tk.CENTER)
        
        # input_label1 = tk.Label(self, text="Enter your Volume Limit:",font= ("inter",16),fg = '#AE2D39',bg = '#CBE7F7')
        # input_label1.place(relx = 0.40, rely =0.3, anchor = tk.CENTER)

        v_int = tk.Entry(self)
        v_int.place(relx = 0.60, rely =0.33, anchor = tk.CENTER)
        
        # input_label2 = tk.Label(self, text="Enter your Weight Limit:", font= ("inter",16),fg = '#AE2D39',bg="#CBE7F7")
        # input_label2.place(relx = 0.40, rely =0.4, anchor = tk.CENTER)

        w_int = tk.Entry(self)
        w_int.place(relx = 0.60, rely =0.42, anchor = tk.CENTER)
        
        # input_label3 = tk.Label(self, text="Enter your Truck Size (seperated by commas):",
        #                         font= ("inter",16),fg = '#AE2D39',bg = '#D3DBF2')
        # input_label3.place(relx = 0.40, rely =0.5, anchor = tk.CENTER)
        
        entry = tk.Entry(self)
        entry.place(relx = 0.60, rely =0.51, anchor = tk.CENTER)        
        
        
        # enter_button = `(self, text="Enter", command=self.run_truck_script)
        self.check_var = tk.BooleanVar()
        self.check_var.set(True)
        # enter_button.pack(pady=30)
        if (platform.system() == 'Darwin'):    
            input_button = Button(self, text="Kullanılacak Dosya", command=self.select_input_file_truck
                                     ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA')
            input_button.place(relx = 0.5, rely = 0.74, anchor = tk.CENTER, relwidth=0.20)
            
            allocate_button = Button(self, text="Yerleştirme Koordinatları", 
                                        command=lambda: self.run_truck_script(sheett_entry,v_int,w_int,entry)
                                        ,font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA' )
            allocate_button.place(relx = 0.50, rely =0.80, anchor = tk.CENTER, relwidth=0.20)
            go_back_button = Button(self, text="Geri Dön", command=self.go_back,
                                       font= ("inter",16),bg = '#AE2D39',fg = '#FAFAFA' )
            go_back_button.place(relx = 0.50, rely =0.86, anchor = tk.CENTER, relwidth=0.20)
            
        else:
            input_button = Button(self, text="Kullanılacak Dosya", command=self.select_input_file_truck
                                     ,font= ("inter",14),bg = '#AE2D39',fg = 'white')
            input_button.place(relx = 0.5, rely = 0.74, anchor = tk.CENTER, relwidth=0.25)
            
            allocate_button = Button(self, text="Yerleştirme Koordinatları", 
                                        command=lambda: self.run_truck_script(sheett_entry,v_int,w_int,entry)
                                        ,font= ("inter",14),bg = '#AE2D39',fg = '#FAFAFA' )
            allocate_button.place(relx = 0.50, rely =0.80, anchor = tk.CENTER, relwidth=0.25)
            
            go_back_button = Button(self, text="Geri Dön", command=self.go_back,
                                       font= ("inter",14),bg = '#AE2D39',fg = '#FAFAFA' )
            go_back_button.place(relx = 0.50, rely =0.86, anchor = tk.CENTER, relwidth=0.25)
        
        check_button = tk.Checkbutton(self, variable=self.check_var)
        check_button.place(relx = 0.55, rely = 0.59, anchor = tk.CENTER)

        
        # check_label = tk.Label(self, text = "Axle Constraints",font= ("inter",16),fg = '#AE2D39',
                               # bg = '#BCD3EB')
        # check_label.place(relx = 0.40, rely = 0.7, anchor = tk.CENTER)
        # sheett_label = tk.Label(self, text="Sheet 1 Name:", font= ("inter",16),fg = '#AE2D39',bg = '#BCD3EB')
        # sheett_label.place(relx = 0.40, rely =0.60, anchor = tk.CENTER)  
        sheett_entry = tk.Entry(self,)
        sheett_entry.place(relx = 0.60, rely =0.655, anchor = tk.CENTER)  
        
       
        
        
      
    
    
        
        
        
        
    
    def run_mamul_script(self,sheet1m_entry,sheet_l_entry, sheet_b_entry):
        sheet1_entry = str(sheet1m_entry.get())
        len_limit = str(self.sheet_l_entry)
        box_limit = str(self.sheet_b_entry)
        output = subprocess.check_output(['python',wms1_path,str(self.input_pathm),sheet1_entry,len_limit, box_limit])
        self.show_output_mamul(output)
        print(len_limit,box_limit)
    
    def run_hammade_script(self,sheet1h_entry,sheet_l_entry, sheet_b_entry):
        sheet1h_entry = str(sheet1h_entry.get())
        len_limit = str(self.sheet_l_entry)
        box_limit = str(self.sheet_b_entry)
        output = subprocess.check_output(['python',wms2_path ,str(self.input_pathh),sheet1h_entry,len_limit, box_limit])
        self.show_output_hammade(output)
        
        
    def run_truck_script(self,sheett_entry,v_int,w_int,entry):
        
        axle_const = (self.check_var.get())
        sheett_name = str(sheett_entry.get())
        v_int = int(v_int.get())
        w_int = int(w_int.get())
        truck_str = entry.get()
        truck_int = list(map(int, truck_str.split(",")))  # Split and convert to integers
        if axle_const == True:
            output = subprocess.check_output(['python',truck1_path, str(self.input_patht), sheett_name, str(v_int), str(w_int)] + [str(x) for x in truck_int])
        else:
            output = subprocess.check_output(['python',truck2_path, str(self.input_patht), sheett_name, str(v_int), str(w_int)] + [str(x) for x in truck_int]) 
        self.show_output_truck(output)
        # plt.savefig('truck_plot.png')

        # Create a Tkinter window to display the plot
        
        # Load the plot image into a Tkinter PhotoImage object
        plot_image = tk.PhotoImage(file='plot.png')
        def delete_photo():
            os.remove('plot.png')
            plot_window.destroy()
        if plot_image:
            plot_window = tk.Toplevel(self.master)
            plot_window.title("2D Plot")
        
            # Create a Tkinter label to display the plot image
            plot_label = tk.Label(plot_window, image=plot_image)
            plot_label.image = plot_image # Save a reference to prevent garbage collection
    
        # # Show the plot in the Tkinter window
            plot_label.pack(expand = True)
        plot_window.protocol("WM_DELETE_WINDOW", delete_photo)
        plot_window.mainloop()

        
    def show_output_mamul(self, output):
        self.master.title("Output")
        self.clear_frame()
        bg_image = tk.PhotoImage(file= WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        output = output.decode('utf-8')
        # output_text = tk.Text(self, width=100)
        # output_text.pack()
        out_label = tk.Label(self, text = "Ürün Yerleşimleri", font = ('inter',32),bg = "#FAFAFA", fg = '#AE2D39')
        out_label.place(relx = 0.5, rely = 0.10,anchor = tk.CENTER )
        
        output_label = scrolledtext.ScrolledText(self, font = ('inter', 12),fg = '#AE2D39',bg = '#FAFAFA')
        output_label.place(relx = 0.5, rely = 0.45, anchor = tk.CENTER,width = 498)
        output_label.insert(tk.END, output)
        if (platform.system() == 'Darwin'):    
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_mamul, 
                                    font = ('inter',20),bg = '#AE2D39',fg = '#FAFAFA' )
            get_text_button = Button(self, text="Metne Aktar", command=lambda: get_text(output)
                                     ,font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
        else:
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_mamul,
                                       font = ('inter',16),bg = '#AE2D39',fg = '#FAFAFA' )
            get_text_button = Button(self, text="Metne Aktar", command=lambda: get_text(output)
                                     ,font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
        go_back_button.place(relx = 0.5, rely = 0.85, anchor = tk.CENTER, relwidth  =0.15)
        
        get_text_button.place(relx = 0.5, rely=0.80, anchor = tk.CENTER, relwidth  =0.15)
        
        def get_text(res_alloc):
           with open('Ürün Yerleşimleri.txt', 'w') as file:
               file.write(output)
        
    def show_output_hammade(self, output):
        self.master.title("Output")
        self.clear_frame()
        bg_image = tk.PhotoImage(file= WMS_submenu)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        output = output.decode('utf-8')
        # output_text = tk.Text(self, width=100)
        # output_text.pack()
        out_label = tk.Label(self, text = "Ürün Yerleşimleri", font = ('inter',32),bg = "#FAFAFA", fg = '#AE2D39')
        out_label.place(relx = 0.5, rely = 0.10,anchor = tk.CENTER )
        output_label = scrolledtext.ScrolledText(self,  font = ('inter', 12),fg = '#AE2D39',bg = '#FAFAFA')
        output_label.place(relx = 0.5, rely = 0.45, anchor = tk.CENTER, width = 498)
        output_label.insert(tk.END, output)
        if (platform.system() == 'Darwin'):    
            
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_hammade, 
                                    font = ('inter',20),bg = '#AE2D39',fg = '#FAFAFA' )
            get_text_button = Button(self, text="Metne Aktar", command=lambda: get_text(output)
                                     ,font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
        else:
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_hammade, 
                                    font = ('inter',16),bg = '#AE2D39',fg = '#FAFAFA' )
            get_text_button = Button(self, text="Metne Aktar", command=lambda: get_text(output)
                                     ,font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
            
        go_back_button.place(relx = 0.5, rely = 0.85, anchor = tk.CENTER, relwidth  =0.15)
        get_text_button.place(relx = 0.5, rely=0.80, anchor = tk.CENTER, relwidth  =0.15)
        
        def get_text(res_alloc):
           with open('Ürün Yerleşimleri.txt', 'w') as file:
               file.write(output)

    def show_output_truck(self, output):
        self.master.title("Output")
        self.clear_frame()
        # output_text = tk.Text(self, width=100)
        # output_text.pack()
        bg_image = tk.PhotoImage(file= truck_output)
        self.image = bg_image
        bg_label = tk.Label(self, image=self.image)
        bg_label.place(x = 0,y = 0,relwidth=1, relheight=1)
        output = output.decode('utf-8')
        out_label = tk.Label(self, text = "Yerleştirme Koordinatları", font = ('inter',32),bg = "#CEDBE4", fg = '#AE2D39')
        out_label.place(relx = 0.5, rely = 0.2,anchor = tk.CENTER )
        output_label = scrolledtext.ScrolledText(self, font = ('inter', 12),fg = '#AE2D39',bg = '#CADAE4')
        output_label.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER, width = 498, height = 300)
        output_label.insert(tk.END, output)
        if (platform.system() == 'Darwin'):    
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_truck,
                                    font = ('inter', 20),bg = '#AE2D39',fg = '#FAFAFA')
        else:
            go_back_button = Button(self, text="Geri Dön", command=self.go_back_truck,
                                    font = ('inter', 16),bg = '#AE2D39',fg = '#FAFAFA')
        go_back_button.place(relx = 0.5, rely = 0.85, anchor = tk.CENTER)
    
        
    
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def go_back(self):
        self.clear_frame()
        self.create_main_menu()
        
    def go_back_wms(self):
        self.clear_frame()
        self.create_wms_menu()
        
    def go_back_truck(self):
        self.clear_frame()
        self.create_truck_menu()
        
    def go_back_mamul(self):
        self.clear_frame()
        self.create_mamul_menu()
        
    def go_back_hammade(self):
        self.clear_frame()
        self.create_hammade_menu()

    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Kapatmak istiyor musun?"):
            self.master.destroy()
            
    def open_pdf(event = None):
    # Specify the URL or path to the PDF file
        pdf_url = "https://drive.google.com/file/d/1lXgY2e5yhkC83Yy8KS_WJHHrpx2iMgPd/view?usp=sharing"
    
    # Open the PDF file in the default web browser
        webbrowser.open(pdf_url)

   
root = tk.Tk()
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
