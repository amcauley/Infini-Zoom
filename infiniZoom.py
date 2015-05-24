'''API notes from http://www.gimp.org/docs/python/ .
   This file should be copied to Program Files\GIMP 2\lib\gimp\2.0\plug-ins.'''

from gimpfu import *

def infiniZoom(img, layer) :
    print("Starting infiniZoom")
    
    oldWidth = layer.width
    oldHeight = layer.height
    
    '''location (old coords) that will be at the origin of the new layer. no need to quantize here, will happen later'''
    finalXOrg = 205
    finalYOrg = 459   
    finalScaleFactor = 1.8812
    totalFrames = 6
    NUM_RECURSE_LAYERS = 6
    
    print("(oldWidth, oldHeight, finalXOrg, finalYOrg) = " + str((oldWidth, oldHeight, finalXOrg, finalYOrg)))
    
    z = finalScaleFactor**(1.0/(totalFrames+1))
    newXOrg = 0
    newYOrg = 0
    zInv = 1/z
    dX = finalXOrg*(1-zInv)/(1-zInv**(totalFrames+1))
    dY = finalYOrg*(1-zInv)/(1-zInv**(totalFrames+1))
    
    print("(zInv, dX, dY) = " + str((zInv, dX, dY)))
    
    for layerCnt in range(0, totalFrames+1):
    
        scaleFactor = z**(layerCnt+1)
        newWidth = int(oldWidth*scaleFactor)
        newHeight = int(oldHeight*scaleFactor)
        newXOrg = newXOrg + dX*(zInv**layerCnt)
        newYOrg = newYOrg + dY*(zInv**layerCnt)
        '''pixel coords should be integers'''
        newX = int(newXOrg)
        newY = int(newYOrg)          
                
        print("(layerCnt, scaleFactor, newX, newY, NUM_RECURSE_LAYERS) = " + str((layerCnt, scaleFactor, newX, newY, NUM_RECURSE_LAYERS)))
        
        layerName = "frame " + str(layerCnt)
        
        print("Creating " + layerName)
        currLayer = layer.copy()
        currLayer.name = layerName
        
        print("Adding " + layerName + " to img")
        img.add_layer(currLayer, 0) 
       
        #scale the entire layer
        print("Scaling Layer")
        '''scale(h, w, oldin) scales the layer to (w, h), using the specified origin (local or image).'''
        currLayer.scale(newWidth, newHeight, 0)       
        
        xTrans = -int(newX*scaleFactor)
        yTrans = -int(newY*scaleFactor)
        print("Translating Layer by " + str((xTrans, yTrans)))
        '''Moves the layer to (x, y) relative to its current position.'''
        ##currLayer.translate(-oldWidth, -oldHeight)    
        currLayer.translate(xTrans, yTrans)
        
        #resize the layer so it matches original layer. this is the equivalent of Layer->"Layer Boundary Size" option
        print("Resizing Layer")
        '''resize(w, h, x, y) resizes the layer to (w, h), positioning the original contents at (x,y).'''    
        ##currLayer.resize(oldWidth, oldHeight, -oldWidth, -oldHeight)
        currLayer.resize(oldWidth, oldHeight, xTrans, yTrans)           
        
        
        ###############################################
        '''This next section handles recursive mini images, i.e. what we're zooming into.'''
        
        miniX = 0
        miniY = 0        
        
        for miniRecurseLevel in range(0, NUM_RECURSE_LAYERS):
        
            miniX = miniX + finalXOrg*((1.0/finalScaleFactor)**miniRecurseLevel)
            miniY = miniY + finalYOrg*((1.0/finalScaleFactor)**miniRecurseLevel)
            
            miniXFinal = miniX*scaleFactor
            miniYFinal = miniY*scaleFactor          
            
            miniWidth = int(oldWidth*scaleFactor/(finalScaleFactor**(miniRecurseLevel+1)))
            miniHeight = int(oldHeight*scaleFactor/(finalScaleFactor**(miniRecurseLevel+1)))
            
            #Add in scaled down version of original image (for the infinite image recursion)
            print("Adding mini layer copy " + str(miniRecurseLevel) + ", mini (xFinal, yFinal, width, height) = " + str((int(miniXFinal), int(miniYFinal), miniWidth, miniHeight)))
            miniName = layerName + " mini " + str(miniRecurseLevel)
            miniLayer = layer.copy()
            miniLayer.name = miniName
            
            print("Adding " + miniName + " to img")
            img.add_layer(miniLayer, 0) 
            
            miniLayer.scale(miniWidth, miniHeight, 0);
        
            xTrans = int(miniXFinal - newX*scaleFactor)
            yTrans = int(miniYFinal - newY*scaleFactor)
            print("Translating Mini Layer by " + str((xTrans, yTrans)))
            '''Moves the layer to (x, y) relative to its current position.'''   
            miniLayer.translate(xTrans, yTrans)      

            print("Merging down Mini Layer")  
            img.merge_down(miniLayer, NORMAL_MODE)
        ###############################################
    
    print("Done!")

'''Disable the rest of this file (register and main) for in-console GIMP debugging, then, in the python-fu console:
    import sys
    sys.path=[gimp.directory+'/plug-ins']+sys.path
    import infiniZoom
    infiniZoom.infiniZoom(gimp.image_list()[0],gimp.image_list()[0].active_layer)
    
    To reload module: reload(infiniZoom)
'''
 
'''register(
    "python_fu_infiniZoom",
    "InfiniZoom",
    "Infinite Zoom GIF Generator",
    "AGM",
    "Open source (BSD 3-clause license)",
    "2014",
    "<Image>/Filters/Test/Draw Map v1",
    "RGB, RGB*",
    [],
    [],
    infiniZoom)
main()
'''