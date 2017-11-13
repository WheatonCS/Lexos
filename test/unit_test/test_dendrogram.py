import pandas as pd

from lexos.models.dendro_model import DendroOption

dtm_data_frame = pd.DataFrame([[0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0],
                               [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0, 4.0],
                               [5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0, 0.0]],
                              index=['catBobcat', 'catCaterpillar',
                                     'wake'],
                              columns=['1', '2', '3', '4', '5', '6', '7', '8'])

options = DendroOption(orientation='left',
                       linkage_method='average',
                       dist_metric='euclidean')


