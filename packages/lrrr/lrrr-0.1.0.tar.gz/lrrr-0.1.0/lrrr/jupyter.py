
import os
from nbconvert import HTMLExporter, MarkdownExporter
from colorama import Fore,Back
from .utils import run
from .markdown import Markdown
from slurm.files import rm


class Jupyter:
    def __init__(self, template, root):
        self.root = root
        # self.exporter = HTMLExporter()
        self.mexporter = MarkdownExporter()
        self.markdown = Markdown(template, root)
        # self.exporter.template_name = 'base'
        # self.exporter.theme = "light"
        # self.anchor_link_text = ""
        self.template = template

    def to_markdown(self, dest, file, to_main):
        (mark, resources) = self.mexporter.from_filename(file)

        # change: ![png](file) -> ![](file)
        # otherwise you have png everywhere
        mark = mark.replace("![png]", "![]")

        # Save embedded images as png files
        if "outputs" in resources:
            for k,v in resources["outputs"].items():
                with open(f"{dest}/{k}", "wb") as fd:
                    fd.write(v)

        fname, ext = os.path.splitext(file)
        with open(f"{dest}/{fname}.md", "w") as fd:
            fd.write(mark)

    def to_html(self, dest, file, to_main):
        fname, ext = os.path.splitext(file)

        self.to_markdown(dest, file, to_main)
        self.markdown.process(dest, f"{dest}/{fname}.md", to_main)

        # remove the temporary markdown file ... all done
        rm(f"{dest}/{fname}.md")

        print(f"{Fore.GREEN}>> Jupyter: {file}{Fore.RESET}")

    # def extractOneTag(self, text, tag):
    #     """
    #     Given a tag, this will return what is inside of it.
    #     """
    #     return text[text.find("<"+tag+">") + len("<"+tag+">"):text.find("</"+tag+">")]

    # def to_html2(self, dest, file, to_main):
    #     """
    #     handle a jupyter notebook
    #     """
    #     (html, resources) = self.exporter.from_filename(file)
    #     # pprint(resources)
    #     html = self.extractOneTag(html, "body")
    #     html = self.template.render(info=html, path=to_main)
    #
    #     fname, ext = os.path.splitext(file)
    #     htmlfile = f'{fname}.html'
    #     with open(f"{dest}/{fname}.html", 'w') as fd:
    #         fd.write(html)
    #
    #     print(f"{Fore.GREEN}>> Jupyter: {htmlfile}{Fore.RESET}")

    # def get_template_names(self):
    #     return self.exporter.get_template_names()
    #
    # def defaults(self):
    #     pprint(html_exporter.trait_values())
