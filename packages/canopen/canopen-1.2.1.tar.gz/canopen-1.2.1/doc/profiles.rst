Device profiles
================

On top of the standard CANopen functionality which includes the DS301
application layer there can be additional profiles specifically for certain
applications.

CiA 402 CANopen device profile for motion controllers and drives
----------------------------------------------------------------

This device profile has a control state machine for controlling the behaviour
of the drive. Therefore one needs to instantiate a node with the
:class:`BaseNode402` class

Create a node with BaseNode402::

    import canopen
    from canopen.profiles.p402 import BaseNode402

    some_node = BaseNode402(3, 'someprofile.eds')
    network = canopen.Network()
    network.add_node(some_node)

The Power State Machine
````````````````````````

The :class:`PowerStateMachine` class provides the means of controlling the
states of this state machine. The static method `on_PDO1_callback()` is added
to the TPDO1 callback.

State changes can be controlled by writing a specific value to register
0x6040, which is called the "Controlword".
The current status can be read from the device by reading the register
0x6041, which is called the "Statusword".
Changes in state can only be done in the 'OPERATIONAL' state of the NmtMaster

TPDO1 needs to be set up correctly. For this, run the the
`BaseNode402.setup_402_state_machine()` method. Note that this setup
routine will change only TPDO1 and automatically go to the 'OPERATIONAL' state
of the NmtMaster::

    # run the setup routine for TPDO1 and it's callback
    some_node.setup_402_state_machine()

Write Controlword and read Statusword::

    # command to go to 'READY TO SWITCH ON' from 'NOT READY TO SWITCH ON' or 'SWITCHED ON'
    some_node.sdo[0x6040].raw = 0x06

    # Read the state of the Statusword
    some_node.sdo[0x6041].raw

During operation the state can change to states which cannot be commanded
by the Controlword, for example a 'FAULT' state.
Therefore the :class:`PowerStateMachine` class (in similarity to the :class:`NmtMaster`
class) automatically monitors state changes of the Statusword which is sent
by TPDO1. The available callback on thet TPDO1 will then extract the
information and mirror the state change in the :attr:`BaseNode402.powerstate_402`
attribute.

Similar to the :class:`NmtMaster` class, the states of the :class:`BaseNode402`
class :attr:`._state` attribute can be read and set (command) by a string::

    # command a state (an SDO message will be called)
    some_node.powerstate_402.state = 'SWITCHED ON'
    # read the current state
    some_node.powerstate_402.state = 'SWITCHED ON'

Available states:

- 'NOT READY TO SWITCH ON'
- 'SWITCH ON DISABLED'
- 'READY TO SWITCH ON'
- 'SWITCHED ON'
- 'OPERATION ENABLED'
- 'FAULT'
- 'FAULT REACTION ACTIVE'
- 'QUICK STOP ACTIVE'

Available commands

- 'SWITCH ON DISABLED'
- 'DISABLE VOLTAGE'
- 'READY TO SWITCH ON'
- 'SWITCHED ON'
- 'OPERATION ENABLED'
- 'QUICK STOP ACTIVE'
