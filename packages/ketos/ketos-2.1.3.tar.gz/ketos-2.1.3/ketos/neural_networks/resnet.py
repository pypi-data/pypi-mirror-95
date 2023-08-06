# ================================================================================ #
#   Authors: Fabio Frazao and Oliver Kirsebom                                      #
#   Contact: fsfrazao@dal.ca, oliver.kirsebom@dal.ca                               #
#   Organization: MERIDIAN (https://meridian.cs.dal.ca/)                           #
#   Team: Data Analytics                                                           #
#   Project: ketos                                                                 #
#   Project goal: The ketos library provides functionalities for handling          #
#   and processing acoustic data and applying deep neural networks to sound        #
#   detection and classification tasks.                                            #
#                                                                                  #
#   License: GNU GPLv3                                                             #
#                                                                                  #
#       This program is free software: you can redistribute it and/or modify       #
#       it under the terms of the GNU General Public License as published by       #
#       the Free Software Foundation, either version 3 of the License, or          #
#       (at your option) any later version.                                        #
#                                                                                  #
#       This program is distributed in the hope that it will be useful,            #
#       but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#       GNU General Public License for more details.                               # 
#                                                                                  #
#       You should have received a copy of the GNU General Public License          #
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
# ================================================================================ #

""" resnet sub-module within the ketos.neural_networks module

    This module provides classes to implement Residual Networks (ResNets).

    Contents:
        ResNetBlock class
        ResNet class
        ResNetInterface class

"""

import tensorflow as tf
import numpy as np
from .dev_utils.nn_interface import RecipeCompat, NNInterface
import json




default_resnet_recipe =  {'block_sets':[2,2,2],
                    'n_classes':2,
                    'initial_filters':16,        
                    'optimizer': RecipeCompat('Adam', tf.keras.optimizers.Adam, learning_rate=0.005),
                    'loss_function': RecipeCompat('BinaryCrossentropy', tf.keras.losses.BinaryCrossentropy),  
                    'metrics': [RecipeCompat('BinaryAccuracy',tf.keras.metrics.BinaryAccuracy),
                                RecipeCompat('Precision',tf.keras.metrics.Precision),
                                RecipeCompat('Recall',tf.keras.metrics.Recall)],
                    }


default_resnet_1d_recipe =  {'block_sets':[2,2,2],
                    'n_classes':2,
                    'initial_filters':2,        
                    'optimizer': RecipeCompat('Adam', tf.keras.optimizers.Adam, learning_rate=0.005),
                    'loss_function': RecipeCompat('CategoricalCrossentropy', tf.keras.losses.CategoricalCrossentropy),  
                    'metrics': [RecipeCompat('CategoricalAccuracy',tf.keras.metrics.CategoricalAccuracy),
                                RecipeCompat('Precision',tf.keras.metrics.Precision, class_id=1),
                                RecipeCompat('Recall',tf.keras.metrics.Recall, class_id=1)],
                    }



class ResNetBlock(tf.keras.Model):
    """ Residual block for ResNet architectures.

        Args: 
            filters: int
                The number of filters in the block
            strides: int
                Strides used in convolutional layers within the block
            residual_path: bool
                Whether or not the block will contain a residual path

        Returns:
            A ResNetBlock object. The block itself is a tensorflow model and can be used as such.
    """
    def __init__(self, filters, strides=1, residual_path=False):
        super(ResNetBlock, self).__init__()

        self.filters = filters
        self.strides = strides
        self.residual_path = residual_path
        self.conv_1 = tf.keras.layers.Conv2D(filters=self.filters, kernel_size=(3,3), strides=self.strides,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())
        self.batch_norm_1 = tf.keras.layers.BatchNormalization()
        self.conv_2 = tf.keras.layers.Conv2D(filters=self.filters, kernel_size=(3,3), strides=1,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())
        self.batch_norm_2 = tf.keras.layers.BatchNormalization()

        if residual_path == True:
            self.conv_down = tf.keras.layers.Conv2D(filters=self.filters, kernel_size=(1,1), strides=self.strides,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())
            self.batch_norm_down = tf.keras.layers.BatchNormalization()
        
        self.dropout = tf.keras.layers.Dropout(0.0)

    def call(self,inputs, training=None):
        residual = inputs

        x = self.batch_norm_1(inputs, training=training)
        x = tf.nn.relu(x)
        x = self.conv_1(x)
        x = self.dropout(x)
        x = self.batch_norm_2(x, training=training)
        x = tf.nn.relu(x)
        x = self.conv_2(x)
        x = self.dropout(x)

        if self.residual_path:
            residual = self.batch_norm_down(inputs, training=training)
            residual = tf.nn.relu(residual)
            residual = self.conv_down(residual)
            x = self.dropout(x)

        x = x + residual
        return x


