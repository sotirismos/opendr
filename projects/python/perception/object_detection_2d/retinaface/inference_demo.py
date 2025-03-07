# Copyright 2020-2024 OpenDR European Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from opendr.engine.data import Image
from opendr.perception.object_detection_2d import RetinaFaceLearner
from opendr.perception.object_detection_2d import draw_bounding_boxes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", help="Device to use (cpu, cuda)", type=str, default="cuda", choices=["cuda", "cpu"])
    parser.add_argument("--backbone", help="Network backbone", type=str, default="resnet", choices=["resnet", "mnet"])

    args = parser.parse_args()

    learner = RetinaFaceLearner(backbone=args.backbone, device=args.device)
    learner.download(".", mode="pretrained")
    learner.load("./retinaface_{}".format(args.backbone))

    learner.download(".", mode="images")
    img = Image.open("./cov4.jpg")
    bounding_boxes = learner.infer(img)

    img = draw_bounding_boxes(img.opencv(), bounding_boxes, learner.classes, show=True)
