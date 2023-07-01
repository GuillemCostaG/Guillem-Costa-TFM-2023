import estudi_descriptors
import imutils
import cv2
import numpy as np
import pandas as pd
import openpyxl

import pandas as pd


nom_imatge='Dataset/First_Turbine_A_MID_1.png'
imageA = cv2.imread(nom_imatge)
imageA_resize = estudi_descriptors.resize_bordes(imageA)
results = estudi_descriptors.TrasnfArt(imageA_resize, 1)

df=pd.DataFrame(results)


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_positioning.xlsx', engine='xlsxwriter')

# Position the dataframes in the worksheet.
df.to_excel(writer, sheet_name='Sheet1', startcol=0)  # Default position, cell A1.

# Close the Pandas Excel writer and output the Excel file.
writer.close()


