# img2desmos 
The `img2desmos` library allows you to convert images into Desmos-style pixel art using Python.

## Installation


```bash
git clone https://github.com/kaitlek/img2desmos.git # or download the zip with the "Code" button above
cd discord-voicemessage-sender
pip install -r requirements.txt
```

## Requirements

Install the required dependencies using the following command:
```bash
pip install -r requirements.txt` 
```

## Usage 

1.  Import the `img2desmos` class from the `img2desmos` module:
2.  Create an instance of the `img2desmos` class:
3.  Use the `DrawImage` method to convert an image into Desmos-style pixel art. Provide the path to the image and specify the desired size (largest side in pixels):
    ```python
	from img2desmos import img2desmos
	i2d = img2desmos()
	i2d.DrawImage(r"D:\image\path.png", 16)  
	#change 16 to however many pixels you want the largest side to be, 
	#greater than 32 is very laggy
	```



## Disclaimer

This library is provided as-is and may require further configuration or adjustments based on your specific use case. Use it responsibly and in compliance with relevant terms and conditions.

Remember to update the paths, sizes, and other details according to your actual project requirements.
