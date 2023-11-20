
# Image Colorizer

This package provides tools to colorize images using deep learning models.

## Installation

Clone this repository and run:

```bash
pip install .
```

## Usage

To use the Image Colorizer, import it in your Python script and provide the paths for the model and images:

```python
from image_colorizer import ImageColorizer

model_path = 'path_to_your_model.pkl'
input_path = 'path_to_your_input_image.jpg'
output_path = 'path_to_save_colorized_image.jpg'

colorizer = ImageColorizer(model_path)
colorizer.colorize(input_path, output_path)
```
