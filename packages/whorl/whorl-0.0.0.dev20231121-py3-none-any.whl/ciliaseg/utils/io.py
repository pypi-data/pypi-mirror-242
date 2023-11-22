import skimage.io as io
import pandas as pd
from ciliaseg.state.image import SEMImage
import os.path

def save_image_as_csv(image: SEMImage, path: str):
    assert path.endswith('.csv'), 'save path filename must end in ".csv"'

    with open(path, 'w') as file:
        file.write('image_name,type,x_vertices,y_vertices,n_vertices,score,bbox\n')

        for s in image.get_stereocilia():
            xstr = str(s.x())
            ystr = str(s.y())

            xstr = xstr.replace(',', ' ')
            ystr = ystr.replace(',', ' ')

            bboxstr = str(s.bbox()).replace(',', ' ')
            file.write(f'{image.filepath},{s.get_label_str()},{xstr},{ystr},{len(s.x())},{s.get_score()},{bboxstr}\n')


def load_stereocilia_from_csv(path: str):
    raise NotImplementedError


