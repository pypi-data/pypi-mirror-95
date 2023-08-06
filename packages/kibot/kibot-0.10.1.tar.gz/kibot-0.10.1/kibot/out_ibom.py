# -*- coding: utf-8 -*-
# Copyright (c) 2020-2021 Salvador E. Tropea
# Copyright (c) 2020-2021 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
import os
from subprocess import (check_output, STDOUT, CalledProcessError)
from .misc import (CMD_IBOM, URL_IBOM, BOM_ERROR, W_EXTNAME)
from .gs import (GS)
from .kiplot import check_script, search_as_plugin
from .out_base import VariantOptions
from .macros import macros, document, output_class  # noqa: F401
from . import log

logger = log.get_logger(__name__)
WARNING_MIX = "Avoid using it in conjunction with with IBoM native filtering options"


class IBoMOptions(VariantOptions):
    def __init__(self):
        with document:
            self.output = GS.def_global_output
            """ Filename for the output, use '' to use the IBoM filename (%i=ibom, %x=html) """
            self.dark_mode = False
            """ Default to dark mode """
            self.hide_pads = False
            """ Hide footprint pads by default """
            self.show_fabrication = False
            """ Show fabrication layer by default """
            self.hide_silkscreen = False
            """ Hide silkscreen by default """
            self.highlight_pin1 = False
            """ Highlight pin1 by default """
            self.no_redraw_on_drag = False
            """ Do not redraw pcb on drag by default """
            self.board_rotation = 0
            """ Board rotation in degrees (-180 to 180). Will be rounded to multiple of 5 """
            self.checkboxes = 'Sourced,Placed'
            """ Comma separated list of checkbox columns """
            self.bom_view = 'left-right'
            """ [bom-only,left-right,top-bottom] Default BOM view """
            self.layer_view = 'FB'
            """ [F,FB,B] Default layer view """
            self.name_format = 'ibom'
            """ Output file name format supports substitutions:
                %f : original pcb file name without extension.
                %p : pcb/project title from pcb metadata.
                %c : company from pcb metadata.
                %r : revision from pcb metadata.
                %d : pcb date from metadata if available, file modification date otherwise.
                %D : bom generation date.
                %T : bom generation time.
                Extension .html will be added automatically.
                Note that this name is used only when output is '' """
            self.include_tracks = False
            """ Include track/zone information in output. F.Cu and B.Cu layers only """
            self.include_nets = False
            """ Include netlist information in output. """
            self.sort_order = 'C,R,L,D,U,Y,X,F,SW,A,~,HS,CNN,J,P,NT,MH'
            """ Default sort order for components. Must contain '~' once """
            self.netlist_file = ''
            """ Path to netlist or xml file. You can use '%F.xml' to avoid specifying the project name.
                Leave it blank for most uses, data will be extracted from the PCB """
            self.extra_fields = ''
            """ Comma separated list of extra fields to pull from netlist or xml file """
            self.normalize_field_case = False
            """ Normalize extra field name case. E.g. 'MPN' and 'mpn' will be considered the same field """
            self.blacklist = ''
            """ List of comma separated blacklisted components or prefixes with *. E.g. 'X1,MH*'.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
            self.no_blacklist_virtual = False
            """ Do not blacklist virtual components.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
            self.blacklist_empty_val = False
            """ Blacklist components with empty value.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
            self.variant_field = ''
            """ Name of the extra field that stores board variant for component.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
            self.variants_whitelist = ''
            """ List of board variants to include in the BOM.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
            self.variants_blacklist = ''
            """ List of board variants to exclude from the BOM.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
            self.dnp_field = ''
            """ Name of the extra field that indicates do not populate status.
                Components with this field not empty will be blacklisted.
                IBoM option, avoid using in conjunction with KiBot variants/filters """
        super().__init__()
        self.add_to_doc('variant', WARNING_MIX)
        self.add_to_doc('dnf_filter', WARNING_MIX)

    def config(self):
        super().config()
        self.netlist_file = self.expand_filename('', self.netlist_file, 'ibom', 'xml')

    def get_targets(self, parent, out_dir):
        if self.output:
            return [self.expand_filename(out_dir, self.output, 'ibom', 'html')]
        logger.warning(W_EXTNAME+'{} uses a name generated by the external tool.'.format(parent))
        logger.warning(W_EXTNAME+'Please use a name generated by KiBot or specify the name explicitly.')
        return []

    def get_dependencies(self):
        files = [GS.pcb_file]
        if os.path.isfile(self.netlist_file):
            files.append(self.netlist_file)
        return files

    def run(self, output_dir):
        super().run(output_dir)
        tool = search_as_plugin(CMD_IBOM, ['InteractiveHtmlBom', 'InteractiveHtmlBom/InteractiveHtmlBom'])
        check_script(tool, URL_IBOM)
        logger.debug('Doing Interactive BoM')
        # Tell ibom we don't want to use the screen
        os.environ['INTERACTIVE_HTML_BOM_NO_DISPLAY'] = ''
        cmd = [tool, GS.pcb_file, '--dest-dir', output_dir, '--no-browser', ]
        # Solve the output name
        output = None
        if self.output:
            output = self.expand_filename(output_dir, self.output, 'ibom', 'html')
            self.name_format = 'ibom'
            cur = os.path.join(output_dir, 'ibom.html')
        # Apply variants/filters
        to_remove = ','.join(self.get_not_fitted_refs())
        if self.blacklist and to_remove:
            self.blacklist += ','
        self.blacklist += to_remove
        # Convert attributes into options
        for k, v in self.get_attrs_gen():
            if not v or k in ['output', 'variant', 'dnf_filter']:
                continue
            cmd.append(BaseOutput.attr2longopt(k))  # noqa: F821
            if not isinstance(v, bool):  # must be str/(int, float)
                cmd.append(str(v))
        # Run the command
        logger.debug('Running: '+str(cmd))
        try:
            cmd_output = check_output(cmd, stderr=STDOUT)
            cmd_output_dec = cmd_output.decode()
            # IBoM returns 0 for this error!!!
            if 'ERROR Parsing failed' in cmd_output_dec:
                raise CalledProcessError(1, cmd, cmd_output)
        except CalledProcessError as e:
            logger.error('Failed to create BoM, error %d', e.returncode)
            if e.output:
                logger.debug('Output from command: '+e.output.decode())
            exit(BOM_ERROR)
        logger.debug('Output from command:\n'+cmd_output_dec+'\n')
        if output:
            logger.debug('Renaming output file: {} -> {}'.format(cur, output))
            os.rename(cur, output)


@output_class
class IBoM(BaseOutput):  # noqa: F821
    """ IBoM (Interactive HTML BoM)
        Generates an interactive web page useful to identify the position of the components in the PCB.
        For more information: https://github.com/INTI-CMNB/InteractiveHtmlBom
        This output is what you get from the InteractiveHtmlBom plug-in (pcbnew). """
    def __init__(self):
        super().__init__()
        with document:
            self.options = IBoMOptions
            """ [dict] Options for the `ibom` output """

    def get_dependencies(self):
        return self.options.get_dependencies()
