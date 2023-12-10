import EasyGeometryLib as egl
from pathlib import Path
import csv

class Model:
    def __init__(self, filename):
        self.filename = Path(filename)
        self.faces, self.edges = [], []

    def run(self, az_real:float=0, az_model:float=0):
        with open(self.filename, encoding='utf-8') as txt:
            data = txt.readlines()
            data = set(data)
            for line in data:
                try:
                    points_in_line = []
                    if 'POINTS' in line:
                        continue
                    line = [float(a) for a in line.split()]
                    for i in range(0,(len(line)//3)):
                        points_in_line.append(egl.Point(line[i*3+0],line[i*3+1],line[i*3+2]))
                    if len(points_in_line) == 3:
                        self.faces.append(egl.Face(points_in_line[0],points_in_line[1],points_in_line[2]))
                    else:
                        self.edges.append(egl.Edge(points_in_line[0],points_in_line[1]))
                except Exception as e:
                    print("ERROR:", e)
                    print(line)
        self.azimuth_rotation(az_real, az_model)

    def azimuth_rotation(self,az_real, az_model):
        pre_delta = az_real - az_model
        if pre_delta<0:
            delta = pre_delta+360
        else:
            delta = pre_delta%360
        for i in self.faces:
            if i.azimuth+delta >= 360:
                i.rotated_azimuth = i.azimuth+delta-360
            elif i.azimuth+delta < 0:
                i.rotated_azimuth = i.azimuth+delta+360
            else:
                i.rotated_azimuth = i.azimuth+delta

        for i in self.edges:
            if i.azimuth+delta >= 360:
                i.rotated_azimuth = i.azimuth+delta-360
            elif i.azimuth+delta < 0:
                i.rotated_azimuth = i.azimuth+delta+360
            else:
                i.rotated_azimuth = i.azimuth+delta

    def print_results(self):
        print('='*100+'\n'+'='*100+'\n'+'='*100+'\n')
        print(self.faces_into)
        for i in self.faces:
            print(i)
        print(self.edges_into)
        for i in self.edges:
            print(i)

    def edges_result_to_csv(self, delimiter=',', suffix = '_result'):
        part_of_name = str(self.filename.stem).replace('_source', '')
        filename = Path(self.filename.parent, f'{part_of_name}{suffix}_E.csv')
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(['x', 'y', 'z', 'azimuth', 'dip', 'edge_azimuth', 'edge_dip', 'rotated_azimuth', 'length'])
            for i in self.edges:
                center = [i.center.x, i.center.y, i.center.z]
                angles = [i.azimuth, i.dip, i.edge_azimuth, i.edge_dip, i.rotated_azimuth]
                center = [round(x,3) for x in center] # Округление координат
                angles = [round(x,2) for x in angles] # Округление углов
                line = center+angles+[round(i.length,3)] # Округление длины измерения
                writer.writerow(line)
        print('Edges in csv:', filename)

    def faces_result_to_csv(self, delimiter=',', suffix = '_result'):
        part_of_name = str(self.filename.stem).replace('_source', '')
        filename = Path(self.filename.parent, f'{part_of_name}{suffix}_F.csv')
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(['x', 'y', 'z', 'azimuth', 'dip', 'rotated_azimuth', 'blender_degree','area'])
            for i in self.faces:
                center = [i.center.x, i.center.y, i.center.z]
                angles = [i.azimuth, i.dip, i.rotated_azimuth, i.degree]
                center = [round(x,3) for x in center] # Округление координат
                angles = [round(x,2) for x in angles] # Округление углов
                line = center+angles+[round(i.area,3)] # Округление площади
                writer.writerow(line)
        print('Faces in csv:', filename)



if __name__ == '__main__':
    folder_path = Path(r'path/to/folder') # Вставить путь к папке с координатами
    paths = folder_path.glob('*_source.txt')
    for path in paths:
        a = Model(path)
        a.run(az_real=0, az_model=0)
        a.edges_result_to_csv(delimiter=',') # Выбрать разделить и подпись к названию файла csv
        a.faces_result_to_csv(delimiter=',')

    # # Если нужно обработать только 1 файл, то используйте это
    # a = Model(path)
    # a.run(az_real=0, az_model=0)
    # a.edges_result_to_csv(delimiter=',')
    # a.faces_result_to_csv(delimiter=',')

