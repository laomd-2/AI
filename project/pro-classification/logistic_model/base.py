class Validable:
    
    def get_params(self, deep=False):
        params = dict()
        for k, v in vars(self).items():
            if not k.startswith("_"):
                params[k] = v
        return params
    
    def set_params(self, **kargs):
        self.__dict__.update(kargs)