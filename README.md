# Simulation_SWDP
Simulation_SWDP is a simulation of a sequential and an iterative software development project.

## Table of contents
* [About the Simulation](#about-the-simulation)
* [Technologies](#technologies)
* [Installation and Usage](#installation-and-usage)

## About the Simulation
The simulation was created as part of a bachelor thesis to investigate the relationship between software architecture and agile software development. The simulation involves the implementation of a sequential and iterative project with the same project framework in order to compare the two approaches. 

### Project Setup
Cross-project variables are defined and a project framework is created on the basis of these. A software architecture, which is represented at module level, is created with a defined number of modules and is represented by a matrix. The matrix contains the dependencies between the modules and allows the degree of coupling of the software architecture to be calculated. Subsequently, a plan of the changes to be implemented is created, whereby a distinction is made between general changes, which are known at the start of the project, and incoming changes, which occur during the runtime of the project. 

### Project Implementation
A sequential project with the waterfall model approach and an iterative project with the Scrum approach are carried out. The general and incoming changes are implemented according to the procedure model. The sequential project is divided into five phases in which the changes are implemented. If a change is added, it is processed in a separate project with all projects being merged into the fourth phase, the test of the system. In the iterative project, all changes are stored in the Product Backlog and the Sprint Backlog is refilled for each Sprint based on the priority of the changes. The end effort of the project is calculated based on the effort of the changes and their time of occurrence. In addition, the average implementation duration of a change is calculated.

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
