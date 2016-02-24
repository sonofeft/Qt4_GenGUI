
from qt4_gengui.generic_dialog import GenericDialog
from qt4_gengui.build_gui import ARIAL_8B, ARIAL_10B, ARIAL_12B, ARIAL_8, ARIAL_10, ARIAL_12


def getOutput(parent = None, inputD = None):
    dialog = GenericDialog(parent, inputD)
    
    dialog.add_some_vertical_space(  )
          
    dialog.add_radio_btns(['Bell Nozzle','Conical Nozzle'], 
                  name='isBell', init_val=0,
                  advance_n=False, fulldesc='Nozzle Geometry', 
                  text_font=ARIAL_10, col=0)
                  
    dialog.add_spin_box( name='Number', n_min=1, n_max=99, init_val=1,
             advance_n=True, fulldesc='Number of Engines', 
             text_align='right', text_font=ARIAL_10, col=2, width=100)
    
    dialog.add_combo_box( ['Eeny','Meeny','Minee'], index_init=1, name='tech_level',
                advance_n=True, fulldesc='Select Technology Level', 
                text_align='right', text_font=ARIAL_10, col=2, width=200)
    
    dialog.add_lineEdit( name='eps', fulldesc='Nozzle Area Ratio',  col=0, 
                     advance_n=True, width=1)


    
    
    dialog.set_IO_values()
    
    result = dialog.exec_()
    
    dialog.get_IO_values()
    
    return (dialog.resultD, result == QtGui.QDialog.Accepted)

if __name__ == '__main__':

    import sys
    from PyQt4 import QtGui
    from PyQt4.QtGui import QDialog, QVBoxLayout, QDialogButtonBox, QApplication, QGridLayout, QWidget
    from PyQt4.QtGui import QLabel, QFont, QGroupBox, QRadioButton, QPushButton, QSizePolicy, QSpinBox
    from PyQt4.QtGui import QHBoxLayout, QComboBox, QLineEdit
    from PyQt4.QtCore import Qt


    # ============ All Testing Code Below Here =======================================
    class Example(QWidget):
        
        def __init__(self):
            super(Example, self).__init__()
            
            self.initUI()
            
        def initUI(self):      

            vbox = QVBoxLayout()

            btn = QPushButton('Dialog', self)
            btn.setSizePolicy(QSizePolicy.Fixed,
                QSizePolicy.Fixed)
            
            btn.move(20, 20)

            vbox.addWidget(btn)

            btn.clicked.connect(self.showDialog)
            
            self.lbl = QLabel('Cosmic Well-Being', self)
            self.lbl.move(130, 20)

            vbox.addWidget(self.lbl)
            self.setLayout(vbox)          
            
            self.setGeometry(300, 300, 250, 180)
            self.setWindowTitle('Font dialog')
            self.show()
            
        def showDialog(self):
            
            resultD, ok = getOutput( inputD = {'three':3, 'eps':25, 'Fvac':125.5})
            if ok:
                print 'resultD =',resultD
                print 'ok   =',ok
                self.lbl.setText('%s'%(resultD,))

            
    def main():
        
        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())



    main()        