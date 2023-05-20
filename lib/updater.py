# CREDITS: https://github.com/jkelol111

def exList(ex):
    ex_str = str(ex)
    print("During the usage of updater.py, we've encountered some errors. Here's the exception:")
    print("======================================================================================")
    print(ex_str)
    print("======================================================================================")
    print("Please do the following:")
    print("- If you're getting errors about config, reread your config file.")
    print("- Make sure you have installed all the dependencies. Read README.md for more info.")
    print("If nothing works, please create a new issue on GitHub: https://github.com/jkelol111/updater.py/issues")
    raise ex
    exit()

def logger(log, subcat):
    infosg = str("[i]")
    warnsg = str("[!]")
    try:
        if log == "cleanup":
            if subcat == "begin":
                print(infosg+" Deleting your temporary update files.")
            elif subcat == "done":
                print(infosg+" Done deleting your temporary update files.")
            elif subcat == "none":
                print(warnsg+" There is nothing to clean.")
        elif log == "update":
            if subcat == "begin":
                print(infosg+" Update/Reinstall commence.")
            elif subcat == "step1":
                print("[1/3] Emptying folder of application.")
            elif subcat == "step1.5":
                print("[1.5/3] Backing up configuration file of application.")
            elif subcat == "step2":
                print("[2/3] Downloading and installing new version of application.")
            elif subcat == "step2.5":
                print("[2.5/3] Restoring app configuration files.")
            elif subcat == "step3":
                print("[3/3] Downloading and installing updater.py for application.")
            elif subcat == "done":
                print(infosg+" Update/Reinstall completed.")
        elif log == "restore":
            if subcat == "begin":
                print(infosg+" Restoring your configuration file.")
            elif subcat == "done":
                print(infosg+" Done restoring your configuration file.")
            elif subcat == "none":
                print(warnsg+" There is no configuration file to restore.")
        elif log == "backup":
            if subcat == "begin":
                print(infosg+" Backing up your configration file.")
            elif subcat == "done":
                print(infosg+" Done backing up your configuration file.")
            elif subcat == "none":
                print(warnsg+" There is no configuration file to back up.")
        elif log == "updateupdater":
            if subcat == "begin":
                print(infosg+" Downloading and installing updater.py for application.")
            elif subcat == "done":
                print(infosg+" Done downloading and installing updater.py for application.")
            elif subcat == "error":
                print(warnsg+" Cannot download and install updater.py for application.")
        elif log == "createlauncher":
            if subcat == "begin":
                print(infosg+" Creating your application launcher.")
            elif subcat == "done":
                print(infosg+" Done creating your application launcher.")
            elif subcat == "error":
                print(warnsg+" Cannot create a launcher file.")
        elif log == "createConfig":
            if subcat == "begin":
                print(infosg+" Creating your configuration file.")
            elif subcat == "done":
                print(infosg+" Done creating your configuration file.")
            elif subcat == "error":
                print(warnsg+" Cannot create a configuration file.")
        elif log == "loadConfig":
            if subcat == "begin":
                print(infosg+" Loading your configuration file.")
            elif subcat == "done":
                print(infosg+" Done loading your configuration file.")
            elif subcat == "warn":
                print(warnsg+" The old configuration file (config.py) is going to be deprecated soon. Please alert your app developer if the change is not made yet!")
            elif subcat == "error":
                print(warnsg+" Cannot load your configuration file.")
        elif log == "notSupported":
            print(warnsg+" Your OS does not support updater.py. The updater will now exit!")
        elif log == "notConfigured":
            print(warnsg+" You have not configured your configuration file (config.yml). The updater will now terminate!")
    except:
        print(warnsg+"logger does not have that!")

