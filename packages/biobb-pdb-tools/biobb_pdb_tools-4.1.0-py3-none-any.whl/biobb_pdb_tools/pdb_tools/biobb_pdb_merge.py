#!/usr/bin/env python3

"""Module containing the Pdbmerge class and the command line interface."""
import argparse
import shutil
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


# 1. Rename class as required
class Pdbmerge(BiobbObject):
    """
    | biobb_pdb_tools Pdbmerge
    | Merges several PDB files into one.

    Args:       
        input_file_path1 (str): PDB file of selected protein. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_pdb_tools/master/biobb_pdb_tools/test/data/pdb_tools/input_pdb_merge1.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_file_path2 (str): PDB file for another selected protein. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_pdb_tools/master/biobb_pdb_tools/test/data/pdb_tools/input_pdb_merge2.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_file_path (str): PDB file with input PDBs merged. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_pdb_tools/master/biobb_pdb_tools/test/reference/pdb_tools/ref_pdb_merge.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic):
            * **binary_path** (*str*) - ("pdb_merge") Example of executable binary property.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pdb_tools.pdb_tools.biobb_pdb_merge import Pdbmerge

            prop = { 
                'binary_path': pdb_merge
            }
            biobb_pdb_merge(input_file_path1='/path/to/input1.pdb',
                    input_file_path2='/path/to/input2.pdb',
                    output_file_path='/path/to/output.pdb',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: pdb_tools
            * version: >=2.5.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self,  input_file_path1, input_file_path2, output_file_path,
                 properties = None, **kwargs) -> None:
        properties = properties or {}

        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        self.io_dict = { 
            'in': { 'input_file_path1': input_file_path1, 'input_file_path2': input_file_path2 }, 
            'out': { 'output_file_path': output_file_path } 
        }

        self.binary_path = properties.get('binary_path', 'pdb_merge')
        self.properties = properties

        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Pdbmerge <biobb_pdb_tools.pdb_tools.pdb_merge>` object."""

        if self.check_restart(): return 0
        self.stage_files()

        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        shutil.copy(self.io_dict['in']['input_file_path1'], self.tmp_folder)

        self.cmd = [self.binary_path,
                self.io_dict['in']['input_file_path1'],
                self.io_dict['in']['input_file_path2'],
                '>',
                self.io_dict['out']['output_file_path']
        ]

        print(self.cmd)
        
        fu.log('Creating command line with instructions and required arguments', self.out_log, self.global_log)

        if self.io_dict['in']['input_file_path2']:
            shutil.copy(self.io_dict['in']['input_file_path2'], self.tmp_folder)
            self.cmd.append(str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path2']).name)))
            fu.log('Appending optional argument to command line', self.out_log, self.global_log)

        self.run_biobb()
        self.copy_to_host()

        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
            self.tmp_folder
        ])
        self.remove_tmp_files()
        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def biobb_pdb_merge(input_file_path1: str,input_file_path2: str, output_file_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Pdbmerge <biobb_pdb_tools.pdb_tools.pdb_merge>` class and
    execute the :meth:`launch() <biobb_pdb_tools.pdb_tools.pdb_merge.launch>` method."""
    return Pdbmerge(input_file_path1=input_file_path1, 
                    input_file_path2=input_file_path2,
                    output_file_path=output_file_path,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Merges several PDB files into one.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=True, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_file_path1', required=True, help='Description for the first input file path. Accepted formats: pdb.')
    parser.add_argument('--input_file_path2', required=True, help='Description for the second input file path (optional). Accepted formats: pdb.')
    required_args.add_argument('--output_file_path', required=True, help='Description for the output file path. Accepted formats: zip.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()
    biobb_pdb_merge(input_file_path1=args.input_file_path1, 
            input_file_path2=args.input_file_path2,
            output_file_path=args.output_file_path, 
            properties=properties)

if __name__ == '__main__':
    main()