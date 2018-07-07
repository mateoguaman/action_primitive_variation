Research of Action Primitive Discovery in Robotics (RAPDR)

1. Description
The main goal of this research is to develop a way for intelligent agents, namely those in the field of Robotics, to creatively problem solve as a means of discovery new action primitives. This ability would be useful in a situation where the agents planning algorithms are failing with the finite set of action primitives that the robot has. 

In this circumstance, the robot could take its set of primitives, and perform some kind of action primitive variations on this existing knowledge base, as a way to discover new primitives which may help solve the problem. For example, a robot may have the goal of removing a boulder mass from its path in order to proceed on a dirt road in a search and rescue context. In the case where the "push object" action primitive is failing for the boulder object (because of its high mass), the robot may perform an action primitive variation, where the robot varys the parameters (for example, push speed) on the action primitive. From this creating problem solving module, the agent may discover the "strike" action, which is a derivative of the "push" action, just with a high speed. In its experimenation, the robot might see that this new primitive causes the boulder mass to break apart, thus removing the obstruction from the path, and allowing the agent to proceed in accomplishing its search and rescue duties. 

We would also like it to be the case that once the agent discovers the new action primitive, that this primitive will be added to its knowledge base of available action primitives for future planning, and as a way to implement continuous learning in the agent. 

2. System Design

 ________________
|				 |  
|   Robot Brain	 |
|________________|

 ____________________
|					 |  
|   Scenario         |
|   Representation	 |
|____________________|

 ____________
|			 |  
|   Gazebo	 |
|____________|

 ____________
|			 |  
|   PDDL	 |
|____________|

a. Robot Brain
The main module of the system will be the robot brain. This module will be where everything stems, but it itself wont contain much. The robot brain will have the ability to decide on a goal, and feed it to the PDDL planning module. For now, all goals of the robot, no matter how small, will go through the PDDL planner. For example, even if the robot wants to execute a very small action (say, a simple primitive like, move arm), it will go through the planner. Eventually, we may bipass this step, but for now, we will keep it simple. 
The robot brain will also have a knowledge base (KB), which will contain the knowledge that the robot has about itself. For now, the only thing that the knowledge base will contain is a list of available action primitives. Within our application/proof of concept, we will be adding to this list upon discovering new primitives. In future applications, we may chose to add to the KB with other lists of known capabilities besides primitives. 

b. Gazebo
This module is quite simple, it will be the physical scenario, with the following elements:
- Baxter Robot 
- Table
- Two blocks (representing buttons)
- a "Grey wall" (representing the obstruction)
- an object C (representing the object to be obtained)

c. Scenario Representation (SR)
This module will be constantly listing to Gazebo to get state information on the objects in the scenario, including location and "state information" (for example, button.state == pressed). Some of these states will have to be "engineered" by us (i.e. to figure out if a button is pressed, we need to see if the robot gripper is within a certain distance of the button)

d. PDDL 
This module will be called by the robot brain, but act as a stand alone module. The PDDL module will take in a goal, and have access to the robot brain KB to do its planning, and be able to pull information about the state as well. This module will be most involved with the others. 

Now that I have described the modules, I want to describe the functionality available to each. And finally, I will describe the specific proof of concept example we are looking to implement.

i) getScenarioScreenshot() 
This function can be called by the PDDL planner at any point in time to grab all scenario information from the SR module. For example, the SR module may be observing location information. When getScenarioScreenshot() is called, the return from the SR module might be [object1.location == (1,2,4), object2.location == (2,2,2)....objectn.location == (2,0,2)]. 

ii) goal 
The "goals" that are requested by the robot brain, and fed to the PDDL planner will take the form of a scenario screen shot, or a subset. For example, we may have goal1 = [object1.location == (1,2,4)]. 

iii) controlGazebo
In order to control the gazebo environment, the PDDL planner will have to have the ability to feed commands to gazebo. We will likely program one, or a set, of gazebo interfaces (in the form of specialized ROSNodes). This will be mostly one-way communication from the PDDL to Gazebo, but there will be some kind of feedback on teh success of primtives. 

3. Description of Proof Concept [attached as a PDF] 

TODO: 

