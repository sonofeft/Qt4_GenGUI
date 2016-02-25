#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
A generic GUI built with pyQt4. Used as starting point for new GUI apps.

This generic GUI places a main page, menu, toolbar, statusbar and sphinx doc directory.
Modify this starting point to suit your projets' needs.


Qt4_GenGUI
Copyright (C) 2016  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import webbrowser

import os
import sys
here = os.path.abspath(os.path.dirname(__file__))

INDEX_PAGE = os.path.join( here, 'html', 'index.html' )

# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2016 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "3 - Alpha" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

import time
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT

from build_gui import GenericGUI, DEBUG_LEVEL
from build_gui import ARIAL_8B, ARIAL_10B, ARIAL_12B, ARIAL_8, ARIAL_10, ARIAL_12
from config_file import ConfigInterface
from recent_files import RecentFiles

import xlChart        


class MyWidget(QtGui.QWidget):
    
    def __init__(self, set_grid_layout=True):
        super(QtGui.QWidget,self).__init__()
        
        self.NextRowNumber = 0
        if set_grid_layout:
            self.grid = QtGui.QGridLayout(self)
            self.grid.setSpacing(0)
        

    def set_next_row_number( self, n ):
        self.NextRowNumber = n
        
    def get_next_row_number(self, advance_n=True):
        n = self.NextRowNumber
        if advance_n:
            self.NextRowNumber += 1
        return n


class MyTabWidget(QtGui.QTabWidget):
    
    def __init__(self):
        super(QtGui.QTabWidget,self).__init__()
        
    
    @pyqtSlot(int)
    def tabChangedSlot(self, argTabIndex):
        GenGUI.objectD['statusBar'].showMessage( "Page %i) "%(int(QtCore.QString.number(argTabIndex))+1,)  + GenGUI.tabL[argTabIndex] )
        
        # Show Nozzle Mode
        if GenGUI.tabL[argTabIndex] == 'Tab 1':
            pass
            
        elif GenGUI.tabL[argTabIndex] == 'Tab 2':
            pass

        QtGui.QMessageBox.information(self,
                      "Tab Index Changed!",
                      "Current Tab Index: "+QtCore.QString.number(argTabIndex) + ', ' + GenGUI.tabL[argTabIndex]);

