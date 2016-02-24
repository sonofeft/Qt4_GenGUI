import sys
from PyQt4 import QtGui
from qt4_gengui.gui_main import GenGUI, MyTabWidget, MyWidget
from qt4_gengui.build_gui import GenericGUI, DEBUG_LEVEL
from qt4_gengui.build_gui import ARIAL_8B, ARIAL_10B, ARIAL_12B, ARIAL_8, ARIAL_10, ARIAL_12


class MyGUI( GenGUI ):

    def __init__(self, centerContent=False):
        super(MyGUI, self).__init__(centerContent=centerContent)
                        
    def initVars(self):
        self.data_file_suffix = '.dat'
        GenGUI.tabL.extend(  ['Orifice 1','Face Seal'] )
        
        self.main_window_title_str = 'Orifice Calcs'
    
    def add_widgets( self ):
        
        self.add_label( advance_n=True, text='My New GUI', name='sample',
                   text_align='', text_font=ARIAL_12B, col=1, width=1)
        
        self.tabWidget  = MyTabWidget() 
        
        for tab_label in GenGUI.tabL:
            tabObj = MyWidget()
            GenGUI.tabObjectD[tab_label] = tabObj
            GenGUI.tabIndexD[tab_label] = self.tabWidget.addTab( tabObj ,tab_label)
            grid = QtGui.QGridLayout()
            grid.setSpacing(0)
            tabObj.setLayout(grid)
        
        
        Nrow = self.get_next_row_number( advance_n=True)
        self.grid.addWidget(self.tabWidget, Nrow, 1, 4, 1)
        self.set_next_row_number( Nrow + 4 )

        tabObj = GenGUI.tabObjectD['Orifice 1']
        self.add_label( advance_n=True, text='Your label Here', name='sample',
                   text_align='', text_font=ARIAL_12B, col=1, width=1, parent=tabObj)

        tabObj = GenGUI.tabObjectD['Face Seal']
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
 
 
 