# -*- coding: utf-8 -*-
# Copyright (c) 2020-2021 Salvador E. Tropea
# Copyright (c) 2020-2021 Instituto Nacional de Tecnología Industrial
# Copyright (c) 2020 @nerdyscout
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
import os
from tempfile import mkdtemp
from shutil import rmtree
from .gs import (GS)
from .kiplot import check_eeschema_do, exec_with_retry, add_extra_options
from .misc import (CMD_EESCHEMA_DO, SVG_SCH_PRINT)
from .out_base import VariantOptions
from .macros import macros, document, output_class  # noqa: F401
from . import log

logger = log.get_logger(__name__)


class SVG_Sch_PrintOptions(VariantOptions):
    def __init__(self):
        with document:
            self.output = GS.def_global_output
            """ Filename for the output SVG (%i=schematic %x=svg) """
        super().__init__()
        self.add_to_doc('variant', "Not fitted components are crossed")

    def get_targets(self, parent, out_dir):
        id = 'schematic'
        ext = 'svg'
        if self.output:
            return [self.expand_filename_sch(out_dir, self.output, id, ext)]
        return [self.expand_filename_sch(out_dir, '%f.%x', id, ext)]

    def run(self, output_dir):
        super().run(output_dir)
        check_eeschema_do()
        if self._comps:
            # Save it to a temporal dir
            sch_dir = mkdtemp(prefix='tmp-kibot-svg_sch_print-')
            fname = GS.sch.save_variant(sch_dir)
            sch_file = os.path.join(sch_dir, fname)
        else:
            sch_dir = None
            sch_file = GS.sch_file
        cmd = [CMD_EESCHEMA_DO, 'export', '--all_pages', '--file_format', 'svg', sch_file, output_dir]
        cmd, video_remove = add_extra_options(cmd)
        ret = exec_with_retry(cmd)
        if ret:
            logger.error(CMD_EESCHEMA_DO+' returned %d', ret)
            exit(SVG_SCH_PRINT)
        if self.output:
            id = 'schematic'
            ext = 'svg'
            cur = self.expand_filename_sch(output_dir, '%f.%x', id, ext)
            new = self.expand_filename_sch(output_dir, self.output, id, ext)
            logger.debug('Moving '+cur+' -> '+new)
            os.rename(cur, new)
        # Remove the temporal dir if needed
        if sch_dir:
            logger.debug('Removing temporal variant dir `{}`'.format(sch_dir))
            rmtree(sch_dir)
        if video_remove:
            video_name = os.path.join(GS.out_dir, 'export_eeschema_screencast.ogv')
            if os.path.isfile(video_name):
                os.remove(video_name)


@output_class
class SVG_Sch_Print(BaseOutput):  # noqa: F821
    """ SVG Schematic Print
        Exports the PCB. Suitable for printing.
        This is a format to document your schematic. """
    def __init__(self):
        super().__init__()
        with document:
            self.options = SVG_Sch_PrintOptions
            """ [dict] Options for the `svg_sch_print` output """
        self._sch_related = True