class ResNet1DBlock(tf.keras.Model):
    """ Residual block for 1D (temporal) ResNet architectures.

        Args: 
            filters: int
                The number of filters in the block
            strides: int
                Strides used in convolutional layers within the block
            residual_path: bool
                Whether or not the block will contain a residual path

        Returns:
            A ResNetBlock object. The block itself is a tensorflow model and can be used as such.
    """
    def __init__(self, filters, strides=1, residual_path=False):
        super(ResNet1DBlock, self).__init__()

        self.filters = filters
        self.strides = strides
        self.residual_path = residual_path
        self.conv_1 = tf.keras.layers.Conv1D(filters=self.filters, kernel_size=300, strides=self.strides,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())
        self.batch_norm_1 = tf.keras.layers.BatchNormalization()
        self.conv_2 = tf.keras.layers.Conv1D(filters=self.filters, kernel_size=300, strides=1,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())
        self.batch_norm_2 = tf.keras.layers.BatchNormalization()

        if residual_path == True:
            self.conv_down = tf.keras.layers.Conv1D(filters=self.filters, kernel_size=1, strides=self.strides,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())
            self.batch_norm_down = tf.keras.layers.BatchNormalization()
        
        self.dropout = tf.keras.layers.Dropout(0.0)

    def call(self,inputs, training=None):
        residual = inputs

        x = self.batch_norm_1(inputs, training=training)
        x = tf.nn.relu(x)
        x = self.conv_1(x)
        x = self.dropout(x)
        x = self.batch_norm_2(x, training=training)
        x = tf.nn.relu(x)
        x = self.conv_2(x)
        x = self.dropout(x)

        if self.residual_path:
            residual = self.batch_norm_down(inputs, training=training)
            residual = tf.nn.relu(residual)
            residual = self.conv_down(residual)
            x = self.dropout(x)

        x = x + residual
        return x





