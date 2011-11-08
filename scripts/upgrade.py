#!/usr/bin/env python

import logging
import optparse
import os
import re
import shutil
import subprocess
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def call_command(command):
    process = subprocess.Popen(command.split(' '),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.communicate()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--from', dest='from_tag', action='store',
                      help='The current version of your OSP instance')
    parser.add_option('-t', '--to', dest='to_tag', action='store',
                      help='The version of OSP that you are upgrading to')
    parser.add_option('', '--osp-path', dest='osp_path', action='store',
                      default='/opt/django/osp',
                      help=('The path to your OSP instance (default: '
                            '/opt/django/osp)'))
    parser.add_option('', '--settings-path', dest='settings_path',
                      action='store', default='/opt/wsgi',
                      help=('The path to your OSP settings module '
                            '(default: /opt/wsgi)'))
    parser.add_option('', '--settings-module', dest='settings_module',
                      action='store', default='osp_settings',
                      help=('The name of your OSP settings module '
                            '(default: osp_settings)'))
    parser.add_option('', '--wsgi-script', dest='wsgi_script',
                      action='store', default='/opt/wsgi/osp.wsgi',
                      help=('The path to your OSP WSGI script '
                            '(default: /opt/wsgi/osp.wsgi)'))
    options, args = parser.parse_args()

    if not os.path.exists(options.osp_path):
        raise Exception('The path "%s" does not exist' % options.osp_path)
    if not os.path.exists(options.settings_path):
        raise Exception('The path "%s" does not exist' % options.settings_path)

    if os.path.exists('./osp/.hg'):
        logging.info('Pulling latest changes to OSP repository')
        os.chdir('osp')
        output, _ = call_command('hg pull')
        output, _ = call_command('hg update')
    else:
        logging.info('Cloning OSP repository')
        output, _ = call_command('hg clone http://osp.googlecode.com/hg/ osp')
        os.chdir('osp')

    if options.to_tag:
        to_version = options.to_tag
    else:
        logging.info('Determining the latest version of OSP')

        tags = open('.hgtags', 'r')
        lines = tags.readlines()
        tags.close()

        to_version = lines[-1].split(' ')[1].strip()
        logging.info('Latest version: %s' % to_version)

    logging.info('Updating repository to the correct version of OSP')
    output, _ = call_command('hg update %s' % to_version)

    if options.from_tag:
        from_version = options.from_tag
    else:
        logging.info('Determining the current version of your OSP instance')

        try:
            setup = open('%s/setup.py' % options.osp_path)
        except IOError:
            raise Exception(('The setup.py file is missing from the '
                             'root of your OSP instance'))

        content = setup.read()
        setup.close()

        match = re.search('version = \'([^\s]*)\'', content)
        from_version = match.group(1)

        logging.info('Current version: %s' % from_version)

    logging.info('Determining which files have changed')
    output, _ = call_command('hg status --rev %s:%s'
                             % (from_version, to_version))

    ignore = ['.hgtags',]

    add = []
    remove = []
    replace = []

    for line in output.split('\n'):
        if line[2:] not in ignore:
            if line[:1] == 'A':
                add.append(line[2:])
            elif line[:1] == 'R':
                remove.append(line[2:])
            elif line[:1] == 'M':
                replace.append(line[2:])

    if add:
        print('\nThe following files will be added:\n\n%s' % '\n'.join(add))
        add_files = raw_input(('\nWould you like to add them now? [Y/n] '))
        if not add_files or add_files.lower() == 'y':
            add_files = True
        elif add_files.lower() == 'n':
            add_files = False

        if add_files:
            logging.info('Adding new files to your OSP instance')
            for f in add:
                f_path = '%s/%s' % (options.osp_path, f)
                output, _ = call_command('mkdir -p %s'
                                         % os.path.dirname(f_path))
                shutil.copy(f, f_path)

    if remove:
        print('\nThe following files will be removed:\n\n%s'
              % '\n'.join(remove))
        remove_files = raw_input(('\nWould you like to remove them '
                                  'now? [Y/n] '))
        if not remove_files or remove_files.lower() == 'y':
            remove_files = True
        elif remove_files.lower() == 'n':
            remove_files = False

        if remove_files:
            logging.info('Removing old files from your OSP instance')
            for f in remove:
                os.remove('%s/%s' % (options.osp_path, f))

    if replace:
        print('\nThe following files will be replaced:\n\n%s'
              % '\n'.join(replace))
        replace_files = raw_input(('\nWould you like to replace them '
                                   'now? [Y/n] '))
        if not replace_files or replace_files.lower() == 'y':
            replace_files = True
        elif replace_files.lower() == 'n':
            replace_files = False

        if replace_files:
            logging.info('Replacing old files in your OSP instance')
            for f in replace:
                shutil.copy(f, '%s/%s' % (options.osp_path, f))

    logging.info('Migrating any database tables that have changed')
    sys.path.append(options.osp_path)
    sys.path.append(options.settings_path)
    apps = ['assessments', 'core', 'notifications', 'surveys', 'visits',]
    for app in apps:
        output, _ = call_command('django-admin.py migrate %s --settings=%s'
                                 % (app, options.settings_module))

    logging.info('Performing file system clean-up')
    os.chdir('..')
    output, _ = call_command('rm -rf osp')
