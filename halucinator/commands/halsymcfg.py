#!/usr/bin/env python

import os
import sys
from halucinator.util.hexyaml import hexint_presenter
import yaml

def addressfile_transform(infile, outfile):
    
    addryaml = None
    with open(infile, 'rb') as f:
        addryaml = yaml.load(f, Loader=yaml.FullLoader)

    yaml.add_representer(int, hexint_presenter)
   
#- addr: 0x800208c
#  class: halucinator.bp_handlers.generic.armv7m_param_log.ARMv7MEABILogger 
#  registration_args: {params: [r0], ret_val: null}
#  function: HAL_Delay

    def construct_intercept_object(addr, func):
        return {
            "addr": addr,
            "class": "halucinator.bp_handlers.generic.armv7m_param_log.ARMv7MEABILogger",
            "function": func,
        }

    # take each intercept and produce an object of the form above
    intercepts = list(map(lambda a: construct_intercept_object(a[0], a[1]), 
                          addryaml["symbols"].items()))


    intercept_object = {"intercepts": intercepts}
    outputyaml = yaml.dump(intercept_object)
    with open(outfile, 'wb+') as w:
        w.write(outputyaml.encode("utf-8"))

def main():
    '''
    Gets Symbols from elf file using the symbols table in the elf
    '''
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-a', '--addrfile', required=True,
                   help='HALucinator Addresses file generated by halsymtool')
    p.add_argument('-o', '--out', required=False,
                   help='YAML file to save output to' +
                   'if will be output to (addrfile)_configtemplate.yaml')

    args = p.parse_args()
    
    if args.addrfile == None:
        print("Address File must be supplied")
    addrfile = args.addrfile

    if args.out == None:
        
        addrbase, addrext = os.path.splitext(addrfile)
        outfile = addrbase + "_configtemplate.yaml"
    else:
        outfile = args.outfile

    addressfile_transform(addrfile, outfile) 
    #except Exception as e:
    #    print("Exception occurred transforming address file\n")
    #    print(e)

if __name__ == '__main__':
    main()    




