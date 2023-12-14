import EasyGeometryLib as egl
from pathlib import Path
import ezdxf
import csv

class PitFrame:
    def __init__(self, dxf_file_path) -> None:
        self.dxf_file_path = Path(dxf_file_path)
        self.faces = []

    def collect_triangles(self):
        doc = ezdxf.readfile(self.dxf_file_path) # Открываем dxf
        for entity in doc.modelspace().query('3DFACE'): # Считываем все треугольники
            vertices = [entity.dxf.vtx0, entity.dxf.vtx1, entity.dxf.vtx2, entity.dxf.vtx3]
            vertices = [v for i, v in enumerate(vertices) if v not in vertices[:i]]
            face = egl.Face(egl.Point(vertices[0].x,vertices[0].y,vertices[0].z),
                           egl.Point(vertices[1].x,vertices[1].y,vertices[1].z),
                           egl.Point(vertices[2].x,vertices[2].y,vertices[2].z))
            self.faces.append(face) # Записываем в список

    def result_to_csv(self, delimiter=',', suffix = '_result'):
        filename = Path(self.dxf_file_path.parent, f'{self.dxf_file_path.stem}{suffix}.csv')
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(['XPT', 'YPT', 'ZPT',
                             'DIPDIRN', 'SDIP', 'AREA']) # Записываем заголовки
            for i in self.faces:
                center = [i.center.x, i.center.y, i.center.z]
                angles = [i.azimuth, i.dip]
                center = [round(x,2) for x in center] # Округление координат
                angles = [round(x,0) for x in angles] # Округление углов
                line = center+angles+[round(i.area,2)] # Округление площади
                writer.writerow(line)

        print('Result in csv:', filename)

if __name__ == '__main__':
    a = PitFrame(r'path/to/dxf') # Вставить путь к dxf
    a.collect_triangles()
    a.result_to_csv(delimiter=',') # Выбрать разделить и подпись к названию файла csv