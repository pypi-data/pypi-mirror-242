# -*- coding: utf-8; -*-

import configparser
import datetime
import os
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

from rattail import config
from rattail.app import AppHandler


class TestParseBoolFunc(TestCase):

    def test_none(self):
        self.assertIsNone(config.parse_bool(None))

    def test_true(self):
        self.assertIs(config.parse_bool(True), True)

    def test_false(self):
        self.assertIs(config.parse_bool(False), False)

    def test_string(self):
        self.assertTrue(config.parse_bool('true'))
        self.assertTrue(config.parse_bool('yes'))
        self.assertTrue(config.parse_bool('on'))
        self.assertTrue(config.parse_bool('1'))

        self.assertFalse(config.parse_bool('false'))
        self.assertFalse(config.parse_bool('no'))
        self.assertFalse(config.parse_bool('off'))
        self.assertFalse(config.parse_bool('0'))


class TestParseListFunc(TestCase):

    def test_none(self):
        value = config.parse_list(None)
        self.assertEqual(len(value), 0)

    def test_single_value(self):
        value = config.parse_list(u'foo')
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0], u'foo')

    def test_single_value_padded_by_spaces(self):
        value = config.parse_list(u'   foo   ')
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0], u'foo')

    def test_slash_is_not_a_separator(self):
        value = config.parse_list(u'/dev/null')
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0], u'/dev/null')

    def test_multiple_values_separated_by_whitespace(self):
        value = config.parse_list(u'foo bar baz')
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'bar')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_commas(self):
        value = config.parse_list(u'foo,bar,baz')
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'bar')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_whitespace_and_commas(self):
        value = config.parse_list(u'  foo,   bar   baz')
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'bar')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_whitespace_and_commas_with_some_quoting(self):
        value = config.parse_list("""
        foo
        "C:\\some path\\with spaces\\and, a comma",
        baz
        """)
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'C:\\some path\\with spaces\\and, a comma')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_whitespace_and_commas_with_single_quotes(self):
        value = config.parse_list("""
        foo
        'C:\\some path\\with spaces\\and, a comma',
        baz
        """)
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], 'foo')
        self.assertEqual(value[1], 'C:\\some path\\with spaces\\and, a comma')
        self.assertEqual(value[2], 'baz')


