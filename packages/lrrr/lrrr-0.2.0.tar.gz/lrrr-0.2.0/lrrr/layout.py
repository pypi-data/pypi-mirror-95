

from .utils import rmdir, run, cleanup
from slurm.files import rm, mkdir, find
import os              # make directories, change current dir, etc
import shutil          # move and delete files/folders
from collections import OrderedDict  # put toc in alphebetical order
from glob import glob  # get contents of folder
# import pygments
import pathlib
from colorama import Fore,Back
from .jupyter import Jupyter
from .markdown import Markdown


SKIP_EXT = [
    ".bag", ".h5", ".pickle", ".gz", ".heic", ".old", ".old2",
    ".caffemodel", ".pnm", ".ps", ".html", ".try"
]

SKIP_FOLDERS = ['old', 'do_not_backup', 'deleteme',
    'large_dataset', 'draft', "__pycache__", ".ipynb_checkpoints", "archive"]


def move_resources(src, dest):
    files = glob(f"{src}/*")
    for file in files:
        # file = os.path.basename(file)
        path = dest + '/' + os.path.basename(file)
        print(f'{Fore.CYAN}>> Copying file {file}{Fore.RESET}')
        shutil.copy(file, path)


class Builder:
    def __init__(self, info):
        template = info["template"]
        root = info.get("root", str(pathlib.Path().absolute()))
        resouces = info.get("resources", "resources")

        self.jup = Jupyter(template, root)
        self.mark = Markdown(template, root)
        self.template = template
        self.root = root
        self.source = info.get("src", "source")
        self.output = info.get("dest", "html")

    def run(self):
        # clean up the input
        cleanup(
            self.source,
            files=[".DS_Store", "deleteme", "dummy"],
            folders=[".ipynb_checkpoints", "__pycache__", "deleteme"]
        )
        self.build_pages()
        self.build_toc2(self.output)
        move_resources("resources", self.output)

    def pandoc(self, file, dest, to_main='.'):
        """
        dest - where html blog goes
        template - html template
        format - doing html
        to_main - get back to source directory. need to keep track of folder
        stucture for navigation bar across the top of the page
        """
        # handle files
        if os.path.isfile(file):
            try:
                f, ext = os.path.splitext(file)
            except Exception:
                print(f'{Fore.RED}*** this file has bad name: {file} ***{Fore.RESET}')
                exit(1)

            ext = ext.lower()

            if ext in ['.md']:
                # convert markdown to html
                self.mark.to_html(dest, file, to_main)

            elif ext == ".rst":
                run(f"pandoc --from rst --to markdown -o {file}.md.try {file}")
                run(f"mv {file} {file}.old")

            elif ext == '.ipynb':
                # generate jupyter to html
                self.jup.to_html(dest, file, to_main)

            elif ext in SKIP_EXT:
                # print(f"{Fore.RED}*** {file}: won't copy to website ***{Fore.RESET}")
                pass

            else:
                path = dest + '/' + file
                # print(f'{Fore.CYAN}>> Copying file {file}{Fore.RESET}')
                shutil.copy(file, path)

        # let's handle directories
        elif os.path.isdir(file):
            if file.lower() in SKIP_FOLDERS:
                print(f'{Fore.YELLOW}>> Skipping folder {file}{Fore.RESET}')
                return

            # this must be a directory, let's change into it
            if to_main == "./..":
                print(f'==[{file:15}] ===============================')

            # make the destination path have the same folder
            path = dest + '/' + file
            mkdir(path)

            # change into it, get the files and recursively call pandoc
            os.chdir(file)
            files = glob('*')
            for f in files:
                self.pandoc(f, '../' + dest + '/' + file, to_main=to_main + '/..')
            os.chdir('../')
        else:
            print('***********************************')
            print(f'*** Unknown File Type: {file}')
            print('***********************************')
            # raise Exception()

    def build_pages(self):

        # delete the old website so we don't miss anything when building
        print('Cleaning out old html ------------------')
        rmdir(self.output)
        mkdir(self.output)

        # change into source and recursively build website
        os.chdir(self.source)

        # grab files and folders
        files = glob("*")
        files.sort()

        # for each file/directory in sourece build it into pdf or copy it
        for f in files:
            self.pandoc(f, '../' + self.output)

        # done
        os.chdir('..')

    def getSubDir(self, path):
        # print(f"{Fore.CYAN}>>   {path}{Fore.RESET}")
        files = {}
        # os.chdir(path)
        fs = find(path,"*.html")
        for f in fs:
            bname = os.path.basename(f)
            name, ext = os.path.splitext(bname)
            name = name.replace('-', ' ').replace('_', ' ').title()
            # name = name.replace('-', ' ').replace('_', ' ')
            # print(name,f)
            files[name] = str(f).split(self.output + "/")[1]
        # return files
        return OrderedDict(sorted(files.items()))


    def getDir(self, path):
        """
        Get and return a list of files and directories in this path
        """
        # print(f"{Fore.GREEN}>> {path}{Fore.RESET}")
        objs = glob(path)
        objs.sort()
        dirs = []
        for o in objs:
            if os.path.isdir(o):
                # don't save these folders
                if o.find('pics') >= 0 or o.find('static') >= 0:
                    pass
                else:
                    dirs.append(o)
            # elif os.path.isfile(o):
            #     files.append(o)
            # else:
            #     print(f"{Fore.RED}*** Unknown: {o} ***{Fore.RESET}")
        return dirs

    def build_toc2(self, path):

        toc = {}

        dirs = self.getDir(path + "/*")

        for d in dirs:
            dd = os.path.basename(d).replace('-', ' ').replace('_', ' ').title()
            toc[dd] = self.getSubDir(d)

        toc = OrderedDict(sorted(toc.items()))

        html = self.template.render(TOC=toc, path='.')
        with open(self.output + '/topics.html', 'w') as fd:
            fd.write(html)
        print(f"{Fore.CYAN}>> Made topics.html{Fore.RESET}")
        # pprint(toc)
