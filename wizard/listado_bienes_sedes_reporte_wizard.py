# -*- coding: utf-8 -*-

from odoo import api, fields, models



from odoo.exceptions import ValidationError

#import logging, csv, operator
##Definimos la Variable Global
#_logger = logging.getLogger(__name__)
import logging.config




class ListadoBienesSedesReporteWizard(models.TransientModel):
    _name = 'bienes.listado.bienes.sedes.reporte.wizard'
                      
    bienes_sedes_id = fields.Many2one('sedes',string='Sedes del Organismo', required=True, 
                          help='Seleccione Sedes del Organismo')


  


    def action_report_bienes_sedes(self):
        sedes_id = self.bienes_sedes_id.id
        
        
        
        sede = self.bienes_sedes_id.sedes_nombre
        
        model_id = ''
        query = "SELECT bi.*, ofi.oficinas_nombre, per.personas_pnombre, per.personas_papellido, eb.estado_bien_nombre " 
        query = query + "FROM bienes as bi "
        query = query + "inner join oficinas ofi on bi.bienes_oficinas_id = ofi.id "
        query = query + "inner join personas per on bi.resp_uso_id = per.id "
        query = query + "left join estado_bien eb on bi.estado_bien_id = eb.id "
        query = query + "where bi.bienes_sedes_id = " + str(sedes_id) + " and bi.active = true and inventario_inicial=1 "
        query = query + "order by ofi.oficinas_nombre, bienes_numbien " 
        
         
        #if date_init:
        #    query = query . "WHERE ee.fecha_pago <= '" + date_init 


        #value.append(model_id)
        value=''
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()        
        
        cantidad = len(record)
                
        datas = {
            'ids' : self.env.context.get('active_ids',[]),
            'sede' : sede,
            'nro_bienes' : cantidad,
        }         
        
        if cantidad == 0:
            raise ValidationError('No existen Bienes asociado a la consulta realizada')
        else:
            datas['bienes_data'] = record
            return self.env.ref('bienes.action_report_bienes_sedes').report_action(self, data=datas)
   
            
            
            

        
        
        
        

        
        
        
        
        #raise ValidationError('Hay Datos ' + str(oficina))
        
        ##fields = ['nombre','fecha_pago','estudiante_tarifa']
        #bienes_data = self.env['bienes'].search_read(domain, fields)

        #if bienes_data:
        #   raise ValidationError('Hay Datos')
        #raise ValidationError('NOOOOO Hay Datos')    


        #datas['estudiante_data'] = estudiante_data     
        #return self.env.ref('escuela.action_report_personalizado_estudiante').report_action(self, data=datas)




        #datas = {
        #    'ids' : self.env.context.get('active_ids',[]),
        #    'title' : self.title, 
        #    'date_init' : self.date_init,          
        #}
        #value=[]

        #Con execute
        
        
        #query = """SELECT * FROM escuela_estudiante as ee """
        #if self.date_init:
        #   date_init = str(self.date_init)
        #   query = query + "WHERE ee.fecha_pago <= '" + date_init + "'"
        #self._cr.execute(query, value)

        #record = self._cr.dictfetchall()
        #datas['estudiante_data'] = record
        #return self.env.ref('escuela.action_report_personalizado_estudiante').report_action(self, data=datas)


        #Sin execute 

        #domain = []
        #if self.date_init:
        #    domain = [('fecha_pago','<=',datas["date_init"])]
        #fields = ['nombre','fecha_pago','estudiante_tarifa']
        #estudiante_data = self.env['escuela.estudiante'].search_read(domain,fields)
        #datas['estudiante_data'] = estudiante_data     
        #return self.env.ref('escuela.action_report_personalizado_estudiante').report_action(self, data=datas)
        
        

            
