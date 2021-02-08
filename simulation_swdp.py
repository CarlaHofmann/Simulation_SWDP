import simpy
import random
import numpy
import threading
import time
import csv


def create_architecture_matrix(num_modules):
    """Create a random number of software architecture modules
       with random dependencies and save these in a matrix"""
    # Create the matrix
    module_matrix = numpy.zeros((num_modules, num_modules))
    k = 0

    # Calculate the frequency of matrix-fields to be filled in
    a = int(num_modules * (random.uniform(0.1, 1)))

    # Fill the matrix-fields
    for i in range(num_modules):
        for j in range(num_modules):
            if i != j:
                if k == a:
                    module_matrix[i][j] = random.uniform(0, 1).__round__(2)
                    k = 0
                else:
                    k += 1

    return module_matrix


def get_coupling_degree(num_modules, module_matrix):
    """Calculate the degree of coupling of the software architecture"""
    ec_list = numpy.sum(module_matrix, axis=0)
    cd_list = []

    # Calculate the instability and coupling degree for every module
    for i in range(num_modules):
        e_coupling = 0
        a_coupling = 0

        for j in range(num_modules):
            if module_matrix[i][j] != 0:
                a_coupling += 1
            if module_matrix[j][i] != 0:
                e_coupling += 1
        if e_coupling == 0 and a_coupling == 0:
            mod_instability = 0
        else:
            mod_instability = e_coupling / (e_coupling + a_coupling)

        mod_coupling_degree = mod_instability * ec_list[i]
        cd_list.append(mod_coupling_degree)

    # Calculate the degree of coupling of the software architecture
    coupling_degree = (numpy.sum(cd_list) / num_modules).__round__(3)
    return coupling_degree


def change_planning(num_g_changes, num_i_changes, module_matrix):
    """Create a change plan with general and incoming changes"""
    module_matrix = module_matrix
    g_ch_list = []
    i_ch_list = []
    gen_effort = 0
    ch_id = 0

    # Create general changes
    for i in range(1, num_g_changes + 1):
        ch_id = i
        type_tuple = change_type_definition(module_matrix)
        ch_type = type_tuple[0]
        ch_dep = type_tuple[1]
        ch_effort = type_tuple[2]
        module_matrix = type_tuple[3]
        ch_priority = 2
        ch_time = 0

        gen_effort = gen_effort + ch_effort
        g_ch_list.append([ch_id, ch_type, ch_dep, ch_effort, ch_priority, ch_time])

    # Create incoming changes
    i_time = numpy.random.normal(gen_effort / 2, gen_effort / 3, num_i_changes)

    for j in range(len(i_time)):
        if i_time[j] < 0:
            i_time[j] = float(str(i_time[j]).replace('-', ''))

    for k in range(num_i_changes):
        ch_id = ch_id + 1
        type_tuple = change_type_definition(module_matrix)
        ch_type = type_tuple[0]
        ch_dep = type_tuple[1]
        ch_effort = type_tuple[2]
        module_matrix = type_tuple[3]
        ch_priority = 1
        ch_time = i_time[k]

        i_ch_list.append([ch_id, ch_type, ch_dep, ch_effort, ch_priority, ch_time])

    # Sort incoming changes by time
    i_ch_list.sort(key=lambda x: x[5])

    return gen_effort, g_ch_list, i_ch_list


def change_type_definition(module_matrix):
    """Definition of the change type and dependent variables"""
    ch_type = random.choice([1, 2, 3])  # randomized change type
    basic_effort = 10

    if ch_type == 1:  # Remove module
        change = remove_module(module_matrix, basic_effort, ch_type)
        ch_dep = change[0]
        ch_effort = change[1]
        module_matrix = change[2]

    elif ch_type == 2:  # Change module
        change = change_module(module_matrix, basic_effort, ch_type)
        ch_dep = change[0]
        ch_effort = change[1]
        module_matrix = change[2]

    else:  # Add module
        change = add_module(module_matrix, basic_effort, ch_type)
        ch_dep = change[0]
        ch_effort = change[1]
        module_matrix = change[2]

    return ch_type, ch_dep, ch_effort, module_matrix


