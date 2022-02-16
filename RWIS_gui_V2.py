import tkinter as tk                
from tkinter import font  as tkfont 
from tkinter import *
from tkinter import filedialog, messagebox, ttk

from turtle import width


import pandas as pd
from pandas import MultiIndex
import numpy as np

import win32com.client as win32
import os
import fnmatch

import re


user_actual = os.getlogin()

global curr_data 
global prev_data




class StartPage(tk.Frame):
            
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="RWIS REPORTS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        

            
        
        def gather_today():
            global curr_data
            self.fname_current = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
            curr_data = self.fname_current
            textlabel_current =Label(self,text="Current data: "+self.fname_current).pack()            
            self.update()
            
            _rwis = open(curr_data)
            rwis = _rwis.read()
            _rwis.close()
            
            #find the date of file
            datetofind ='\d{2}/\d{2}/\d{4}'
            _dateoffile = re.search(datetofind, rwis)
            t_dateoffile = _dateoffile.group(0)
            
            #split data sections in file to 4 sections: date info, atmospheric, surface, and sub
            note, rwis_atmo, rwis_surf, rwis_sub = rwis.split('\n\n\n')
            
            #write these sections into 3 distinct files
            atmo_data = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Atmospheric_t_split.txt','w')
            atmo_data.writelines(rwis_atmo)
            atmo_data.close()
            surf_data = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Surface_t_split.txt','w')
            surf_data.writelines(rwis_surf)
            surf_data.close()
            sub_data = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Sub_t_split.txt','w')
            sub_data.writelines(rwis_sub)
            sub_data.close()  
            
            self.update()
            
            return curr_data, t_dateoffile
        

        def gather_yesterday():
            
            global prev_data
            self.fname_previous = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
            prev_data = self.fname_previous
            textlabel_previous =Label(self,text="Previous data: "+ self.fname_previous).pack()            
            self.update()
            
            _rwis = open(prev_data)
            rwis = _rwis.read()
            _rwis.close()
            
            #find the date of file
            datetofind ='\d{2}/\d{2}/\d{4}'
            _dateoffile = re.search(datetofind, rwis)
            y_dateoffile = _dateoffile.group(0)
            
            #split data sections in file to 4 sections: date info, atmospheric, surface, and sub
            note, rwis_atmo, rwis_surf, rwis_sub = rwis.split('\n\n\n')
            
            #write these sections into 3 distinct files
            atmo_data = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Atmospheric_y_split.txt','w')
            atmo_data.writelines(rwis_atmo)
            atmo_data.close()
            surf_data = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Surface_y_split.txt','w')
            surf_data.writelines(rwis_surf)
            surf_data.close()
            sub_data = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Sub_y_split.txt','w')
            sub_data.writelines(rwis_sub)
            sub_data.close()
            self.update()
            
            return prev_data, y_dateoffile
        
        
        
        
        
        
                        #################
                        ##   BUTTONS   ##
                        #################
        
        button_T = tk.Button(self, text="Select Today's Report",
                            command= gather_today)
        button_T.pack()

        button_T = tk.Button(self, text="Select Yesterday's Report",
                            command= gather_yesterday)
        button_T.pack()

        button1 = tk.Button(self, text="Run Atmospheric Diff",
                            command= lambda: self.controller.show_frame("Atmospheric_Report"))
        button1.pack()
        
        button2 = tk.Button(self,text="Run Surface Diff", command=lambda: controller.show_frame("Surface_Report"))
        button2.pack()



