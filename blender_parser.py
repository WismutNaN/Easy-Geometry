'''
Copy to blender text editor
'''
import bpy

class Point():
    def __init__(self,vector):
        self.x = vector.co[0]
        self.y = vector.co[1]
        self.z = vector.co[2]

    def __str__(self):
        return '{}\t{}\t{}'.format(self.x, self.y, self.z)

class Model:
    def __init__(self):
        pass

    def parser_dimensions(self):
        self.faces, self.edges = [], []
        for i in range(0,len(list(bpy.data.grease_pencils["Annotations"].layers['RulerData3D'].frames))):
            dimensions = bpy.data.grease_pencils["Annotations"].layers['RulerData3D'].frames[i].strokes
            for dimension in dimensions:
                if len(dimension.points) == 3:
                    self.faces.append([Point(vector) for vector in dimension.points])
                else:
                    self.edges.append([Point(vector) for vector in dimension.points])

    def print_faces(self):
        print('FACES POINTS', len(self.faces))
        for i in self.faces:
            print('{}\t\t{}\t\t{}'.format(i[0], i[1], i[2]))

    def print_edges(self):
        print('EDGES POINTS', len(self.edges))
        for i in self.edges:
            print('{}\t\t{}'.format(i[0], i[1]))

    def resutlt_to_txt(self,type='auto'):
        filename = bpy.data.filepath.replace('.blend', '_source.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            if type == 'auto' or type == 0:
                if len(self.faces) > len(self.edges):
                    type = 'faces'
                else:
                    type = 'edges'

            if type == 'edges' or type == 1:
                file.write('EDGES POINTS {}\n'.format(len(self.edges)))
                for i in self.edges:
                    file.write('{}\t{}\n'.format(i[0], i[1]))

            if type == 'faces' or type == 2:
                file.write('FACES POINTS {}\n'.format(len(self.faces)))
                for i in self.faces:
                    file.write('{}\t{}\t{}\n'.format(i[0], i[1], i[2]))

        print('Result in file:', filename)


print(('='*100+'\n')*80)
model = Model()
model.parser_dimensions()
model.resutlt_to_txt(0)
# Type 0 == auto, Type 1 == edges, Type 2 == faces