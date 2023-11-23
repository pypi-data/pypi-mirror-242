
from pathlib import Path
import sys, io, argparse
from PIL import Image

__all__ = ['Shrinker', 'DEFAULT_IMAGE_WIDTH', 'DEFAULT_SHRINKAGE_MINIMUM',
           'DEFAULT_SHRINKABLE_SIZE_KB', 'IMAGE_FILE_EXTENSIONS']


PKG_NAME = 'image-shrinker'
REQUIRED_PYTHON_VERSION = (3,8)  # for Pillow package
DEFAULT_IMAGE_WIDTH = 1024
DEFAULT_SHRINKABLE_SIZE_KB = 128
DEFAULT_SHRINKAGE_MINIMUM = 5/100   # 5%
IMAGE_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class _ShrinkConfig:
    def __init__(self, cmd_args, width=None, height=None, shrinkable_kb=None, quiet=None):
        self.width = DEFAULT_IMAGE_WIDTH if (width is None and height is None) \
            else 0 if height is not None \
            else width
        self.height = 0 if self.width != 0 \
            else height
        self.shrinkable_kb = shrinkable_kb if shrinkable_kb is not None \
            else DEFAULT_SHRINKABLE_SIZE_KB
        self.quiet = cmd_args.quiet if cmd_args.quiet is not None \
            else quiet if quiet is not None \
            else False

    def fyi(self, message, prefix='INFO: '):
        # Messages that likely are unactionable (already shrunk, etc)
        if not self.quiet:
            print(prefix + message)

    def say(self, message, prefix='INFO: '):
        # Messages that might be actionable (too narrow, too short, etc)
        print(prefix + message)

    def __repr__(self):
        return f'_ShrinkConfig(cmd_args, {self.width}, {self.height}, {self.shrinkable_kb}, {self.quiet})'