try:
    from git import Repo
    from yaml import safe_load
    from yaml import dump

    from platform import system

    from os import mkdir
    from os.path import isdir
    from os.path import isfile
    from os import remove
    from os import access
    from os import W_OK
    from os import chmod
    from os.path import dirname
    from os.path import realpath
    from stat import S_IWUSR
    from stat import S_IXUSR

    from shutil import rmtree
    from shutil import copy2
    
    from getpass import getuser

    try:
        import tqdm
        commandlineprogressbar = True
    except ImportError:
        commandlineprogressbar = False

    if isfile(dirname(realpath(__file__))+"/config.py") == True:
        logger("loadConfig", "begin")
        logger("loadConfig", "warn")
        import config as cfg
        config_contents = dict(
            appIdentifier = cfg.appIdentifier,
            appRepo = cfg.appRepo,
            appDir = cfg.appDir,
            appExecName = cfg.appExecName,
            backupOn = cfg.backupOn,
            createLaunchScriptOn = cfg.createLaunchScriptOn
        )
        with open(dirname(realpath(__file__))+"/config.yml", 'w') as config_file:
            dump(config_contents, config_file)
        with open(dirname(realpath(__file__))+"/config.yml", 'r') as stream:
            config_contents = safe_load(stream)
        appIdentifier = config_contents["appIdentifier"]
        appRepo = config_contents["appRepo"]
        appDir = config_contents["appDir"]
        appExecName = config_contents["appExecName"]
        backupOn = config_contents["backupOn"]
        createLaunchScriptOn = config_contents["createLaunchScriptOn"]
        configFile = str(appDir+"/config.yml")
        updaterFile = str(appDir+"/updater.py")
        logger("loadConfig", "done")
    elif isfile(dirname(realpath(__file__))+"/config.yml") == True:
        logger("loadConfig", "begin")
        with open(dirname(realpath(__file__))+"/config.yml", 'r') as stream:
            config_contents = safe_load(stream)
        appIdentifier = config_contents["appIdentifier"]
        appRepo = config_contents["appRepo"]
        appDir = config_contents["appDir"]
        appExecName = config_contents["appExecName"]
        backupOn = config_contents["backupOn"]
        createLaunchScriptOn = config_contents["createLaunchScriptOn"]
        configFile = str(appDir+"/config.yml")
        updaterFile = str(appDir+"/updater.py")
        logger("loadConfig", "done")
    else:
        logger("loadConfig", "error")
        exit()
    username = getuser()
    tmpBackupDirWin = str("C:/Users/"+username+"/.tmp_updater"+"/"+appIdentifier)
    tmpBackupDirNix = str("/home/"+username+"/.tmp_updater"+"/"+appIdentifier)
    tmpBackupDirOSX = str("/Users/"+username+"/.tmp_updater"+"/"+appIdentifier)


    configured = bool(False)
except Exception as e:
    exList(e)

def onerrorPatch(func, path, exc_info):
    if not access(path, W_OK):
        chmod(path, S_IWUSR)
        func(path)

def checkConfig():
    global configured
    if appIdentifier == "com.sample.nothing":
        configured = bool(False)
    elif appRepo == "http://www.example.com/project.git":
        configured = bool(False)
    elif appDir == "Nothing":
        configured = bool(False)
    elif appExecName == str("Nothing.py"):
        configured = bool(False)
    else:
        configured = bool(True)

def cleanupNow():
    try:
        logger("cleanup", "begin")
        if system() == "Windows":
            if isdir(tmpBackupDirWin) == bool(True):
                rmtree(tmpBackupDirWin, onerror=onerrorPatch)
            elif isdir(tmpBackupDirWin) == bool(False):
                logger("cleanup", "none")
        elif system() == "Linux":
            if isdir(tmpBackupDirNix) == bool(True):
                rmtree(tmpBackupDirNix)
            elif isdir(tmpBackupDirNix) == bool(False):
                logger("cleanup", "none")
        elif system() == "Darwin":
            if isdir(tmpBackupDirOSX) == bool(True):
                rmtree(tmpBackupDirOSX)
            elif isdir(tmpBackupDirOSX) == bool(False):
                logger("cleanup", "none")
        else:
            logger("notSupported", "")
        logger("cleanup", "done")
    except Exception as e:
        exList(e)

def restoreConfigNow():
    try:
        logger("restore", "begin")
        if system() == "Windows":
            bckconfigFileWin = str(tmpBackupDirWin+"/config.yml")
            if isfile(bckconfigFileWin) == bool(True):
                copy2(bckconfigFileWin, appDir)
            elif isfile(bckconfigFileWin) == bool(False):
                logger("restore", "none")
        elif system() == "Linux":
            bckconfigFileNix = str(tmpBackupDirNix+"/config.yml")
            if isfile(bckconfigFileNix) == bool(True):
                copy2(bckconfigFileNix, appDir)
            elif isfile(bckconfigFileNix) == bool(False):
                logger("restore", "none")
        elif system() == "Darwin":
            bckconfigFileOSX = str(tmpBackupDirOSX+"/config.yml")
            if isfile(bckconfigFileOSX) == bool(True):
                copy2(bckconfigFileOSX, appDir)
            elif isfile(bckconfigFileOSX) == bool(False):
                logger("restore", "none")
        else:
            logger("notSupported", "")
        logger("restore", "done")
    except Exception as e:
        exList(e)