class ResNetArch(tf.keras.Model):
    """ Implements a ResNet architecture, building on top of ResNetBlocks.

        Args:
            block_sets: list of ints
                A list specifying the block sets and how many blocks each  set contains.
                Example: [2,2,2] will create a ResNet with 3 block sets, each containing
                2 ResNetBlocks (i.e.: a total of 6 residual blocks)
            
            n_classes:int
                The number of classes. The output layer uses a Softmax activation and
                will contain this number of nodes, resulting in model outputs with this
                many values summing to 1.0.

            initial_filters:int
                The number of filters used in the first ResNetBlock. Subsequent blocks 
                will have two times more filters than their previous block.

            pre_trained_base: instance of ResNetArch
                A pre-trained resnet model from which the residual blocks will be taken. 
                Use by the the clone_with_new_top method when creating a clone for transfer learning

        Returns:
            A ResNetArch object, which is a tensorflow model.
    """

    def __init__(self,  n_classes, pre_trained_base=None, block_sets=None, initial_filters=16, **kwargs):
        super(ResNetArch, self).__init__(**kwargs)

        
        self.n_classes = n_classes
        if pre_trained_base:
            self.conv_initial = pre_trained_base[0]
            self.blocks = pre_trained_base[1]
        else:
            self.n_sets = len(block_sets)
            self.block_sets = block_sets
            self.input_filters = initial_filters
            self.output_filters = initial_filters
            self.conv_initial = tf.keras.layers.Conv2D(filters=self.output_filters, kernel_size=(3,3), strides=1,
                                                    padding="same", use_bias=False,
                                                    kernel_initializer=tf.random_normal_initializer())

            self.blocks = tf.keras.models.Sequential(name="dynamic_blocks")

            for set_id in range(self.n_sets):
                for block_id in range(self.block_sets[set_id]):
                    #Frst layer of every block except the first
                    if set_id != 0 and block_id == 0:
                        block = ResNetBlock(self.output_filters, strides=2, residual_path=True)
                    
                    else:
                        if self.input_filters != self.output_filters:
                            residual_path = True
                        else:
                            residual_path = False
                        block = ResNetBlock(self.output_filters, residual_path=residual_path)

                    self.input_filters = self.output_filters

                    self.blocks.add(block)
                
                self.output_filters *= 2

        self.batch_norm_final = tf.keras.layers.BatchNormalization()
        self.average_pool = tf.keras.layers.GlobalAveragePooling2D()
        self.fully_connected = tf.keras.layers.Dense(self.n_classes)
        self.softmax = tf.keras.layers.Softmax()
    
    def freeze_init_layer(self):
        """Freeze the initial convolutional layer"""
        self.layers[0].trainable = False

    def unfreeze_init_layer(self):
        """Unffreeze the initial convolutional layer"""
        self.layers[0].trainable = True
    
    def freeze_block(self, block_ids):
        """ Freeze specific residual blocks

            Args:
                blocks_ids: int
                    The block number to be freezed (starting from zero)
        """

        for block_id in block_ids:
            self.layers[1].layers[block_id].trainable = False

    def unfreeze_block(self, block_ids):
        """ Unfreeze specific residual blocks

            Args:
                blocks_ids: int
                    The block number to be unfreezed (starting from zero)
        """

        for block_id in block_ids:
            self.layers[1].layers[block_id].trainable = True
    
    def freeze_top(self):
        """Freeze the classification block"""
        for layer in self.layers[2:]:
            layer.trainable = False
    
    def unfreeze_top(self):
        """Unfreeze the classification block"""
        for layer in self.layers[2:]:
            layer.trainable = True

    def get_feature_extraction_base(self):
        """ Retrive the feature extraction base (initial convolutional layer + residual blocks)
        
            Returns:
                list containing the feature extraction layers
        """
        return [self.conv_initial, self.blocks]

    def clone_with_new_top(self, n_classes=None, freeze_base=True):
        """ Clone this instance but replace the original classification top with a new (untrained) one
        
            Args:
                n_classes:int
                    The number of classes the new classification top should output.
                    If None(default), the original number of classes will be used.
                freeze_base:bool
                    If True, the weights of the feature extraction base will be froze (untrainable) in the new model.
                
            Returns:
                cloned_model: instance of ResNetArch
                    The new model with the old feature extraction base and new classification top.
         """
        if freeze_base == True:
            self.trainable = False

        if n_classes is None:
            n_classes = self.n_classes

        pre_trained_base = self.get_feature_extraction_base()
        cloned_model = type(self)(n_classes=n_classes, pre_trained_base=pre_trained_base)

        return cloned_model
        
    def call(self, inputs, training=None):
        output = self.conv_initial(inputs)
        output = self.blocks(output, training=training)
        output = self.batch_norm_final(output, training=training)
        output = tf.nn.relu(output)
        output = self.average_pool(output)
        output = self.fully_connected(output)
        output = self.softmax(output)

        return output
    




