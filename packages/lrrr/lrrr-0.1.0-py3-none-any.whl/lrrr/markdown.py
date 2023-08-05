

import os
from colorama import Fore,Back
from .utils import run


class Markdown:
    def __init__(self, template, root):
        self.template = template
        self.root = root

    def filter_unicode(self, md):
        """
        Sometimes I have (historically) been bitten by invisible (unprintable)
        unicode sneaking into my work causing issues. This is far less common
        today, but just in case, this filters it out.
        """
        return ''.join(char for char in md if char in printable)

    def process(self, dest, file, to_main, EXTENTIONS=None, TEMPLATE=None):
        """
        Generate the html and save to disk
        """
        # yaml: sets up date/title ... not sure it is worth it
        # footnotes: something[^1] ... [^1]: http://somewhere.com
        # emoji: why not?
        if EXTENTIONS is None:
            EXTENTIONS = "markdown\
            +footnotes\
            +emoji".replace(" ","")

        # generate the body of the html
        if TEMPLATE is None:
            cmd = f"pandoc -f {EXTENTIONS} -t html5 {file}"
        else:
            cmd = f"pandoc -f {EXTENTIONS} --template {TEMPLATE} -t html5 {file}"


        # print(f"{Fore.RED}>> {cmd} {Fore.RESET}")
        html = run(cmd)
        # print(html)
        html = self.template.render(info=html, path=to_main)

        fname, ext = os.path.splitext(file)

        with open(f"{dest}/{fname}.html", 'w') as fd:
            fd.write(html)

    def to_html(self, dest, file, to_main):
        """
        Generate the html and save to disk
        """

        EXTENTIONS = "markdown\
        +yaml_metadata_block\
        +footnotes\
        +emoji".replace(" ","")

        TEMPLATE = f"{self.root}/resources/template.markdown.pandoc"

        self.process(dest, file, to_main, EXTENTIONS, TEMPLATE)

        print(f"{Fore.MAGENTA}>> Markdown: {file}.html{Fore.RESET}")
