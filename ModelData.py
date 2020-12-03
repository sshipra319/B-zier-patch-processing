# Shipra Saini
# 2018-12-04

import sys
import numpy as np

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.xmin = float("inf")
    self.ymin = float("inf")
    self.zmin = float("inf")
    self.xmax = float("-inf")
    self.ymax = float("-inf")
    self.zmax = float("-inf")
    self.s_Transform = ();    
    self.xCentre = 0
    self.yCentre = 0
    self.zCentre = 0
    self.phi = 0.0
    self.theta = 0.0
    self.psi = 0.0
    self.m_Patches = []
    self.resolution = 0.0
    
    
    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
     
        with open(inputFile, 'r') as fp:
            lines = fp.read().replace('\r', '').split('\n')
            
        for (index, line) in enumerate(lines, start=1):
                line = line.strip()
                
                if line.startswith('p'):
                    patches = tuple(map(int,line.replace('p','').split()))
                    l_patches = list()
                    for patch in patches:
                        l_patches.append(patch-1)
                        
                    t_patches = tuple(l_patches)
                    if len(t_patches) != 16:
                        print("Line" + str(index) + "is a malformed patch")
                    else:
                        self.m_Patches.append(t_patches)
                
                elif line.startswith('v'):
                    t_vertices = tuple(map(float,line.replace('v','').split()))
                    
                    if len(t_vertices) != 3:
                        print("Line " + str(index) + " is a malformed vertex spec.")
                    else:
                        self.m_Vertices.append(t_vertices)                           
                        if t_vertices[0] < self.xmin:
                            self.xmin = t_vertices[0]    #min coordinates
                        if t_vertices[1] < self.ymin:
                            self.ymin = t_vertices[1]
                        if t_vertices[2] < self.zmin:
                            self.zmin = t_vertices[2]
                        if t_vertices[0] > self.xmax:   #max coordinates
                            self.xmax = t_vertices[0]
                        if t_vertices[1] > self.ymax:
                            self.ymax = t_vertices[1]                                
                        if t_vertices[2] > self.zmax:
                            self.zmax = t_vertices[2]                                 
                    
                elif line.startswith('f'):
                    
                    faces = tuple(map(int,line.replace('f','').split()))
                    l_faces = list()
                    for face in faces:
                        l_faces.append(face-1)
                        
                    t_faces = tuple(l_faces)
                    if len(t_faces) != 3:
                        print("Line " + str(index) + " is a malformed face spec.")
                    else:
                        self.m_Faces.append(t_faces)
                            
                elif line.startswith('w'):
                    
                        t_window = tuple(map(float,line.replace('w','').split()))
                        
                        if len(t_window) != 4:
                            print("Line " + str(index) + " is a malformed window spec.")
                        else:
                            self.m_Window = t_window
                            
                elif line.startswith('s'):
                    
                        t_viewport = tuple(map(float,line.replace('s','').split()))
                        
                        if len(t_viewport) != 4:
                            print("Line " + str(index) + " is a malformed viewport spec.")
                        else:
                            self.m_Viewport = t_viewport                          
                
                             
                
    ##################################################
    # TODO: Put your version of loadFile() from HMWK 01
    # here.  Enhance this routine to do a running computation
    # of the bounding box.
    ##################################################

  def getBoundingBox( self ) :      
      
      return (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)      
      
    ##################################################
    # TODO: Put your code to return the bounding box here.
    # Your routine should return a tuple with six
    # elements:
    #   ( xmin, xmax, ymin, ymax, zmin, zmax )
    ##################################################

  def specifyTransform( self, ax, ay, sx, sy, distance ) :   
      
     self.s_Transform = (ax, ay, sx, sy, distance)
     
    ##################################################
    # TODO: Put your code to remember the transformation here.
    ##################################################

  def getTransformedVertex( self, vNum, doPerspective, doEuler ) :  
      
      ax = self.s_Transform[0]
      ay = self.s_Transform[1]
      sx = self.s_Transform[2]
      sy = self.s_Transform[3]
      d = self.s_Transform[4]
      x = self.m_Vertices[vNum][0]
      y = self.m_Vertices[vNum][1]
      z = self.m_Vertices[vNum][2]
      
      if doEuler == 1:
          xp = self.r00*x + self.r01*y + self.r02*z + self.ex
          yp = self.r10*x + self.r11*y + self.r12*z + self.ey
          zp = self.r20*x + self.r21*y + self.r22*z + self.ez  
          
          x, y, z = xp, yp, zp
          
      
      if doPerspective == 1:
          x = self.ax + (self.sx * (x/(1-(z/d)))) if z<d else 0.0
          y = self.ay + (self.sy * (y/(1-(z/d)))) if z<d else 0.0
    
      else:
         x_t = ax + (sx*x)
         y_t = ay + (sy*y)
          
     
      z_t = 0.0
      
      return (x_t, y_t ,z_t)
  
    ##################################################
    # TODO: Put your code to return a transformed version of
    # vertex n here.  Remember, vNum goes 0 .. n-1,
    # where n is the number of vertices.
    # Your routine should return a tuple with three
    # elements:
    #   ( x', y', z' )
    ##################################################
    
  def getCentre(self):
      
      self.xCentre = (self.xmax + self.xmin)/2
      self.yCentre = (self.ymax + self.ymin)/2
      self.zCentre = (self.zmax + self.zmin)/2
      
      return (self.xCentre, self.yCentre, self.zCentre)
  
 
  def specifyEulerAngles(self, phi, theta, psi):
      
      phi = (phi*np.pi)/180.0
      theta = (theta*np.pi)/180.0
      psi = (psi*np.pi)/180.0
      
      cosPhi,   sinPhi   = np.cos( phi ),   np.sin( phi )
      cosTheta, sinTheta = np.cos( theta ), np.sin( theta )
      cosPsi,   sinPsi   = np.cos( psi ),   np.sin( psi )
      
      cPhiXcPsi = cosPhi*cosPsi
      cPhiXsPsi = cosPhi*sinPsi
      sPhiXcPsi = sinPhi*cosPsi
      sPhiXsPsi = sinPhi*sinPsi
      
      self.r00 = cosPsi * cosTheta
      self.r01 = -cosTheta * sinPsi
      self.r02 = sinTheta

      self.r10 = cPhiXsPsi + sPhiXcPsi*sinTheta
      self.r11 = cPhiXcPsi - sPhiXsPsi*sinTheta
      self.r12 = -cosTheta*sinPhi

      self.r20 = -cPhiXcPsi*sinTheta + sPhiXsPsi
      self.r21 = cPhiXsPsi*sinTheta + sPhiXcPsi
      self.r22 = cosPhi*cosTheta
      
      self.getCentre()
      
      self.ex  = -self.r00*self.xCentre - self.r01*self.yCentre - self.r02*self.zCentre + self.xCentre
      self.ey  = -self.r10*self.xCentre - self.r11*self.yCentre - self.r12*self.zCentre + self.yCentre
      self.ez  = -self.r20*self.xCentre - self.r21*self.yCentre - self.r22*self.zCentre + self.zCentre
      
  def transformXYZ(self, points, doPerspective, doEuler):
      
      x = points[0]
      y = points[1]
      z = points[2]
      ax = self.s_Transform[0]
      ay = self.s_Transform[1]
      sx = self.s_Transform[2]
      sy = self.s_Transform[3]
      d = self.s_Transform[4]
      
      if doEuler == 1:
          xp = self.r00*x + self.r01*y + self.r02*z + self.ex
          yp = self.r10*x + self.r11*y + self.r12*z + self.ey
          zp = self.r20*x + self.r21*y + self.r22*z + self.ez  
          
          x, y, z = xp, yp, zp
          
      
      if doPerspective == 1:
          x_t = ax + (sx * (x/(1-(z/d)))) if z<d else 0.0
          y_t = ay + (sy * (y/(1-(z/d)))) if z<d else 0.0
          
      else:
          x_t = ax + (sx*x)
          y_t = ay + (sy*y)  
      
      
      z_t = 0.0
      
      return (x_t, y_t ,z_t)  

  
  def getPatches(self)    : return self.m_Patches
  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
    
    fx = -w[0]
    fy = -w[1]
    gx = width*v[0]
    gy = height*v[1]
    sx = (width*(v[2] - v[0]))/(w[2] - w[0])
    sy = (height*(v[3] - v[1]))/(w[3] - w[1])
    ax = (fx*sx) + gx
    ay = (fy*sy) + gy
    
    return (ax, ay, sx, sy)

  ##################################################
  # TODO: Put your code to return the transform here.
  # Your routine should use w, v, width, and height
  # parameters according to the description in
  #   "4303 Homework 02 Transform.pdf"
  # to compute the transform.
  # Your routine should return a tuple with four
  # elements:
  #   ( ax, ay, sx, sy )
  ##################################################

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load and the canvas size.
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )
  print( 'Canvas size:', width, height )

  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy )

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
