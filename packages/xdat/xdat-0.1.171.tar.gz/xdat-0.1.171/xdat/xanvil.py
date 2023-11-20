"""
Credit: https://pypi.org/project/xdat/

# incoming files:
mf1 = MFile.from_media(mo)
with mf1.open() as f1:
   ...

# outgoing files:
mf = MFile.from_lambda(f"myfile.xlsx", lambda f: df.to_excel(f))
mo = mf.to_media()
"""

from contextlib import contextmanager
import io
from scriptine import path

try:
    import anvil.media
except ImportError:
    pass


class MFile:
    def __init__(self, fname, content_type=None):
        self.fname = fname
        self.content_type = content_type

        if self.content_type is None:
            if fname.endswith('.xlsx'):
                self.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif fname.endswith('.xls'):
                self.content_type = 'application/vnd.ms-excel'
            elif fname.endswith('.csv'):
                self.content_type = 'text/csv'
            else:
                self.content_type = 'application/octet-stream'

        self.f = None

    @contextmanager
    def open(self, mode='r'):
        if mode == 'w':
            self.f = io.BytesIO()

        else:
            assert self.f is not None, "Can't read a file before it is written"
            self.f.seek(0)

        yield self.f

    @property
    def content(self):
        with self.open() as f:
            return f.read()

    @classmethod
    def from_media(cls, media_object):
        o = cls(media_object.name, content_type=media_object.content_type)

        with o.open(mode='w') as f:
            f.write(media_object.get_bytes())

        return o

    @classmethod
    def from_lambda(cls, fname, func):
        o = cls(fname)

        with o.open(mode='w') as f:
            func(f)

        return o

    def to_media(self):
        return anvil.BlobMedia(self.content_type, self.content, name=self.fname)

    def to_folder(self, folder):
        folder = path(folder)
        folder.ensure_dir()

        file_path = folder.joinpath(self.fname)
        with open(file_path, 'wb') as f:
            f.write(self.content)

        return file_path
