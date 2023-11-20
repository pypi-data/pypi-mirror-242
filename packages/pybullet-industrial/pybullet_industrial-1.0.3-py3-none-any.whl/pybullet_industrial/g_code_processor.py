import pybullet as p
from pybullet_industrial import RobotBase
from pybullet_industrial import linear_interpolation
from pybullet_industrial import circular_interpolation
from pybullet_industrial import ToolPath
import numpy as np


class GCodeProcessor:
    """Initializes a GCodeProcessor object with the provided parameters.

    Args:
        gcode_input (str, optional): Simulated input G-code
        robot (RobotBase, optional): The robot which is controlled
        endeffector_list (list, optional): List of endeffectors to use
        m_commands (list, optional): M-commands to execute
        t_commands (list, optional): T-commands to execute
        offset (np.array, optional): Point which defines the origin
        axis (int, optional): The axis around which the circle
                                is interpolated .Defaults to 2 which
                                corresponds to the z-axis (0=x,1=y)
        interpolation_precision (int, optional): Precision of interpolation
        interpolation_approach (int, optional): Number of interpolations
                                                before determining precision
    """

    def __init__(self, gcode_input: str = None, robot: RobotBase = None,
                 endeffector_list: list = None,
                 m_commands: dict = None,
                 t_commands: dict = None,
                 offset: np.array = np.array([[0.0, 0.0, 0.0],
                                              [0.0, 0.0, 0.0]]),
                 axis: int = 2, interpolation_precision: int = 0.01,
                 interpolation_approach: int = 1000):

        #  Converting G-Code into special list format
        if gcode_input is not None:
            self.gcode = self.read_gcode(gcode_input)

        # Initializing class variables
        self.new_point = []
        self.new_or = []
        self.last_point = []
        self.last_or = []
        self.r_val = 0
        self.robot = robot
        self.endeffector_list = endeffector_list
        self.active_endeffector = self.__get_active_endeffector()
        self.offset = offset
        self.axis = axis
        self.interpolation_precision = interpolation_precision
        self.interpolation_approach = interpolation_approach
        self.m_commands = m_commands
        self.t_commands = t_commands

        # Setting the default G-commands
        self.g_commands = {
            "54": [lambda: self.__g_54()],
            "500": [lambda: self.__g_500()],
            "17": [lambda: self.__g_17()],
            "18": [lambda: self.__g_18()],
            "19": [lambda: self.__g_19()]
        }

        if robot is not None:
            self.__calibrate_tool()

    @staticmethod
    def read_gcode(gcode_input: str):
        """Reads g-code row by row and saves the processed data in
        a list.
        Comments that start with % are ignored and all the other data is
        stored as it gets read in.

        Args:
            filename (list[str]): Source of information

        Returns:
            gcode (list)
        """

        gcode_input = gcode_input.splitlines()
        gcode = []

        # Loop over the lines of the file
        for line in gcode_input:

            if not line.strip():
                continue

            # Read in G-Code if line is not a comment and not empty
            if line[0] != "%" and len(line) > 1:

                # Initialize a new line as a list
                new_line = []

                # Split the line into its components
                data = line.split()

                # Loop over the components
                for i in data:
                    # Determine the ID of the component
                    id_val = i[0]

                    # Extract the value of the component
                    val2 = float(i[1:])

                    if id_val in ["G", "M", "T"]:
                        # Insert the value into the corresponding
                        # column of the new line
                        new_line.append([id_val, int(val2)])
                    else:
                        new_line.append([id_val, val2])

                # Add the finished line to the list
                gcode.append(new_line)

        return gcode

    def __iter__(self):
        """ Initialization of the the class variables which are responsible
        for the iteration

        Returns:
        self(GCodeProcessor): Iterator
        """

        self.elementary_operations = []
        self.index_operation = 0
        self.index_gcode = 0
        self.path = []
        return self

    def __next__(self):
        """Switches between running elementary operation and reading
        in commands from the G-code to create elementary operations.
        Every line of the G-code causes the built
        of new elementary operations"""

        # Runs elementary operations
        if self.index_operation < len(self.elementary_operations):
            i = self.index_operation
            self.index_operation += 1
            self.elementary_operations[i]()

        # Reads the G-Code command to create elementary operations
        elif self.index_gcode < len(self.gcode):
            self.elementary_operations = []
            self.index_operation = 0

            i = self.index_gcode
            cmd_type = self.gcode[i][0][0]
            cmd_int = self.gcode[i][0][1]

            self.last_point = np.array(self.new_point)
            self.last_or = np.array(self.new_or)

            self.__create_elementary_operations(cmd_type, cmd_int)

            self.index_gcode += 1

            return self.gcode[i]

        else:
            raise StopIteration

    def __create_elementary_operations(self, cmd_type: str, cmd_int: int):
        """Appends all the elemenatry operations which are necessary to execute
        the recent command. All the elementary operations are safed with the
        help of lambda calls.

        Args:
            cmd_type(str): Current G-command type
            cmd_int(int): Current G-command integer
        """

        if cmd_type == "G":
            if cmd_int > 3:
                for operation in self.g_commands[str(cmd_int)]:
                    self.elementary_operations.append(lambda: operation())
            else:
                path = self.__build_path()
                self.elementary_operations = self.__create_movement_operations(
                    path)

        elif cmd_type == "M":
            for operation in self.m_commands[str(cmd_int)]:
                self.elementary_operations.append(lambda: operation())

        elif cmd_type == "T":
            for operation in self.t_commands[str(cmd_int)]:
                self.elementary_operations.append(lambda: operation())

            self.elementary_operations.append(lambda: self.__calibrate_tool())

    def __build_path(self):
        """Calculates a new point and new orientation based on the new
        coordinates and offset. Depending on the G-command type, a
        specific tool path is returned. G0 commands create a path
        with 2 interpolation steps, while higher G-1-2-3
        commands generate a path with the chosen precision.

        Returns:
            path(ToolPath): Interpolated tool path
        """

        cmd = self.gcode[self.index_gcode]
        g_com = cmd[0][1]

        self.__build_new_point(cmd)

        if g_com == 0:
            path = self.__build_simple_path()
        else:
            path = self.__build_precise_path(g_com)

        orientation = p.getQuaternionFromEuler(self.new_or)
        path.orientations = np.transpose([orientation]
                                         * len(path.orientations[0]))

        return path

    def __build_new_point(self, cmd: list):
        """Calculates the new point of a G-Code command with respect
        to the current offset.

        Args:
            cmd(list): Current command line
        """

        variables = {'G': np.nan, 'X': np.nan, 'Y': np.nan, 'Z': np.nan,
                     'A': np.nan, 'B': np.nan, 'C': np.nan, 'R': np.nan}

        for val in cmd:
            if val[0] in variables:
                variables[val[0]] = val[1]
            else:
                raise KeyError("Variable '{}' is not defined.".format(val[0]))

        xyz_val = np.array([variables['X'], variables['Y'],
                            variables['Z']])
        abc_val = np.array([variables['A'], variables['B'],
                            variables['C']])
        self.r_val = variables['R']

        # Setting the new point considering the offset
        self.new_point = np.array([0.0, 0.0, 0.0])
        for i, value in enumerate(xyz_val):
            if np.isnan(value):
                self.new_point[i] = self.last_point[i]
            else:
                self.new_point[i] = value + self.offset[0][i]

        # Setting the new orientation
        orientation = np.array([0.0, 0.0, 0.0])
        for i, value in enumerate(abc_val):
            if np.isnan(value):
                orientation[i] = self.last_or[i] - self.offset[1][i]
            else:
                orientation[i] = value

        orientation = p.getQuaternionFromEuler(orientation)
        orientation_offset = p.getQuaternionFromEuler(self.offset[1])

        # Transforming the oriention considering the offset
        point = np.array([0.0, 0.0, 0.0])
        _, self.new_or = p.multiplyTransforms(
            point, orientation, point, orientation_offset)

        self.new_or = p.getEulerFromQuaternion(self.new_or)

    def __build_simple_path(self):
        """ Returns the simple path of a G0-interpolation

        Returns:
            path(ToolPath): G0-toolpath
        """

        path = linear_interpolation(self.last_point,
                                    self.new_point,
                                    2)

        return path

    def __build_precise_path(self, g_com: int):
        """Returns the percise path for G-2-3-Interpolations by calculating
        the neccessary amount of interpolation steps considering the precision
        of the interpolation.

        Args:
            g_com(int): Current G-command type
        """

        interpolation_steps = self.interpolation_approach
        percise_path = True

        for _ in range(2):

            # Building the Path if there is a linear interpolation
            if g_com == 1:
                path = linear_interpolation(self.last_point,
                                            self.new_point,
                                            interpolation_steps)

            # Building the path if there is a circular interpolation
            elif g_com in [2, 3]:
                if g_com == 2:
                    path = circular_interpolation(self.last_point,
                                                  self.new_point, self.r_val,
                                                  interpolation_steps,
                                                  self.axis, True)
                else:
                    path = circular_interpolation(self.last_point,
                                                  self.new_point, self.r_val,
                                                  interpolation_steps,
                                                  self.axis, False)
            # Calculating the total ditance
            if percise_path:
                percise_path = False
                total_distance = 0
                point_distance = 0
                previous_postion = self.last_point

                for position, _, _ in path:

                    # Calculating the point distance
                    point_distance = np.linalg.norm(
                        position - previous_postion)

                    # Adding point distnace to global distance
                    total_distance += point_distance
                    previous_postion = position

                interpolation_steps = total_distance/self.interpolation_precision
                interpolation_steps = int(np.ceil(interpolation_steps))

        return path

    def __create_movement_operations(self, path: ToolPath):
        """Returns a list of elementary operations to move the robot based
        on a given tool path and active endeffector.

        Args:
            path(ToolPath): input tool path

        Returns:
            elementary_operations(list): elementary operations to move robot
        """

        active = self.active_endeffector  # abbreviation
        elementary_operations = []

        for position, orientation, _ in path:
            if self.active_endeffector == -1:
                elementary_operations.append(
                    lambda i=position, j=orientation:
                    self.robot.set_endeffector_pose(i, j))

            else:
                elementary_operations.append(
                    lambda i=position, j=orientation:
                    self.endeffector_list[active].set_tool_pose(i, j))

        return elementary_operations

    def __get_active_endeffector(self):
        """Returns the index of the active endeffector.

        Returns:
            active_endeffector(int): index of the active endeffector
        """

        active_endeffector = -1

        if self.endeffector_list is not None:
            for n, i in enumerate(self.endeffector_list):
                if i.is_coupled():
                    active_endeffector = n
                    break
        return active_endeffector

    def __calibrate_tool(self):
        """This method sets the current postion of the active tool. This
        ensures a smooth transition between tool changes.
        """

        self.active_endeffector = self.__get_active_endeffector()
        actv = self.active_endeffector  # abbreviation

        if self.active_endeffector == -1:
            self.new_point = self.robot.get_endeffector_pose()[0]
            or_euler = p.getEulerFromQuaternion(
                self.robot.get_endeffector_pose()[1])
            self.new_or = np.array(or_euler)
        else:
            self.new_point = self.endeffector_list[actv].get_tool_pose()[0]
            or_euler = p.getEulerFromQuaternion(
                self.endeffector_list[actv].get_tool_pose()[1])
            self.new_or = np.array(or_euler)

    def __g_54(self):
        # Activation of the zero offset
        self.offset = np.array([self.last_point, self.last_or])

    def __g_500(self):
        # Deactivation of the zero offset
        self.offset = np.array([[0.0, 0.0, 0.0],
                                [0.0, 0.0, 0.0]])

    def __g_17(self):
        # Axis selelection for circular interpolation
        self.axis = 2  # X-Y Axis

    def __g_18(self):
        # Axis selelection for circular interpolation
        self.axis = 1  # X-Z Axis

    def __g_19(self):
        # Axis selelection for circular interpolation
        self.axis = 0  # Y-Z Axis
