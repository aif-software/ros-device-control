# MultiSense Stereo Camera S27 Documentation

Here is some documentation about the topics that the stereo camera broadcasts.

## /left

### /left/image_mono

A 8 bit grayscale image from the MultiSense’s left camera. This image has no distortion compensation applied to it, and is the raw input to the main MultiSense stereo pipeline.

### /left/image_rect

A 8 bit grayscale image from the MultiSense’s left camera rectified using the [MultiSense calibration](https://docs.carnegierobotics.com/calibration/stereo.html). This is the output from the MultiSense rectification process, and is a direct input for the MultiSense disparity matching algorithm.

#### /left/topic/camera_info

Info about the image that is not included in the metadata of the image itself, such as distortion model.

### /left/disparity

The disparity source refers to the disparity values computed from the left rectified camera’s perspective. For each pixel in the left rectified image, the disparity source provides the difference in the horizontal position between that pixel and the pixels along the corresponding epipolar line in the right rectified image.
More info can be found [here](https://docs.carnegierobotics.com/sources/overview.html#disparity).

### /left/cost

The corresponding cost for each pixel in the disparity image. Higher cost values represent less confidence in the disparity value generated for that pixel location.

### /left/depth

Depth value that is calculated from the stereo disparity data. Provided as a standard floating-point depth map aligned with the left camera’s frame. Data type is float32.

### /left/openni_depth

Depth value that is calculated from the stereo disparity data. Should be used if the analysis pipeline uses OpenNI-format of depth image analysis. Also aligned with the left camera’s frame. Data type is unsigned 16-bit.

<brk>

## /aux

### /aux/image_mono

A 8 bit grayscale image from the MultiSense’s aux camera. This image has no distortion compensation applied to it, and is the luminance component (Y) of the planar YCbCr420 encoding for aux color images.

### /aux/image_rect

A 8 bit grayscale image from the MultiSense’s aux camera rectified using the [MultiSense calibration](https://docs.carnegierobotics.com/calibration/stereo.html), and is the luminance component (Y) of the planar YCbCr420 encoding of aux color images.

### /aug/image_color

A 16 bit image from the MultiSense’s aux camera encoding the Cb and Cr components of the aux cameras planar YCbCr420 encoding. The 8 bit Cb and 8 bit Cr components are packed into each 16 bit pixel. The chroma image is 1/4 resolution of the corresponding luma image. This image has no distortion compensation applied to it.

### /aux/image_rect_color

A 16 bit image from the MultiSense’s aux camera encoding the Cb and Cr components of the aux cameras planar YCbCr420 encoding. This image is rectified using the [MultiSense calibration](https://docs.carnegierobotics.com/calibration/stereo.html).
