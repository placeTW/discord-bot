# Boba

## Prerequisites

- Set the working directory to here before running the Python programs
- Download the [pre-trained model](https://mega.nz/file/Y0ZRnDgb#gLnKv0uYP-5y1LKJIFod-KuZ7hXw1XMUTlbz0GCNFuc) and place it under `commands/boba/models` as `boba.pth`

## Step 1: Training

Run `train.py`. It uses a Python library `detecto` which is built on top of pytorch.

By default, it trains on CPU. Of course you can see its instructions in the console to switch to GPU.

## Step 2: Validation

Run `validate.py` to see how poorly the model was trained.

It loads the model from `models/boba.pth` generated from step 1.

## Step 3: Prediction

Run `predict.py` to see how we can finally use our trained model to predict a single image for Discord usage.

It loads the model from `models/boba.pth` generated from step 1 again to do the prediction.

## Image Source

[Unsplash](https://unsplash.com/)

## Data Annotation Tool

Don't edit those xml files in `custom_dataset` manually. Use some tool.

I choose you, [labelImg](https://github.com/HumanSignal/labelImg).

1. Open the folder `custom_dataset`
2. Press `w` to add bounding boxes around boba to add labels, when it asks for label name, write `boba`
3. Save when you're done with labeling for all images

## Required Python Packages

- detecto: object detection
- pillow: scaling image
