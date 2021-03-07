# Simulation_SWDP
Simulation_SWDP is a simulation of a sequential and an iterative software development project.

## Table of contents
* [About the Simulation](#about-the-simulation)
* [Technologies](#technologies)
* [Installation and Usage](#installation-and-usage)

## About the Simulation
The simulation was created as part of a bachelor thesis to investigate the relationship between software architecture and agile software development. The simulation involves the implementation of a sequential and iterative project with the same project framework in order to compare the two approaches. 

### Project Setup
Cross-project variables are defined and a project framework is created based on them. By calling the method create_architecture_matrix(), a software architecture represented at module level is created with a defined number of modules and represented by a matrix. The matrix contains the dependencies between the modules and allows the calculation of the coupling degree of the software architecture within the method get_coupling_degree(). Subsequently, a plan of changes to be implemented is created by calling the method change_planning(), whereby a distinction is made between general changes that are known at the beginning of the project and incoming changes that occur during the runtime of the project.

### Project Implementation
A sequential project with the waterfall model approach and an iterative project with the Scrum approach are defined by the classes SequentialProject() and IterativeProject(). By definition, the classes have the instantiation processes run_sp() and run_ip(). The general and incoming changes are implemented according to the process model. The sequential project is divided into five phases in which the changes are implemented. When a change is added, it is processed in a separate project by calling the process_i_changes() method. All projects are merged in the fourth phase, which is the testing of the whole system. In the iterative project, all changes are stored in the product backlog and the sprint backlog is refilled by the fill_sprint_backlog() method for each sprint based on the priority of the changes. The end effort of the project is calculated based on the effort of the changes and their time of occurrence. In addition, the average implementation time of a change is calculated.

## Technologies
The project is created with: 
* Python Version 3.8
* SimPy Version 4.0.1
* NumPy Version 1.19.5

## Installation and Usage
Clone the repository and use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages SimPy and NumPy.
```
pip install simpy
pip install numpy
```
Open [simulation_swdp.py](https://github.com/CarlaHofmann/Simulation_SWDP/blob/205df58c034ee1f98d7eba2e8852f6e500fc16cc/simulation_swdp.py). 

Adjust the number of simulations you want to run by changing the for-loop in line 478. Run the python file to setup and execute the simulation.
