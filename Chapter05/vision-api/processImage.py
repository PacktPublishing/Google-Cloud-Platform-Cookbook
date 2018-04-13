import argparse
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image

bucket_id = 'images' #Enter bucket name
 
def upload2GCS(project_id, file_name):
    # Uploads the images to Google Storage
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_id)
    gcs_filename = "tmp" #Adding a prefix to the file name
    gcs_filename = gcs_filename + file_name
    blob2 = bucket.blob(gcs_filename)
    blob2.upload_from_filename(filename=file_name)
    return("File uploaded to GCS : ", file_name)

def visionTest(project_id, img_file):
    # Function verifies if the images contains a face and is not spoofed using the Cloud Vision API
    
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY') # Names of likelihood from google.cloud.vision.enums
    vclient = vision.ImageAnnotatorClient()
    content = img_file.read()
    image = types.Image(content=content)
    faceResult = vclient.face_detection(image=image).face_annotations
    if not faceResult:
        return("Uploaded images does not contains a person's face")
    else:
    # Test for safe content
        response = vclient.safe_search_detection(image=image)
        safe = response.safe_search_annotation
        if likelihood_name[safe.spoof] in ['LIKELY', 'VERY_LIKELY']:
            return('Possible spoofed image')
        else:
            return('Upload2GCS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument('file_name', help='Local file name')
    
    args = parser.parse_args()
    with open(args.file_name, 'rb') as image:
        result = visionTest(args.project_id, image)
    if result == "Upload2GCS":
        result = upload2GCS(args.project_id, args.file_name)    
    print(result)

