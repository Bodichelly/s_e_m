import os
import ast
import glob
import inspect


class MethodsUtils:
    # Methods utils
    def _get_all_methods(self, cls):
        all_methods = []
        for _, method in inspect.getmembers(cls, inspect.isfunction):
            if method.__name__ != '__init__':
                all_methods.append(method.__name__)
        return all_methods

    def _get_own_methods(self, cls, clean=False):
        own_methods = []
        for method_name, method in inspect.getmembers(cls, inspect.isfunction):
            if method_name != '__init__' and self._is_own_method(cls, method):
                own_methods.append(method.__name__ if clean else method_name)
        return own_methods

    def _get_inherited_methods(self, cls):
        return [element for element in self._get_all_methods(cls) if
                element not in self._get_own_methods(cls, True)]

    def _get_overridden_methods(self, cls):
        overridden_methods = []

        # Get the parent class(es) of the subclass
        parent_classes = cls.__bases__

        if parent_classes and parent_classes[0] == object:
            return overridden_methods

        # Iterate over the methods of the subclass
        for method_name, method in cls.__dict__.items():
            # Check if the method is overridden in the subclass
            for parent_class in parent_classes:
                if hasattr(parent_class, method_name):
                    parent_method = getattr(parent_class, method_name)
                    if method != parent_method:
                        overridden_methods.append(method_name)
                    break

        return overridden_methods

    def _get_hidden_methods(self, cls):
        return [method for method in self._get_own_methods(cls) if
                method.startswith('_') and not method.startswith('__')]

    def _get_unique_own_methods(self, cls):
        return [method for method in self._get_own_methods(cls) if method not in self._get_overridden_methods(cls)]

    def _is_own_method(self, cls, method):
        if method.__qualname__.split('.', 1)[0] == cls.__name__:
            return True
        return False
        # return method_name in cls.__dict__

class AttrsUtils:
    # Attrs utils
    def _get_hidden_attributes(self, cls):
        return [attr for attr in self._get_own_attributes(cls) if attr.startswith('_')]

    def _get_own_attributes(self, cls):
        own_attributes = []
        for name, value in cls.__dict__.items():
            if not name.startswith('__') and not inspect.isroutine(value):
                own_attributes.append(name)
        return own_attributes

    def _get_all_attributes(self, cls):
        return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]

    def _get_inherited_attributes(self, cls):
        return [attr for attr in self._get_all_attributes(cls) if attr not in self._get_own_attributes(cls)]



