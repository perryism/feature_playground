import re
def parse(txt):
    func_names = re.findall(r"(?<=def)\s+\w+\s*(?=\()", txt)
    return [ n.strip() for n in func_names ]

import logging
logger = logging.getLogger(__name__)
class WrapperTemplate(object):
    def __init__(self, txt):
        self.txt = txt.strip()

    def render(self):
        indented = "\n".join([ "    " + line for line in self.txt.split("\n")])
        func_names = parse(self.txt)

        if len(func_names) == 0:
            raise Exception("No function found")
        elif len(func_names) > 1:
            logger.warn("More than one function found, Use the first one %s", func_names[0])

        func_name = func_names[0]
        return f"""
def process(df):
{indented}
    return {func_name}
""".strip()