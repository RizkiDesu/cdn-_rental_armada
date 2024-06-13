from odoo import _, api, fields, models
import xlsxwriter
import os
import base64

# CREATED BY TRIADI
# ------------------------------- WIZARD ARMADA TERSEDIA EXPORT EXCEL --------------------------------
class WizardArmadaTersedia(models.TransientModel):
    _name = 'wizard.armada.tersedia'
    _description = 'Wizard Armada Tersedia'
    
    jenis_armada = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'), ('mobil', 'Mobil')], tracking=True)    
    state = fields.Selection(string='Status Armada', selection=[('tidak_siap', 'Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])
    file_export_name = fields.Char(string='Nama File')
    file_export_data      = fields.Binary(string='File Export')
    
    
    def export_excel(self):
        file_name = f"{self.jenis_armada}_{self.state}"

        # Determine the file path
        path_module = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(path_module, file_name)

        # Create an Excel file
        with xlsxwriter.Workbook(file_path) as workbook:
            cell_format = workbook.add_format()
            worksheet = workbook.add_worksheet()
            cell_format.set_align('center')
            cell_format.set_valign('center')
            cell_format.set_font_size(10)
            # cell_format.set_bold()
            cell_format.set_border(1)

            cell_format1 = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 10,
                'bold': True,
                'border': 1,
                'bg_color': '#30649c',
                'locked': True,
                'font_color': 'white'
            })
            worksheet.merge_range('A2:I3', 'RENTAL ARMADA', cell_format1)
            worksheet.write('A4', 'No', cell_format)
            worksheet.write('B4', 'Nama Armada', cell_format)
            worksheet.write('C4', 'Plat Nomor', cell_format)
            worksheet.write('D4', 'Merek', cell_format)
            worksheet.write('E4', 'Jenis Kendaraan', cell_format)
            worksheet.write('F4', 'No Rangka', cell_format)
            worksheet.write('G4', 'Tahun Pembuatan', cell_format)
            worksheet.write('H4', 'State', cell_format)
            worksheet.write('I4', 'Terakhir Service', cell_format)
            worksheet.freeze_panes(4, 0)  # Membekukan baris pertama

            armada = self.env['cdn.armada'].search([('jenis_armada', '=', self.jenis_armada),('state', '=', self.state)])  # Change domain if needed
            
            # Write data
            row = 4
            no = 1
            for kendaraan in armada:
                worksheet.write(row, 0, no, cell_format)
                worksheet.write(row, 1, "{} {}".format(kendaraan.merek_id.name, kendaraan.jenis_kendaraan.name), cell_format) # model cdn.merek dan cdn kendaraan
                worksheet.write(row, 2, kendaraan.no_plat, cell_format)
                worksheet.write(row, 3, kendaraan.merek_id.name, cell_format)
                worksheet.write(row, 4, kendaraan.jenis_armada, cell_format)
                worksheet.write(row, 5, kendaraan.no_rangka, cell_format)
                worksheet.write(row, 6, kendaraan.tahun_pembuatan, cell_format)
                worksheet.write(row, 7, kendaraan.state, cell_format)
                worksheet.write(row, 8, kendaraan.terakhir_service, cell_format)
                row += 1
                no += 1
        # Read the file and encode it to base64
        with open(file_path, 'rb') as file:
            file_data = file.read()
            encoded_file_data = base64.b64encode(file_data).decode('utf-8')

        # Save the file data to the record
        self.write({
            'file_export_name': file_name,
            'file_export_data': encoded_file_data,
        })

        # Optionally, remove the temporary file
        os.remove(file_path)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=wizard.armada.tersedia&id={}&field=file_export_data&filename_field=file_export_name&download=true'.format(self.id),
            'target': 'self',
        }

    def generated_data(self):
        armada_list = []
        armada = self.env["cdn.armada"].search_read(fields=["id", "name"])
        for rec in armada:
            armada_list.append(rec)
        return armada_list

    def export_pdf(self):
        data = {
            "armadas": self.generated_data(),
        }
        return self.env.ref(
            "cdn_rental_armada.report_armada_semua"
        ).report_action(self, data=data)
