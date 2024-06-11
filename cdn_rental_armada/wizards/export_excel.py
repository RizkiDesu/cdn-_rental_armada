from odoo import _, api, fields, models
import xlsxwriter
import os
import base64

class WizardArmadaTersedia(models.TransientModel):
    _name = 'wizard.armada.tersedia'
    _description = 'Wizard Armada Tersedia'
    
    jenis_armada = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'), ('mobil', 'Mobil')], tracking=True)    
    state = fields.Selection(string='Status Armada', selection=[('tidak_siap', 'Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])
    
    def export_excel(self):
        excel_path = 'ARMADA_EXCEL.xlsx'

        # path_module         = os.path.dirname(os.path.realpath(__file__))
        # file_name           = path_module + '\\temp.xlsx'
        workbook            = xlsxwriter.Workbook(excel_path)

        cell_format         = workbook.add_format()
        cell_format.set_align('center')
        cell_format.set_font_size(15)
        cell_format.set_bold()
        # worksheet.merge_range('A1:G1', 'Laporan .....', cell_format)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 20)

        worksheet.write('A9', 'No',             cell_format)
        worksheet.write('B9', 'Field 1',        cell_format)
        worksheet.write('C9', 'Field 2',        cell_format)

        # set cell lainnya ....

        workbook.close()

        with open(excel_path, 'rb') as file:
            file_base64 = base64.b64encode(file.read())

        self.file_export_name   = 'nama_laporan.xlsx'

        self.write({'file_export': file_base64})

        if os.path.exists(excel_path):
            os.remove(excel_path)
        
        return {
            'type'      : 'ir.actions.act_url',
            'target'    : 'self',
            'url'       : '/web/binary/download_document?model={}&field=file_export&id={}&file_name={}'.format(
                self._name,
                self.id, 
                self.file_export_name
            )
        }
