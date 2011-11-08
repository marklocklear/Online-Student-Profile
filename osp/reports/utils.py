from django.http import HttpResponse
import xlwt

char_width = 255
# TODO: auto size height, limit width to reasonable default
def generate_xls_report(filename, sheet_name, columns, rows):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)
    r = c = 0
    for column in columns:
        ws.write(r, c, column)
        try:
            ws.col(c).width = len(column) * char_width
        except TypeError:
            ws.col(c).width = len(str(column)) * char_width
        c += 1
    r = 1
    for row in rows:
        c = 0
        for field in row:
            ws.write(r, c, field)
            try:
                row_width = len(field) * char_width
            except TypeError:
                row_width = len(str(field)) * char_width
            if ws.col(c).width < row_width:
                ws.col(c).width = row_width
            c += 1
        r += 1
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = ('attachment; filename=%s' % filename)
    wb.save(response)
    return response