def remove_module(module_matrix, basic_effort, change_type):
    """Remove a module and the associated dependencies from the software architecture"""
    ch_effort = basic_effort * (change_type + 1)
    e_coupling = 0
    a_coupling = 0
    module = random.randint(0, len(module_matrix) - 1)

    # Calculate the instability of the module to be deleted
    for i in range(len(module_matrix)):
        if module_matrix[module][i] != 0:
            a_coupling += 1
        if module_matrix[i][module] != 0:
            e_coupling += 1

    if e_coupling == 0 and a_coupling == 0:
        ch_dep = 0
    else:
        ch_dep = e_coupling / (e_coupling + a_coupling)

    # Calculate coupling degree of the module to be deleted
    ec_list = numpy.sum(module_matrix, axis=0)
    ch_dep = ch_dep * ec_list[module]
    if ch_dep != 0:
        ch_effort *= (ch_dep * 10)

    # Remove module from module matrix
    x = list(module_matrix.tolist())
    for j in range(len(x)):
        x[j].pop(module - 1)
    x.pop(module - 1)
    module_matrix = numpy.array([numpy.array(xi) for xi in x])

    return ch_dep, ch_effort, module_matrix


def change_module(module_matrix, basic_effort, change_type):
    """Change a module from the software architecture"""
    ch_effort = basic_effort * (change_type + 1)
    e_coupling = 0
    a_coupling = 0
    module = random.randint(0, len(module_matrix) - 1)

    # Calculate the instability of the module to be changed
    for i in range(len(module_matrix)):
        if module_matrix[module][i] != 0:
            a_coupling += 1
        if module_matrix[i][module] != 0:
            e_coupling += 1

    if e_coupling == 0 and a_coupling == 0:
        ch_dep = 0
    else:
        ch_dep = e_coupling / (e_coupling + a_coupling)

    # Calculate coupling degree of the module to be changed
    ec_list = numpy.sum(module_matrix, axis=0)
    ch_dep = ch_dep * ec_list[module]
    if ch_dep != 0:
        ch_effort *= (ch_dep * 10)

    return ch_dep, ch_effort, module_matrix


def add_module(module_matrix, basic_effort, change_type):
    """Add a module and associated dependencies to the software architecture"""
    ch_effort = basic_effort * (change_type + 1)
    e_coupling = 0
    a_coupling = 0
    module = len(module_matrix)+1
    x = module_matrix.tolist()
    y = []
    a = int(module * (random.uniform(0.1, 1)))
    k = 0

    # Add a module and associated dependencies to the module matrix
    for i in range(module):
        if k == a:
            y.append(random.uniform(0.0, 1.0).__round__(2))
            k = 0
        else:
            y.append(0.0)
            k += 1

    for j in range(module-1):
        if k == a:
            x[j].append(random.uniform(0.0, 1.0).__round__(2))
            k = 0
        else:
            x[j].append(0.0)
            k += 1

    x.append(y)
    module_matrix = numpy.array([numpy.array(xi) for xi in x])
    module_matrix[module - 1][module - 1] = 0.0

    # Calculate the instability of the new module
    for k in range(module-1):
        if module_matrix[module-1][k] != 0:
            a_coupling += 1
        if module_matrix[k][module-1] != 0:
            e_coupling += 1

    if e_coupling == 0 and a_coupling == 0:
        ch_dep = 0
    else:
        ch_dep = e_coupling / (e_coupling + a_coupling)

    # Calculate coupling degree of the new module
    ec_list = numpy.sum(module_matrix, axis=0)
    ch_dep = ch_dep * ec_list[module-1]
    if ch_dep != 0:
        ch_effort *= (ch_dep * 10)

    return ch_dep, ch_effort, module_matrix


