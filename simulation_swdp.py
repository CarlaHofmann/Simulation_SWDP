import simpy
import random
import numpy
import csv


def create_architecture_matrix(num_modules):
    """Create a random number of software architecture modules
       with random dependencies and save these in a matrix"""
    # Create a zero-matrix
    module_matrix = numpy.zeros((num_modules, num_modules))
    k = 0

    # Calculate the frequency of matrix-fields to be filled in
    a = int(num_modules * (random.uniform(0.0, 0.3)))

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
    s_list = []

    for i in range(len(module_matrix)):
        for j in range(len(module_matrix)):
            if module_matrix[i][j] != 0:
                s_list.append(module_matrix[i][j])

    # Calculate the degree of coupling of the software architecture
    coupling_degree = (numpy.sum(s_list) / (num_modules * (num_modules - 1))).__round__(3)

    return coupling_degree


def change_planning(num_g_changes, num_i_changes, module_matrix):
    """Create a change plan with general and incoming changes"""
    module_matrix = module_matrix
    g_ch_list = []
    i_ch_list = []
    gen_effort = 0
    in_effort = 0
    ch_id = 0

    # Create general changes
    for i in range(num_g_changes):
        ch_id = i + 1
        type_tuple = change_type_definition(module_matrix)
        ch_type = type_tuple[0]
        ch_effort = type_tuple[1].__round__()
        module_matrix = type_tuple[2]
        ch_priority = 2
        ch_time = 0

        gen_effort += ch_effort
        g_ch_list.append([ch_id, ch_type, ch_effort, ch_priority, ch_time])

    # Create incoming changes
    i_time = numpy.random.normal(gen_effort / 2, gen_effort / 3, num_i_changes)

    for j in range(len(i_time)):
        if i_time[j] < 0:
            i_time[j] = float(str(i_time[j]).replace('-', ''))
        if i_time[j] > gen_effort:
            i_time[j] = random.uniform(0, gen_effort)

    for k in range(num_i_changes):
        ch_id = ch_id + 1
        type_tuple = change_type_definition(module_matrix)
        ch_type = type_tuple[0]
        ch_effort = type_tuple[1].__round__()
        module_matrix = type_tuple[2]
        ch_priority = 1
        ch_time = i_time[k].__round__()

        in_effort += ch_effort
        i_ch_list.append([ch_id, ch_type, ch_effort, ch_priority, ch_time])

    return gen_effort, g_ch_list, i_ch_list, in_effort


def change_type_definition(module_matrix):
    """Definition of the change type and dependent variables"""
    ch_type = random.choice([1, 2, 3])  # randomized change type
    basic_effort = 10

    if ch_type == 1:  # Remove module
        change = remove_module(module_matrix, basic_effort, ch_type)
        ch_effort = change[0]
        module_matrix = change[1]

    elif ch_type == 2:  # Change module
        change = change_module(module_matrix, basic_effort, ch_type)
        ch_effort = change[0]
        module_matrix = change[1]

    else:  # Add module
        change = add_module(module_matrix, basic_effort, ch_type)
        ch_effort = change[0]
        module_matrix = change[1]

    return ch_type, ch_effort, module_matrix


def remove_module(module_matrix, basic_effort, change_type):
    """Remove a module and the associated dependencies from the software architecture"""
    ch_effort = basic_effort * (change_type + 1)
    ch_dep = 0

    if len(module_matrix) != 0:
        module = random.randint(0, len(module_matrix) - 1)

        for i in range(len(module_matrix)):
            if module_matrix[module][i] != 0:
                ch_dep += 1

        ch_effort += (ch_effort * ch_dep)

        # Remove module from module matrix
        x = list(module_matrix.tolist())
        for j in range(len(x)):
            x[j].pop(module - 1)
        x.pop(module - 1)
        module_matrix = numpy.array([numpy.array(xi) for xi in x])

        return ch_effort, module_matrix


