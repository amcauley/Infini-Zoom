'''API notes from http://www.gimp.org/docs/python/ .
   This file should be copied to Program Files\GIMP 2\lib\gimp\2.0\plug-ins.'''

from gimpfu import *

def infiniZoom(img, layer) :
    print("Starting infiniZoom")
    
    oldWidth = layer.width
    oldHeight = layer.height
    
    '''location (old coords) that will be at the origin of the new layer. no need to quantize here, will happen later'''
    finalXOrg = oldWidth/2
    finalYOrg = oldHeight/2    
    finalScaleFactor = 2
    numSteps = 5
    
    for layerCnt in range(1, numSteps):
    
        linScale = 1.0*layerCnt/numSteps
        scaleFactor = 1+1.0*(finalScaleFactor-1)*linScale
        newWidth = int(oldWidth*scaleFactor)
        newHeight = int(oldHeight*scaleFactor)
        newXOrg = finalXOrg*linScale
        newYOrg = finalYOrg*linScale
        newX = int(newXOrg*scaleFactor)
        newY = int(newYOrg*scaleFactor)
        
        print("(layerCnt, scaleFactor, newX, newY) = " + str((layerCnt, scaleFactor, newX, newY)))
        
        layerName = "layer " + str(layerCnt)
        
        print("Creating new layer: " + layerName)
        currLayer = layer.copy()
        currLayer.name = layerName
        
        print("Adding " + str(layerName) + " to img")
        img.add_layer(currLayer, 0) 
       
        #scale the entire layer
        print("Scaling Layer")
        '''scale(h, w, oldin) scales the layer to (w, h), using the specified origin (local or image).'''
        currLayer.scale(newWidth, newHeight, 0)       

        #move the upper left corner of the scaled image so that the desired region of the scaled layer is visible
        print("Translating Layer")
        '''Moves the layer to (x, y) relative to its current position.'''
        ##currLayer.translate(-oldWidth, -oldHeight)    
        currLayer.translate(-newX, -newY)
        
        #resize the layer so it matches original layer. this is the equivalent of Layer->"Layer Boundary Size" option
        print("Resizing Layer")
        '''resize(w, h, x, y) resizes the layer to (w, h), positioning the original contents at (x,y).'''    
        ##currLayer.resize(oldWidth, oldHeight, -oldWidth, -oldHeight)
        currLayer.resize(oldWidth, oldHeight, -newX, -newY)
    
    print("Done!")

'''Disable the rest of this file (register and main) for in-console GIMP debugging, then, in the python-fu console:
    import sys
    sys.path=[gimp.directory+'/plug-ins']+sys.path
    import test_infiniZoom
    test_infiniZoom.infiniZoom(gimp.image_list()[0],gimp.image_list()[0].active_layer)
    
    To reload module: reload(test_infiniZoom)
'''
 
'''register(
    "python_fu_test_infiniZoom",
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