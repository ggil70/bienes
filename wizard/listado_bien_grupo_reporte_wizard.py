# -*- coding: utf-8 -*-

from odoo import api, fields, models



from odoo.exceptions import ValidationError

#import logging, csv, operator
##Definimos la Variable Global
#_logger = logging.getLogger(__name__)
import logging.config




class ListadoBienGrupoReporteWizard(models.TransientModel):
    _name = 'bienes.grupo.bien.reporte.wizard'
    bienes_grupo_id = fields.Many2one('grupo_bien',string='Grupo del Bien', required=True, 
                                        help='Seleccione Grupo del Bien')
    bienes_clasificador_id = fields.Many2one('clasificador_bien', 'Clasificador', domain="[('grupo_bien_id','=',bienes_grupo_id)]",
                         help='Seleccione Clasificador del Bien')
                         
    bienes_modelo_id = fields.Many2one('modelo_bien', 'Modelo del Bien', domain="[('clasificador_id','=',bienes_clasificador_id)]",
                         help='Seleccione Modelo del Bien')




    @api.onchange('bienes_grupo_id')
    def onchange_grupo(self):
        self.bienes_clasificador_id =  ''
        self.bienes_modelo_id =  ''


    @api.onchange('bienes_clasificador_id')
    def onchange_clasificador(self):
        self.bienes_modelo_id =  ''  



    def action_report_grupo_bienes(self):
        grupo_id = self.bienes_grupo_id.id
        grupo = self.bienes_grupo_id.grupo_bien_nombre.strip()
        grupo = grupo.upper()
        consulta = "GRUPO = " + grupo

        domain = []
        domain = [('grupo_bien_id','=',grupo_id)]

        clasificador_id = self.bienes_clasificador_id.id
        if clasificador_id:
            domain = [('clasificador_bien_id','=',clasificador_id)]
            clasificador = self.bienes_clasificador_id.clasificador_nombre.strip()
            clasificador = clasificador.upper()
            consulta = consulta + " / CLASIFICADOR = " + clasificador 
            
        modelo_id = self.bienes_modelo_id.id
        if modelo_id:
            domain = [('modelo_bien_id','=',modelo_id)]
            modelo = self.bienes_modelo_id.modelo_nombre.strip()
            modelo = modelo.upper()
            consulta = consulta + " / MODELO = " + modelo
            
        today = fields.Datetime.now()
        fecha = today.strftime('%d/%m/%Y')
        
        #fecha = str(today.day) + "/" + str(today.month) + "/" + str(today.year)  
      
        grupo_data = self.env['bienes'].search_read(domain)
        
        #cantidad = self.env['bienes'].search_count(domain)
        cantidad = len(grupo_data)
        
        datas = {
            'ids' : self.env.context.get('active_ids',[]),
            'consulta' : consulta,
            'nro_bienes' : cantidad,
            'grupo': grupo
        }         
        
        if cantidad == 0:
            raise ValidationError('No existen Bienes asociado a la consulta realizada')
        else:
            datas['grupo_data'] = grupo_data
            return self.env.ref('bienes.action_report_bien_grupo').report_action(self, data=datas)
   
            
            
            
