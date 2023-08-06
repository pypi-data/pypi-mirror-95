# Keras data format converter

Generating equal keras models with the desired data format  


## Requirements
tensorflow >= 2.0


## API
`convert_channels_first_to_last(model: keras.Model, inputs_to_transpose: List[str] = None, verbose: bool = False) -> keras.Model`

`convert_channels_last_to_first(model: tf.keras.Model, inputs_to_transpose: List[str] = None, verbose: bool = False) \
        -> tf.keras.Model`

`model`: Keras model to convert

`inputs_to_transpose`: list of input names that need to be transposed due tothe data foramt changing  

`verbose`: detailed output

## Getting started

```python
from tensorflow import keras
from keras_data_format_converter import convert_channels_last_to_first

# Load Keras model
keras_model = keras.models.load_model("my_image_model")

# Call the converter (image_input is an input that needs to be transposed, can be different for your model)
converted_model = convert_channels_last_to_first(keras_model, ["image_input"])
```

## License
This software is covered by MIT License.
