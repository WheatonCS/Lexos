from lexos.receivers.base_receiver import BaseReceiver


class KmeansOption:
    def __init__(self,):


class KmeansReceiver(BaseReceiver):
    def options_from_front_end(self) -> KmeansOption:
        """Get the Kmeans option from front end.

        :return: a KmeansOption object to hold all the options.
        """