class GenGUI(GenericGUI):
    """A generic GUI built with pyQt4. Used as starting point for new GUI apps.
    """
    objectD = {} # later set to self.objectD of GenGUI
    tabL = [] # used by MyTabWidget to ID tabs
    tabIndexD = {} # index=tab label, value=tabWidget index
    tabObjectD = {}# index=tab label, value=QtGui.QWidget()


    def __init__(self, centerContent=True, has_menu_bar=True, 
                  has_tool_bar=True, enable_recent_files=True):
        
        super(GenGUI, self).__init__(centerContent=centerContent, has_menu_bar=has_menu_bar,
                                      has_tool_bar=has_tool_bar)
        
        GenGUI.objectD = self.objectD # make sure objectD from GenericGUI is same as GenGUI
        
        self.enable_recent_files = enable_recent_files
        
        self.initVars()
        self.initUI()
        
    def initVars(self):
        self.data_file_suffix = '.inp'
        GenGUI.tabL.extend( ['Tab 1','Tab 2'] )
        
        self.main_window_title_str = 'Qt4_GenGUI'

    def add_widgets( self ):
        
        self.add_label( advance_n=True, text='Your label Here', name='sample',
                   text_align='', text_font=ARIAL_12B, col=1, width=1)
                   
        self.add_push_button( name='testBtn', fulldesc='This is a Test',
                           advance_n=False, text_font=ARIAL_12B, col=3, 
                           connect_function=self.print_output, background='', pressed_bgrnd='')
        
        self.add_radio_btns(['radio 1','radio 2','radio 3'], 
                          name='main_radio', init_val=2,
                          advance_n=False, fulldesc='Radio Choices', 
                          text_font=ARIAL_10, col=0)    
        
        self.add_image( advance_n=False, path_to_image=r'D:\py_proj_2016\Qt4_GenGUI\qt4_gengui\images\document.png', name='doc',
                        image_align='', col=2, width=1, height=1)
        
        # ====================================================
        if GenGUI.tabL:
            self.tabWidget  = MyTabWidget() 
            
            for tab_label in GenGUI.tabL:
                tabObj = MyWidget()
                GenGUI.tabObjectD[tab_label] = tabObj
                GenGUI.tabIndexD[tab_label] = self.tabWidget.addTab( tabObj ,tab_label)
                #grid = QtGui.QGridLayout()
                #grid.setSpacing(0)
                #tabObj.setLayout(grid) <=== done by MyWidget
            
            
            Nrow = self.get_next_row_number( advance_n=True)
            self.grid.addWidget(self.tabWidget, Nrow, 1, 4, 1)
            self.set_next_row_number( Nrow + 4 )

            tabObj = GenGUI.tabObjectD['Tab 1']
            self.add_label( advance_n=True, text='Your label Here', name='sample',
                       text_align='', text_font=ARIAL_12B, col=1, width=1, parent=tabObj)

            tabObj = GenGUI.tabObjectD['Tab 2']
            self.add_radio_btns(['tab 1','tab 2','tab 3'], 
                              name='tab_radio', init_val=2,
                              advance_n=False, fulldesc='Tab Choices', 
                              text_font=ARIAL_10, col=0, parent=tabObj)
                                
        self.add_check_box( advance_n=True, text='Choose Good', name='chkbox_sample',
                   text_font=ARIAL_12, col=3, width=1,
                   parent=None, layout=None)

        # =============================================
                   
        #self.add_some_vertical_space()
        
        
        self.add_list_box(['choice 1','choice 2','choice 3'], 
                          name='choiceNum', init_val=1,
                          advance_n=True, fulldesc='Generic Choices', 
                          connect_function=None, text_font=ARIAL_10, col=0)
                          
        self.add_some_horizontal_space( col=10, stretch=11)
        # ================================
        self.add_lineEdit( advance_n=False, text_font=ARIAL_10, onChange_function=None,
                                name='myval', fulldesc='Some Value',  col=2, width=1)
                           
        self.add_spin_box( name='Number', n_min=1, n_max=99, init_val=13,
                       advance_n=True, fulldesc='Number of Things', 
                        text_align='right', text_font=ARIAL_10, col=0, width=120)
        
        # ===================================
        self.add_combo_box( ['combo 1','combo 2','combo 3'], index_init=0, name='cycle_desc',
                        advance_n=False, fulldesc='Select Combo Item', 
                        text_align='right', text_font=ARIAL_10, col=0, width=100)
        
        self.add_hbox_lineEdit( advance_n=True, text_font=ARIAL_10,
                                name='mix_rat', fulldesc='Mixture Ratio',  col=2, width=1)
                                
    def initUI(self):
        
        self.objectD['QMainWindow'] = self
        
        if self.enable_recent_files:
            self.recent_file_obj = RecentFiles(self.main_window_title_str)
            self.recent_file_obj.chdir()
            
            self.current_filePath = self.recent_file_obj.get_dir()
        else:
            self.current_filePath = here
            
        self.current_fileName = ''
        self.current_config_interface = None # Will change to default at bottom of init
        self.has_changes = False


        
        self.inputD = {} # holds inputs to GUI
        
        openAction = self.add_action( name='Open', connect_function=self.open_file, 
                     shortcut='Ctrl+O', status_tip='Open File', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/open.jpg'))
                
        saveAction = self.add_action( name='Save', connect_function=self.save_file, 
                     shortcut='Ctrl+S', status_tip='Save File', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/save_v4.jpg'))
                
        saveAsAction = self.add_action( name='SaveAs', connect_function=self.saveAs_file, 
                     shortcut='F12', status_tip='SaveAs File', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/saveas.jpg'))
                
        runAction = self.add_action( name='Run', connect_function=self.run_calculation, 
                     shortcut='F5', status_tip='Run Calculation', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/run.jpg'))
        
        excelAction = self.add_action( name='Launch Excel', connect_function=self.launch_excel, 
                     shortcut='F7', status_tip='Launch Excel', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/excel.jpg'))
        
        helpAction = self.add_action( name='Launch Help', connect_function=self.launch_help, 
                     shortcut='F1', status_tip='Launch Help', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/help.jpg'))
        
        printAction = self.add_action( name='Print', connect_function=self.print_output, 
                     shortcut='Ctrl+P', status_tip='Print Results', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/print.png'))
        
        exitAction = self.add_action( name='Exit', connect_function=self.maybe_exit, 
                     shortcut='Ctrl+Q', status_tip='Exit Application', tool_size=(40,40), 
                     icon_path=os.path.join(here,'./images/exit.jpg'))
        

        if self.enable_recent_files:
            self.recentFileActs = []
            for i in range(RecentFiles.MaxRecentFiles):
                self.recentFileActs.append(
                        QtGui.QAction(self, visible=False,
                                triggered=self.openRecentFile))

        
        self.status_bar = self.statusBar()
        self.objectD['statusBar'] = self.status_bar

        if self.has_menu_bar:
            self.gen_menubar = self.menuBar()
            self.add_menu_item( name='Open', menu_header='File')
            self.add_menu_item( name='Save', menu_header='File')
            self.add_menu_item( name='SaveAs', menu_header='File')
            fileMenu = self.add_menu_item( name='Print', menu_header='File')
            
            if self.enable_recent_files:
                self.separatorAct = fileMenu.addSeparator()
                for i in range(RecentFiles.MaxRecentFiles):
                    fileMenu.addAction(self.recentFileActs[i])
                fileMenu.addSeparator()        
            
            self.add_menu_item( name='Exit', menu_header='File')

            self.add_menu_item( name='Run', menu_header='Tools')
            self.add_menu_item( name='Launch Excel', menu_header='Tools')

            self.add_menu_item( name='Launch Help', menu_header='Help')
            
        
        # Debug print of default values
        if DEBUG_LEVEL > 2:
            for key,val in sorted( self.input_widget_by_nameD.items() ):
                print '%15s'%key,val[-1]
            print

        self.setGeometry(100, 100, 500, 300)
        self.setMinimumSize(500,300)
        #self.setWindowTitle('Qt4_GenGUI')
        
        self.updateRecentFileActions()
        
        self.add_widgets()

        self.tabWidget.connect(self.tabWidget,SIGNAL("currentChanged(int)"),
                               self.tabWidget,SLOT("tabChangedSlot(int)"))
        
        if len(sys.argv) > 1:
            print 'Opening Data File:',sys.argv[1]
            fname = sys.argv[1]
            if not fname.lower().endswith(self.data_file_suffix.lower()):
                print '   Assuming data suffix: "%s"'%self.data_file_suffix
                fname = fname + self.data_file_suffix
                
            fname = os.path.abspath( fname )
            if os.path.isfile( fname ):
                self.load_file( fname )
                print '...NOTICE... loaded file:'
                print '    ',fname
            else:
                print '...ERROR... could not find file:'
                print '    ',fname
                
            self.updateRecentFileActions()
        
        self.clear_changes() # No current changes to worry about
        
        self.set_main_window_title()
        
        self.show()


    def updateRecentFileActions(self):
        
        if not self.has_menu_bar:
            return
            
        if not self.enable_recent_files:
            return

        fileL = self.recent_file_obj.recent_fileL
        
        numRecentFiles = min(len(fileL), RecentFiles.MaxRecentFiles)

        for i in range(numRecentFiles):
            head,tail = os.path.split( fileL[i] )
            text = "&%d %s" % (i + 1, tail)
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData( fileL[i] )
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, RecentFiles.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

        
    def openRecentFile(self):
        action = self.sender()
        if action:
            self.load_file( str(action.data().toString()) )
            #print dir( action.data() )
            #print action.data().toString()


    def flag_changes(self):
        self.has_changes = True
        if self.current_config_interface is not None:
            self.current_config_interface.has_changes = True # Has current changes to worry about

    def clear_changes(self):
        self.has_changes = False
        if self.current_config_interface is not None:
            self.current_config_interface.has_changes = False # No current changes to worry about
    
    def set_main_window_title(self):
        s = self.main_window_title_str
        
        if self.current_fileName:
            s = s + ' (%s)'%self.current_fileName
        self.setWindowTitle( s )
    
    def set_pending_file_value(self, name, val):
        
        self.has_changes = True
        
        if self.current_config_interface is not None:
            self.current_config_interface['Input',name] = val
            if DEBUG_LEVEL > 2:
                print 'Set Pending File Value',name,val
        
    
    def continue_after_possible_save(self):
        """
        Return True if there are pending changes to the current inputs 
        AND... the user elects to stop current action and save.
        """
        
        if self.current_config_interface is None and (not self.has_changes):
            return True
        else:
            if self.has_changes or self.current_config_interface.has_changes:
                
                msg = "Do you want to Save First?\n"+\
                      "\n YES\t\tSave changes and Exit"+\
                      "\n NO\t\tDiscard change and Exit"+\
                      "\n CANCEL\tKeep application open"
                reply = QtGui.QMessageBox.question(self, 'There are pending changes to the input.', 
                                                    msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
                if reply == QtGui.QMessageBox.Yes:
                    self.save_file()
                    return True
                elif reply == QtGui.QMessageBox.No:
                    return True
            else:
                return True
        return False # Returns False if Cancel is selected
        
    def load_file(self, full_fname):
        
        if self.enable_recent_files:
            self.recent_file_obj.update( full_fname )
            self.updateRecentFileActions()
        
        head,tail = os.path.split( full_fname )
        
        self.current_filePath = head
        self.current_fileName = tail
        
        self.current_config_interface = ConfigInterface( config_filename=full_fname, sectionL=['Input'] )
        
        inputD = self.current_config_interface.get_dictionary()
        if 'Input' in inputD:
            self.inputD = inputD['Input']
            self.set_IO_values( )
        
        self.status_bar.showMessage( 'Opened File: "%s"'%self.current_fileName )
        self.updateRecentFileActions()
        
        # No current changes to worry about
        self.clear_changes() # No current changes to worry about        
        
        self.set_main_window_title()

    def closeEvent(self, event):
        
        if self.continue_after_possible_save():
            event.accept()
        else:
            event.ignore()
            QtGui.QMessageBox.information(self,
                          "Cancelled Exit Command",
                          'Pending Changes To: "%s"'%self.current_fileName);
        
    def maybe_exit(self):
        
        if self.continue_after_possible_save():
            QtGui.qApp.quit()
        else:
            QtGui.QMessageBox.information(self,
                          "Cancelled Exit Command",
                          'Pending Changes To: "%s"'%self.current_fileName);


    def open_file(self):
        
        if not self.continue_after_possible_save():
            QtGui.QMessageBox.information(self,
                          "Cancelled Open Command",
                          'Pending Changes To: "%s"'%self.current_fileName);
            return
        
        Qfname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self.current_filePath, 
                                                   'Qt4_GenGUI (*%s)'%self.data_file_suffix )
        
        if Qfname:
            self.load_file( str( Qfname ) )
    
    def save_file(self):
        
        if self.current_config_interface is not None:

            if self.enable_recent_files:
                self.recent_file_obj.update( self.current_config_interface.config_filename )
                self.updateRecentFileActions()
            
            resultD = self.get_IO_values()
            keyL = resultD.keys()
            keyL.sort(key=str.lower)
            for key in keyL:
                self.current_config_interface['Input',key] = resultD[key]
            self.current_config_interface.save_file()
            
            self.status_bar.showMessage( 'Saved to File: "%s"'%self.current_fileName )
            
            self.set_main_window_title()
            QtGui.QMessageBox.information(self,
                          "Saved to File: %s"%self.current_fileName,
                          'at: "%s"'%self.current_filePath);
        
            #self.updateRecentFileActions()
            
            # No current changes to worry about
            self.clear_changes() # No current changes to worry about        
            
        else:
            self.saveAs_file()
    
    def saveAs_file(self):
        
        Qfname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', self.current_filePath, 
                                                   'Qt4_GenGUI (*%s)'%self.data_file_suffix )
        
        if Qfname:
            fname = str( Qfname )
            head,tail = os.path.split( fname )

            if self.enable_recent_files:
                self.recent_file_obj.update( fname )
                self.updateRecentFileActions()
            
            self.current_filePath = head
            self.current_fileName = tail
            
            self.current_config_interface = ConfigInterface( config_filename=fname, sectionL=['Input'] )
            
            resultD = self.get_IO_values()
            keyL = resultD.keys()
            keyL.sort(key=str.lower)
            for key in keyL:
                self.current_config_interface['Input',key] = resultD[key]
            self.current_config_interface.save_file()
            
            self.status_bar.showMessage( 'Saved to File: "%s"'%self.current_fileName )
        
            self.updateRecentFileActions()
            
            self.set_main_window_title()
            # No current changes to worry about
            self.clear_changes() # No current changes to worry about        
    
    def launch_excel(self):
        
        self.get_IO_values() # loads self.inputD
        
        keyL = self.inputD.keys()
        keyL.sort( key=str.lower )
        
        xl = xlChart.xlChart()
        xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message
        
        rs = []
        for key in keyL:
            rs.append([key, self.inputD[key]])
        
        xl.makeDataSheet( rs, sheetName='GenGUI', rowFormatL=None)
        xl.pageSetupForSheet(landscape=0, fitWidth=1, fitHeight=1, marginInches=0.0)
        
        png_file = os.path.join(here, 'images', 'document.png')
        
        xl.AddPictureToDataSheet(imgAbsPath=png_file, sheetName='GenGUI', 
            left=250, top=50, width=150, height=150)
            
        
        #QtGui.QMessageBox.information(self,
        #              "Need Excel Logic!",
        #              "Run Excel here.");

    
    def run_calculation(self):
        QtGui.QMessageBox.information(self,
                      "Need Calculation Logic!",
                      "Run Calculation here.");
    
    def print_output(self):
        #self.run_calculation()
        QtGui.QMessageBox.information(self,
                      "Need Print Logic!",
                      "Run Print here.");
    
    def launch_help(self):
        webbrowser.open(INDEX_PAGE)

def main():
    app = QtGui.QApplication(sys.argv)
    my_widget = GenGUI()
    my_widget.show()

    sys.exit(app.exec_())    

if __name__ == '__main__':
    #C = GenGUI()
    main()