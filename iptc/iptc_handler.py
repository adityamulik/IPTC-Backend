from django.conf import settings

import pandas as pd
import math
from iptcinfo3 import IPTCInfo
import logging
import os
import sys
import subprocess
import glob



# Logger Details
logging.basicConfig(filename="iptc_logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.ERROR)


class IPTCKeyword():

    def __init__(self, file):
        self.file = file

    def is_nan(self, row_data):
        """
        Checks if a excel cell has empty value.
        """
        return math.isnan(row_data)

    def save_metadata(self):
        """
        Saves metadata defined in the excelsheet and
        saves to iptc database.
        """
        # Load file
        retouch_file = pd.read_csv(self.file)
        
        # Loop over rows
        for index, row in retouch_file.iterrows():
            # Check if image exists
            try:
                print(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg")
                info = IPTCInfo(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg", force=True)
                info['headline'] = row['headline']
                info['keywords'] = [row['keywords']]
                info['creator'] = row['creator']
                info['date created'] = row['date_created']
                info['sub-location'] = row['sub-location']
                info['city'] = row['city']
                info['province/state'] = row['province/state']
                info['country/primary location name'] = row['country']
                info['category'] = row['category']
                info['description'] = row['description']
                try:
                    info.save()
                    print("Worked!")
                except:
                    logger.error(f"Error saving metadata in IPTC database for image {row['image_name']}.jpg")
            except:
                logger.error(f"{row['image_name']}.jpg is not available.")
        return "IPTC Field mapping completed."

    def get_metadata(self):
        """
        Gets all metadata of a image file from iptc.
        """
        # Load file
        retouch_file = pd.read_csv(self.file)
        
        # Loop over rows
        for index, row in retouch_file.iterrows():
            info = IPTCInfo(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg")
            print(f"Image: {row['image_name']}.jpg")
            print("Headline: ", info['headline'])
            print("Keywords: ", info['keywords'])
            print("Creator: ", info['creator'])
            print("City: ", info['city'])
            print(f"Sub-location: {info['sub-location']}")
            print(f"Description: {info['description']} \n")
        return "IPTC Metadata returned."


def modify_input_for_multiple_files(property_id, image):
    dict = {}
    dict['id'] = property_id
    dict['images'] = image
    return dict

def discard_files():
    for fl in glob.glob(settings.MEDIA_ROOT + "/excel/*"):
        os.remove(fl)
    for fl in glob.glob(settings.MEDIA_ROOT + "/images/*"):
        os.remove(fl)
    os.remove(settings.BASE_DIR + "/images.zip")
    return None

if __name__ == "__main__":
    IPTCKeyword()