def change_module(module_matrix, basic_effort, change_type):
    """Change a module from the software architecture"""
    ch_effort = basic_effort * (change_type + 1)
    module = random.randint(0, len(module_matrix) - 1)

    ac_list = numpy.sum(module_matrix, axis=1)
    ch_effort += (ch_effort * ac_list[module])

    return ch_effort, module_matrix


def add_module(module_matrix, basic_effort, change_type):
    """Add a module and associated dependencies to the software architecture"""
    ch_effort = basic_effort * (change_type + 1)
    ch_dep = 0
    module = len(module_matrix)
    x = module_matrix.tolist()
    y = []
    k = 0

    # Calculate the frequency of matrix-fields to be filled in
    a = int(module * (random.uniform(0.1, 1)))

    # Add a module and associated dependencies to the module matrix
    for i in range(module + 1):
        if k == a:
            y.append(random.uniform(0.0, 1.0).__round__(2))
            k = 0
        else:
            y.append(0.0)
            k += 1

    for j in range(module):
        if k == a:
            x[j].append(random.uniform(0.0, 1.0).__round__(2))
            k = 0
        else:
            x[j].append(0.0)
            k += 1

    x.append(y)
    module_matrix = numpy.array([numpy.array(xi) for xi in x])
    module_matrix[module][module] = 0.0

    for i in range(len(module_matrix)):
        if module_matrix[module][i] != 0:
            ch_dep += 1

    ch_effort += (ch_effort * ch_dep)

    return ch_effort, module_matrix


class SequentialProject(object):
    """Sequential Project"""  # add more information
    def __init__(self, env, gen_effort, i_change_list_sp):
        self.env = env
        self.time_counter = 0
        self.gen_effort = gen_effort
        self.i_ch_list = []
        self.i_ch_list_sp = i_change_list_sp
        self.ph_list = []
        self.final_effort = 0
        self.test_start = 0

        # Start Run Process when initialising the object
        self.process = env.process(self.run_sp())

    def run_sp(self):
        """Run the simulation of a sequential project"""
        # Calculate the effort of the individual phases and the test start
        self.ph_list = [self.gen_effort * 0.2, self.gen_effort * 0.2, self.gen_effort * 0.3,
                        self.gen_effort * 0.2, self.gen_effort * 0.1]
        self.test_start = self.ph_list[0] + self.ph_list[1] + self.ph_list[2]

        # Save incoming changes in a new list
        for i in range(len(self.i_ch_list_sp)):
            self.i_ch_list.append(self.i_ch_list_sp[i])

        # Run the "Process Phases" Process
        self.process_phases()

    def process_phases(self):
        """Processing the individual project phases one after the other"""
        for i in range(len(self.ph_list)):
            if i == 3:
                while self.test_start > self.time_counter:
                    self.time_counter = self.test_start
                    self.process_i_changes()
                self.final_effort += self.ph_list[i]
                self.time_counter += self.ph_list[i]
                self.process_i_changes()
            elif i == 4:
                if self.test_start > self.time_counter:
                    while self.test_start > self.time_counter:
                        self.time_counter = self.test_start
                        self.process_i_changes()
                    self.final_effort += (self.ph_list[3] + self.ph_list[i])
                    self.time_counter += (self.ph_list[3] + self.ph_list[i])
                else:
                    self.final_effort += self.ph_list[i]
                    self.time_counter += self.ph_list[i]
            else:
                self.final_effort += self.ph_list[i]
                self.time_counter += self.ph_list[i]
                self.process_i_changes()

    def process_i_changes(self):
        """Processing of incoming changes"""
        while any(change for change in self.i_ch_list if change[4] <= self.time_counter):
            for change in (i for i in self.i_ch_list if i[4] <= self.time_counter):
                ch_effort = change[2]
                ch_time = change[4]

                if ch_time <= self.ph_list[0]:
                    p = 0.1
                elif self.ph_list[0] < ch_time <= self.ph_list[1]:
                    p = 0.2
                elif self.ph_list[1] < ch_time <= self.ph_list[2]:
                    p = 0.4
                else:
                    p = 0.7

                ch_effort += (ch_effort * p)

                # Change ready for testing
                if (ch_time + (ch_effort * 0.7)) > self.test_start:
                    self.test_start += (ch_time + ch_effort * 0.7 - self.test_start)

                self.final_effort += (ch_effort * 0.7)
                self.ph_list[3] += (ch_effort * 0.2)
                self.ph_list[4] += (ch_effort * 0.1)

                self.i_ch_list.remove(change)
            break

    def average_implementation_duration_sp(self):
        """Calculate ..."""
        duration_list = []
        for i in range(len(self.i_ch_list_sp)):
            ch_time = self.i_ch_list_sp[i][4]
            duration = self.time_counter - ch_time
            duration_list.append(duration)

        avg_duration = numpy.sum(duration_list) / (len(duration_list))

        return avg_duration

    def get_sp_final_effort(self):
        """Return the final effort of the sequential project"""
        return self.final_effort.__round__()