class ResNet1DArch(tf.keras.Model):
    """ Implements a 1D (temporal) ResNet architecture, building on top of ResNetBlocks.

        Args:
            block_sets: list of ints
                A list specifying the block sets and how many blocks each  set contains.
                Example: [2,2,2] will create a ResNet with 3 block sets, each containing
                2 ResNetBlocks (i.e.: a total of 6 residual blocks)
            
            n_classes:int
                The number of classes. The output layer uses a Softmax activation and
                will contain this number of nodes, resulting in model outputs with this
                many values summing to 1.0.

            initial_filters:int
                The number of filters used in the first ResNetBlock. Subsequent blocks 
                will have two times more filters than their previous block.

            pre_trained_base: instance of ResNet1DArch
                A pre-trained resnet model from which the residual blocks will be taken. 
                Use by the the clone_with_new_top method when creating a clone for transfer learning

        Returns:
            A ResNet1DArch object, which is a tensorflow model.
    """

    def __init__(self, n_classes, pre_trained_base=None, block_sets=None, initial_filters=16, **kwargs):
        super(ResNet1DArch, self).__init__(**kwargs)
        self.n_classes = n_classes
        if pre_trained_base:
            self.conv_initial = pre_trained_base[0]
            self.blocks = pre_trained_base[1]
        else:
            self.n_sets = len(block_sets)
            self.block_sets = block_sets
            self.input_filters = initial_filters
            self.output_filters = initial_filters
            self.conv_initial = tf.keras.layers.Conv1D(filters=self.output_filters, kernel_size=30, strides=1,
                                                padding="same", use_bias=False,
                                                kernel_initializer=tf.random_normal_initializer())

            self.blocks = tf.keras.models.Sequential(name="dynamic_blocks")

            for set_id in range(self.n_sets):
                for block_id in range(self.block_sets[set_id]):
                    #Frst layer of every block except the first
                    if set_id != 0 and block_id == 0:
                        block = ResNet1DBlock(self.output_filters, strides=2, residual_path=True)
                    
                    else:
                        if self.input_filters != self.output_filters:
                            residual_path = True
                        else:
                            residual_path = False
                        block = ResNet1DBlock(self.output_filters, residual_path=residual_path)

                    self.input_filters = self.output_filters

                    self.blocks.add(block)
                
                self.output_filters *= 2

        self.batch_norm_final = tf.keras.layers.BatchNormalization()
        self.average_pool = tf.keras.layers.GlobalAveragePooling1D()
        self.fully_connected = tf.keras.layers.Dense(self.n_classes)
        self.softmax = tf.keras.layers.Softmax()
    
    
    def freeze_init_layer(self):
        """Freeze the initial convolutional layer"""
        self.layers[0].trainable = False

    def unfreeze_init_layer(self):
        """Unffreeze the initial convolutional layer"""
        self.layers[0].trainable = True
    
    def freeze_block(self, block_ids):
        """ Freeze specific residual blocks

            Args:
                blocks_ids: list of ints
                    The block numbers to be freezed (starting from zero)
        """

        for block_id in block_ids:
            self.layers[1].layers[block_id].trainable = False

    def unfreeze_block(self, block_ids):
        """ Unfreeze specific residual blocks

            Args:
                blocks_ids: list of ints
                    The block numbers to be freezed (starting from zero)
        """

        for block_id in block_ids:
            self.layers[1].layers[block_id].trainable = True
    
    def freeze_top(self):
        """Freeze the classification block"""
        for layer in self.layers[2:]:
            layer.trainable = False
    
    def unfreeze_top(self):
        """Unfreeze the classification block"""
        for layer in self.layers[2:]:
            layer.trainable = True

    def get_feature_extraction_base(self):
        """ Retrive the feature extraction base (initial convolutional layer + residual blocks)
        
            Returns:
                list containing the feature extraction layers
        """
        return [self.conv_initial, self.blocks]

    def clone_with_new_top(self, n_classes=None, freeze_base=True):
        """ Clone this instance but replace the original classification top with a new (untrained) one
        
            Args:
                n_classes:int
                    The number of classes the new classification top should output.
                    If None(default), the original number of classes will be used.
                freeze_base:bool
                    If True, the weights of the feature extraction base will be froze (untrainable) in the new model.
                
            Returns:
                cloned_model: instance of ResNetArch
                    The new model with the old feature extraction base and new classification top.
         """
        if freeze_base == True:
            self.trainable = False

        if n_classes is None:
            n_classes = self.n_classes

        pre_trained_base = self.get_feature_extraction_base()
        cloned_model = type(self)(n_classes=n_classes, pre_trained_base=pre_trained_base)

        return cloned_model

    def call(self, inputs, training=None):
        output = self.conv_initial(inputs)
        output = self.blocks(output, training=training)
        output = self.batch_norm_final(output, training=training)
        output = tf.nn.relu(output)
        output = self.average_pool(output)
        output = self.fully_connected(output)
        output = self.softmax(output)

        return output




