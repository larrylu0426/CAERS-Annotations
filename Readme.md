# High-accuracy CAER-S Annotation

## Introduction to CAER-S

- CAER-S is an image-based dataset of Context-Aware Emotion Recognition, which is presented in ["Context-Aware Emotion Recognition Networks"(ICCV 2019)](https://caer-dataset.github.io/file/JiyoungLee_iccv2019_CAER-Net.pdf). The download link of CAER-S is [here](https://drive.google.com/a/yonsei.ac.kr/file/d/1cqB_5UmFQXacjPeRb8Aw1VE2v0vO4bdo/view?usp=sharing)

- CAER-S is extracted from [CAER](https://caer-dataset.github.io/index.html), which contains about 70K images.

- CAER and CAER-S are annotated with an extended list of 7 emotion categories.

- Each image is labeled with its source video.

## Introduction to High-accuracy CAER-S Annotation

- High-accuracy CAER-S Annotation provides the face bounding box information of the focused human who is the highest relevant to the image's label.

- High-accuracy CAER-S Annotation use `dlib` to make a pre-labeling and each line in it is checked and adjusted one by one manually.

- High-accuracy CAER-S Annotation ignores invalid images.

- The annotation of each image only contains one human's face bounding box.

## Motivation

- CAER-S only provides images and their labels (foler name).

- CAER-Net-S and CAER-Net use `dlib` to extract facial images but didn't provide their extracted images. It's hard to reproduce the results which are based on CAER-S.

- Some images in the CAER-S are logic-fuzzy and visual-fuzzy. These need to be ignored.

- Some images contain more than one human and a little images contain some misleading objects, such like photos， statues，and X-rays. These are hard to use `dlib` to make automated labeling.


## Questions or Issues?

Please make an issue or contact with me: larrylu0426@gmail.com