class IterativeProject(object):
    """Iterative Project"""  # add more information

    def __init__(self, env, sprint_effort_ip, g_change_list_ip, i_change_list_ip):
        self.env = env
        self.sprint_effort = sprint_effort_ip
        self.time_counter = 0
        self.final_effort = 0
        self.i_ch_list_ip = i_change_list_ip
        self.i_ch_list = []
        self.product_backlog = g_change_list_ip
        self.sprint_backlog = list()
        self.sprint_backlog_effort = 0
        self.ch_done = list()

        # Start Run Process when initialising the object
        self.process = self.env.process(self.run_ip())

    def run_ip(self):
        """Run the simulation of an iterative project"""
        # Save incoming changes in a new list
        for i in range(len(self.i_ch_list_ip)):
            self.i_ch_list.append(self.i_ch_list_ip[i])

        # Sort incoming changes by time
        self.i_ch_list.sort(key=lambda x: x[4])

        self.fill_sprint_backlog()

    def fill_sprint_backlog(self):
        """Fill the Sprint Backlog with changes from the Product Backlog. The order in which the
        changes are taken over is based on the priorities of the changes. If the Sprint Backlog
        is full, a Sprint is carried out."""
        while self.product_backlog:
            while self.sprint_backlog_effort < self.sprint_effort and self.product_backlog:
                if any(change for change in self.product_backlog if change[3] == 1):
                    for i in range(len(self.product_backlog)):
                        if self.product_backlog[i][3] == 1:
                            self.sprint_backlog_effort += self.product_backlog[i][2]
                            self.sprint_backlog.append(self.product_backlog[i])
                            self.product_backlog.pop(i)
                            break
                else:
                    self.sprint_backlog_effort += self.product_backlog[0][2]
                    self.sprint_backlog.append(self.product_backlog[0])
                    self.product_backlog.pop(0)
                    break

            if not self.product_backlog and self.sprint_backlog_effort < self.sprint_effort:
                self.sprint_effort = self.sprint_backlog_effort

            self.run_sprint()

    def run_sprint(self):
        """Implementation of a sprint. Processing the changes in the Sprint Backlog."""
        # If not all changes can be processed, an adjustment is made to the incomplete
        # change and it is moved back into the product backlog with priority 0.
        change = []
        if self.sprint_backlog_effort > self.sprint_effort:
            change = self.sprint_backlog[len(self.sprint_backlog) - 1]
            change[2] = self.sprint_backlog_effort - self.sprint_effort
            self.sprint_backlog.pop(len(self.sprint_backlog) - 1)

        # Calculate new time
        self.time_counter += self.sprint_effort

        for i in range(len(self.sprint_backlog)):
            if self.sprint_backlog[i][3] == 1:
                self.ch_done.append([self.sprint_backlog[i][0], self.time_counter])

        # Check if changes have occurred during the sprint
        self.fill_product_backlog()

        # Calculate new final effort
        self.final_effort += self.sprint_effort

        # Clear Sprint effort and Sprint Backlog
        self.sprint_backlog_effort = 0
        self.sprint_backlog = []
        if change:
            self.sprint_backlog.append(change)
            self.sprint_backlog_effort += change[2]

    def fill_product_backlog(self):
        """Fill the Product Backlog with incoming changes when they occur"""
        while self.i_ch_list and self.i_ch_list[0][4] <= self.time_counter:
            self.product_backlog.append(self.i_ch_list[0])
            self.i_ch_list.pop(0)

    def average_implementation_duration_ip(self):
        """Calculate average implementation duration of incoming changes"""
        self.ch_done.sort(key=lambda x: x[0])
        self.i_ch_list_ip.sort(key=lambda x: x[0])
        duration_list = []

        for i in range(len(self.ch_done)):
            if self.ch_done[i][0] == self.i_ch_list_ip[i][0]:
                ch_time = self.i_ch_list_ip[i][4]
                duration = self.ch_done[i][1] - ch_time
                duration_list.append(duration)

        avg_duration = numpy.sum(duration_list) / (len(duration_list))

        return avg_duration

    def get_ip_final_effort(self):
        """Return the final effort of the iterative project"""
        return self.final_effort.__round__()


