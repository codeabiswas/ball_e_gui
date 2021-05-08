"""
helper_doc_reader.py
---
This file contains the DocReader class, which reads all the docs from their respective .md files
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

from pathlib import Path


class DocReader():
    """DocReader.
    This class reads all the docs for the GUI and stores using {Q:A} format in a dictionary object
    """

    def __init__(self, filepath):
        """__init__.

        Initializes the DocReader object

        :param filepath: The file path for the doc
        """
        self.filepath = filepath

    def get_doc(self):
        """get_doc.

        Stores in {Q:A} dictionary object given the .md filename
        """
        path = "{source}/Developer/ball_e_gui/docs/{doc_path}".format(
            source=Path.home(), doc_path=self.filepath)
        qn_list = list()
        ans_list = list()
        with open(path) as f:
            contents = f.read().splitlines()

        for content in contents:
            if content.startswith("##"):
                mod_content = content.strip("##")
                mod_content = mod_content.strip()
                qn_list.append(mod_content)
            elif len(content) > 0 and not(content.startswith('#')):
                mod_content = content.strip()
                ans_list.append(mod_content)

        return {qn_list[i]: ans_list[i] for i in range(len(qn_list))}
