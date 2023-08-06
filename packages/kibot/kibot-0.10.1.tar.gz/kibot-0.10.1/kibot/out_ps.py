# -*- coding: utf-8 -*-
# Copyright (c) 2020 Salvador E. Tropea
# Copyright (c) 2020 Instituto Nacional de Tecnología Industrial
# Copyright (c) 2018 John Beard
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
# Adapted from: https://github.com/johnbeard/kiplot
from pcbnew import PLOT_FORMAT_POST, FromMM, ToMM, SKETCH, FILLED
from .misc import AUTO_SCALE
from .out_any_layer import AnyLayer
from .drill_marks import DrillMarks
from .gs import GS
from .misc import KICAD_VERSION_5_99
from .macros import macros, document, output_class  # noqa: F401


class PSOptions(DrillMarks):
    def __init__(self):
        super().__init__()
        with document:
            self.line_width = 0.15
            """ [0.02,2] For objects without width [mm] (KiCad 5) """
            self.mirror_plot = False
            """ Plot mirrored """
            self.negative_plot = False
            """ Invert black and white """
            self.sketch_plot = False
            """ Don't fill objects, just draw the outline """
            self.scaling = 1
            """ Scale factor (0 means autoscaling)"""
            self.scale_adjust_x = 1.0
            """ Fine grain adjust for the X scale (floating point multiplier) """
            self.scale_adjust_y = 1.0
            """ Fine grain adjust for the Y scale (floating point multiplier) """
            self.width_adjust = 0
            """ This width factor is intended to compensate PS printers/plotters that do not strictly obey line width settings.
                Only used to plot pads and tracks """
            self.a4_output = True
            """ force A4 paper size """
        self._plot_format = PLOT_FORMAT_POST

    def _configure_plot_ctrl(self, po, output_dir):
        super()._configure_plot_ctrl(po, output_dir)
        po.SetWidthAdjust(self.width_adjust)
        po.SetFineScaleAdjustX(self.scale_adjust_x)
        po.SetFineScaleAdjustX(self.scale_adjust_y)
        po.SetA4Output(self.a4_output)
        po.SetPlotMode(SKETCH if self.sketch_plot else FILLED)
        if GS.kicad_version_n < KICAD_VERSION_5_99:
            po.SetLineWidth(FromMM(self.line_width))
        po.SetNegative(self.negative_plot)
        po.SetMirror(self.mirror_plot)
        # Scaling/Autoscale
        if self.scaling == AUTO_SCALE:
            po.SetAutoScale(True)
            po.SetScale(1)
        else:
            po.SetAutoScale(False)
            po.SetScale(self.scaling)

    def read_vals_from_po(self, po):
        super().read_vals_from_po(po)
        self.width_adjust = po.GetWidthAdjust()
        self.scale_adjust_x = po.GetFineScaleAdjustX()
        self.scale_adjust_y = po.GetFineScaleAdjustX()
        self.a4_output = po.GetA4Output()
        self.sketch_plot = po.GetPlotMode() == SKETCH
        if GS.kicad_version_n < KICAD_VERSION_5_99:
            self.line_width = ToMM(po.GetLineWidth())
        self.negative_plot = po.GetNegative()
        self.mirror_plot = po.GetMirror()
        # scaleselection
        sel = po.GetScaleSelection()
        sel = sel if sel < 0 or sel > 4 else 4
        self.scaling = (AUTO_SCALE, 1.0, 1.5, 2.0, 3.0)[sel]


@output_class
class PS(AnyLayer):
    """ PS (Postscript)
        Exports the PCB to a format suitable for printing.
        This output is what you get from the File/Plot menu in pcbnew. """
    def __init__(self):
        super().__init__()
        with document:
            self.options = PSOptions
            """ [dict] Options for the `ps` output """
