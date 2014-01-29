import os
import sys
import glob
import subprocess
import logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

__version__ = '0.8'
__all__ = ['do']

ACTION = ['delete', 'export']


logger = logging.getLogger('backup')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
log_dir = 'logs'
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
__id = datetime.now()
log_file = r'%s\%s.%s' % (log_dir, __id.strftime('%Y%m%d_%H%M%S'), 'log')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


def _exe(command):
    """
    Execute new process with parameters.

    :param command: exe with args
    :return: exitcode
    """
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, b''):
            logger.debug(line.rstrip())
        exitcode = p.wait()
    except KeyboardInterrupt:
        logger.warning('Aborted by user')
        sys.exit(0)
    return exitcode


def _get_range(occurred):
    """
    Translate user friendly date range to date tuple.

    :param occurred: Last mont, this month, Last 30 days, Last 7 days, Yesterday, today
    :return: tuple of dates, eg (datetime.date(2013, 12, 29), datetime.date(2014, 1, 28))
    """
    today = date.today()
    if occurred == 'Last month':
        d = today - relativedelta(months=1)
        return date(d.year, d.month, 1), date(today.year, today.month, 1) - relativedelta(days=1)
    elif occurred == 'This month':
        return date(today.year, today.month, 1), today
    elif occurred == 'Last 30 days':
        d = today - relativedelta(days=30)
        return d, today
    elif occurred == 'Last 7 days':
        d = today - relativedelta(days=7)
        return d, today
    elif occurred == 'Yesterday':
        d = today - relativedelta(days=1)
        return d, d
    elif occurred == 'Today':
        return today, today


def name_from_date(occurred):
    """
    Generate filename from user friendly date range.

    :param occurred: Last mont, this month, Last 30 days, Last 7 days, Yesterday, today
    :return: string with formatted date range.
    """
    date_format = '%Y%m%d'
    date = _get_range(occurred)
    return '%s-%s' % (date[0].strftime(date_format), date[1].strftime(date_format))


def export_cmd(command, export_path, occurred, mark_as_deleted=False):
    """
    This function enables you to export data from a DLib database server.

    :param command: EsmDlibM.exe path.
    :param export_path: Specify the folder path where data is exported to.
    :param occurred: These parameters provide the user a convenient way to filter events by occurred time.
    :param mark_as_deleted: Mark copied events as deleted from the source database. These events will no
    longer be visible in the management console but will still remain in the database.
    """
    tmp_export_path = export_path + r'tmp'
    if not os.path.isdir(tmp_export_path):
        os.makedirs(tmp_export_path)
    cmd = r'"%s" /exportToFile /path:"%s" /occurred:"%s"' % (command, tmp_export_path, occurred)
    if mark_as_deleted:
        cmd += ' /markEventsAsDeleted'
    logger.info('Running %s' % cmd)
    result = _exe(cmd)
    if result == 0:
        try:
            os.chdir(tmp_export_path)
            dat_file = sorted(glob.glob('*.dat'), key=os.path.getmtime, reverse=True)[0]
            hash_file = dat_file + '.hash'
            dat_new_name = name_from_date(occurred)
            dat_new_path = r'%s%s_%s' % (export_path, dat_new_name, dat_file)
            hash_new_path = dat_new_path + '.hash'
            os.rename(dat_file, dat_new_path)
            os.rename(hash_file, hash_new_path)
            logger.info('Backup file saved %s' % dat_new_path)
        except IndexError:
            logger.error('Something went wrong, .dat file is missing')
        except WindowsError as we:
            print we
    else:
        logger.critical('%s finished with exit code %s' % (command, result))


def delete_cmd(command, db_path):
    """
    This function enables you to delete events that are marked as deleted from the database.

    :param command: EsmDlibM.exe path
    :param db_path: Specify the path to the database server which contains events marked as deleted.
    """
    cmd = r'"%s" /commitDeletedRecords /dbpath:"%s"' % (command, db_path)
    logger.info('Running %s' % cmd)
    result = _exe(cmd)
    if result == 0:
        logger.info('Events removed from database')
    else:
        logger.critical('%s finished with exit code %s' % (command, result))


def do(cmd, args):
    """
    Simple function runner.
    :param cmd: eg ['delete', 'export']
    :param args: specific args for action, for details, check ACTION_cmd docstrings
    """
    if cmd in ACTION:
        globals()['%s_cmd' % cmd](**args)
    else:
        logger.error('Not supported action')