class Shrinker:
    def __init__(self, root_dir: str, testrun=False):
        """
        :param root_dir: Where to start looking for images.
            If it's a file, use its parent (this allows using __file__
            to start in the same directory as the script file)
        :param test: If False this script will change images files!
            If True, no files are changed. If not specified,
        """
        self.root_dir = Path(root_dir)
        if self.root_dir.is_file():
            self.root_dir = self.root_dir.parent
        print(f'INFO: <root-dir> is {self.root_dir}')

        ap = argparse.ArgumentParser(prog=PKG_NAME,
            description='''Shrinks images! Read the docs at:
                https://image-shrinker.readthedocs.org''')
        ap.add_argument('-s', '--shrink', required=True, action='store_true',
            help=f'(required) to avoid unintentional invoking and shrinking')
        ap.add_argument('-q', '--quiet',
            action='store_const', const=True, default=None,
            help=f'Don\'t show INFO messages that are probably not actionable')
        ap.add_argument('-t', '--test',
            action='store_const', const=True, default=testrun,
            help=f'Test run only. Do not modify any image file')
        ap.add_argument('--noprompt', action='store_true',
            help=f'(danger) replaces image files without asking the user')
        self.cmd_args = ap.parse_args(sys.argv[1:] or ['--help'])

        self._configs = {'': _ShrinkConfig(self.cmd_args)}
        self._config_dirs_sorted = None     # sort when needed
        self._halting = False
        self._verify_requirements()

    def for_subdir(self,
            directory: str,
            width: int = None, height: int = None,
            shrinkable_kb: int = None,
            quiet: bool = None):
        dir = self._normalize_fn(directory)
        if dir != '':
            dir_p = Path(self.root_dir, dir)
            if not dir_p.exists():
                self._halting = True
                print(f'ERROR: Not found: <root-dir>/{dir}')
            elif not dir_p.is_dir():
                self._halting = True
                print(f'ERROR: Is not a directory: <root-dir>/{dir}')
        cfg = dict(
            width=width, height=height, quiet=quiet,
            shrinkable_kb=shrinkable_kb,
        )
        cfg = {k:v for k,v in cfg.items() if v is not None}
        self._configs[dir] = _ShrinkConfig(self.cmd_args, **cfg)
        self._config_dirs_sorted = None     # to force re-sorting
        return self

    def do_shrinking(self):
        if self._halting:
            return self
        images_all = self._find_all_image_files()
        for image in images_all:
            try:
                with Image.open(self.root_dir / image) as image_obj:
                    self._shrink_image(image, image_obj)
            except Exception as e:
                print(f'ERROR: While processing image: {image}\n\t{e}')
        return self

    def _find_all_image_files(self):
        images_all = []
        for ext in IMAGE_FILE_EXTENSIONS:
            paths = self.root_dir.glob(f'**/*.{ext}')
            paths = [p.relative_to(self.root_dir) for p in paths]
            paths = [self._normalize_fn(str(p)) for p in paths]
            images_all.extend(paths)
        return sorted(images_all)

    def _shrink_image(self, img: str, img_obj: Image):
        cfg = self._get_config_for_image(img)
        img_p = Path(self.root_dir / img)
        img_size_kb = round(img_p.stat().st_size/1024)
        img_width = img_obj.width
        img_height = img_obj.height

        # ---- Is image shrinkable? Look at width & height.
        shrink_WxH = None
        if img_size_kb < cfg.shrinkable_kb:
            cfg.fyi(f'Already size<{cfg.shrinkable_kb}KB: ({img_width}x{img_height} / {img_size_kb:,}KB) {img}')
        elif cfg.width > 0:
            if img_width == cfg.width:
                cfg.fyi(f'Already W={cfg.width}: ({img_width}x{img_height} / {img_size_kb:,}KB) {img}')
                if img_size_kb > cfg.shrinkable_kb:
                    cfg.fyi(f'\tManual shrinking might be required since file size is greater than {cfg.shrinkable_kb:,}KB')
            elif img_width < cfg.width:
                cfg.say(f'Too narrow (W<{cfg.width}) to shrink: ({img_width}x{img_height} / {img_size_kb:,}KB) {img}')
                if img_size_kb > cfg.shrinkable_kb:
                    cfg.say(f'\tManual shrinking might be required since file size is greater than {cfg.shrinkable_kb:,}KB ')
            else:
                shrink_WxH = (cfg.width, 999999)
        elif cfg.height > 0:
            if img_height == cfg.height:
                cfg.fyi(f'Already H={cfg.height}: ({img_width}x{img_height} / {img_size_kb:,}KB) {img}')
                if img_size_kb > cfg.shrinkable_kb:
                    cfg.fyi(f'\tManual shrinking might be required since file size is greater than {cfg.shrinkable_kb:,}KB')
            elif img_height < cfg.height:
                cfg.say(f'Too short (H<{cfg.height}) to shrink: ({img_width}x{img_height} / {img_size_kb:,}KB) {img}')
                if img_size_kb > cfg.shrinkable_kb:
                    cfg.say(f'\tManual shrinking might be required since file size is greater than {cfg.shrinkable_kb:,}KB')
            else:
                shrink_WxH = (999999, cfg.height)
        if shrink_WxH is None:
            return

        # ---- Shrink the image (into memory)
        img_obj.thumbnail(shrink_WxH)
        shrunk_mem = io.BytesIO()
        img_obj.save(shrunk_mem, img_obj.format, optimize=True)
        shrunk_size_kb = round(shrunk_mem.tell() / 1024)
        shrunk_width = img_obj.width
        shrunk_height = img_obj.height

        # ---- Is it worth saving? Look at %-shrank
        shrank_pct = 100 * (1 - (shrunk_size_kb/img_size_kb))
        if shrank_pct < DEFAULT_SHRINKAGE_MINIMUM:
            cfg.say(f'Not enough shrinkage: {img_size_kb:,}KB-->{shrunk_size_kb:,}KB ({shrank_pct:.1f}%): {img}')
            if img_size_kb > cfg.shrinkable_kb:
                cfg.say(f'\tManual shrinking might be required since file size is greater than {cfg.shrinkable_kb:,}KB ')
            return

        # ---- Show shrinking stats and prompt user to proceed
        save_img = False       # an extra check for safer code
        cfg.say(('Doing' if self.cmd_args.noprompt else 'Do')
            + f' ({img_width}x{img_height} / {img_size_kb:,}K)'
            + f'-->({shrunk_width}x{shrunk_height} / {shrunk_size_kb:,}K)'
            + ('?' if not self.cmd_args.noprompt else '!') + f' for {img}')
        if self.cmd_args.noprompt:
            save_img = True
        else:
            while True:
                response = input('Enter "s" to shrink, "q" to quit, [enter] to skip this image> ').strip().lower()
                if response == 's':
                    save_img = True
                    break
                elif response == 'q':
                    exit(0)
                elif response == '':
                    return

        # ---- Save the image
        if save_img and not self.cmd_args.test:
            img_p.write_bytes(shrunk_mem.getvalue())

    def _get_config_for_image(self, image_fpath: str) -> _ShrinkConfig:
        if self._config_dirs_sorted is None:
            self._config_dirs_sorted = sorted(
                self._configs.keys(),
                key=lambda dir: (len(dir), dir),
                reverse=True)   # From longest to shortest dir
        cfg = None
        for dir in self._config_dirs_sorted:
            if image_fpath.startswith(dir):
                cfg = self._configs[dir]
                break
        return cfg or _ShrinkConfig(self.cmd_args)

    def _verify_requirements(self):
        # ---- Required: minimum version of Python
        if sys.version_info < REQUIRED_PYTHON_VERSION:
            print(f'ERROR: {PKG_NAME} needs at least Python'
                + '.'.join(str(x) for x in REQUIRED_PYTHON_VERSION))
            print('... but you are running only Python '
                + '.'.join(str(x) for x in sys.version_info))
            exit(9)
        # ---- Required: Pillow (PIL) package is installed
        # Assume installed. It's a dependency of this package.

    @staticmethod
    def _normalize_fn(fname: str, unprefix=True):
        """Normalize name for OS-independence, comparability"""
        fname = fname.replace('\\', '/')    # un-Windows-ize
        if unprefix:
            if fname.startswith('./'):
                fname = fname[2:]
            fname = fname.lstrip('/')
        fname = fname.rstrip('/')           # remove trailing slash
        return fname