class IterativeProject(object):
    """Iterative Project"""  # add more information
    def __init__(self, env, sprint_effort_ip, g_change_list_ip, i_change_list_ip):
        self.env = env
        self.sprint_effort = sprint_effort_ip
        self.sprint_time = sprint_effort_ip
        self.final_effort = 0
        self.ch_list = i_change_list_ip
        self.product_backlog = g_change_list_ip
        self.sprint_backlog = list()
        self.sprint_backlog_effort = 0

        # Start Run Process when initialising the object
        self.process = self.env.process(self.run())

    def run(self):
        """Run the simulation of an iterative project"""
        # Run the "Fill Product Backlog" and "Fill Sprint Backlog" Processes concurrently
        t1 = threading.Thread(target=self.fill_product_backlog)
        t2 = threading.Thread(target=self.fill_sprint_backlog)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def fill_product_backlog(self):
        """Fill the Product Backlog with incoming changes when they occur"""
        while self.ch_list:
            time.sleep(self.ch_list[0][5] - time.perf_counter())
            self.product_backlog.append(self.ch_list[0])
            self.ch_list.pop(0)

    def fill_sprint_backlog(self):
        """Fill the Sprint Backlog with changes from the Product Backlog. The order in which the
        changes are taken over is based on the priorities of the changes. If the Sprint Backlog
        is full, a Sprint is carried out."""
        while self.product_backlog:
            while self.sprint_backlog_effort < self.sprint_effort and self.product_backlog:
                if any(change for change in self.product_backlog if change[4] == 0):
                    for i in range(len(self.product_backlog)):
                        if self.product_backlog[i][4] == 0:
                            self.sprint_backlog_effort += self.product_backlog[i][3]
                            self.sprint_backlog.append(self.product_backlog[i])
                            self.product_backlog.pop(i)
                            break
                elif any(change for change in self.product_backlog if change[4] == 1):
                    for i in range(len(self.product_backlog)):
                        if self.product_backlog[i][4] == 1:
                            self.sprint_backlog_effort += self.product_backlog[i][3]
                            self.sprint_backlog.append(self.product_backlog[i])
                            self.product_backlog.pop(i)
                            break
                else:
                    self.sprint_backlog_effort += self.product_backlog[0][3]
                    self.sprint_backlog.append(self.product_backlog[0])
                    self.product_backlog.pop(0)

            self.run_sprint()

    def run_sprint(self):
        """Implementation of a sprint. Processing the changes in the Sprint Backlog."""
        # Calculate new final effort
        self.final_effort = self.final_effort + self.sprint_effort

        # If not all changes can be processed, an adjustment is made to the incomplete
        # change and it is moved back into the product backlog with priority 0.
        if self.sprint_backlog_effort > self.sprint_effort: # Macht man halbe Sache im Sprint?
            change = self.sprint_backlog[len(self.sprint_backlog) - 1]
            sprint_dif = self.sprint_backlog_effort - self.sprint_effort
            change[3] = change[3] - sprint_dif
            change[4] = 0  # set priority 0
            self.product_backlog.append(change)

        # Wait till Sprint time is passed and clear Sprint effort and Sprint Backlog
        if time.perf_counter() < self.sprint_time:
            time.sleep(self.sprint_time - time.perf_counter())
        self.sprint_backlog_effort = 0
        self.sprint_backlog = list()

        # Calculate new Sprint time
        self.sprint_time = self.sprint_time + self.sprint_effort

    def get_ip_final_effort(self):
        """Return the final effort of the iterative project"""
        return self.final_effort


