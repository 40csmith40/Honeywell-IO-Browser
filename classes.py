import xml.etree.ElementTree as ET

class SubBlock():

    ns = {'xmlns': 'x-schema:ConfigFileSchema.xml'}

    def __init__(self, block):
        
        self.parameters = {}

        self.block = block
        self.block_name = block.find('xmlns:BlockDef', self.ns).find('xmlns:BlockName', self.ns).text.strip()
        self.block_id = block.find('xmlns:BlockDef', self.ns).find('xmlns:BlockId', self.ns).text.strip()
        self.name = self.block.find('xmlns:BlockDef', self.ns).find('xmlns:TemplateName', self.ns).text.strip()
        self.base_template_name = self.block.find('xmlns:BlockDef', self.ns).find('xmlns:TemplateName', self.ns).text.strip()
        self.is_io = self.base_template_name.split(':')[0] == 'SERIES_C_IO'

        for parameter in self.block.find('xmlns:Parameters', self.ns).findall('xmlns:Parameter', self.ns):
            if parameter.find('xmlns:ParamValue', self.ns).text:
                self.parameters[parameter.find('xmlns:ParamName', self.ns).text.strip()] = parameter.find('xmlns:ParamValue', self.ns).text.strip()
            else:
                self.parameters[parameter.find('xmlns:ParamName', self.ns).text.strip()] = None

    def get_parameter(self, parameter):

        try:

            param = self.parameters[parameter]

        except KeyError:

            param = "N/A"

        return param


class XMLFile():

    ns = {'xmlns': 'x-schema:ConfigFileSchema.xml'}

    def __init__(self, path):

        self.sub_blocks = []
        self.parameters = {}
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.block = self.root.find('xmlns:Block', self.ns)
        self.block_def = self.block.find('xmlns:BlockDef', self.ns)
        self.name = self.block_def.find('xmlns:TemplateName', self.ns).text.strip()
        self.base_template_name = self.block_def.find('xmlns:TemplateName', self.ns).text.strip()
        self.assigned_to = self.block_def.find('xmlns:AssignedTo', self.ns)

        if self.assigned_to is not None:
            self.assigned_to = self.assigned_to.text.strip()
        else:
            self.assigned_to = "N/A"
        
        self.is_io = self.base_template_name.split(':')[0] == 'SERIES_C_IO'
        self.is_cm = self.base_template_name == 'SYSTEM:CONTROLMODULE'
        self.get_sub_blocks()

        for parameter in self.block.find('xmlns:Parameters', self.ns).findall('xmlns:Parameter', self.ns):
            if parameter.find('xmlns:ParamValue', self.ns).text:
                self.parameters[parameter.find('xmlns:ParamName', self.ns).text.strip()] = parameter.find('xmlns:ParamValue', self.ns).text.strip()
            else:
                self.parameters[parameter.find('xmlns:ParamName', self.ns).text.strip()] = None

    def get_parameter(self, parameter):

        try:

            param = self.parameters[parameter]

        except KeyError:

            param = "N/A"

        return param


    def get_sub_blocks(self):

        emb_blocks = self.block.find('xmlns:EmbBlocks', self.ns)

        if emb_blocks:

            for sub_block in emb_blocks.findall('xmlns:Block', self.ns):
                
                self.sub_blocks.append(SubBlock(sub_block))