class ResNetInterface(NNInterface):
    """ Creates a ResNet model with the standardized Ketos interface.

        Args:
             block_sets: list of ints
                A list specifying the block sets and how many blocks each  set contains.
                Example: [2,2,2] will create a ResNet with 3 block sets, each containing
                2 ResNetBlocks (i.e.: a total of 6 residual blocks)
            
            n_classes:int
                The number of classes. The output layer uses a Softmax activation and
                will contain this number of nodes, resulting in model outputs with this
                many values summing to 1.0.

            initial_filters:int
                The number of filters used in the first ResNetBlock. Subsequent blocks 
                will have two times more filters than their previous block.

            optimizer: ketos.neural_networks.RecipeCompat object
                A recipe compatible optimizer (i.e.: wrapped by the ketos.neural_networksRecipeCompat class)

            loss_function: ketos.neural_networks.RecipeCompat object
                A recipe compatible loss_function (i.e.: wrapped by the ketos.neural_networksRecipeCompat class)

            metrics: list of ketos.neural_networks.RecipeCompat objects
                A list of recipe compatible metrics (i.e.: wrapped by the ketos.neural_networksRecipeCompat class).
                These metrics will be computed on each batch during training.

            secondary_metrics: list of ketos.neural_networks.RecipeCompat objects
                A list of recipe compatible metrics (i.e.: wrapped by the ketos.neural_networksRecipeCompat class).
                These can be used as additional metrics. Computed at each batch during training but only printed or
                logged as the average at the end of the epoch
                
    """

    @classmethod
    def _build_from_recipe(cls, recipe, recipe_compat=True):
        """ Build a ResNet model from a recipe.

            Args:
                recipe: dict
                    A recipe dictionary. optimizer, loss function
                    and metrics must be instances of ketos.neural_networks.RecipeCompat.
                    
                    Example recipe:
                    
                    >>> {{'block_sets':[2,2,2], # doctest: +SKIP
                    ...    'n_classes':2,
                    ...    'initial_filters':16,        
                    ...    'optimizer': RecipeCompat('Adam', tf.keras.optimizers.Adam, learning_rate=0.005),
                    ...    'loss_function': RecipeCompat('FScoreLoss', FScoreLoss),  
                    ...    'metrics': [RecipeCompat('CategoricalAccuracy',tf.keras.metrics.CategoricalAccuracy)],
                    }

                     

            Returns:
                An instance of ResNetInterface.

        """

        block_sets = recipe['block_sets']
        n_classes = recipe['n_classes']
        initial_filters = recipe['initial_filters']
        
        if recipe_compat == True:
            optimizer = recipe['optimizer']
            loss_function = recipe['loss_function']
            metrics = recipe['metrics']
            
        else:
            optimizer = cls._optimizer_from_recipe(recipe['optimizer'])
            loss_function = cls._loss_function_from_recipe(recipe['loss_function'])
            metrics = cls._metrics_from_recipe(recipe['metrics'])
            

        instance = cls(block_sets=block_sets, n_classes=n_classes, initial_filters=initial_filters, optimizer=optimizer, loss_function=loss_function, metrics=metrics)

        return instance

    @classmethod
    def _read_recipe_file(cls, json_file, return_recipe_compat=True):
        """ Read a ResNet recipe saved in a .json file.

            Args:
                json_file:string
                    Full path (including filename and extension) to the .json file containing the recipe.
                return_recipe_compat:bool
                    If True, returns a dictionary where the optimizer, loss_function, metrics and 
                    secondary_metrics (if available) values are instances of the ketos.neural_networks.nn_interface.RecipeCompat.
                    The returned dictionary will be equivalent to:
                            
                            >>> {'block_sets':[2,2,2], # doctest: +SKIP
                            ... 'n_classes':2,
                            ... 'initial_filters':16,        
                            ... 'optimizer': RecipeCompat('Adam', tf.keras.optimizers.Adam, learning_rate=0.005),
                            ... 'loss_function': RecipeCompat('FScoreLoss', FScoreLoss),  
                            ... 'metrics': [RecipeCompat('CategoricalAccuracy',tf.keras.metrics.CategoricalAccuracy)]}

                    If False, the optimizer, loss_function, metrics and secondary_metrics (if available) values will contain a
                    dictionary representation of such fields instead of the RecipeCompat objects:
                            >>> {'block_sets':[2,2,2], # doctest: +SKIP
                            ... 'n_classes':2,
                            ... 'initial_filters':16,        
                            ... 'optimizer': {'name':'Adam', 'parameters': {'learning_rate':0.005}},
                            ... 'loss_function': {'name':'FScoreLoss', 'parameters':{}},  
                            ... 'metrics': [{'name':'CategoricalAccuracy', 'parameters':{}}]}

                Returns:
                    recipe, according to 'return_recipe_compat.

        """

        with open(json_file, 'r') as json_recipe:
            recipe_dict = json.load(json_recipe)

        optimizer = cls._optimizer_from_recipe(recipe_dict['optimizer'])
        loss_function = cls._loss_function_from_recipe(recipe_dict['loss_function'])
        metrics = cls._metrics_from_recipe(recipe_dict['metrics'])
        
        if return_recipe_compat == True:
            recipe_dict['optimizer'] = optimizer
            recipe_dict['loss_function'] = loss_function
            recipe_dict['metrics'] = metrics
            
        else:
            recipe_dict['optimizer'] = cls._optimizer_to_recipe(optimizer)
            recipe_dict['loss_function'] = cls._loss_function_to_recipe(loss_function)
            recipe_dict['metrics'] = cls._metrics_to_recipe(metrics)
        
        recipe_dict['block_sets'] = recipe_dict['block_sets']
        recipe_dict['n_classes'] = recipe_dict['n_classes']
        recipe_dict['initial_filters'] = recipe_dict['initial_filters']

        return recipe_dict

    def __init__(self, block_sets=default_resnet_recipe['block_sets'], n_classes=default_resnet_recipe['n_classes'], initial_filters=default_resnet_recipe['initial_filters'],
                       optimizer=default_resnet_recipe['optimizer'], loss_function=default_resnet_recipe['loss_function'], metrics=default_resnet_recipe['metrics']):
        super(ResNetInterface, self).__init__(optimizer, loss_function, metrics)
        self.block_sets = block_sets
        self.n_classes = n_classes
        self.initial_filters = initial_filters

        self.model=ResNetArch(block_sets=block_sets, n_classes=n_classes, initial_filters=initial_filters)

    def _extract_recipe_dict(self):
        """ Create a recipe dictionary from a ResNetInterface instance.

            The resulting recipe contains all the fields necessary to build the same network architecture used by the instance calling this method.
            
            Returns:
                recipe:dict
                    A dictionary containing the recipe fields necessary to build the same network architecture.
                    The output is equivalent to:
                        >>> {'block_sets':[2,2,2], # doctest: +SKIP
                        ...    'n_classes':2,
                        ...    'initial_filters':16,        
                        ...    'optimizer': RecipeCompat('Adam', tf.keras.optimizers.Adam, learning_rate=0.005),
                        ...    'loss_function': RecipeCompat('FScoreLoss', FScoreLoss),  
                        ...    'metrics': [RecipeCompat('CategoricalAccuracy',tf.keras.metrics.CategoricalAccuracy)]}
        """

        recipe = {}
        recipe['interface'] = type(self).__name__
        recipe['block_sets'] = self.block_sets
        recipe['n_classes'] = self.n_classes
        recipe['initial_filters'] = self.initial_filters
        recipe['optimizer'] = self._optimizer_to_recipe(self.optimizer)
        recipe['loss_function'] = self._loss_function_to_recipe(self.loss_function)
        recipe['metrics'] = self._metrics_to_recipe(self.metrics)
        
        return recipe