class SequentialProject(object):
    """Sequential Project"""  # add more information
    def __init__(self, env, gen_effort, i_change_list_sp):
        self.env = env
        self.gen_effort = gen_effort
        self.i_ch_list = i_change_list_sp
        self.ph_list = []
        self.final_effort = 0

        # Start Run Process when initialising the object
        self.process = env.process(self.run())

    def run(self):
        """Run the simulation of a sequential project"""
        # Calculate the effort of the individual phases
        self.ph_list = [self.gen_effort * 0.2, self.gen_effort * 0.2, self.gen_effort * 0.3,
                        self.gen_effort * 0.2, self.gen_effort * 0.1]

        # Run the "Process Phases" and "Process Incoming Changes" Processes
        self.process_phases(self.ph_list)
        self.process_i_changes()

    def process_phases(self, effort_list):
        """Processing the individual project phases one after the other"""
        for i in range(5):
            self.final_effort += effort_list[i]

    def process_i_changes(self):
        """Processing of incoming changes"""
        incoming_effort = 0
        while self.i_ch_list:
            ch_effort = self.i_ch_list[0][3]
            ch_time = self.i_ch_list[0][5]

            # Check during which phase the incoming change occurs and adapt the effort
            if ch_time <= self.ph_list[0]:
                ch_effort += (ch_effort * 0.1)
            elif self.ph_list[0] < ch_time <= self.ph_list[1]:
                ch_effort += (ch_effort * 0.2)
            elif self.ph_list[1] < ch_time <= self.ph_list[2]:
                ch_effort += (ch_effort * 0.4)
            else:
                ch_effort += (ch_effort * 0.7)

            self.i_ch_list.pop(0)
            incoming_effort += ch_effort

        e_list = [incoming_effort * 0.2, incoming_effort * 0.2, incoming_effort * 0.3,
                  incoming_effort * 0.2 + self.ph_list[3], incoming_effort * 0.1]
        self.process_phases(e_list)

    def get_sp_final_effort(self):
        """Return the final effort of the sequential project"""
        return self.final_effort


# Setup the documentation of the results
execution_id = 0
execution_doc = open('execution_doc.csv', 'w', newline='')
doc_rows = [['Execution Nr.', 'Modules', 'Coupling Degree', 'General Changes', 'General Effort',
            'Incoming Changes', 'End Effort IP', 'End Effort SP']]

# Setup and start the simulation
environment = simpy.Environment()
environment.run()

# Execute the simulation several times
for i in range(1):
    NUMBER_OF_MODULES = random.randint(10, 50)
    NUMBER_OF_GENERAL_CHANGES = random.randint(5, 15)
    NUMBER_OF_INCOMING_CHANGES = random.randint(5, 15)

    # Configuration of the general project variables
    MODULE_MATRIX = create_architecture_matrix(NUMBER_OF_MODULES)
    COUPLING_DEGREE = get_coupling_degree(NUMBER_OF_MODULES, MODULE_MATRIX)
    CHANGE_PLAN_TUPLE = change_planning(NUMBER_OF_GENERAL_CHANGES, NUMBER_OF_INCOMING_CHANGES, MODULE_MATRIX)
    GENERAL_EFFORT = CHANGE_PLAN_TUPLE[0]
    G_CHANGE_LIST = CHANGE_PLAN_TUPLE[1]
    I_CHANGE_LIST = CHANGE_PLAN_TUPLE[2]
    SPRINT_EFFORT = 120

    # Start and run the iterative project
    ip = IterativeProject(environment, SPRINT_EFFORT, G_CHANGE_LIST, I_CHANGE_LIST)
    total_effort_ip = ip.get_ip_final_effort()

    # Start and run the sequential project
    sp = SequentialProject(environment, GENERAL_EFFORT, I_CHANGE_LIST)
    total_effort_sp = sp.get_sp_final_effort()

    # Documentation of the execution results
    execution_id += 1
    doc_rows.extend([[execution_id, NUMBER_OF_MODULES, COUPLING_DEGREE, NUMBER_OF_GENERAL_CHANGES,
                    GENERAL_EFFORT.__round__(), NUMBER_OF_INCOMING_CHANGES, total_effort_ip.__round__(),
                    total_effort_sp.__round__()]])
    print([[execution_id, NUMBER_OF_MODULES, COUPLING_DEGREE, NUMBER_OF_GENERAL_CHANGES,
            GENERAL_EFFORT.__round__(), NUMBER_OF_INCOMING_CHANGES, total_effort_ip.__round__(),
            total_effort_sp.__round__()]])

# Write execution results in the csv file
with execution_doc:
    csv_writer = csv.writer(execution_doc, delimiter=',')
    csv_writer.writerows(doc_rows)
print(time.time())
