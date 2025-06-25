import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
from ITRFThai import ITRFThai as itrf


# a=itrf([1,1525000.627,666575.053],-0.21,-0.029,-0.076,47)

class itrfAPP:
    def __init__(self):
        pass


def open_csv():
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        display_csv_data(file_path)
        #print(file_path)


def transform(file_path):
    Tx=entryTx.get()
    Ty=entryTy.get()
    Tz=entryTz.get()
    if file_path:
        messagebox.showerror('Error', 'Open CSV first')


def display_csv_data(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            # # ['6', '1525008.915', '666553.656', '0']
            # for row in csv_reader:
            #     print(row)
            header = next(csv_reader)  # Read the header row
            tree.delete(*tree.get_children())  # Clear the current data

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in csv_reader:
                tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")



root= tk.Tk()
root.title("ITRF Transform")
root.geometry("600x600")
Tx= tk.Label(root,text="Tx")
entryTx=tk.Entry(root)
entryTx.insert(0,"-0.21")
Ty= tk.Label(root,text="Ty")
entryTy=tk.Entry(root)
entryTy.insert(0,"-0.029")
Tz= tk.Label(root,text="Tz")
entryTz=tk.Entry(root)
entryTz.insert(0,"-0.076")

Tx.pack(side="top")
entryTx.pack( padx=10,pady=0)
Ty.pack(side="top")
entryTy.pack(padx=10,pady=0)
Tz.pack(side="top")
entryTz.pack(padx=10,pady=0)


open_button = tk.Button(root,text="Open CSV File",command = open_csv)
open_button.pack(side="top",padx=20, pady=20)

transform_button = tk.Button(root,text="Transform ITRF",command = transform)
transform_button.pack(side="top",padx=20, pady=0)
# open_button.pack(padx=100, pady=100)
status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()
tree = ttk.Treeview(root, show="headings")
tree.pack(padx=20, pady=10, fill="both", expand=True)

root.mainloop()


# root = tk.Tk()
# root.title("CSV File Viewer")

# open_button = tk.Button(root, text="Open CSV File", command=open_csv_file)
# open_button.pack(padx=20, pady=10)



# root.mainloop()