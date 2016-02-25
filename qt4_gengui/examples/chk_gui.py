import sys
import os
from PyQt4 import QtGui
from qt4_gengui.gui_main import GenGUI, MyTabWidget, MyWidget
from qt4_gengui.build_gui import GenericGUI, DEBUG_LEVEL
from qt4_gengui.build_gui import ARIAL_8B, ARIAL_10B, ARIAL_12B, ARIAL_8, ARIAL_10, ARIAL_12
from PyQt4.QtCore import pyqtSlot
from PyQt4 import QtCore

here = os.path.abspath(os.path.dirname(__file__))

class MyTabWidget(QtGui.QTabWidget):
    
    def __init__(self):
        super(QtGui.QTabWidget,self).__init__()
        
    
    @pyqtSlot(int)
    def tabChangedSlot(self, argTabIndex):
        GenGUI.objectD['statusBar'].showMessage( "Page %i) "%(int(QtCore.QString.number(argTabIndex))+1,)\
                                                  + GenGUI.tabL[argTabIndex] )
        
        # Show Nozzle Mode
        if GenGUI.tabL[argTabIndex] == 'Pollywog':
            print 'GenGUI.tabL[argTabIndex] =',GenGUI.tabL[argTabIndex]
            
        elif GenGUI.tabL[argTabIndex] == 'Tree Frog':
            print 'Entered Tree Frog tab'

class MyGUI( GenGUI ):

    def __init__(self, centerContent=False, enable_recent_files=True):
        
        super(MyGUI, self).__init__(centerContent=centerContent, 
                                     enable_recent_files=enable_recent_files)
                                     
        self.setGeometry(100, 100, 600, 300)
        self.setMinimumSize(500,300)
    
    def say_hello(self):
        #self.run_calculation()
        QtGui.QMessageBox.information(self,
                      "Hello World!",
                      "This is a new Menu Item");
    
                        
    def initVars(self):
        self.data_file_suffix = '.dat'
        GenGUI.tabL.extend(  ['Pollywog','Tree Frog'] )
        
        
        self.add_action( name='Hello', connect_function=self.say_hello, 
                     shortcut='Ctrl+H', status_tip='Say Hello', 
                     icon_path=os.path.join(here,'./hello.jpg'))
        
        GenGUI.toolbarL = ['Open', 'Save', 'SaveAs', 'Run', 'Hello',
                           'Launch Excel', 'Launch Help', 'Print', 'Exit']
        # First member of each list is menu header. Rest of list are menu items.
        GenGUI.standard_menuLL = [['File', 'Open', 'Save', 'SaveAs', 'Print', 'Exit'], 
                                  ['Tools','Run','Launch Excel'], 
                                  ['Help','Launch Help', 'About', 'Hello']]

        
        # Will create a configuration file at:
        #    C:\Users\<Your Name>\<main_window_title_str>.cfg
        self.main_window_title_str = 'Pollywog Calcs' # <== builds *.cfg file
    
    def add_widgets( self ):
        
        self.add_label( advance_n=True, text='My New GUI', name='sample',
                   text_align='', text_font=ARIAL_12B, col=1, width=1)
        
        self.tabWidget  = MyTabWidget() 
        
        for tab_label in GenGUI.tabL:
            tabObj = MyWidget()
            GenGUI.tabObjectD[tab_label] = tabObj
            GenGUI.tabIndexD[tab_label] = self.tabWidget.addTab( tabObj ,tab_label)
        
        
        Nrow = self.get_next_row_number( advance_n=True)
        self.grid.addWidget(self.tabWidget, Nrow, 1, 4, 1)
        self.set_next_row_number( Nrow + 4 )

        tabObj = GenGUI.tabObjectD['Pollywog']
        self.add_label( advance_n=True, text='Your label Here', name='sample',
                   text_align='', text_font=ARIAL_12B, col=1, width=1, parent=tabObj)

        tabObj = GenGUI.tabObjectD['Tree Frog']
        self.add_radio_btns(['tab 1','tab 2','tab 3'], 
                          name='tab_radio', init_val=2,
                          advance_n=False, fulldesc='Tab Choices', 
                          text_font=ARIAL_10, col=0, parent=tabObj)


def main():
    app = QtGui.QApplication(sys.argv)
    myWidget = MyGUI()
    myWidget.show()

    sys.exit(app.exec_())    

if __name__ == '__main__':
    #C = GenGUI()
    main()
 
 
 