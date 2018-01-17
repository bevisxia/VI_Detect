# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 18:03
# @Author  : zhangxinhe
# @File    : frame_parser.py
import numpy as np
import tensorflow as tf
from libs.object_detection.utils import visualization_utils as vis_util
#from managers.component_manager import ComponentManager
from managers.config_manager import ConfigManager
from modules.frame.item import Item

def parse_origin_video_frame(origin_frame, session, detection_graph, category_index):
    image_np_expanded = np.expand_dims(origin_frame, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = session.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        origin_frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        #ComponentManager.get_category_index(),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=2)

    return origin_frame, scores, classes, boxes

def item_detect(scores, classes, boxes, category_index):

    item_list = []
    for i in range(len(scores[0])):
        item_score = scores[0][i]
        if item_score > 0.6:
            box = tuple(boxes[0][i].tolist())
            ymin, xmin, ymax, xmax = box

            # modified by xiabing. if box is too big. then ignore it.
            #if (xmax - xmin > 0.4) | (ymax - ymin > 0.4):
            #    continue

            item_id = classes[0][i]
            width = ConfigManager.get_width()
            height = ConfigManager.get_height()

            item_name = (category_index.get(classes[0][i]))['name']
            item_x = (xmin * width + xmax * width) / 2
            item_y = (ymin * height + ymax * height) / 2
            item = Item(item_id, item_name, item_x, item_y, item_score)
            item_list.append(item)
    return item_list