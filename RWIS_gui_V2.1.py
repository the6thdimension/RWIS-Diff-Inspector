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

import asyncio
import tracemalloc


user_actual = os.getlogin()

global curr_data 
global prev_data
global AtmoSiteList_t, AtmoSiteList_y 
global SurfaceSiteList_t, SurfaceSiteList_y
global q

AtmoSiteList_t = []
AtmoSiteList_y = []
SurfaceSiteList_t = []
SurfaceSiteList_y = []







class StartPage(tk.Frame):
            
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="RWIS REPORTS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        
        
        
                
        def gather_today():
            global curr_data
            global t_dateoffile
            global AtmoSiteList_t
            global SurfaceSiteList_t
            
            StartPage.fname_current = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
            curr_data = StartPage.fname_current
            textlabel_current =Label(StartPage,text="Current data: "+StartPage.fname_current).pack()            
            StartPage.update()
            
            _rwis = open(curr_data)
            rwis = _rwis.read()
            _rwis.close()
            
            #find the date of file
            datetofind ='\d{2}/\d{2}/\d{4}'
            _dateoffile = re.search(datetofind, rwis)
            t_dateoffile = _dateoffile.group(0)
            
            #split data sections in file to 4 sections: date info, atmospheric, surface, and sub
            note, rwis_atmo_t, rwis_surf_t, rwis_sub_t = rwis.split('\n\n\n')

            #Atmospheric===============================
            t_atmo = rwis_atmo_t.split('\n')
            t_atmo = t_atmo[4:]
            
            AtmoSiteList_t = []
            AtmoIssueList = []
            for line in t_atmo:
                sites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', line)
                AtmoSiteList_t.append(sites)
            
                issues = re.findall('No .{,}', line)  
                AtmoIssueList.append(issues)     

            i = 0
            for a in AtmoSiteList_t:
                a.extend(AtmoIssueList[i])
                i = i + 1
            
            for i in AtmoSiteList_t:
                i.pop(1)   
                
                #-------> compiles to a list[site,issue]
                t_surf = rwis_surf_t.split('\n')
                t_surf[4:]
                t_surf = t_surf[4:]
                
                SurfaceSiteList_t = []    
                
                SiteSurf = []
                
                for s_issue in t_surf:

                    find_surfsites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', s_issue)  
                    SiteSurf.append(find_surfsites)
                
                SensorSurf = []
                for line in t_surf:
                    sensors = re.findall('\s\d\s',line)
                    for item in sensors:
                        s = item
                        SensorSurf.append(s)
                    
                #Create a list for the Issues
                IssueSurf = []
                for s_issue in t_surf:
                    find_surfissues = re.findall('No .{,}', s_issue)  
                    IssueSurf.append(find_surfissues) 
                
                
                SurfaceSiteList_t = SiteSurf
                
                o = 0
                for ss in SurfaceSiteList_t:
                    ss.extend(SensorSurf[o])
                    ss.extend(IssueSurf[o])
                    o = o + 1
                
                for v in SurfaceSiteList_t:
                    v.pop(4)
                    v.pop(2)
                    v.pop(1)
                    
                
                        
                collection_today = (AtmoSiteList_t, SurfaceSiteList_t)
                
                return collection_today   
            
        
                        #################
                        ##   BUTTONS   ##
                        #################
        
        button_T = tk.Button(self, text="Select Today's Report",
                            command = lambda : gather_today)
        button_T.pack()
        
        
        def gather_yesterday():
        
            global prev_data
            global AtmoSiteList_y
            global SurfaceSiteList_y 
            global T       
            
            StartPage.fname_previous = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
            prev_data = StartPage.fname_previous
            textlabel_previous =Label(StartPage,text="Previous data: "+ StartPage.fname_previous).pack()            
            StartPage.update()
            
            _rwis = open(prev_data)
            rwis = _rwis.read()
            _rwis.close()
            
            #find the date of file
            datetofind ='\d{2}/\d{2}/\d{4}'
            _dateoffile = re.search(datetofind, rwis)
            y_dateoffile = _dateoffile.group(0)
            
            #split data sections in file to 4 sections: date info, atmospheric, surface, and sub
            note, rwis_atmo_y, rwis_surf_y, rwis_sub_y = rwis.split('\n\n\n')
            
        #Atmospheric===============================
            y_atmo = rwis_atmo_y.split('\n')
            y_atmo = y_atmo[4:]
            
            AtmoSiteList_y = []
            AtmoIssueList = []
            for line in y_atmo:
                sites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', line)
                AtmoSiteList_t.append(sites)
            
                issues = re.findall('No .{,}', line)  
                AtmoIssueList.append(issues)     

            i = 0
            for a in AtmoSiteList_y:
                a.extend(AtmoIssueList[i])
                i = i + 1
            
            for i in AtmoSiteList_y:
                i.pop(1)   
                
                #-------> compiles to a list[site,issue]
            
            
            
            y_surf = rwis_surf_y.split('\n')
            y_surf[4:]
            y_surf = y_surf[4:]
            
            SurfaceSiteList_y = []    
            
            SiteSurf = []
            
            for s_issue in y_surf:

                find_surfsites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', s_issue)  
                SiteSurf.append(find_surfsites)
            
            SensorSurf = []
            for line in y_surf:
                sensors = re.findall('\s\d\s',line)
                for item in sensors:
                    s = item
                    SensorSurf.append(s)
                
            #Create a list for the Issues
            IssueSurf = []
            for s_issue in y_surf:
                find_surfissues = re.findall('No .{,}', s_issue)  
                IssueSurf.append(find_surfissues) 
            
            
            SurfaceSiteList_y = SiteSurf
            
            o = 0
            for ss in SurfaceSiteList_y:
                ss.extend(SensorSurf[o])
                ss.extend(IssueSurf[o])
                o = o + 1
            
            for v in SurfaceSiteList_y:
                v.pop(4)
                v.pop(2)
                v.pop(1)
            
            
            collection_yesterday = (AtmoSiteList_y, SurfaceSiteList_y)
            
            return collection_yesterday
            
        


        button_T = tk.Button(self, text="Select Yesterday's Report",
                            command= gather_yesterday)
        button_T.pack()


        def run_atmospheric(self):
            

        
            AtmoSiteList_t, w = gather_today()
            AtmoSiteList_y, u = gather_yesterday()

            df_t = pd.DataFrame(AtmoSiteList_t) #Frame the site identifying info
            df_y = pd.DataFrame(AtmoSiteList_y)
            df_t.columns = ['Site', 'Today\'s Issue'] #Name the Columns for site info
            df_t.set_index("Site", inplace =True)
        
            #df.insert(2, 'Issue', IssueAtmos) #Attach the issue to the dataframe
            
            
            df_y.columns = ['Site', 'Yesterday\'s Issue']
            df_y.set_index("Site", inplace =True)
            
            
                #Merge the data
            d={"left_only":"Today", "right_only":"Yesterday","both":"both"}
            G = df_t.merge( df_y, how='outer', left_on='Site', right_on='Site', suffixes =('_Today','_Yesterday'), indicator = True)
            G['_merge'] = G['_merge'].map(d)
            #G = G[G.Site.notnull()]
            #G.reset_index( drop=True, inplace=True)
            Atmospheric_Diff = G
            Atmospheric_Diff 
            
            #Assess change in data
            changes = np.where(Atmospheric_Diff['Today\'s Issue'] != Atmospheric_Diff['Yesterday\'s Issue'], "Diff", "-")
            Atmospheric_Diff["Attention"] = changes

            #Reorder columns
            #Atmospheric_Diff = Atmospheric_Diff[['Attention','Site','Today\'s Issue','Yesterday\'s Issue','_merge']]
            
            
            #I want the able to be display the dataframe here
            Aview =  LabelFrame(Atmospheric_Report, text='Atmospheric', height=800, width=800) #frame for data
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
            
            tva["column"] = list(Atmospheric_Diff.columns)
            tva['show'] = 'headings'
            for column in tva['column']:
                tva.heading(column, text=column)
            df_rows = Atmospheric_Diff.to_numpy().tolist()
            for row in df_rows:
                tva.insert('','end', values = row)
            self.Atmospheric_Dif = Atmospheric_Diff
        
        


        button1 = tk.Button(self, text="Run Atmospheric Diff",
                            command= run_atmospheric)
        button1.pack()
        
        
        
        def run_surface(self):
        
                w, SurfaceSiteList_t = gather_today()
                u, SurfaceSiteList_y = gather_yesterday()
                
                #Create a dataframe for the surface information    
                ds_t = pd.DataFrame(SurfaceSiteList_t) #Frame the site identifying info
                ds_t.columns = ['Site', 'Sensor','Issue'] #Name the Columns for site info
                #df.insert(2, 'Issue', IssueSurf) #Attach the issue to the dataframe
                
                ds_t.set_index("Site", inplace =True)
                
                    #Create a dataframe for the surface information    
                ds_y = pd.DataFrame(SurfaceSiteList_y) #Frame the site identifying info
                ds_y.columns = ['Site', 'Sensor','Issue'] #Name the Columns for site info
                #df.insert(2, 'Issue', IssueSurf) #Attach the issue to the dataframe
                
                ds_y.set_index("Site", inplace =True) 
                
                        #Merge the data
                d={"left_only":"Today", "right_only":"Yesterday","both":"both"}
                G = ds_t.merge( ds_y, how='outer', left_on='Site', right_on='Site', suffixes =('_Today','_Yesterday'), indicator = True)
                G['_merge'] = G['_merge'].map(d)
                #G = G[G.Site.notnull()]
                #G.reset_index( drop=True, inplace=True)
                Surface_Diff = G
                Surface_Diff 
                
                #Assess change in data
                changes = np.where(Surface_Diff['Issue_Today'] != Surface_Diff['Issue_Yesterday'], "Diff", "-")
                Surface_Diff["Attn: Issue"] = changes
                
                changes2 = np.where(Surface_Diff['Sensor_Today'] != Surface_Diff['Sensor_Yesterday'], "Diff", "-")
                Surface_Diff["Attn: Sensor"] = changes2



                #I want the able to be display the dataframe here
                Sview =  LabelFrame(Surface_Report, text='Surface', height=800, width=800) #frame for data
                Sview.pack( fill=BOTH, expand=True, pady=10)
                
                tvs = ttk.Treeview(Sview)
                
                tvs.place(relx=0,rely=0)
                treescrolly = tk.Scrollbar(Sview, orient="vertical", command=tvs.yview)
                tvs.configure(yscrollcommand=treescrolly.set)
                treescrolly.pack(side ="right",fill='y')
                
                tvs["column"] = list(Surface_Diff.columns)
                tvs['show'] = 'headings'
                for column in tvs['column']:
                    tvs.heading(column, text=column)
                df_rows = Surface_Diff.to_numpy().tolist()
                for row in df_rows:
                    tvs.insert('','end', values = row)
          
        
        
        
        button2 = tk.Button(self,text="Run Surface Diff", command=lambda: controller.show_frame("Surface_Report"))
        button2.pack()