class Atmospheric_Report(tk.Frame):             
     

    #def refresh(self, Atmospheric_Report):
    #    tk.Frame.destroy(self)
    #    tk.Frame.__init__(self)
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent,width=600, height=800)
        
        self.update()
        
        
        self.controller = controller
            
        label = tk.Label(self, text="Atmospheric Report", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        

        t_atmo = ATMOSPHERIC_TODAY()
        y_atmo = ATMOSPHERIC_YESTERDAY()
        df = Atmospheric()

        #I want the able to be display the dataframe here
        Aview =  LabelFrame(self, text='Atmospheric', height=800, width=800) #frame for data
        Aview.pack( fill=BOTH, expand=True, pady=10)
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        
        tva = ttk.Treeview(Aview,style="mystyle.Treeview")
        tva.tag_configure('diff', background='#FFFF00')
        
        tva.place(relx=0,rely=0)
        treescrolly = tk.Scrollbar(Aview, orient="vertical", command=tva.yview)
        tva.configure(yscrollcommand=treescrolly.set)
        treescrolly.pack(side ="right",fill='y')
        
        tva["column"] = list(df.columns)
        tva['show'] = 'headings'
        for column in tva['column']:
            tva.heading(column, text=column)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            tva.insert('','end', values = row)
            
        
        def Print_Atmospheric_Report():
            messagebox.showinfo("Say Hello", "Hello World")
            print('Atmospheric Report')
            
            
        button_upat = tk.Button(self, text="Update", command= Print_Atmospheric_Report)
        button_upat.pack()
        
        


    
        


class Surface_Report(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Surface Report", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)        
        
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        t_surf = SURFACE_TODAY()
        y_surf = SURFACE_YESTERDAY()
        df = Surface()

        #I want the able to be display the dataframe here
        Sview =  LabelFrame(self, text='Surface', height=800, width=800) #frame for data
        Sview.pack( fill=BOTH, expand=True, pady=10)
        
        tvs = ttk.Treeview(Sview)
        
        tvs.place(relx=0,rely=0)
        treescrolly = tk.Scrollbar(Sview, orient="vertical", command=tvs.yview)
        tvs.configure(yscrollcommand=treescrolly.set)
        treescrolly.pack(side ="right",fill='y')
        
        tvs["column"] = list(df.columns)
        tvs['show'] = 'headings'
        for column in tvs['column']:
            tvs.heading(column, text=column)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            tvs.insert('','end', values = row)



print('RWIS - Diff Finder, created by Joshua McMahon for Lumin8 Technologies. JAN 2022. V1.0') 


#####################################################################################################################################
##############################################################################################################################################
#
#ABOVE
#   imports
#   CLASSes for Reports
#       +Start Page
#       +Atmospheric
#       Surface
#----------------------------------------------------------------------------------------------------------------------------------
#BELOW:
#   Function Definitions    
#   Pandas Tabling
#   GUI Frame configuration
#   Execution of the main program
#   
######################################################################################################################################
##########################################################################################################################################
# In[246]:





def ATMOSPHERIC_TODAY():
    
    #Read in atmospheric aggregate
    _atmos = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Atmospheric_t_split.txt')
    Atmospheric = _atmos.readlines()
    _atmos.close()
    
    #Create a list for the site Identifying information
    SiteAtmos = []
    for a_issue in Atmospheric:

        find_atmosites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', a_issue)  
        SiteAtmos.append(find_atmosites)

    #Create a list for the Issues
    IssueAtmos = []
    for a_issue in Atmospheric:
        find_atmoissues = re.findall('No .{,}', a_issue)  
        IssueAtmos.append(find_atmoissues) 
        
        
    #Create a dataframe for the atmospheric information    
    df = pd.DataFrame(SiteAtmos) #Frame the site identifying info
    df.columns = ['Site', 'Site Alt'] #Name the Columns for site info
    df.insert(2, 'Issue', IssueAtmos) #Attach the issue to the dataframe
    
    #df.set_index("Site", inplace =True)
    
    df
    
    return df


def SURFACE_TODAY():
    
    #Read in surface aggregate
    _surf = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Surface_t_split.txt')
    Surface = _surf.readlines()
    _surf.close()
    
    #Create a list for the site Identifying information
    SiteSurf = []
    for s_issue in Surface:

        find_surfsites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', s_issue)  
        SiteSurf.append(find_surfsites)

    #Create a list for the Issues
    IssueSurf = []
    for s_issue in Surface:
        find_surfissues = re.findall('No .{,}', s_issue)  
        IssueSurf.append(find_surfissues) 
        
        
    #Create a dataframe for the surface information    
    df = pd.DataFrame(SiteSurf) #Frame the site identifying info
    df.columns = ['Site', 'Site Alt'] #Name the Columns for site info
    df.insert(2, 'Issue', IssueSurf) #Attach the issue to the dataframe
    
    #df.set_index("Site", inplace =True)
    
    df
    
    return df


def ATMOSPHERIC_YESTERDAY():
    
    #Read in atmospheric aggregate
    _atmos = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Atmospheric_y_split.txt')
    Atmospheric = _atmos.readlines()
    _atmos.close()
    
    #Create a list for the site Identifying information
    SiteAtmos = []
    for a_issue in Atmospheric:

        find_atmosites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', a_issue)  
        SiteAtmos.append(find_atmosites)

    #Create a list for the Issues
    IssueAtmos = []
    for a_issue in Atmospheric:
        find_atmoissues = re.findall('No .{,}', a_issue)  
        IssueAtmos.append(find_atmoissues) 
        
        
    #Create a dataframe for the atmospheric information    
    df = pd.DataFrame(SiteAtmos) #Frame the site identifying info
    df.columns = ['Site', 'Site Alt'] #Name the Columns for site info
    df.insert(2, 'Issue', IssueAtmos) #Attach the issue to the dataframe
    
    #df.set_index("Site", inplace =True)
    
    df
    
    return df

def SURFACE_YESTERDAY():
    
    #Read in surface aggregate
    _surf = open(f'C:\\Users\\{user_actual}\\Documents\\RWIS\\DataSplit\\Surface_y_split.txt')
    Surface = _surf.readlines()
    _surf.close()
    
    #Create a list for the site Identifying information
    SiteSurf = []
    for s_issue in Surface:

        find_surfsites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', s_issue)  
        SiteSurf.append(find_surfsites)

    #Create a list for the Issues
    IssueSurf = []
    for s_issue in Surface:
        find_surfissues = re.findall('No .{,}', s_issue)  
        IssueSurf.append(find_surfissues) 
        
    Sensor_num = []
    for s_issue in Surface:
        find_surfsensor = re.findall('\s\d\s', s_issue)  
        Sensor_num.append(find_surfsensor)        
        
    #Create a dataframe for the surface information    
    df = pd.DataFrame(SiteSurf) #Frame the site identifying info
    df.columns = ['Site', 'Site Alt'] #Name the Columns for site info
    df.insert(2, 'Sensor', IssueSurf)
    df.insert(3, 'Issue', IssueSurf) #Attach the issue to the dataframe
    
    #df.set_index("Site", inplace =True)
    
    df
    
    return df

   

def RUN_TODAY():
    
    t_atmo = ATMOSPHERIC_TODAY()
    t_surf = SURFACE_TODAY()
   
    return t_atmo, t_surf


def RUN_YESTERDAY():
    
    y_atmo = ATMOSPHERIC_YESTERDAY()
    y_surf = SURFACE_YESTERDAY()

    return y_atmo, y_surf           
    
            

def Atmospheric():
            #Fetch Today + Yesterday Dataframe
            y_atmo, y_surf = RUN_YESTERDAY()
            t_atmo, t_surf = RUN_TODAY()

            #Merge the data
            d={"left_only":"Today", "right_only":"Yesterday","both":"both"}
            G = t_atmo.merge( y_atmo, how='outer', left_on='Site', right_on='Site', suffixes =('_Today','_Yesterday'), indicator = True)
            G['_merge'] = G['_merge'].map(d)
            G = G[G.Site.notnull()]
            G.reset_index( drop=True, inplace=True)
            Atmospheric_Diff = G
            Atmospheric_Diff 

            #Assess change in data
            changes = np.where(Atmospheric_Diff['Issue_Today'] != Atmospheric_Diff['Issue_Yesterday'], "Diff", "-")
            Atmospheric_Diff["Attention"] = changes

            #Reorder columns
            Atmospheric_Diff = Atmospheric_Diff[['Attention','Site','Issue_Today','Issue_Yesterday','_merge','Site Alt_Today','Site Alt_Yesterday']]

            #Beautify
            Atmospheric = Atmospheric_Diff.drop(['_merge','Site Alt_Today','Site Alt_Yesterday'], axis=1)
            Atmospheric

            #x = Atmospheric.style.apply(highlight_diff, axis=1)
            return Atmospheric #x
        
        

def Surface():
    #Fetch Today + Yesterday Dataframe
    y_atmo, y_surf = RUN_YESTERDAY()
    t_atmo, t_surf = RUN_TODAY()

    #Merge the data
    d={"left_only":"Today", "right_only":"Yesterday","both":"both"}
    G = t_surf.merge( y_surf, how='outer', left_on='Site', right_on='Site', suffixes =('_Today','_Yesterday'), indicator = True)
    G['_merge'] = G['_merge'].map(d)
    G = G[G.Site.notnull()]
    G.reset_index( drop=True, inplace=True)
    Surface_Diff = G
    Surface_Diff 

    #Assess change in data
    changes = np.where(Surface_Diff['Issue_Today'] != Surface_Diff['Issue_Yesterday'], "Diff", "-")
    Surface_Diff["Attention"] = changes

    #Reorder columns
    Surface_Diff = Surface_Diff[['Attention','Site','Issue_Today','Issue_Yesterday','_merge','Site Alt_Today','Site Alt_Yesterday']]

    #Beautify
    Surface = Surface_Diff.drop(['_merge','Site Alt_Today','Site Alt_Yesterday'], axis=1)
    Surface

    #x = Surface.style.apply(highlight_diff, axis=1)
    return Surface

       
        
        
        

def highlight_diff(s):
    if s.Attention == 'Diff':
        return ['background-color: yellow']*4
    else:
        return ['background-color: transparent']*4
    


class My_GUI(tk.Tk):



    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.title('RWIS - Diff Finder V 1.1')   #********************************************************************TITLE & VERSION**************************
        self.geometry('600x400')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        

        self.frames = {}
        for F in (StartPage, Atmospheric_Report, Surface_Report):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            
            #def refresh(self):
             #   self.destroy()
              #  self.__init__(self)


            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



print('RUNNING PROGRAM...')

if __name__ == "__main__":
    app = My_GUI()
    app.mainloop()