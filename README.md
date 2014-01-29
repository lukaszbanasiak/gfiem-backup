GFIEM-backup-wrapper
====================

Wrapper for EsmDlibM.exe to automated backups in GFI EventsManager.

EsmDlibM.exe enables you to run operations against the file storage system where processed events
are stored (database backend). Such operations include Importing or Exporting data.

For now, two functions are supported (See TODO for missing functions):

1. export (exportToFile): This function enables you to export data from a DLib database server.

2. delete (commitDeletedRecords): This function enables you to delete events that are marked as deleted from the database.

## Features ##

1. Create backup files name from date range of events that are exported (default in EsmDlibM.exe is file creation time :)
2. Saving stdout to a log file

## Usage ##
Run `gfi-backup.exe` with one of the two parameters: `export` or `delete`

Example

    C:\bin>gfi-backup.exe export
    2014-01-29 09:46:56,270 INFO Running "C:\Program Files (x86)\GFI\EventsManag
    er2013\EsmDlibM.exe" /exportToFile /path:"C:\GFI-export\tmp" /occurred:"Last mon
    th" /markEventsAsDeleted

## Configuration ##

Edit `default.ini` file or crete new one.

    [main]
    command = C:\Program Files (x86)\GFI\EventsManager2013\EsmDlibM.exe
    
    [export]
    export_path = C:\GFI-export\
    occurred = Last month
    ; Uncomment next line to enable mark copied events as deleted
    ;mark_as_deleted = yes
    
    [delete]
    dbpath = C:\GFI-db\


main section

- `command`: path to EsmDlibM.exe

export section

- `export_path`: Specify the folder path where data is exported to.
- `occurred`: These parameters provide the user a convenient way to filter events by occurred time.
- `mark_as_deleted`: Mark copied events as deleted from the source database. These events will no longer be visible in the management console but will still remain in the database. 

delete section

- `db_path`: Specify the path to the database server which contains events marked as deleted.

You can create a couple of configuration files and run the program with different settings.

For example, we like to create weekly backups.
Create a file `weekly.ini` with the following content.

    [main]
    command = C:\Program Files (x86)\GFI\EventsManager2013\EsmDlibM.exe
    
    [export]
    export_path = C:\GFI-export\
    occurred = Last 7 days

Run or schedule `gfi-backup.exe export -c weekly.ini`

## Download ##
[https://github.com/lukaszbanasiak/gfiem-backup/releases](https://github.com/lukaszbanasiak/gfiem-backup/releases "Releases")

## TODO ##
Cover all functions and parameters from EsmDlibM:

- importFromSQL
- importFromDlib
- copyData
- importFromLegacyFile
- importFromFile
- exportToSQL