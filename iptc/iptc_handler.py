import pandas as pd
import math
from iptcinfo3 import IPTCInfo
import logging
import sys
from django.conf import settings


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
            print(f"Image no {row['image_name']}.")
            # Check if image exists
            try:
                info = IPTCInfo(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg", force=True)
                # info['headline'] = row['Headline']
                info['caption/abstract'] = row['Description/Caption']
                info['keywords'] = [row['keywords']]
                # info['keywords'] = [row['keywords']]
                # print(row["keywords"])
                # info['custom1'] = row['Length']
                # info['custom2'] = row['Creator/Photgrapher']
                # info['release date'] = row['Date Created']
                # info['sub-location'] = row['sub-location']
                # info['city'] = row['City']
                # info['province/state'] = row['State/Province']
                # info['country/primary location name'] = row['Country']
                # info['category'] = row['Category OR IPTC Scene']
                if math.isnan(row['Special Instructions']):
                    pass
                else:
                    info['special instructions'] = row['Special Instructions']
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
            print(f"Image no {row['image_name']}.")
            info = IPTCInfo(f"{settings.MEDIA_ROOT}/images/{row['image_name']}.jpg")
            # print(f"Image: {row['image_name']}.jpg")
            print("Headline: ", info['headline'])
            print("Keywords: ", info['keywords'])
            # print("Caption: ", info['caption/abstract'])
            # print("City: ", info['city'])
            print(f"Sub-location: {info['sub-location']} \n")
        return "IPTC Metadata returned."

# iptc = IPTCKeyword(sys.argv[1])
# iptc.save_metadata()
# iptc.get_metadata()

def modify_input_for_multiple_files(property_id, image):
    dict = {}
    dict['id'] = property_id
    dict['images'] = image
    return dict

if __name__ == "__main__":
    IPTCKeyword()