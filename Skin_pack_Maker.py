import json
import uuid
import os
from shutil import copyfile
from zipfile import ZipFile

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory



lang={}




    

class skinDialog:
    def __init__(self,master,nameVar,pictureFileVar):
        top=self.top=Toplevel(master)
        rt=0
        self.l=Label(top,text="Name",justify=LEFT).grid(row=rt,column=1)
        Entry(master=top,textvariable=nameVar,width=37,borderwidth=1).grid(row=rt,column=2,columnspan=2)
        rt+=1
        self.l=Label(top,text="file",justify=LEFT).grid(row=rt,column=1)
        Entry(top,textvariable=pictureFileVar,width=30,borderwidth=1).grid(row=rt,column=2)
        Button(top,text="Browse",command=lambda: self.browseSkin(pictureFileVar)).grid(row=rt,column=3)
        rt+=1
        Button(top,text='Done',command=self.cleanup).grid(row=rt,column=3)
    def browseSkin(self,pathVar):
        pathVar.set(askopenfilename(master=self.top, title="Browse for Skin",filetypes =(("Skin File", "*.png"),
                                                                             ("All Files","*.*"))))
        self.top.lift()
    def cleanup(self):
        ##self.value=self.e.get()
        self.top.destroy()
class mainWindow:
    def __init__(self,master):
        self.skins=[]
        self.master=master
        self.master.title("Skin Pack maker")
        self.workingDir = StringVar()
        workingDir=self.workingDir
        self.packName = StringVar()
        self.relVersion = StringVar()
        relVersion=self.relVersion
        self.subVersion = StringVar()
        subVersion=self.subVersion
        minorVersion = StringVar()
        self.minorVersion=minorVersion
        description=StringVar()
        self.description=description

        r=0

        Label(self.master, text="Working Directory",borderwidth=1, justify=LEFT).grid(row=r,column=1)
        Entry(self.master, textvariable=workingDir,borderwidth=1, width=40).grid(row=r,column=2,columnspan=3)
        Button(self.master, text="Browse",command=self.browseWorkingDir,borderwidth=1 ).grid(row=r,column=5)

        r+=1

        Label(self.master, text="Name",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        Entry(self.master, textvariable=self.packName,borderwidth=1,width=47).grid(row=r,column=2,columnspan=4)
        r+=1

        Label(self.master, text="Version",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        Entry(self.master, textvariable=relVersion,borderwidth=1,width=3).grid(row=r,column=2)
        Entry(self.master, textvariable=subVersion,borderwidth=1,width=3).grid(row=r,column=3)
        Entry(self.master, textvariable=minorVersion,borderwidth=1,width=3).grid(row=r,column=4)

        r+=1

        Label(self.master, text="Description",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        Entry (self.master, textvariable=description,borderwidth=1,width=47).grid(row=r,column=2,columnspan=4)

        r+=1
        Label(self.master, text="Skins",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        self.listbox = Listbox(self.master)
        self.listbox.grid(row=r,column=2,columnspan=3,rowspan=2)
        self.addButton=Button(self.master, text="Add Skin",command=lambda: self.addSkin(self.listbox))
        self.addButton.grid(row=r,column=5)
        r+=1
        self.delButton=Button(self.master, text="Delete",command=self.deleteSkin ).grid(row=r,column=5)
        r+=1
        self.delButton=Button(self.master, text="Export",command=self.export ).grid(row=r,column=5)
    def browseWorkingDir(self):
        name = askdirectory(title="Working Folder")
        self.workingDir.set(name)
    def export(self):
        if len(self.skins)>0:
            subVersion=self.subVersion
            relVersion=self.relVersion
            minorVersion=self.minorVersion
            description=self.description
            manifest={}
            manifest["format_version"]=1
            manifest["header"]={}
            manifest["header"]["name"]=self.packName.get()
            manifest["header"]["uuid"]=str(uuid.uuid1())
            manifest["header"]["version"]=[int(relVersion.get()),int(subVersion.get()),int(minorVersion.get())]
            manifest["modules"]=[]
            manifest["modules"].append({})

            manifest["modules"][0]["type"]="skin_pack"
            manifest["modules"][0]["uuid"]=str(uuid.uuid1())
            manifest["modules"][0]["version"]=[int(relVersion.get()),int(subVersion.get()),int(minorVersion.get())]

            pack_manifest={}
            pack_manifest["header"]={}
            pack_manifest["header"]["pack_id"]=str(uuid.uuid1())
            pack_manifest["header"]["name"]=self.packName.get()
            pack_manifest["header"]["packs_version"]=str(relVersion.get())+"."+str(subVersion.get())+"."+str(minorVersion.get())
            pack_manifest["header"]["description"]="Skins used by RavinMaddHatter"
            pack_manifest["header"]["modules"]=[]
            pack_manifest["header"]["modules"].append({})
            pack_manifest["header"]["modules"][0]["description"]="description"
            pack_manifest["header"]["modules"][0]["version"]=str(relVersion.get())+"."+str(subVersion.get())+"."+str(minorVersion.get())
            pack_manifest["header"]["modules"][0]["uuid"]=str(uuid.uuid1())
            pack_manifest["header"]["modules"][0]["type"]="skin_pack"

            skins={}
            skins["geometry"]= "skinpacks/skins.json"
            skins["skins"]= self.skins
            skins["serialize_name"]= self.packName.get()
            skins["localization_name"]= "Lname"
            with open(os.path.join(self.workingDir.get(),'manifest.json'), 'w+') as outfile:
                json.dump(manifest,outfile,indent=4)
            with open(os.path.join(self.workingDir.get(),'pack_manifest.json'), 'w+') as outfile:
                json.dump(pack_manifest,outfile,indent=4)
            with open(os.path.join(self.workingDir.get(),'skins.json'), 'w+') as outfile:
                json.dump(skins,outfile,indent=4)
            try:
                os.mkdir(os.path.join(self.workingDir.get(),"texts"))
            except:
                pass
            with open(os.path.join(self.workingDir.get(),"texts","en_us.lang"),"w+") as outfile:
                for L in ["skin.Lname.Lname1=name1",
                          "skin.Lname.Lname2=name2",
                          "skin.Lname.Lname3=name3",
                          "skinpack.Lname=name"]:
                    outfile.writelines(L)
            os.chdir(self.workingDir.get())
            file_paths = self.get_all_file_paths(self.workingDir.get())
            with ZipFile(os.path.join(self.workingDir.get(),self.packName.get()+".mcpack"),'w') as zip: 
                # writing each file one by one 
                for file in file_paths:
                    file=file.replace(os.path.join(self.workingDir.get(),""),"")
                    print(file)
                    zip.write(file)
    def get_all_file_paths(self,directory): 
  
        # initializing empty file paths list 
        file_paths = [] 
      
        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(directory): 
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
      
        # returning all file paths 
        return file_paths
    def deleteSkin(self):
        items = self.listbox.curselection()
        if len(items)>0:
            self.skins.pop(items[0])
            self.listbox.delete(ANCHOR)
    def addSkin(self,lb):
        name=StringVar()
        path=StringVar()
        w=skinDialog(root,name,path)
        self.addButton["state"]="disabled"
        root.wait_window(w.top)
        self.addButton["state"] = "normal"
        if len(name.get())>0 and len(path.get())>0:
            self.skins.append({
                "localization_name":name.get(),
                "geometry":"geometry.humanoid.custom",
                "texture":path.get(),
                "type":"free"
                })
            lb.insert(END,name.get())
            print(path.get())
            print(self.workingDir.get())
            print(os.path.basename(path.get()))
            newName=os.path.join(self.workingDir.get(),os.path.basename(path.get()))
            print(newName)
            copyfile(path.get(), newName)
            print(path.get())
        
            

root = Tk()
m=mainWindow(root)
root.mainloop(  )




