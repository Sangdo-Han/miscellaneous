import inspect
import tensorflow as tf
import matplotlib.pyplot as plt

class Watcher(object):
    def __init__(self, model, watch_level:int="1"):
        self.model = model
        self.watch_level = watch_level    
        self.framework_type = self._detect_framework()    
        self.layers = self.get_layer(self.framework_type)

    def get_layer(self, framework_type):
        if framework_type == "tensorflow":
            return self._get_tf_layers()
        elif framework_type == "pytorch":
            return self._get_torch_layers()
        else:
            raise NotImplementedError(f"framework named {framework_type} is not supported yet")

    def _detect_framework(self):
        inspect.get
        return

    def _get_tf_layers(self, model):
        return model.layers()
    
    def _get_torch_layers(self, model):
        return model.layers()
    