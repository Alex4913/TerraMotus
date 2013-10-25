import threading
import Queue

import ode
import time

import src.tools.convert as convert

class thread(threading.Thread):
  FPS = 30.0
  self.exit = False

  # Variable to store depth data.
  depthData = None

  # Store whether the data has been renewed
  updatedFlag = False

  # ODE Shared access
  world = None
  collisionSpace = None
  ground = None
  contacts = None

  bodies = []
  geoms = []
    
  def getDepthData():
    if(not(self.queue.empty()) and not(self.updatedFlag)):
      self.depthData = self.queue.get()
      self.updated = True

  def resetUpdatedFlag(state = False):
    self.updatedFlag = state

  # Collision callback
  def near_callback(self, args, obj1, obj2):
    # Check if the objects do collide
    contacts = ode.collide(obj1, obj2)
  
    # Create contact joints
    (world, contactGroup) = args
  
    for contact in contacts:
      contact.setBounce(0.2)
  
      # Friction
      contact.setMu(5000)
  
      # Create a joint between them to repel
      joint = ode.ContactJoint(world, contactGroup, contact)
      joint.attach(obj1.getBody(), obj2.getBody())
  
  def initODE(self):
    self.world = ode.World()
    self.world.setGravity((0, 0, -9.81))
    self.world.setERP(0.2)
    self.world.setCFM(1E-5)
  
    self.collisionSpace = ode.Space()
  
    verts = convert.depthToVertices(self.depthData)
    faces = convert.depthToODEFaces(self.depthData, verts)

    meshData = ode.TriMeshData()
    meshData.build(verts, faces)
    self.ground = ode.GeomTriMesh(meshData, self.collisionSpace)
  
    self.contacts = ode.JointGroup()

  def createSphere(self, world, collisionSpace, x, y, z, r, mass):
    sphereBody = ode.Body(world)

    M = ode.Mass()
    M.setSphereTotal(mass, r)
    M.mass = mass

    sphereBody.setMass(M)
    sphereBody.setPosition((x, y, z))

    sphereGeom = ode.GeomSphere(collisionSpace, r)
    sphereGeom.setBody(sphereBody)

    return (sphereBody, sphereGeom)

  def __init__(self, depthData, queue):
    self.queue = queue
    threading.Thread.__init__(self)

    self.depthData = depthData

  def run(self):
    self.initODE()
    simTimeStep = 1.0 / self.FPS

    (body, geom) = self.createSphere(self.world, self.collisionSpace, 40, 40, 10, 2, 1)

    self.bodies = [body]
    self.geoms = [geom]

    while(not(self.exit)):
      self.collisionSpace.collide((self.world, self.contacts),
                                    self.near_callback)
      self.world.step(simTimeStep)
      time.sleep(simTimeStep)
      self.contacts.empty()

    print "Physics Engine Stopped"

  def stop(self):
    self.exit = True
