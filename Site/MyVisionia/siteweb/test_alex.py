import darknet.darknet as dn
import cv2 as cv2
import faulthandler

def image_detection(image_or_path, network, class_names, class_colors, thresh):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    width = dn.network_width(network)
    height = dn.network_height(network)
    darknet_image = dn.make_image(width, height, 3)

    if type(image_or_path) == "str":
        image = cv2.imread(image_or_path)
    else:
        image = image_or_path
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    dn.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = dn.detect_image(network, class_names, darknet_image, thresh=thresh)
    dn.free_image(darknet_image)
    image = dn.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

def load_network(config_file, data_file, weights, batch_size=1):
    """
    load model description and weights from config files
    args:
        config_file (str): path to .cfg model file
        data_file (str): path to .data model file
        weights (str): path to weights
    returns:
        network: trained model
        class_names
        class_colors
    """
    network = dn.load_net_custom(
        config_file.encode("ascii"),
        weights.encode("ascii"), 0, batch_size)
    metadata = dn.load_meta(data_file.encode("ascii"))
    class_names = [metadata.names[i].decode("ascii") for i in range(metadata.classes)]
    colors = dn.class_colors(class_names)
    return network, class_names, colors

faulthandler.enable()
#test_img = prepare_batch("/NNvision/darknet/data/dog.jpg","/NNvision/darknet/cfg/yolov4-tiny.cfg",channels=3)
img = cv2.imread("/NNvision/darknet/data/dog.jpg")

network, classNames, classColors = dn.load_network("/NNvision/darknet/cfg/yolov4-tiny.cfg", "/NNvision/darknet/cfg/coco.data", "/NNvision/darknet/yolov4-tiny.weights")
image_detection(img, network, classNames, classColors, 0.2)