def backupConfigNow():
    cleanupNow()
    try:
        logger("backup", "begin")
        if system() == "Windows":
            mkdir(tmpBackupDirWin)
            if isfile(configFile) == bool(True):
                copy2(configFile, tmpBackupDirWin)
            elif isfile(configFile) == bool(False):
                logger("backup", "none")
        elif system() == "Linux":
            mkdir(tmpBackupDirNix)
            if isfile(configFile) == bool(True):
                copy2(configFile, tmpBackupDirNix)
            elif isfile(configFile) == bool(False):
                logger("backup", "none")
        elif system() == "Darwin":
            mkdir(tmpBackupDirWin)
            if isfile(configFile) == bool(True):
                copy2(configFile, tmpBackupDirWin)
            elif isfile(configFile) == bool(False):
                logger("backup", "none")
        else:
            logger("notSupported", "")
        logger("backup", "done")
    except Exception as e:
        exList(e)


def updateNow(program_path):
    checkConfig()
    if configured == bool(False):
        logger("notConfigured", "")
        exit()
    elif configured == bool(True):
        try:
            logger("update", "begin")

            logger("update", "step1")
            if backupOn == bool(True):
                logger("update", "step1.5")
                backupConfigNow()
            rmtree(program_path, onerror=onerrorPatch)

            logger("update", "step2")
            if not isdir(program_path):
                mkdir(program_path)
            Repo.clone_from(appRepo, program_path)

            if backupOn == bool(True):
                logger("update", "step2.5")
                restoreConfigNow()

            if createLaunchScriptOn == bool(True):
                createLauncherNow()

            logger("update", "done")
        except Exception as e:
            exList(e)

def configureConfigNow(appid, repo, directory, appexename, bckOn, createlauncherOn):
    try:
        logger("createConfig", "begin")
        config_contents = dict(
            appIdentifier = appid,
            appRepo = repo,
            appDir = directory,
            appExecName = appexename,
            backupOn = bckOn,
            createLaunchScriptOn = createlauncherOn
        )
        with open(dirname(realpath(__file__))+"/config.yml", 'w') as config_file:
            dump(config_contents, config_file)
        logger("createConfig", "done")
        global appIdentifier
        global appRepo
        global appDir
        global appExecName
        global backupOn
        global createLaunchScriptOn
        global configFile
        global updaterFile
        appIdentifier = appid
        appRepo = repo
        appDir = directory
        appExecName = appexename
        backupOn = bckOn
        createLaunchScriptOn = createlauncherOn

        configFile = str(appDir+"/config.yml")
        updaterFile = str(appDir+"/updater.py")
    except Exception as e:
        logger("createConfig", "error")
        exList(e)

def createLauncherNow():
    try:
        logger("createlauncher", "begin")
        if system() == "Windows":
            launchScriptWinDir = str("C:/Users/"+username+"/Desktop/"+appIdentifier+".bat")
            launchScriptWin = open(launchScriptWinDir, "w")
            launchScriptWin.write("@echo off\n")
            launchScriptWin.write("python "+dirname(realpath(__file__))+"/"+appExecName+"\n")
            launchScriptWin.write("pause")
            launchScriptWin.close()
        elif system() == "Linux" or system() == "Darwin":
            launchScriptNixDir = str("~/Desktop/"+appIdentifier+".sh")
            launchScriptNix = open(launchScriptNixDir+".sh", "w")
            launchScriptWin.write("python "+dirname(realpath(__file__))+"/"+appExecName+"\n")
            launchScriptNix.write("read")
            launchScriptNix.close()
            chmod(launchScriptNixDir, S_IXUSR)
        else:
            logger("notSupported", "")
        logger("createlauncher", "done")
    except Exception as e:
        logger("createlauncher", "error")
        exList(e)