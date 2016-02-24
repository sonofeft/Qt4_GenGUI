
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog, QVBoxLayout, QDialogButtonBox, QApplication, QGridLayout, QWidget
from PyQt4.QtGui import QLabel, QFont, QGroupBox, QRadioButton, QPushButton, QSizePolicy, QSpinBox
from PyQt4.QtGui import QHBoxLayout, QComboBox, QLineEdit, QListWidget, QListWidgetItem, QPixmap
from PyQt4.QtCore import Qt

from build_gui import ARIAL_8B, ARIAL_10B, ARIAL_12B, ARIAL_8, ARIAL_10, ARIAL_12
from build_gui import DEBUG_LEVEL

class GenericDialog(QDialog):
    def __init__(self, parent=None, inputD=None):
        super(GenericDialog, self).__init__(parent)
        
        if inputD is None:
            self.inputD = {}
        else:
            self.inputD = inputD
            
        # ==================== build parameters =======================================
        self.NextRowNumber = 0
        self.resultD = {} # Result Dictionary
        self.resultD.update( self.inputD )
        
        self.objectD = {}               # index=name, value=PyQt4 object
        self.input_widget_by_nameD = {} # index=name, value=tuple(widgetObj, typeDesc)
        self.selection_textD = {}      # index=name, value=text of selection (used for radio buttons and list boxes)
        self.onChange_functionD = {}   # index=name, value=function to call on change

        # 
        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)

        # ============  Add All Dialog Widgets Below Here ==========

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.grid.addWidget(buttons, 222,1)
    
    def print_internal_dicts(self):
        print '_'*20,'GenericDialog Dictionary Variables','_'*20
        keyL = self.input_widget_by_nameD.keys()
        keyL.sort( key=str.lower )
        for key in keyL:
            print 'self.input_widget_by_nameD key =',key
        print
        
        keyL = self.inputD.keys()
        keyL.sort( key=str.lower )
        for key in keyL:
            print 'self.inputD key =',key
        print
        
        keyL = self.resultD.keys()
        keyL.sort( key=str.lower )
        for key in keyL:
            print 'self.resultD key =',key
        print

    def onChange_function(self, widget=None, widget_name=''):
        """Override this function for any special processing when widgets change"""
        pass
        if DEBUG_LEVEL > 2:
            print 'Original onChange_function'

    def get_IO_values(self):
        """
        Adds widget values to self.resultD  dictionary of all I/O variables
        """
        localD = {}
        
        for name in self.input_widget_by_nameD:
            # Look at the type of widget
            widget, widget_type = self.input_widget_by_nameD[name]
            
            # ======= do dimensionless QLineEdit objects here
            if widget_type in ['line_edit']:
                localD[name] = str( widget.text() )
                #widget.setText( '%s'%val )
                
            elif widget_type == 'radio_btn_list':
                
                if name == "isBell":
                    localD[name] = str( widget[0].isChecked() )
                else:
                    localD[name] = self.selection_textD[ name ]
                    #print 'In get_IO_values',name,'=',localD[name]
            
            elif widget_type == 'list_box_list':
                localD[name] = self.selection_textD[ name ]
                #print 'In get_IO_values',name,'=',localD[name]
            
            elif widget_type == 'combo_box':
                localD[name] = str( widget.currentText() )
        
        self.resultD.update( localD )
        return self.resultD
        

    def set_IO_values( self ):
        # Iterate through all the I/O widgets
        for name,val in self.inputD.items():
            val = '%s'%val
            #print 'generic dialog setting',name,'to',val
            # If the widget is in the dictionary...
            if name in self.input_widget_by_nameD:
                # Look at the type of widget
                widget, widget_type = self.input_widget_by_nameD[name]
                
                # ======= do dimensionless QLineEdit objects here
                if widget_type == 'line_edit':
                    #print 'generic dialog setting',name,'to',val
                    if str( widget.text() ) != '%s'%val:
                        widget.setText( '%s'%val )
                        #print 'generic dialog setting',name,'to',val,'should == %s'%str( widget.text() )
                
                elif widget_type == 'radio_btn_list':
                    if name == "isBell":
                        if val in ['True','1']:
                            widget[0].setChecked(True)
                        else:
                            widget[1].setChecked(True)
                        #print radio.text(), radio.isChecked()
                    else:
                        for i,radio in enumerate(widget): # NOTE... widget is actually a list of QRadioButton objects
                            if val == str( radio.text() ):
                                radio.setChecked(True)
                                
                elif widget_type == 'list_box_list':
                    for i in range( widget.count() ):
                        item = widget.item(i)
                        if str( item.text() ) == val:
                            widget.setItemSelected( item, True )
                            
                        
                elif widget_type == 'combo_box':
                    if str( widget.currentText() ) != str(val):
                        index = widget.findText(val)
                        if index >= 0:
                             widget.setCurrentIndex(index)       
         
        
        self.onChange_function()
                     
    def set_next_row_number(self, n ):
        self.NextRowNumber = n
        
    def get_next_row_number(self, advance_n=True):
        n = self.NextRowNumber
        if advance_n:
            self.NextRowNumber += 1
        return n

    def advance_row_number():
        return self.get_next_row_number(advance_n=True)
                
    def spin_box_changed(self, spin_box_name ):
        sbox_val = self.objectD[spin_box_name].value()
        #print 'Spin Box "%s" Changed To:'%spin_box_name, sbox_val
        
        self.onChange_function( widget=self.objectD[spin_box_name], widget_name=spin_box_name )

    def combo_box_changed(self, combo_box_name ):
        
        cbox_text = self.objectD[combo_box_name].currentText()
        #print 'Combo Box "%s" Changed To:'%combo_box_name, cbox_text
        
        self.onChange_function( widget=self.objectD[combo_box_name], widget_name=combo_box_name )

    def line_edit_changed(self, lineEditName):
        
        ledit_text = str(self.objectD[lineEditName].text()).strip()
        #print 'Line Edit "%s" Changed To:'%lineEditName, ledit_text
        
        self.onChange_function( widget=self.objectD[lineEditName], widget_name=lineEditName )
        
                
    def list_box_changed(self, list_box_name ):
        
        name = list_box_name.replace('_list_box','')
        
        itemL = self.objectD[list_box_name].selectedItems()
        if itemL:
            item = itemL[0]
            i = int(self.objectD[list_box_name].indexFromItem( item ).row())
            self.selection_textD[name] = str(item.text())
            
        if DEBUG_LEVEL > 2:
            print 'List Box "%s" Changed To:'%list_box_name, ' i=%i'%i
        
        self.onChange_function( widget=self.objectD[list_box_name], widget_name=list_box_name )

    def radio_btn_changed(self, radio_btn_name ):
        
        if DEBUG_LEVEL > 2:
            print 'Radio Button "%s" changed'%radio_btn_name
        radio_btnL = self.objectD[radio_btn_name]
        
        name = radio_btn_name.replace('_radio_group_box','')
        
        for i,btn in enumerate(radio_btnL):
            if btn.isChecked():
                if DEBUG_LEVEL > 2:
                    print 'Selected Text =', str(btn.text()),'  index=%i'%i
                self.selection_textD[name] = str(btn.text())

    def add_some_vertical_space( self ):

        # Add some space in the middle ================================
        NRow = self.get_next_row_number(advance_n=True)
        
        vbox = QVBoxLayout()
        vbox.addStretch()
        widget = QWidget()
        widget.setLayout(vbox)
        self.grid.addWidget(widget, NRow, 0)


    def add_list_box(self, choicesL, 
                          name='isBell', init_val=3,
                          advance_n=True, fulldesc='Nozzle Geometry', 
                          connect_function=None, text_font=ARIAL_10, col=0):
                                            
        NRow = self.get_next_row_number(advance_n)
        # Need to change next row number by length of choicesL
        if advance_n:
            for i in range(1, len(choicesL)):
                self.get_next_row_number(advance_n)
        
        self.selection_textD[name] = ''
        
        listWidget = QListWidget()
        for i,choice in enumerate( choicesL ):
            item = QListWidgetItem(choice)
            listWidget.addItem(item)
            if i == init_val:
                #item.setChecked(True)
                listWidget.setItemSelected( item, True )
                self.selection_textD[name] = choice
        #listWidget.setCurrentRow( init_val )
                
        self.grid.addWidget(listWidget,      NRow, col, len(choicesL), 1)
        
        self.objectD['%s_list_box'%name] = listWidget
        self.input_widget_by_nameD[name] = (listWidget , 'list_box_list')
        
        listWidget.itemClicked.connect( lambda: self.list_box_changed( '%s_list_box'%name ) ) 
    

    def add_push_button(self, name='test', fulldesc='This is a Test',
                           advance_n=True, text_font=ARIAL_12B, col=0, 
                           connect_function=None, background='', pressed_bgrnd=''):
                           # springgreen #00FF7F , lightgreen #90EE90 , powderblue #B0E0E6
                                            
        NRow = self.get_next_row_number(advance_n)
        btn = QPushButton(fulldesc, self)
        btn.setFont( text_font )
        
        if background and pressed_bgrnd:
            btn.setStyleSheet("QPushButton { background-color:%s } "%background +\
                               "QPushButton:pressed { background-color: %s }"%pressed_bgrnd  )
        
        self.grid.addWidget(btn,      NRow, col)
        
        self.objectD['%s_push_btn'%name] = btn
        self.input_widget_by_nameD[name] = (btn , 'push_btn')
        
        if connect_function is not None:
            btn.clicked.connect( connect_function )


    def add_image(self, advance_n=True, path_to_image='', name='',
                   image_align='', col=0, width=1, height=1):
        
        NRow = self.get_next_row_number(advance_n)
        lbl = QLabel('', self)
        pixmap = QPixmap(path_to_image) # should be absolute path
        lbl.setPixmap(pixmap)
        
        if width==1 and height==1:
            self.grid.addWidget(lbl,  NRow, col)
        else:
            self.grid.addWidget(lbl,  NRow, col, height, width)
        
        if image_align=='right':
            self.grid.setAlignment(lbl, Qt.AlignRight )

        if name:
            self.objectD['%s_pixmap'%name] = lbl
            self.input_widget_by_nameD[name] = (lbl , 'pixmap')

    def add_label(self, advance_n=True, text='label text', name='',
                   text_align='', text_font=ARIAL_12, col=0, width=1):
        
        NRow = self.get_next_row_number(advance_n)
        lbl = QLabel(text, self)
        lbl.setFont( text_font )
        
        if width==1:
            self.grid.addWidget(lbl,  NRow, col)
        else:
            self.grid.addWidget(lbl,  NRow, col, 1, width)
        
        if text_align=='right':
            self.grid.setAlignment(lbl, Qt.AlignRight )

        if name:
            self.objectD['%s_label'%name] = lbl
            self.input_widget_by_nameD[name] = (lbl , 'label')


    def add_radio_btns(self, choicesL, 
                          name='isBell', init_val=3,
                          advance_n=True, fulldesc='Nozzle Geometry', 
                          text_font=ARIAL_10, col=0):
                                            
        NRow = self.get_next_row_number(advance_n)
        # Need to change next row number by length of choicesL
        if advance_n:
            for i in range(1, len(choicesL)):
                self.get_next_row_number(advance_n)
        
        radio_btnL = [] # a list of radio buttons in this group
        self.selection_textD[name] = ''
        
        # First build the radio buttons
        groupBox = QGroupBox(fulldesc)
        vbox = QVBoxLayout()
        for i,choice in enumerate( choicesL ):
            radio = QRadioButton(choice, groupBox)
            vbox.addWidget(radio)
            if i == init_val:
                radio.setChecked(True)
                self.selection_textD[name] = str( choice )
                
            radio_btnL.append( radio )
            
            radio.toggled.connect( lambda: self.radio_btn_changed( '%s_radio_group_box'%name ) ) 

            
        #vbox.addStretch(1)
        groupBox.setLayout(vbox)
        
        self.grid.addWidget(groupBox,      NRow, col, len(choicesL), 1)
        
        self.objectD['%s_radio_group_box'%name] = radio_btnL
        self.input_widget_by_nameD[name] = (radio_btnL , 'radio_btn_list')
    
    

    def add_spin_box(self, name='Number', n_min=1, n_max=99, init_val=1,
                       advance_n=True, fulldesc='Number of Engines', 
                        text_align='right', text_font=ARIAL_10, col=0, width=120):
                            
        NRow = self.get_next_row_number(advance_n)
        
        lbl = QLabel("    %s "%fulldesc, self)
        lbl.setFont( text_font )
        
        spin_box =  QSpinBox(self)    
        spin_box.setFont( text_font )
        spin_box.setFixedWidth( width )
        spin_box.setRange( n_min, n_max)
        spin_box.setValue( init_val )
        
        self.grid.addWidget(lbl,      NRow, col)
            
        hbox = QHBoxLayout()
        hbox.addWidget(spin_box)
        hbox.addStretch(1)
        widget = QWidget()
        widget.setLayout(hbox)
        self.grid.addWidget(widget , NRow, col+1)
        
        if text_align=='right':
            self.grid.setAlignment(lbl, Qt.AlignRight )
        
        self.objectD['%s_spin_box'%name] = spin_box 
        self.input_widget_by_nameD[name] = (spin_box , 'spin_box')
            
        spin_box.valueChanged.connect( lambda: self.spin_box_changed( '%s_spin_box'%name ) )   

    

    def add_combo_box( self, choicesL, index_init=0, name='cycle_desc',
                        advance_n=True, fulldesc='Select Engine Cycle', 
                        text_align='right', text_font=ARIAL_10, col=0, width=100):
        
        NRow = self.get_next_row_number(advance_n)
        
        lbl = QLabel("    %s "%fulldesc, self)
        combo_box = QComboBox(self)    
        lbl.setFont( text_font )
        combo_box.setFont( text_font )
        
        self.objectD['%s_combo_box'%name] = combo_box
        for choice in choicesL:
            combo_box.addItem(choice)
        combo_box.setCurrentIndex(index_init)
        self.grid.addWidget(lbl,      NRow, col)
        
        
            
        hbox = QHBoxLayout()
        hbox.addWidget(combo_box)
        hbox.addStretch(1)
        widget = QWidget()
        widget.setLayout(hbox)
        
        self.grid.addWidget(widget, NRow, col+1)
        
        combo_box.setFixedWidth( width )
        
        if text_align=='right':
            self.grid.setAlignment(lbl, Qt.AlignRight )
            
        combo_box.activated[str].connect( lambda: self.combo_box_changed( '%s_combo_box'%name ) )   
            
        self.input_widget_by_nameD[name] = (combo_box, 'combo_box')
    
    

    def add_hbox_lineEdit(self, advance_n=True, text_font=ARIAL_10,
                                name='ofcore', fulldesc='Core Mixture Ratio (O/F)',  col=0, width=1):
        
        NRow = self.get_next_row_number(advance_n)

        hbox = QHBoxLayout()

        lbl = QLabel(fulldesc, self )
        lbl.setFont( text_font )
        hbox.addWidget(lbl)
        
        lineEdit = QLineEdit( self )
        lineEdit.setFont( text_font )
        hbox.addWidget(lineEdit)
        hbox.addStretch(1)
        widget = QWidget()
        widget.setLayout(hbox)
        
        lineEdit.textEdited[str].connect(lambda: self.line_edit_changed('%s_lineEdit'%name))
        
        if width > 1:
            self.grid.addWidget(widget, NRow, col, 1, width)
        else:
            self.grid.addWidget(widget, NRow, col)
        
        self.objectD['%s_lineEdit'%name] = lineEdit
        self.input_widget_by_nameD[name] = (lineEdit, 'line_edit')
    

    def add_lineEdit(self, advance_n=True, text_font=ARIAL_10, onChange_function=None,
                                name='ofcore', fulldesc='Core Mixture Ratio (O/F)',  col=0, width=1):
        
        NRow = self.get_next_row_number(advance_n)
        
        lbl = QLabel(fulldesc, self )
        lbl.setFont( text_font )
        self.grid.addWidget(lbl,      NRow, col)
        self.grid.setAlignment(lbl, Qt.AlignRight )
        
        lineEdit = QLineEdit( self )
        lineEdit.setFont( text_font )
        
        lineEdit.textEdited[str].connect(lambda: self.line_edit_changed('%s_lineEdit'%name))
        
        if width > 1:
            self.grid.addWidget(lineEdit, NRow, col+1, 1, width)
        else:
            lineEdit.setFixedWidth( 100 )
            
            hbox = QHBoxLayout()
            hbox.addWidget(lineEdit)
            hbox.addStretch(1)
            widget = QWidget()
            widget.setLayout(hbox)
            
            self.grid.addWidget(widget, NRow, col+1)
        
        self.objectD['%s_lineEdit'%name] = lineEdit
        self.input_widget_by_nameD[name] = (lineEdit, 'line_edit')
    
        if onChange_function:
            self.onChange_functionD[name] = onChange_function