# Setup and start the simulation
environment = simpy.Environment()
environment.run()

# Setup the documentation of the results
execution_id = 0
execution_doc = open('execution_doc.csv', 'w', newline='')
doc_rows = [['Execution Nr.', 'Modules', 'Coupling Degree', 'General Changes', 'General Effort',
             'Incoming Changes', 'Incoming Effort', 'End Effort SP', 'Avg. Duration SP', 'End Effort IP',
             'Avg. Duration IP']]

# Execute the simulation several times
for i in range(100000):
    NUMBER_OF_MODULES = random.randint(50, 100)
    NUMBER_OF_GENERAL_CHANGES = random.randint(15, 30)
    NUMBER_OF_INCOMING_CHANGES = random.randint(15, 30)
    SPRINT_EFFORT = 120  # 3 week sprints

    # Configuration of the general project variables
    MODULE_MATRIX = create_architecture_matrix(NUMBER_OF_MODULES)
    COUPLING_DEGREE = get_coupling_degree(NUMBER_OF_MODULES, MODULE_MATRIX)
    CHANGE_PLAN_TUPLE = change_planning(NUMBER_OF_GENERAL_CHANGES, NUMBER_OF_INCOMING_CHANGES, MODULE_MATRIX)
    GENERAL_EFFORT = CHANGE_PLAN_TUPLE[0]
    G_CHANGE_LIST = CHANGE_PLAN_TUPLE[1]
    I_CHANGE_LIST = CHANGE_PLAN_TUPLE[2]
    I_EFFORT = CHANGE_PLAN_TUPLE[3]

    # Start and run the sequential project
    sp = SequentialProject(environment, GENERAL_EFFORT, I_CHANGE_LIST)
    avg_duration_sp = sp.average_implementation_duration_sp()
    total_effort_sp = sp.get_sp_final_effort()

    # Start and run the iterative project
    ip = IterativeProject(environment, SPRINT_EFFORT, G_CHANGE_LIST, I_CHANGE_LIST)
    avg_duration_ip = ip.average_implementation_duration_ip()
    total_effort_ip = ip.get_ip_final_effort()

    # Documentation of the execution results
    execution_id += 1
    doc_rows.extend([[execution_id, NUMBER_OF_MODULES, COUPLING_DEGREE, NUMBER_OF_GENERAL_CHANGES,
                      GENERAL_EFFORT, NUMBER_OF_INCOMING_CHANGES, I_EFFORT, total_effort_sp,
                      avg_duration_sp, total_effort_ip, avg_duration_ip]])

# Write execution results in the csv file
with execution_doc:
    csv_writer = csv.writer(execution_doc, delimiter=',')
    csv_writer.writerows(doc_rows)