class Atmospheric_Report(tk.Frame):              
     
    #def refresh(self, Atmospheric_Report):
    #    tk.Frame.destroy(self)
    #    tk.Frame.__init__(self)
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent,width=600, height=800)
        self.controller = controller
            
        label = tk.Label(self, text="Atmospheric Report", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        
        
        
        
             
                        #################
                        ##   BUTTONS   ##
                        #################
        
        
        
        #button_upat = tk.Button(self, text="Update", command = Atmospheric_Report.run_atmospheric(df_t,df_y))
        #button_upat.pack()
        
        

            
        
        
       
               
        
        def Print_Atmospheric_Report():
            messagebox.showinfo("Say Hello", "Hello World")
            print('Atmospheric Report')
            
            
        
        


    
        


class Surface_Report(tk.Frame):
    
                

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Surface Report", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)        
        
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
       

        


print('RWIS - Diff Finder, created by Joshua McMahon for Lumin8 Technologies. JAN 2022. V1.3') 


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

 
    
    




        
        

def highlight_diff(s):
    if s.Attention == 'Diff':
        return ['background-color: yellow']*4
    else:
        return ['background-color: transparent']*4
    


class My_GUI(tk.Tk):

    global AtmoSiteList_t
    global SurfaceSiteList_t

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        def get_page(self, page_class):
            return self.frames[page_class]
        
        self.shared_data = {"AtmoSiteList_t": AtmoSiteList_t, "SurfaceSiteList_t": SurfaceSiteList_t}
        

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
    
    



def gather_today():
    global curr_data
    global t_dateoffile
    global AtmoSiteList_t
    global SurfaceSiteList_t
    
    StartPage.fname_current = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
    curr_data = StartPage.fname_current
    textlabel_current =Label(StartPage,text="Current data: "+StartPage.fname_current).pack()            
    StartPage.update()
    
    _rwis = open(curr_data)
    rwis = _rwis.read()
    _rwis.close()
    
    #find the date of file
    datetofind ='\d{2}/\d{2}/\d{4}'
    _dateoffile = re.search(datetofind, rwis)
    t_dateoffile = _dateoffile.group(0)
    
    #split data sections in file to 4 sections: date info, atmospheric, surface, and sub
    note, rwis_atmo_t, rwis_surf_t, rwis_sub_t = rwis.split('\n\n\n')

    #Atmospheric===============================
    t_atmo = rwis_atmo_t.split('\n')
    t_atmo = t_atmo[4:]
    
    AtmoSiteList_t = []
    AtmoIssueList = []
    for line in t_atmo:
        sites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', line)
        AtmoSiteList_t.append(sites)
    
        issues = re.findall('No .{,}', line)  
        AtmoIssueList.append(issues)     

    i = 0
    for a in AtmoSiteList_t:
        a.extend(AtmoIssueList[i])
        i = i + 1
    
    for i in AtmoSiteList_t:
        i.pop(1)   
        
        #-------> compiles to a list[site,issue]
        t_surf = rwis_surf_t.split('\n')
        t_surf[4:]
        t_surf = t_surf[4:]
        
        SurfaceSiteList_t = []    
        
        SiteSurf = []
        
        for s_issue in t_surf:

            find_surfsites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', s_issue)  
            SiteSurf.append(find_surfsites)
        
        SensorSurf = []
        for line in t_surf:
            sensors = re.findall('\s\d\s',line)
            for item in sensors:
                s = item
                SensorSurf.append(s)
            
        #Create a list for the Issues
        IssueSurf = []
        for s_issue in t_surf:
            find_surfissues = re.findall('No .{,}', s_issue)  
            IssueSurf.append(find_surfissues) 
        
        
        SurfaceSiteList_t = SiteSurf
        
        o = 0
        for ss in SurfaceSiteList_t:
            ss.extend(SensorSurf[o])
            ss.extend(IssueSurf[o])
            o = o + 1
        
        for v in SurfaceSiteList_t:
            v.pop(4)
            v.pop(2)
            v.pop(1)
            
         
                
        collection_today = (AtmoSiteList_t, SurfaceSiteList_t)
        
        return collection_today   
            

    
def gather_yesterday():
        
        global prev_data
        global AtmoSiteList_y
        global SurfaceSiteList_y 
        global T       
        
        StartPage.fname_previous = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
        prev_data = StartPage.fname_previous
        textlabel_previous =Label(StartPage,text="Previous data: "+ StartPage.fname_previous).pack()            
        StartPage.update()
        
        _rwis = open(prev_data)
        rwis = _rwis.read()
        _rwis.close()
        
        #find the date of file
        datetofind ='\d{2}/\d{2}/\d{4}'
        _dateoffile = re.search(datetofind, rwis)
        y_dateoffile = _dateoffile.group(0)
        
        #split data sections in file to 4 sections: date info, atmospheric, surface, and sub
        note, rwis_atmo_y, rwis_surf_y, rwis_sub_y = rwis.split('\n\n\n')
        
    #Atmospheric===============================
        y_atmo = rwis_atmo_y.split('\n')
        y_atmo = y_atmo[4:]
        
        AtmoSiteList_y = []
        AtmoIssueList = []
        for line in y_atmo:
            sites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', line)
            AtmoSiteList_t.append(sites)
        
            issues = re.findall('No .{,}', line)  
            AtmoIssueList.append(issues)     

        i = 0
        for a in AtmoSiteList_y:
            a.extend(AtmoIssueList[i])
            i = i + 1
        
        for i in AtmoSiteList_y:
            i.pop(1)   
            
            #-------> compiles to a list[site,issue]
        
        
        
        y_surf = rwis_surf_y.split('\n')
        y_surf[4:]
        y_surf = y_surf[4:]
        
        SurfaceSiteList_y = []    
        
        SiteSurf = []
        
        for s_issue in y_surf:

            find_surfsites = re.findall('OH\d{3}\S{,3}\W{,8}\S{3}', s_issue)  
            SiteSurf.append(find_surfsites)
        
        SensorSurf = []
        for line in y_surf:
            sensors = re.findall('\s\d\s',line)
            for item in sensors:
                s = item
                SensorSurf.append(s)
            
        #Create a list for the Issues
        IssueSurf = []
        for s_issue in y_surf:
            find_surfissues = re.findall('No .{,}', s_issue)  
            IssueSurf.append(find_surfissues) 
        
        
        SurfaceSiteList_y = SiteSurf
        
        o = 0
        for ss in SurfaceSiteList_y:
            ss.extend(SensorSurf[o])
            ss.extend(IssueSurf[o])
            o = o + 1
        
        for v in SurfaceSiteList_y:
            v.pop(4)
            v.pop(2)
            v.pop(1)
        
        
        collection_yesterday = (AtmoSiteList_y, SurfaceSiteList_y)
        
        return collection_yesterday
    
    

def run_atmospheric():
    try:

        AtmoSiteList_t, w = gather_today()
        AtmoSiteList_y, u = gather_yesterday()

        df_t = pd.DataFrame(AtmoSiteList_t) #Frame the site identifying info
        df_y = pd.DataFrame(AtmoSiteList_y)
        df_t.columns = ['Site', 'Today\'s Issue'] #Name the Columns for site info
        df_t.set_index("Site", inplace =True)
    
        #df.insert(2, 'Issue', IssueAtmos) #Attach the issue to the dataframe
        
        
        df_y.columns = ['Site', 'Yesterday\'s Issue']
        df_y.set_index("Site", inplace =True)
        
        
            #Merge the data
        d={"left_only":"Today", "right_only":"Yesterday","both":"both"}
        G = df_t.merge( df_y, how='outer', left_on='Site', right_on='Site', suffixes =('_Today','_Yesterday'), indicator = True)
        G['_merge'] = G['_merge'].map(d)
        #G = G[G.Site.notnull()]
        #G.reset_index( drop=True, inplace=True)
        Atmospheric_Diff = G
        Atmospheric_Diff 
        
        #Assess change in data
        changes = np.where(Atmospheric_Diff['Today\'s Issue'] != Atmospheric_Diff['Yesterday\'s Issue'], "Diff", "-")
        Atmospheric_Diff["Attention"] = changes

        #Reorder columns
        #Atmospheric_Diff = Atmospheric_Diff[['Attention','Site','Today\'s Issue','Yesterday\'s Issue','_merge']]
        
        
        #I want the able to be display the dataframe here
        Aview =  LabelFrame(Atmospheric_Report, text='Atmospheric', height=800, width=800) #frame for data
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
        
        tva["column"] = list(Atmospheric_Diff.columns)
        tva['show'] = 'headings'
        for column in tva['column']:
            tva.heading(column, text=column)
        df_rows = Atmospheric_Diff.to_numpy().tolist()
        for row in df_rows:
            tva.insert('','end', values = row)
    
    except:
        print("No data for atmospheric")  


    
    
def run_surface():
        
    try:
   
        w, SurfaceSiteList_t = gather_today()
        u, SurfaceSiteList_y = gather_yesterday()
        
        #Create a dataframe for the surface information    
        ds_t = pd.DataFrame(SurfaceSiteList_t) #Frame the site identifying info
        ds_t.columns = ['Site', 'Sensor','Issue'] #Name the Columns for site info
        #df.insert(2, 'Issue', IssueSurf) #Attach the issue to the dataframe
        
        ds_t.set_index("Site", inplace =True)
        
            #Create a dataframe for the surface information    
        ds_y = pd.DataFrame(SurfaceSiteList_y) #Frame the site identifying info
        ds_y.columns = ['Site', 'Sensor','Issue'] #Name the Columns for site info
        #df.insert(2, 'Issue', IssueSurf) #Attach the issue to the dataframe
        
        ds_y.set_index("Site", inplace =True) 
        
                #Merge the data
        d={"left_only":"Today", "right_only":"Yesterday","both":"both"}
        G = ds_t.merge( ds_y, how='outer', left_on='Site', right_on='Site', suffixes =('_Today','_Yesterday'), indicator = True)
        G['_merge'] = G['_merge'].map(d)
        #G = G[G.Site.notnull()]
        #G.reset_index( drop=True, inplace=True)
        Surface_Diff = G
        Surface_Diff 
        
        #Assess change in data
        changes = np.where(Surface_Diff['Issue_Today'] != Surface_Diff['Issue_Yesterday'], "Diff", "-")
        Surface_Diff["Attn: Issue"] = changes
        
        changes2 = np.where(Surface_Diff['Sensor_Today'] != Surface_Diff['Sensor_Yesterday'], "Diff", "-")
        Surface_Diff["Attn: Sensor"] = changes2



        #I want the able to be display the dataframe here
        Sview =  LabelFrame(Surface_Report, text='Surface', height=800, width=800) #frame for data
        Sview.pack( fill=BOTH, expand=True, pady=10)
        
        tvs = ttk.Treeview(Sview)
        
        tvs.place(relx=0,rely=0)
        treescrolly = tk.Scrollbar(Sview, orient="vertical", command=tvs.yview)
        tvs.configure(yscrollcommand=treescrolly.set)
        treescrolly.pack(side ="right",fill='y')
        
        tvs["column"] = list(Surface_Diff.columns)
        tvs['show'] = 'headings'
        for column in tvs['column']:
            tvs.heading(column, text=column)
        df_rows = Surface_Diff.to_numpy().tolist()
        for row in df_rows:
            tvs.insert('','end', values = row)
    except:
        print('File is empty')