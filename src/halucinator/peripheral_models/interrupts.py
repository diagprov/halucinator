# Copyright 2018 National Technology & Engineering Solutions of Sandia, LLC 
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, there is a 
# non-exclusive license for use of this work by or on behalf of the U.S. 
# Government. Export of this data may require a license from the United States 
# Government.

import peripheral_server
from collections import deque, defaultdict
import logging
log = logging.getLogger("Interrupts")
# log.setLevel(logging.DEBUG)

@peripheral_server.peripheral_model  # Register the pub/sub calls and methods that need mapped
class Interrupts(object):
    '''
        Models and external interrupt controller
        Use when need to trigger and interrupt and need additional state
        about it
    '''
    Active_Interrupts = defaultdict(bool)

    @classmethod
    @peripheral_server.reg_rx_handler
    def interrupt_request(cls, msg):
        log.info("Int Request: %s" % str(msg))
        isr_num = msg['num']
        source = msg['source'] if 'source' in msg else None
        cls.trigger_interrupt(isr_num, source)
    
    @classmethod
    def trigger_interrupt(cls, isr_num, source=None):
        if source is not None:
            cls.set_active(source)
        log.info("Triggering Interrupt: %i" % isr_num)
        peripheral_server.trigger_interrupt(isr_num)

    @classmethod
    def set_active(cls, key):
        log.debug("Set Active: %s" % str(key))
        cls.Active_Interrupts[key] = True

    @classmethod
    def clear_active(cls, key):
        log.debug("Clear Active: %s" % str(key))
        cls.Active_Interrupts[key] = False

    @classmethod
    def is_active(cls, key):
        log.debug("Is Active: %s" % str(key))
        return cls.Active_Interrupts[key]