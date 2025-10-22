import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
from ITRFThai import ITRFThai
import numpy as np
import os


class itrfAPP:
    def __init__(self,root):
        self.root = root
        self.root.title("ITRF Transform")
        self.root.geometry("600x800")

        self.frame1 = tk.Frame(root)
        self.frame1.pack()
        self.frame2 = tk.Frame(root)
        self.frame2.pack()
        self.frame3 = tk.Frame(root)
        self.frame3.pack()
        self.frame4 = tk.Frame(root)
        self.frame4.pack()
        self.frame5 = tk.Frame(root)
        self.frame5.pack()

        #Tx Ty Tz
        self.Tx= tk.Label(self.frame1,text="Tx")
        self.entryTx=tk.Entry(self.frame1)
        self.entryTx.insert(0,"-0.21")
        self.Ty= tk.Label(self.frame2,text="Ty")
        self.entryTy=tk.Entry(self.frame2)
        self.entryTy.insert(0,"-0.029")
        self.Tz= tk.Label(self.frame3,text="Tz")
        self.entryTz=tk.Entry(self.frame3)
        self.entryTz.insert(0,"-0.076")
        #zone
        self.zone= tk.Label(self.frame4,text="zone")

        options = ["47","48"]
        self.clicked = tk.StringVar() 
        self.clicked.set( "47" ) 
        self.drop=tk.OptionMenu(self.frame4,self.clicked,*options)
        
        #self.entryzone=tk.Entry(root)

        self.Tx.pack(side="left")
        self.entryTx.pack( padx=10,pady=0)
        self.Ty.pack(side="left")
        self.entryTy.pack(padx=10,pady=0)
        self.Tz.pack(side="left")
        self.entryTz.pack(padx=10,pady=0)

        self.zone.pack(side="left")
        self.drop.pack()


        self.open_button = tk.Button(self.frame5,text="Open CSV File",command = self.open_csv)
        self.open_button.pack(side="left",pady=10)
        self.transform_button = tk.Button(self.frame5,text="Transform ITRF",command = self.transform)
        self.transform_button.pack(side="left",padx=20)
        self.countno = tk.Label(root, text="Data count:")
        self.countno.pack()
        self.status_label = tk.Label(root, text="no file")
        self.status_label.pack()

        self.tree1 = ttk.Treeview(root, show="headings")
        self.tree1.pack(pady=10, fill="both", expand=True)

        self.tree2 = ttk.Treeview(root, show="headings")
        self.tree2.pack( fill="both", expand=True)


        self.EN=np.empty((0,5),float)
        
        

    def open_csv(self):
        self.file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.display_csv_data(self.file_path)
          #print(file_path) 


    def transform(self):
        Tx=float(self.entryTx.get())
        Ty=float(self.entryTy.get())
        Tz=float(self.entryTz.get())
        #zone=self.entryzone.get()
        zone=self.clicked.get()
        # print(self.EN)
        # EN=np.empty((0,3),float)
        self.EN2=np.empty((0,5),float)
        for row in self.EN:
            en = ITRFThai(float(row[1]),float(row[2]),float(row[3]),Tx,Ty,Tz,int(zone))
            en.transform()
            e = round(en.E,3)
            n = round(en.N,3)
            z = round(en.h,3)
            # print(n,e)
            self.EN2 = np.append(self.EN2,np.array([[row[0],n,e,z,row[4]]]),axis=0)

        self.writeCSV()

        if self.status_label['text'] =="no file":
            messagebox.showerror('Error', 'Open CSV first')


    def writeCSV(self):

        try:
            os.mkdir("csv")
        except FileExistsError:
            pass
        
        nfilename = "ITRF"+self.filename
        nfilepath = "csv/"+nfilename
        np.savetxt(nfilepath,self.EN2,delimiter=",",fmt="%s",header="no,N,E,Z,desc")
        try:
            with open(nfilepath,'r',newline='') as file:
                self.csv_reader = csv.reader(file)
                self.header = next(self.csv_reader)  # Read the header row
                self.tree2.delete(*self.tree2.get_children())  # Clear the current data
                self.tree2["columns"] = self.header
                self.lenEN2=len(self.EN2)
                for col in self.header:
                    self.tree2.heading(col, text=col)
                    self.tree2.column(col, width=100)



                for i in range(10):
                    if i== len(self.EN2):
                        break
                    else:
                        self.tree2.insert("", "end", values=(self.EN2[i][0],self.EN2[i][1],self.EN2[i][2],self.EN2[i][3],self.EN2[i][4]))
                self.countno.config(text=f"Data count: {self.lenEN2}")
                self.status_label.config(text=f"CSV file loaded: {nfilepath}")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def display_csv_data(self,file_path):
        self.EN=np.empty((0,5),float)
        try:
            with open(file_path, 'r', newline='') as file:
                self.csv_reader = csv.reader(file)

                self.filename=os.path.basename(file_path)
                # print(self.filename)
                self.header = next(self.csv_reader)  # Read the header row
                self.tree1.delete(*self.tree1.get_children())  # Clear the current data
                
                self.tree1["columns"] = self.header
                for col in self.header:
                    self.tree1.heading(col, text=col)
                    self.tree1.column(col, width=100)

                for row in self.csv_reader:
                    # self.tree1.insert("", "end", values=row)
                    self.EN=np.append(self.EN,np.array([[row[0],row[1],row[2],row[3],row[4]]]),axis=0)
                self.lenEN=len(self.EN)

                for i in range(10):
                    if i== len(self.EN):
                        break
                    else:
                        self.tree1.insert("", "end", values=(self.EN[i][0],self.EN[i][1],self.EN[i][2],self.EN[i][3],self.EN[i][4]))
                self.countno.config(text=f"Data count: {self.lenEN}")
                self.status_label.config(text=f"CSV file loaded: {file_path}")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = itrfAPP(root)
    root.mainloop()


