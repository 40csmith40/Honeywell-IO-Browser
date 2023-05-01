import os
from alive_progress import alive_bar
from classes import XMLFile

DIR_NAME = "Export"

name_lookup = {}
io_channels = []


import csv  

modules = []
header = ['IOMNUM', 'IONAME', 'IOLINK', 'IOP', 'CHANNUM', 'PNTTYPE', "PVEXEULO", "PVEULO", "PVEUHI", "PVEXEUHI"]

        
with alive_bar(len(os.listdir(DIR_NAME))) as bar:

    for file in os.listdir(DIR_NAME):

        if file.endswith('cnf.xml'):

            modules.append(XMLFile(os.path.join(DIR_NAME, file)))
            bar()
        else:
            bar()
            continue

rows = []

# Create lookup dict
with alive_bar(len(modules)) as bar:

    for module in modules:
        if not module.is_io:
            for sub_block in module.sub_blocks:
                if sub_block.is_io:
                    name_lookup[sub_block.block_id] = sub_block.block_name
        bar()

with alive_bar(len(modules)) as bar:

    for module in modules:

        if module.is_io:

            iomnum = module.get_parameter("IOMNUM")

            for sub_block in module.sub_blocks:

                try:

                    io_name = name_lookup[sub_block.block_id]

                except KeyError:

                    io_name = "N/A"

                row = [
                    iomnum, 
                    io_name,
                    module.assigned_to,
                    sub_block.get_parameter("IOP"), 
                    sub_block.get_parameter("CHANNUM"), 
                    sub_block.get_parameter("PNTTYPE"), 
                    sub_block.get_parameter("PVEXEULO"), 
                    sub_block.get_parameter("PVEULO"), 
                    sub_block.get_parameter("PVEUHI"), 
                    sub_block.get_parameter("PVEXEUHI")
                    ]

                rows.append(row)
        bar()


with open('IO.csv', 'w', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)