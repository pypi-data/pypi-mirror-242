import process_metrics

from time import sleep
import torch

_ = process_metrics.init()


model = torch.hub.load("ultralytics/yolov5", "yolov5n")
sleep(200)
