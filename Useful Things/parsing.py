import logging
import numpy as np
import traffic_routing_pb2


def array_to_msg(line):
    """Returns a message of type Float1DArray with elements in list-like argument."""
    array_msg = traffic_routing_pb2.Float1DArray()
    array_msg.elems.extend(line.tolist())
    return array_msg


def matrix_to_msg(matrix):
    """Returns a message of type Float2DArray with elements from the input two-dimensional array."""
    matrix_msg = traffic_routing_pb2.Float2DArray()
    if matrix is None:
        return matrix_msg
    for i in range(matrix.shape[0]):
        matrix_msg.lines.append(array_to_msg(matrix[i, :]))
    return matrix_msg


def msg_to_matrix(msg, n_lines=None, n_cols=None):
    """Decodes a 2D array from a protobuf message and returns it as numpy array.

    :param msg: Message of type Float2DArray, as defined in traffic_routing.proto
    :param n_lines: (Optional) Length of array. If not indicated, it is inferred from the message.
    :param n_cols: (Optional) Width of array. If not indicated, it is inferred from the first line of the array.
    :return: Numpy array or None if msg has wrong format.
    """
    if not msg or not msg.lines:
        logging.error("Detected empty array message.")
        return None

    # Get input data size
    if n_lines is None or n_cols is None:
        n_lines = len(msg.lines)
        n_cols = len(msg.lines[0].elems)

    # Build array from message
    matrix = np.zeros((n_lines, n_cols))
    for i in range(n_lines):
        if len(msg.lines[i].elems) != n_cols:  # Detect line with more than n_cols elements
            logging.error("Detected inconsistent number of elements per line.")
            return None
        matrix[i] = np.array(msg.lines[i].elems)
    return matrix


def msg_to_image(msg, height=None, width=None):
    """Reads a protobuf message of type Image and returns it as numpy array.

    :param msg: Message of type Image, as defined in traffic_routing.proto
    :param height: (Optional) Height of image. If not indicated, it is inferred from the first color channel.
    :param width: (Optional) Width of image. If not indicated, it is inferred from the first line.
    :return: Numpy array with dimensions (3, Height, Width) or None if msg has wrong format.
    """
    if not msg or not msg.img or not msg.img.matrices:
        logging.error("Received empty image message.")
        return None

    # Get input data size
    n_channels = len(msg.img.matrices)
    if height is None or width is None:
        height = msg.height
        width = msg.width
    if n_channels != 3 and n_channels != 1:
        logging.error("Detected image with incorrect number of color channels. Must be either 3 (RGB) or "
                      "1 (grayscale).")
        return None

    image = np.zeros((height, width, n_channels))
    for i in range(n_channels):
        image[:, :, i] = msg_to_matrix(msg.img.matrices[i])

    return image


def image_to_msg(img):
    """Receives an image as numpy array and returns it as a protobuf message of type Image."""
    if img.ndim == 2:  # Expand dimensions if the image is grayscale
        img = np.expand_dims(img, axis=0)
    elif img.ndim != 3:
        logging.error("Detected image with incorrect number dimensions. Must be either 3xMxN (Color image) or "
                      "MxN (grayscale).")
        return traffic_routing_pb2.Image()

    # Get image size
    img_height = img.shape[0]
    img_width = img.shape[1]

    # Build Image message
    img_msg = traffic_routing_pb2.Image(width=img_width, height=img_height)
    for i in range(img.shape[2]):
        img_msg.img.matrices.append(matrix_to_msg(img[:, :, i]))

    return img_msg
