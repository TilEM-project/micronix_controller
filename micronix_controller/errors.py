from enum import Enum

class ErrorMessages(Enum):
    RECEIVE_BUFFER_OVERRUN = (10, "Receive Buffer Overrun: The Receive Buffer has reached or exceeded maximum capacity.")
    MOTOR_DISABLED = (11, "Motor Disabled: The command that triggered this error was trying to move the servo while it was disabled.")
    NO_ENCODER_DETECTED = (12, "No Encoder Detected: The command that triggered this error was trying to access encoder data when no encoder was attached.")
    INDEX_NOT_FOUND = (13, "Index Not Found: The controller moved across the full range of motion and did not find an index.")
    HOME_REQUIRES_ENCODER = (14, "Home Requires Encoder: The HOM command requires an encoder signal.")
    MOVE_LIMIT_REQUIRES_ENCODER = (15, "Move Limit Requires Encoder: The MLN and MLP commands require an encoder signal.")
    COMMAND_IS_READ_ONLY = (20, "Command is Read Only: The command that triggered this error only supports read operations. The command must be followed by a question mark to be accepted. Ex: XXX?")
    ONE_READ_OPERATION_PER_LINE = (21, "One Read Operation Per Line: Multiple read operations on the same command line. Only one read operation is allowed per line, even if addressed to separate axes.")
    TOO_MANY_COMMANDS_ON_LINE = (22, "Too Many Commands On Line: The maximum number of allowed commands per command line has been exceeded. No more than 8 commands are allowed on a single command line.")
    LINE_CHARACTER_LIMIT_EXCEEDED = (23, "Line Character Limit Exceeded: The maximum number of characters per command line has been exceeded. Each line has an 80 character limit.")
    MISSING_AXIS_NUMBER = (24, "Missing Axis Number: The controller could not find an axis number or the beginning of an instruction. Check the beginning of the command for erroneous characters.")
    MALFORMED_COMMAND = (25, "Malformed Command: The controller could not find a 3-letter instruction in the input. Check to ensure that each instruction in the line has exactly 3 letters referring to a command.")
    INVALID_COMMAND = (26, "Invalid Command: The 3-letter instruction entered is not a valid command. Ensure that the 3-letter instruction is a recognizable command.")
    GLOBAL_READ_OPERATION_REQUEST = (27, "Global Read Operation Request: A read request for a command was entered without an axis number. A read request cannot be used in a global context.")
    INVALID_PARAMETER_TYPE = (28, "Invalid Parameter Type: The parameter entered does not correspond to the type of number that the instruction requires or the allowable precision for a parameter has been exceeded.")
    INVALID_CHARACTER_IN_PARAMETER = (29, "Invalid Character in Parameter: There is an alpha character in a parameter that should be a numeric character.")
    COMMAND_CANNOT_BE_USED_IN_GLOBAL_CONTEXT = (30, "Command Cannot Be Used In Global Context: The command entered must be addressed to a specific axis number. Not all commands can be used in a global context.")
    PARAMETER_OUT_OF_BOUNDS = (31, "Parameter Out Of Bounds: The parameter is out of bounds. The current state of the controller will not allow this parameter to be used.")
    INCORRECT_JOG_VELOCITY_REQUEST = (32, "Incorrect Jog Velocity Request: The jog velocity can only be changed during motion by using a new JOG command. If the VEL command is used to change the velocity, this error will be triggered.")
    NOT_IN_JOG_MODE = (33, "Not In Jog Mode: Sending a JOG command during motion initiated by a move command will trigger this error. To initiate Jog Mode, the controller should be at stand-still.")
    TRACE_ALREADY_IN_PROGRESS = (34, "Trace Already In Progress: This error is triggered when a new trace command is received after a trace is already in progress.")
    TRACE_DID_NOT_COMPLETE = (35, "Trace Did Not Complete: An error occurred while recording trace data. Try the operation again.")
    COMMAND_CANNOT_BE_EXECUTED_DURING_MOTION = (36, "Command Cannot Be Executed During Motion: Only certain commands can be executed when motion is in progress.")
    MOVE_OUTSIDE_SOFT_LIMITS = (37, "Move Outside Soft Limits: If a requested move will take the controller outside of the preset travel limits, then the command will not be executed.")
    READ_NOT_AVAILABLE_FOR_THIS_COMMAND = (38, "Read Not Available For This Command: This error is triggered by a read request from a command that does not support a read operation.")
    PROGRAM_NUMBER_OUT_OF_RANGE = (39, "Program Number Out of Range: The number entered for the program number was either less than 1 or greater than 16.")
    PROGRAM_SIZE_LIMIT_EXCEEDED = (40, "Program Size Limit Exceeded: The program has exceeded the character limit of 4 Kb.")
    PROGRAM_FAILED_TO_RECORD = (41, "Program failed to Record: Error in recording program. Erase program and try operation again.")
    END_COMMAND_MUST_BE_ON_ITS_OWN_LINE = (42, "End Command Must Be on its Own Line: The End command used to end a program must be on a separate line from all other instructions.")
    FAILED_TO_READ_PROGRAM = (43, "Failed to Read Program: An error occurred while trying to read a program. Try the Operation again.")
    COMMAND_ONLY_VALID_WITHIN_PROGRAM = (44, "Command Only Valid Within Program: The command that triggered this error is only suitable for use within a program.")
    PROGRAM_ALREADY_EXISTS = (45, "Program Already Exists: A program already exists for the indicated program parameter. The program must be erased with the ERA command before being written again.")
    PROGRAM_DOES_NOT_EXIST = (46, "Program Doesn’t Exist: The indicated program does not exist. This error can occur when you try to execute a program number that has not had a program assigned to it.")
    READ_OPERATIONS_NOT_ALLOWED_INSIDE_PROGRAM = (47, "Read Operations Not Allowed Inside Program: Read Operations are not permitted in programs.")
    COMMAND_NOT_ALLOWED_WHILE_PROGRAM_IN_PROGRESS = (48, "Command Not Allowed While Program in Progress: The command that triggered this error was given while a program was executing.")
    LIMIT_ACTIVATED = (50, "Limit Activated: Motion in the direction of the activated limit switch is disallowed if limit switches are enabled.")
    END_OF_TRAVEL_LIMIT = (51, "End of Travel Limit: The requested move will take the controller outside of its valid travel range, therefore the move is disallowed.")
    HOME_IN_PROGRESS = (52, "Home In Progress: A Home or a Move To Limit Procedure is in progress. Motion commands are disallowed during this time.")
    IO_FUNCTION_ALREADY_IN_USE = (53, "IO Function Already In Use: The I/O Function in question is already assigned to another I/O pin.")
    LIMITS_ARE_NOT_CONFIGURED_PROPERLY = (55, "Limits Are Not Configured Properly: Both Limit Switches are active, so motion is disallowed in both directions. Most likely the LPL (Limit Polarity command) setting should be switched.")
    COMMAND_NOT_AVAILABLE_IN_THIS_VERSION = (80, "Command Not Available in this Version: The command entered is not supported in this version of the firmware.")
    ANALOG_ENCODER_NOT_AVAILABLE_IN_THIS_VERSION = (81, "Analog Encoder Not Available In this Version: The current version of firmware installed does not support analog encoders.")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @property
    def message(self):
        return f"{self.name}: {self.description}"
