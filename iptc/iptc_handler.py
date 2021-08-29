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
                # print(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg")
                info = IPTCInfo(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg", force=True)
                info['headline'] = row['headline']
                info['keywords'] = row['keywords']
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
            try:
                info = IPTCInfo(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg")
                row['headline'] = info['headline']
                print("Headline", info['headline'])
                row['keywords'] = info['keywords']
                x = "".join(info['keywords'])
                print("Keywords", x)
                row['creator'] = info['creator']
                print("Creator", info['creator'])
                row['date created'] = info['date_created']
                print("Date Created", info['date_created'])
                row['sub-location'] = info['sub-location']
                print("Sub-location", info['sub-location'])
                row['city'] = info['city']
                print("City", info['city'])
                row['province/state'] = info['province/state']
                print("Province/ State", info['province/state'])
                row['country'] = info['country/primary location name']
                print("Country", info['country/primary location name'])
                row['category'] = info['category']
                print("Category", info['category'])
                row['description'] = info['description']
                print("Description", info['description'])
            except:
                pass
        # retouch_file.to_csv("output.csv")
        return "IPTC Metadata returned."

    def validate_excel(self):
        """
        Validates all images name in excel.
        """
        # Load file
        retouch_file = pd.read_csv(self.file)

        # Error Images
        error_images = []

        # Loop over rows
        for index, row in retouch_file.iterrows():
            # print(row['image_name'])            
            if not os.path.isfile(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg"):
                error_images.append(row["image_name"])
        if len(error_images) > 0:
            response = {"error": error_images}
        else:
            response = {"success": 0}
        return response

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
    return None

if __name__ == "__main__":
    IPTCKeyword()