class MetricsCalculator(MethodsUtils, AttrsUtils):
    def __init__(self):
        self.class_metrics = {}
        self.total_metrics = {}

    def calculate(self, module):
        self._reset_metrics()

        # Process the module
        self._process_module(module)

        # Print the results
        print("\nClass metrics:")
        for cls, metrics in self.class_metrics.items():
            print(f"Class: {cls.__name__}")
            print(f"\tDepth of Inheritance Tree: {metrics['dit']}")
            print(f"\tNumber of Children: {metrics['noc']}")
            print(f"\tMIF: {metrics['mif']}")
            print(f"\tMHF: {metrics['mhf']}")
            print(f"\tAHF: {metrics['ahf']}")
            print(f"\tAIF: {metrics['aif']}")
            print(f"\tPOF: {metrics['pof']}")

        print("\nTotal metrics:")
        print(f"\tDepth of Inheritance Tree: {self.total_metrics['dit']}")
        print(f"\tNumber of Children: {self.total_metrics['noc']}")
        print(f"\tMIF: {self.total_metrics['mif'][0] / (self.total_metrics['mif'][1] or 1)}")
        print(f"\tMHF: {self.total_metrics['mhf'][0] / (self.total_metrics['mhf'][1] or 1)}")
        print(f"\tAHF: {self.total_metrics['ahf'][0] / (self.total_metrics['ahf'][1] or 1)}")
        print(f"\tAIF: {self.total_metrics['aif'][0] / (self.total_metrics['aif'][1] or 1)}")
        print(f"\tPOF: {self.total_metrics['pof'][0] / (self.total_metrics['pof'][1] or 1)}")

    def _reset_metrics(self):
        self.class_metrics = {}
        self.total_metrics = {
            'dit': 0,
            'noc': 0,
            'mif': [0, 0],
            'mhf': [0, 0],
            'ahf': [0, 0],
            'aif': [0, 0],
            'pof': [0, 0],
        }

    def _process_module(self, module):
        classes = inspect.getmembers(module, inspect.isclass)
        for name, cls in classes:
            self._process_class(cls)

        self.total_metrics['dit'] = max(self.class_metrics[cls]['dit'] for cls in self.class_metrics)
        self.total_metrics['noc'] = max(self.class_metrics[cls]['noc'] for cls in self.class_metrics)

    def _process_class(self, cls):
        # Calculate the depth of inheritance tree
        dit = self._calculate_dit(cls)

        # Calculate the number of children
        noc = self._calculate_noc(cls)

        # Calculate MOOD indicators
        mif_data = self._calculate_mif(cls)
        mhf_data = self._calculate_mhf(cls)
        ahf_data = self._calculate_ahf(cls)
        aif_data = self._calculate_aif(cls)
        pof_data = self._calculate_pof(cls)

        # Store the metrics for the class
        self.class_metrics[cls] = {
            'dit': dit,
            'noc': noc,
            'mif': mif_data[0],
            'mhf': mhf_data[0],
            'ahf': ahf_data[0],
            'aif': aif_data[0],
            'pof': pof_data[0]
        }

        # Update the total metrics
        self.total_metrics['mif'][0] += mif_data[1]
        self.total_metrics['mif'][1] += mif_data[2]

        self.total_metrics['mhf'][0] += mhf_data[1]
        self.total_metrics['mhf'][1] += mhf_data[2]

        self.total_metrics['ahf'][0] += ahf_data[1]
        self.total_metrics['ahf'][1] += ahf_data[2]

        self.total_metrics['aif'][0] += aif_data[1]
        self.total_metrics['aif'][1] += aif_data[2]

        self.total_metrics['pof'][0] += pof_data[1]
        self.total_metrics['pof'][1] += pof_data[2]

    def _calculate_dit(self, cls):
        if cls.__bases__[0] == object:
            return 0
        else:
            return max(self._calculate_dit(base_cls) for base_cls in cls.__bases__) + 1

    def _calculate_noc(self, cls):
        direct_subclasses = cls.__subclasses__()
        count = len(direct_subclasses)
        for subclass in direct_subclasses:
            count += self._calculate_noc(subclass)
        return count

    # MOOD
    def _calculate_mif(self, cls):
        total_methods = len(self._get_all_methods(cls))
        inherited_methods = len(self._get_inherited_methods(cls))

        return [inherited_methods/(total_methods or 1), inherited_methods, total_methods]

    def _calculate_mhf(self, cls):
        hidden_methods_num = len(self._get_hidden_methods(cls))
        all_methods_num = len(self._get_own_methods(cls))

        return [hidden_methods_num / (all_methods_num or 1), hidden_methods_num, all_methods_num]

    def _calculate_ahf(self, cls):
        hidden_attrs_num = len(self._get_hidden_attributes(cls))
        own_attrs_num = len(self._get_own_attributes(cls))

        return [hidden_attrs_num/(own_attrs_num or 1), hidden_attrs_num, own_attrs_num]

    def _calculate_aif(self, cls):
        all_attrs_num = len(self._get_all_attributes(cls))
        inherited_attrs_num = len(self._get_inherited_attributes(cls))

        return [inherited_attrs_num / (all_attrs_num or 1), inherited_attrs_num, all_attrs_num]

    def _calculate_pof(self, cls):
        unique_own_methods_num = len(self._get_unique_own_methods(cls))
        overridden_methods_num = len(self._get_overridden_methods(cls))
        noc = self._calculate_noc(cls)
        return [overridden_methods_num / (unique_own_methods_num * noc or 1), overridden_methods_num, (unique_own_methods_num * noc)]
