# encoding: utf-8

import gvsig
from gvsig import getResource

import thread
import os.path
import subprocess
import shutil

from java.lang import System
from java.io import File
from java.io import FileInputStream
from java.io import FileOutputStream
from java.util import Properties

from org.apache.commons.io import FileUtils
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.scripting.swing.api import ScriptingSwingLocator, JScriptingComposer
from org.gvsig.tools import ToolsLocator

import javax.swing.ImageIcon
import javax.imageio.ImageIO
from javax.swing import AbstractAction, Action
from org.gvsig.scripting import ScriptingLocator

GVSIG_JARS= (
  #"gvSIG/extensiones/org.gvsig.geometry.app.jts/jts-1.13.jar",
  #
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2gis-api-1.3.0.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2gis-ext-1.3.0.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2gis-functions-1.3.0.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2gis-network-1.3.0.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2gis-utilities-1.3.0.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2network-1.2.4.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2spatial-1.2.4.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2spatial-api-1.2.4.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/cts-1.3.4.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/jackson-core-2.3.1.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/java-network-analyzer-0.1.6.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/jgrapht-core-1.0.1.jar",
  #"gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/poly2tri-core-0.1.2.jar",
  
  "gvSIG/extensiones/org.gvsig.h2spatial.app.mainplugin/lib/h2-1.4.188.jar",
  "gvSIG/extensiones/org.gvsig.postgresql.app.mainplugin/lib/postgresql-9.1-901.jdbc3.jar",
  "gvSIG/extensiones/org.gvsig.oracle.app.mainplugin/lib/ojdbc-11.2.0.4.0.jar",
  "gvSIG/extensiones/org.gvsig.mssqlserver.app.mainplugin/lib/sqlserver-jdbc-6.0.0.jar",
  "gvSIG/extensiones/org.gvsig.mysql.app.mainplugin/lib/mysql-connector-java-6.0.6.jar",
  "gvSIG/extensiones/org.gvsig.spatialite.app.mainplugin/lib/sqlite-jdbc-3.21.0.jar",
)

def getDataFolder():
  return ScriptingLocator.getManager().getDataFolder("squirrelsql").getAbsolutePath()

def launchSQuirreLSQL():
  pluginsManager = PluginsLocator.getManager()
  appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
  
  java = os.path.join( System.getProperties().getProperty("java.home"), "bin", "java")

  squirrelhome = getResource(__file__, "app").replace("\\","/")
  settings = getDataFolder().replace("\\","/")

  CP = squirrelhome+"/squirrel-sql.jar"
  for fname in os.listdir(squirrelhome+"/lib"):
    CP += ":"+squirrelhome+"/lib/"+fname
  for jar in GVSIG_JARS:
    CP += ":"+appfolder+"/"+jar
 
  cmd = [
    java,
    "-cp",CP,
    "-splash:"+squirrelhome+"/icons/splash.jpg",
    "net.sourceforge.squirrel_sql.client.Main",
    "--native-laf",
    "--log-config-file", squirrelhome+"/log4j.properties",
    "--squirrel-home", squirrelhome,
    "--user-settings-dir", settings,
  ]
  #print cmd
  subprocess.call(cmd)


class SQuirreLSQLAction(AbstractAction):

  def __init__(self):
    AbstractAction.__init__(self,"SQuirreLSQL")
    self.putValue(Action.ACTION_COMMAND_KEY, "SQuirreLSQL");
    self.putValue(Action.SMALL_ICON, self.load_icon(getResource(__file__,"images","acorn16x16.png")));
    self.putValue(Action.SHORT_DESCRIPTION, "SQuirreLSQL");

  def load_icon(self, afile):
    if not isinstance(afile,File):
      afile = File(str(afile))
    return javax.swing.ImageIcon(javax.imageio.ImageIO.read(afile))

  def actionPerformed(self,e):
    composer = e.getSource().getContext()
    thread.start_new_thread(launchSQuirreLSQL,tuple())

def selfRegister():
  i18nManager = ToolsLocator.getI18nManager()
  manager = ScriptingSwingLocator.getUIManager()
  action = SQuirreLSQLAction()
  manager.addComposerTool(action)
  manager.addComposerMenu(i18nManager.getTranslation("Tools"),action)

def main(*args):
  thread.start_new_thread(launchSQuirreLSQL,tuple())
