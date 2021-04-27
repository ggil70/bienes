# -*- coding: utf-8 -*-

from odoo import api, fields, models



from odoo.exceptions import ValidationError

#import logging, csv, operator
##Definimos la Variable Global
#_logger = logging.getLogger(__name__)
import logging.config




class ListadoBienMarcaReporteWizard(models.TransientModel):
    _name = 'bienes.marca.bien.reporte.wizard'
    bienes_grupo_id = fields.Many2one('grupo_bien',string='Grupo del Bien', required=True, 
                                        help='Seleccione Grupo del Bien')
    bienes_clasificador_id = fields.Many2one('clasificador_bien', 'Clasificador', domain="[('grupo_bien_id','=',bienes_grupo_id)]",
                         required=True, help='Seleccione Clasificador del Bien')
                         
    bienes_marcas_id = fields.Many2one('marcas', 'Marca del Bien', required=True,
                         help='Seleccione Modelo del Bien')


    bienes_marcas_id = fields.Many2one('marcas', 'Marca del Bien', required=True,
                         help='Seleccione Modelo del Bien')





    @api.onchange('bienes_grupo_id')
    def onchange_grupo(self):
        self.bienes_clasificador_id =  ''
        self.bienes_modelo_id =  ''

    #@api.onchange('bienes_marcas_id')
    #def onchange_marcas(self):
    #    self.modelo_fab_id =  ''

    
    
    def action_report_clasificacion_marca_bienes(self):
        grupo_id = self.bienes_grupo_id.id
        grupo = self.bienes_grupo_id.grupo_bien_nombre.strip()
        grupo = grupo.upper()
        consulta = "GRUPO = " + grupo

        domain = []
        #domain = [('grupo_bien_id','=',grupo_id)]

        clasificador_id = self.bienes_clasificador_id.id
        #domain = [('clasificador_bien_id','=',clasificador_id)]
        clasificador = self.bienes_clasificador_id.clasificador_nombre.strip()
        clasificador = clasificador.upper()
        consulta = consulta + " / CLASIFICADOR = " + clasificador 


        marca_id = self.bienes_marcas_id.id
        #domain = [('marcas_id','=',marca_id)]
        domain = [('clasificador_bien_id','=',clasificador_id),('marcas_id','=',marca_id)]
        marca = self.bienes_marcas_id.marcas_nombre.strip()
        marca = marca.upper()
        consulta = consulta + " / MARCA = " + marca

        #modelo_id = self.modelo_fab_id.id
        #if modelo_id:
        #    domain = [('modelo_fab_id','=',modelo_id)]
        #    modelo = self.modelo_fab_id.id.modelo_fab_nombre.strip()
        #    modelo = modelo.upper()
        #    consulta = consulta + " / MODELO DE FABRICA = " + modelo 


        today = fields.Datetime.now()
        fecha = today.strftime('%d/%m/%Y')
        
        #fecha = str(today.day) + "/" + str(today.month) + "/" + str(today.year)  
      
        grupo_marca_data = self.env['bienes'].search_read(domain ,order='grupo_bien_id, clasificador_bien_id, modelo_bien_id, bienes_numbien asc')
        
        #cantidad = self.env['bienes'].search_count(domain)
        cantidad = len(grupo_marca_data)
        
        datas = {
            'ids' : self.env.context.get('active_ids',[]),
            'consulta' : consulta,
            'nro_bienes' : cantidad,
            'grupo': grupo,
            'marca':marca
            
        }         
        
        if cantidad == 0:
            raise ValidationError('No existen Bienes asociado a la consulta realizada')
        else:
            datas['grupo_marca_data'] = grupo_marca_data
            return self.env.ref('bienes.action_report_bien_clasificacion_marca').report_action(self, data=datas)
   
            
            
            
