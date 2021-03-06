# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS). 
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains 
# certain rights in this software.

from avatar2.archs.architecture import *
from avatar2.archs import avr as avatararch
from avatar2 import Avatar, QemuTarget
from halucinator.util.logging import *
from .. import Architecture

class AVRQemuTarget(QemuTarget):
    '''
        Implements a QEMU target that has function args for use with
        halucinator.  Enables read/writing and returning from
        functions in a calling convention aware manner
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def architecture(self):
        return Architecture.AVR8

    def get_arg(self, idx):
        print("------ get_arg: ignored")
        '''
            Gets the value for a function argument (zero indexed)

            :param idx  The argument index to return
            :returns    Argument value
        '''
        pass

    def set_arg(self, idx, value):
        print("------ set_arg: ignored")
        '''
            Sets the value for a function argument (zero indexed)


            :param idx      The argument index to return
            :param value    Value to set index to 
        '''
        pass

    def get_ret_addr(self):
        print("------ get_ret_addr: ignored")
        '''
            Gets the return address for the function call

            :returns Return address of the function call
        '''
        pass

    def set_ret_addr(self, ret_addr):
        print("------ set_ret_addr: ignored")
        '''
            Sets the return address for the function call
            :param ret_addr Value for return address
        '''
        pass

    def execute_return(self, ret_value):
        print("------ execute_return: ignored")
        pass

    def get_symbol_name(self, addr):
        """
        Get the symbol for an address

        :param addr:    The name of a symbol whose address is wanted
        :returns:         (Symbol name on success else None
        """

        return self.avatar.config.get_symbol_name(addr)


PATCH_MEMORY_SIZE = 4096
INTERCEPT_RETURN_INSTR_ADDR = 0x4000 - PATCH_MEMORY_SIZE


def add_patch_memory(avatar):
    ''' 
        Use a patch memory to return from intercepted functions, as 
        it allows tracking number of intercepts
    '''

    log.info("Adding Patch Memory %s:%i" %
             (hex(INTERCEPT_RETURN_INSTR_ADDR), PATCH_MEMORY_SIZE))
    #avatar.add_memory_range(INTERCEPT_RETURN_INSTR_ADDR, PATCH_MEMORY_SIZE,
    #                        name='patch_memory', permissions='rwx')


def write_patch_memory(qemu):
    print("--- Write patch memory ignored")


    RET_INSTRUCTION = 0x9508


    pass


def arch_specific_setup(config, qemu):

    qemu.regs.sp = qemu.init_sp
    return


def resolve_avatar_cpu(config):
    # TODO: Select Uno or Mega2560.
    return avatararch.AVR_UNO


emulator = AVRQemuTarget
