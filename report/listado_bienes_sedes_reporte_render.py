# -*- coding= utf-8 -*-

from odoo import api, fields, models
from odoo.tools import float_round
from odoo.exceptions import ValidationError

class ReporteFichaOficinaListadoRender(models.AbstractModel):
    _name = "report.bienes.listado_bienes_sedes_reporte_render"
    
    def m_observacion(self, observa):
        
        
        if observa == None:
            return observa
        else:   
            observa = str(observa)
            if len(observa) > 120:
                observa = observa[0:115] + "[...]"        
            return observa


    #def f_costo(self, costo):
    #    costo_f = "{0:.7f}".format(costo)
    #    return costo_f


        
    @api.model
    def _get_report_values(self, docids, data):
        """in this function can access the data returned from the button
        click function"""
        today = fields.Datetime.now()
        fecha = today.strftime('%d/%m/%Y')
        
        
        return {
            'docs': data['bienes_data'],
            'sede':data["sede"],
            #'oficina':data["oficina"],
            'nro_bienes':data["nro_bienes"],
            'date_today': fecha,
            'm_observacion': self.m_observacion,
            #'f_costo': self.f_costo,
            #'tot_costo': data["tot_costo"],
        }
        
