import trimesh
import numpy
from stl import mesh
import bedrock
import os
import shutil
from openpyxl import Workbook
from zipfile import ZipFile 



templateWorld='Base World.mcworld'
fileName='DoomReadyToPrint.STL'
YOffset=5
desiredSize=150
buildCenterX=0
buildCenterY=0



## setup parameters
outputFileName=fileName.replace(".STL","")
path_to_save="temp"
blocks=0
solidBlocks=0
outV=v.matrix.copy()
wb = Workbook()


##Make import mesh and turn it into a big
m = trimesh.load(fileName) #import a mesh
v=m.voxelized(pitch=1)#voxelize a mesh with a simple scale 
biggest=max(v.matrix.shape)#get biggest dimension
v=m.voxelized(pitch=biggest/desiredSize)#scale to match biggest dimension.
dims=v.matrix.shape

##make temp folder
if not os.path.isdir(path_to_save):#make a temp folder to work out of
    os.mkdir(path_to_save)
else:
    for filename in os.listdir(path_to_save):
        file_path = os.path.join(path_to_save, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
with ZipFile(templateWorld, 'r') as zipObj:
    zipObj.extractall(path_to_save)
    
##Processing the world to make it hollow and put the excel sheet together
with bedrock.World(path_to_save) as world:
    selectedBlock = bedrock.Block("minecraft:stone")
    for z in range(dims[2]):
        ws1 = wb.create_sheet("Y layer " +str(z+YOffset))
        for y in range(dims[1]):
            for x in range(dims[0]):
                if x>0 and y>0 and z>0:
                    if x+1<dims[0] and y+1<dims[1] and z+1<dims[2]:
                        if v.matrix[x+1][y][z] and v.matrix[x-1][y][z]:
                            if v.matrix[x][y+1][z] and v.matrix[x][y-1][z]:
                                if v.matrix[x][y][z+1] and v.matrix[x][y][z-1]:
                                    outV[x][y][z]=False
                if outV[x][y][z]:
                    blocks+=1
                    world.setBlock(x-round(dims[0]/2), z+YOffset, y-round(dims[2]/2), selectedBlock)
                    ws1.cell(row=x+1,column=y+1).value=str(x-round(dims[0]/2+buildCenterX))+"/"+str(y-round(dims[2]/2+buildCenterY))
                if v.matrix[x][y][z]:
                    solidBlocks+=1
    world.save()
wb.save(filename = outputFileName+'.xlsx')

#Clean up temp files
startDir=os.getcwd()
os.chdir(os.path.join(startDir,path_to_save))
with ZipFile(outputFileName+".mcworld", 'w') as zipF:
    zipF.write("world_icon.jpeg")
    zipF.write("levelname.txt")
    zipF.write("level.dat_old")
    zipF.write("level.dat")
    for root, dirs, files in os.walk("db"):
        for file in files:
            zipF.write(os.path.join(root, file))
##pack up world 
shutil.move(os.path.join(os.getcwd(),outputFileName+".mcworld"),os.path.join(startDir,outputFileName+".mcworld"))
#print blocks required.
print("numblocks:%d num stacks:%d num shulkers:%d"%(blocks,blocks/64,blocks/64/27))




