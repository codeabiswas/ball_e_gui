from pathlib import Path


class DocReader():
    def __init__(self, filepath):
        self.filepath = filepath

    def get_doc(self):
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
