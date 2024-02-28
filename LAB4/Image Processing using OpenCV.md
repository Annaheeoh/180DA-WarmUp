# Image Processing Using OpenCV

## Introduction
Welcome to our exploration of OpenCV, a powerful tool in the realm of image processing. In today's digital landscape, the manipulation and analysis of images are integral across diverse fields such as healthcare, surveillance, entertainment, and automotive industries. OpenCV, developed by Intel in the late 1990s and maintained by Willow Garage and Itseez, stands as a cornerstone in this domain, offering a comprehensive library of functions and algorithms for image and video analysis. Throughout this tutorial, we will delve into the basic fundamental practical applications of OpenCV, ranging from facial recognition and visual search to medical diagnosis and quality control. By understanding how OpenCV empowers us to address real-world challenges, we can harness its capabilities to enhance our understanding and utilization of image processing techniques.

## A Breif Background of Image Processing
Image processing involves applying methods to images to improve them or extract valuable information. It's a form of signal processing where input is an image, and output can be the enhanced picture or its features. There are two types of image processing: analog and digital. Analog processing improves physical copies like prints, while digital methods allow computer-assisted alterations. Image analysts use various interpretative approaches in their work. Digital image processing techniques facilitate computer-assisted image editing. In digital processing, data undergoes three main phases: preprocessing, augmentation and display, and information extraction.

<img src="https://github.com/ECE-180D-WS-2024/Wiki-Knowledge-Base/blob/main/Images/Image.jpg" width="300">
Figure 1. How Image Processing works, Source: https://www.researchgate.net/publication/309242883_Image_Acquisition_Noise_removal_Edge_Detection_Methods_in_Image_Processing_Using_Matlab_for_Prawn_Species_Identification

When diving into the world of image processing with OpenCV, illuminating the path to mastering its myriad functionalities. Let's explore three fundamental aspects of image processing using OpenCV tutorials: Changing colorspaces, Image Gradient, and Contours.

## Tutorials
### Tutorial 1: Changing colorspcaes
In this tutorial, we will explore the intricacies of image color-space conversion, mastering transitions such as BGR ↔ Gray and BGR ↔ HSV. Also, you'll adeptly employ fundamental functions like cv.cvtColor() and cv.inRange().
Color-space conversion is a cornerstone in image processing, with OpenCV offering an extensive array of over 150 conversion techniques. However, our primary focus will be on two key methods: BGR ↔ Gray and BGR ↔ HSV.

For seamless color conversion, we'll leverage the versatility of the cv.cvtColor() function, where the 'flag' parameter defines the specific transition. For instance, BGR → Gray conversion will utilize the flag cv.COLOR_BGR2GRAY, while BGR → HSV will employ cv.COLOR_BGR2HSV.

```
    import cv2 as cv
    flags = [i for i in dir(cv) if i.startswith('COLOR_')]
    print( flags )

```
Different software uses different scales. So, if you are comparing OpenCV values with them, you need to normalize these ranges. For HSV, the hue range is [0, 179], saturation range is [0, 255], and value range is [0, 255].

### Tutorial 2: Image Gradient
In this tutorial, we will dicuss about finding image gradients using functions cv.Sobel(), cv.Scharr(), cv.Laplacian(), and others. OpenCV provides three types of gradient filters or High-pass filters: Sobel, Scharr, and Laplacian. Let's explore each of them.
 
Before we dive into extracting image derivatives with OpenCV, let's quickly grasp what image derivatives are and why they matter. Image derivatives are crucial for detecting edges in images. They pinpoint areas where pixel intensity changes sharply, essentially mapping out the boundaries within an image. This fundamental concept serves as the basis for edge detection algorithms.

#### 1. Sobel and Scharr Derivatives
The Sobel operator combines Gaussian smoothing with differentiation, making it robust against noise. It allows specifying the direction of derivatives (vertical or horizontal) using the 'yorder' and 'xorder' arguments, respectively. Additionally, the 'ksize' argument lets you define the kernel size. If 'ksize' equals -1, a 3x3 Scharr filter is applied, which typically yields better results than a 3x3 Sobel filter. 


<img src="https://github.com/ECE-180D-WS-2024/Wiki-Knowledge-Base/blob/main/Images/Sobel%20Operator.png" width="300">
Figure 2. Sober operator, source: https://theailearner.com/tag/scharr-operator/

### Tutorial 3: Contours
Contours are essentially curves that connect continuous points along the boundary of regions with the same color or intensity. They serve as a valuable tool for shape analysis, object detection, and recognition. To work effectively with contours, it's advisable to use binary images. Therefore, before detecting contours, it's recommended to apply thresholding or Canny edge detection. In OpenCV, the process of finding contours is akin to locating white objects on a black background. Thus, it's crucial to ensure that the object of interest appears white while the background remains black for optimal detection.

```
import numpy as np
import cv2 as cv
im = cv.imread('test.jpg')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
 ```

## Conclusion
In summary, image processing emerges as a powerful tool, allowing us to manipulate and analyze digital images effectively. Throughout this tutorial, we delved into key techniques such as changing color spaces, utilizing image gradients, and identifying contours. Changing color spaces facilitates the simplification of image complexities, enabling more accurate and efficient processing. Image gradients provide essential information about the intensity variations within an image, aiding in edge detection and object boundary identification. Contour detection further enhances our ability to segment and extract meaningful features from images. These techniques represent fundamental elements of image processing under the OpenCV library. With further exploration and application, individuals can develop captivating visualizations and extract valuable insights, particularly in the fields of artificial intelligence, facial recognition, and advanced image processing techniques.

## References
1. Nagalakshmi, Dr & Jyothi, Singaraju. (2015). Image Acquisition, Noise removal, Edge Detection Methods in Image Processing Using Matlab for Prawn Species Identification. G Nagalakshmi, S Jyothi.
2. https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
3. https://www.projectpro.io/recipes/what-are-sobel-and-scharr-derivatives-opencv
4. https://theailearner.com/tag/scharr-operator/