class TestRattailConfig(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_file(self, fname, content):
        path = os.path.join(self.tempdir, fname)
        with open(path, 'wt') as f:
            f.write(content)
        return path

    def setup_files(self):
        self.site_path = self.write_file('site.conf', """
[rattail]
        """)

        self.host_path = self.write_file('host.conf', """
[rattail.config]
include = "{}"
        """.format(self.site_path))

        self.app_path = self.write_file('app.conf', """
[rattail.config]
include = "{}"
        """.format(self.host_path))

        self.custom_path = self.write_file('custom.conf', """
[rattail.config]
include = "%(here)s/app.conf"
        """)

    def test_init_defaults(self):
        cfg = config.RattailConfig()
        self.assertEqual(cfg.files_requested, [])
        self.assertEqual(cfg.files_read, [])

    def test_init_params(self):
        self.setup_files()

        # files
        cfg = config.RattailConfig()
        self.assertEqual(cfg.files_requested, [])
        self.assertEqual(cfg.files_read, [])
        cfg = config.RattailConfig(files=[self.site_path])
        self.assertEqual(cfg.files_requested, [self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path])

        # usedb
        cfg = config.RattailConfig()
        self.assertFalse(cfg.usedb)
        cfg = config.RattailConfig(usedb=True)
        self.assertTrue(cfg.usedb)

        # preferdb
        cfg = config.RattailConfig()
        self.assertFalse(cfg.preferdb)
        cfg = config.RattailConfig(preferdb=True)
        self.assertTrue(cfg.preferdb)

    def test_read_file_with_recurse(self):
        self.setup_files()
        cfg = config.RattailConfig()
        cfg.read_file(self.custom_path, recurse=True)
        self.assertEqual(cfg.files_requested, [self.custom_path, self.app_path, self.host_path, self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path, self.host_path, self.app_path, self.custom_path])

    def test_read_file_once_only(self):
        self.setup_files()

        another_path = self.write_file('another.conf', """
[rattail.config]
include = "{custom}" "{site}" "{app}" "{site}" "{custom}"
        """.format(custom=self.custom_path, app=self.app_path, site=self.site_path))

        cfg = config.RattailConfig()
        cfg.read_file(another_path, recurse=True)
        self.assertEqual(cfg.files_requested, [another_path, self.custom_path, self.app_path, self.host_path, self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path, self.host_path, self.app_path, self.custom_path, another_path])

    def test_read_file_skip_missing(self):
        self.setup_files()
        bogus_path = '/tmp/does-not/exist'
        self.assertFalse(os.path.exists(bogus_path))

        another_path = self.write_file('another.conf', """
[rattail.config]
include = "{bogus}" "{app}" "{bogus}" "{site}"
        """.format(bogus=bogus_path, app=self.app_path, site=self.site_path))

        cfg = config.RattailConfig()
        cfg.read_file(another_path, recurse=True)
        self.assertEqual(cfg.files_requested, [another_path, bogus_path, self.app_path, self.host_path, self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path, self.host_path, self.app_path, another_path])

    @patch('rattail.config.logging.config.fileConfig')
    def test_configure_logging(self, fileConfig):
        cfg = config.RattailConfig()

        # logging not configured by default
        cfg.configure_logging()
        self.assertFalse(fileConfig.called)

        # but config option can enable it
        cfg.set('rattail.config', 'configure_logging', 'true')
        cfg.configure_logging()
        self.assertEqual(fileConfig.call_count, 1)
        fileConfig.reset_mock()

        # invalid logging config is ignored
        fileConfig.side_effect = configparser.NoSectionError('loggers')
        cfg.configure_logging()
        self.assertEqual(fileConfig.call_count, 1)


class TestRattailConfigWrapper(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_file(self, filename, content):
        path = os.path.join(self.tempdir, filename)
        with open(path, 'wt') as f:
            f.write(content)
        return path

    def test_legacy(self):
        myconfig = config.RattailConfigWrapper()
        self.assertEqual(repr(myconfig), "RattailConfigWrapper(style=legacy)")

    def test_configuration(self):
        myfile = self.write_file('my.conf', """\
[rattail.config]
use_configuration = true
""")

        myconfig = config.RattailConfigWrapper(files=[myfile])
        self.assertEqual(repr(myconfig), "RattailConfigWrapper(style=configuration)")

    def test_wuttaconfig(self):
        myfile = self.write_file('my.conf', """\
[rattail.config]
use_wuttaconfig = true
""")

        myconfig = config.RattailConfigWrapper(files=[myfile])
        self.assertEqual(repr(myconfig), "RattailConfigWrapper(style=wuttaconfig)")

    def test_getattr(self):
        myconfig = config.RattailConfigWrapper()
        self.assertIs(myconfig.files_read, myconfig.config.files_read)

    def test_setattr(self):
        myconfig = config.RattailConfigWrapper()
        self.assertFalse(hasattr(myconfig.config, 'foo'))
        myconfig.foo = 'bar'
        self.assertEqual(myconfig.config.foo, 'bar')


class TestRattailWuttaConfig(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_file(self, filename, content):
        path = os.path.join(self.tempdir, filename)
        with open(path, 'wt') as f:
            f.write(content)
        return path

    def test_prioritized_files(self):
        first = self.write_file('first.conf', """\
[foo]
bar = 1
""")

        second = self.write_file('second.conf', """\
[rattail.config]
require = %(here)s/first.conf
""")

        myconfig = config.RattailWuttaConfig(files=[second])
        files = myconfig.prioritized_files
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0], second)
        self.assertEqual(files[1], first)
        self.assertIs(files, myconfig.get_prioritized_files())

    def test_setdefault(self):
        myconfig = config.RattailWuttaConfig()

        # nb. the tests below are effectively testing the custom get()
        # method in addition to setdefault()

        # value is empty by default
        self.assertIsNone(myconfig.get('foo.bar'))
        self.assertIsNone(myconfig.get('foo', 'bar'))

        # but we can change that by setting default
        myconfig.setdefault('foo.bar', 'baz')
        self.assertEqual(myconfig.get('foo.bar'), 'baz')
        self.assertEqual(myconfig.get('foo', 'bar'), 'baz')

        # also can set a default via section, option (as well as key)
        self.assertIsNone(myconfig.get('foo.blarg'))
        myconfig.setdefault('foo' ,'blarg', 'blast')
        self.assertEqual(myconfig.get('foo.blarg'), 'blast')
        self.assertEqual(myconfig.get('foo', 'blarg'), 'blast')

        # error is raised if args are ambiguous
        self.assertRaises(ValueError, myconfig.setdefault, 'foo', 'bar', 'blarg', 'blast')

        # try that for get() too
        self.assertRaises(ValueError, myconfig.get, 'foo', 'bar', 'blarg', 'blast')

    def test_getbool(self):
        myconfig = config.RattailWuttaConfig()
        self.assertFalse(myconfig.getbool('foo.bar'))
        myconfig.setdefault('foo.bar', 'true')
        self.assertTrue(myconfig.getbool('foo.bar'))

    def test_getint(self):
        myconfig = config.RattailWuttaConfig()
        self.assertIsNone(myconfig.getint('foo.bar'))
        myconfig.setdefault('foo.bar', '42')
        self.assertEqual(myconfig.getint('foo.bar'), 42)

    def test_getlist(self):
        myconfig = config.RattailWuttaConfig()
        self.assertEqual(myconfig.getlist('foo.bar'), [])
        myconfig.setdefault('foo.bar', 'hello world')
        self.assertEqual(myconfig.getlist('foo.bar'), ['hello', 'world'])

    def test_getdate(self):
        myconfig = config.RattailWuttaConfig()
        self.assertIsNone(myconfig.getdate('foo.date'))
        myconfig.setdefault('foo.date', '2023-11-20')
        value = myconfig.getdate('foo.date')
        self.assertIsInstance(value, datetime.date)
        self.assertEqual(value, datetime.date(2023, 11, 20))

    def test_get_app(self):
        myconfig = config.RattailWuttaConfig()
        app = myconfig.get_app()
        self.assertIsInstance(app, AppHandler)

    def test_parse_list(self):
        myconfig = config.RattailWuttaConfig()
        self.assertEqual(myconfig.parse_list(None), [])
        self.assertEqual(myconfig.parse_list('hello world'), ['hello', 'world'])

    def test_beaker_invalidate_setting(self):
        # TODO: this doesn't really test anything, just gives coverage
        myconfig = config.RattailWuttaConfig()
        myconfig.beaker_invalidate_setting('foo')
