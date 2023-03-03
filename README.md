# Fully transparent AI model inference

This repo contains an Evervault Cage which hosts a model for brain tumor segmentation. The client script uses the attestation measures of the Cage shown in the public deployment workflow to verify that the code running in the Cage does the following and no more:

* Loads in model weights from a private S3 bucket. These weights are kept secret from the user, so that the model provider could charge for their use.
* Hosts a `/upload` endpoint for file uploads. When a file is received, the brain tumor segmentation model is run on the received image. The result is returned in a download to the user.

This allows users to upload sensitive images to the Cage, while proving that their images cannot be leaked from the Cage.