class ResNet1DInterface(ResNetInterface): 
    @classmethod
    def transform_batch(cls, x, y, y_fields=['label'], n_classes=2):
        """ Transforms a training batch into the format expected by the network.

            When this interface is subclassed to make new neural_network classes, this method can be overwritten to
            accomodate any transformations required. Common operations are reshaping of input arrays and parsing or one hot encoding of the labels.

            Args:
                x:numpy.array
                    The batch of inputs with shape (batch_size, width, height)
                y:numpy.array
                    The batch of labels.
                    Each label must be represented as an integer, ranging from zero to n_classes
                    The array is expected to have a field named 'label'.
                n_classes:int
                    The number of possible classes for one hot encoding.
                    
                

            Returns:
                X:numpy.array
                    The transformed batch of inputs
                Y:numpy.array
                    The transformed batch of labels

            Examples:
                >>> import numpy as np
                >>> # Create a batch of 10 5x5 arrays
                >>> inputs = np.random.rand(10,5,5)
                >>> inputs.shape
                (10, 5, 5)

                    
                >>> # Create a batch of 10 labels (0 or 1)
                >>> labels = np.random.choice([0,1], size=10).astype([('label','<i4')])
                >>> labels.shape
                (10,)

                >>> transformed_inputs, transformed_labels = NNInterface.transform_batch(inputs, labels, n_classes=2)
                >>> transformed_inputs.shape
                (10, 5, 5, 1)

                >>> transformed_labels.shape
                (10, 2)
                
        """

        
        X = cls._transform_input(x)
        Y = np.array([cls._to1hot(class_label=label, n_classes=n_classes) for label in y['label']])
        
        return (X,Y)

    @classmethod
    def _transform_input(cls,input):
        """ Transforms a training input to the format expected by the network.

            Similar to :func:`NNInterface.transform_train_batch`, but only acts on the inputs (not labels). Mostly used for inference, rather than training.
            When this interface is subclassed to make new neural_network classes, this method can be overwritten to
            accomodate any transformations required. Common operations are reshaping of an input.

            Args:
                input:numpy.array
                    An input instance. Must be of shape (n,m) or (k,n,m).

            Raises:
                ValueError if input does not have 2 or 3 dimensions.

            Returns:
                tranformed_input:numpy.array
                    The transformed batch of inputs

            Examples:
                >>> import numpy as np
                >>> # Create a batch of 10 5x5 arrays
                >>> batch_of_inputs = np.random.rand(10,5,5)
                >>> selected_input = batch_of_inputs[0]
                >>> selected_input.shape
                (5, 5)
                 
                >>> transformed_input = NNInterface._transform_input(selected_input)
                >>> transformed_input.shape
                (1, 5, 5, 1)

                # The input can also have shape=(1,n,m)
                >>> selected_input = batch_of_inputs[0:1]
                >>> selected_input.shape
                (1, 5, 5)
                 
                >>> transformed_input = NNInterface._transform_input(selected_input)
                >>> transformed_input.shape
                (1, 5, 5, 1)

                
        """
        if input.ndim == 1:
            transformed_input = input.reshape(1,input.shape[0],1)
        elif input.ndim == 2:
            transformed_input = input.reshape(input.shape[0],input.shape[1],1)
        else:
            raise ValueError("Expected input to have 1 or 2 dimensions, got {}({}) instead".format(input.ndims, input.shape))

        return transformed_input

    def __init__(self, block_sets=default_resnet_1d_recipe['block_sets'], n_classes=default_resnet_1d_recipe['n_classes'], initial_filters=default_resnet_1d_recipe['initial_filters'],
                       optimizer=default_resnet_1d_recipe['optimizer'], loss_function=default_resnet_1d_recipe['loss_function'], metrics=default_resnet_1d_recipe['metrics']):
        super(ResNet1DInterface, self).__init__(optimizer=optimizer, loss_function=loss_function, metrics=metrics)
        self.block_sets = block_sets
        self.n_classes = n_classes
        self.initial_filters = initial_filters
       
        self.model=ResNet1DArch(block_sets=block_sets, n_classes=n_classes, initial_filters=initial_filters)
       
