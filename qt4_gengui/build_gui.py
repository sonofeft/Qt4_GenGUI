
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QVBoxLayout, QDialogButtonBox, QApplication, QGridLayout, QWidget
from PyQt4.QtGui import QLabel, QFont, QGroupBox, QRadioButton, QPushButton, QSizePolicy, QSpinBox
from PyQt4.QtGui import QHBoxLayout, QComboBox, QLineEdit, QListWidget, QListWidgetItem, QPixmap
from PyQt4.QtGui import QCheckBox
from PyQt4.QtCore import Qt

ARIAL_8B = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
ARIAL_8 = QtGui.QFont("Arial", 8)

ARIAL_10B = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)
ARIAL_10 = QtGui.QFont("Arial", 10)

ARIAL_12B = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
ARIAL_12 = QtGui.QFont("Arial", 12)

DEBUG_LEVEL = 0 # 0=no debug printing, 1=only most important, 2=medium, >=3 all output

class GenericGUI(QtGui.QMainWindow):
    def __init__(self, centerContent=True):
        super(GenericGUI, self).__init__()
        
        self.inputD = {} # holds inputs to GUI
        # ==================== build parameters =======================================
        self.NextRowNumber = 0
        
        self.objectD = {}               # index=name, value=PyQt4 object
        self.input_widget_by_nameD = {} # index=name, value=tuple(widgetObj, typeDesc)
        self.english_unitsD = {}        # index=name, value=units (e.g. psia, lbf, in, etc.)
        self.selection_textD = {}      # index=name, value=text of selection (used for radio buttons and list boxes)
        self.onChange_functionD = {}   # index=name, value=function to call on change

        # ====================================
        
        
        self.centralwidget=QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)
        
        if centerContent:
            self.vLayout = QtGui.QVBoxLayout(self.centralwidget)
            self.hLayout = QtGui.QHBoxLayout()

            self.grid = QtGui.QGridLayout()
            self.grid.setSpacing(0)

            # center the grid with stretch on both sides
            self.hLayout.addStretch(1)
            self.hLayout.addLayout(self.grid)
            self.hLayout.addStretch(1)

            self.vLayout.addLayout(self.hLayout)
            # push grid to the top of the window
            self.vLayout.addStretch(1)
        else:
            self.grid = QtGui.QGridLayout(self.centralwidget)
            self.grid.setSpacing(0)

            self.centralwidget.setLayout(self.grid)


        # ============  Add All Dialog Widgets Below Here ==========
    
    def print_internal_dicts(self):
        print '_'*20,'GenericDialog Dictionary Variables','_'*20
        keyL = self.input_widget_by_nameD.keys()
        keyL.sort( key=str.lower )
        for key in keyL:
            print 'self.input_widget_by_nameD key =',key
        print
        
    def onChange_function(self, widget=None, widget_name=''):
        """Override this function for any special processing when widgets change"""
        self.flag_changes() # mark has_changes flags
        
        if DEBUG_LEVEL > 2:
            print 'Original onChange_function'

    def get_IO_values(self):
        """
        Adds widget values to self.inputD  dictionary of all I/O variables
        """
        localD = {}
        
        for name in self.input_widget_by_nameD:
            # Look at the type of widget
            widget, widget_type = self.input_widget_by_nameD[name]
            
            # ======= do dimensionless QLineEdit objects here
            if widget_type in ['line_edit', 'english_line_edit']:
                localD[name] = str( widget.text() )
                #widget.setText( '%s'%val )
            
            elif widget_type == 'check_box':
                if widget.isChecked():
                    localD[name] = 'yes'
                else:
                    localD[name] = 'no'
                #print 'in get_IO_values, check_box value =',localD[name],'for',name
            
            elif widget_type == 'radio_btn_list':
                
                localD[name] = self.selection_textD[ name ]
                #print 'In get_IO_values',name,'=',localD[name]
            
            elif widget_type == 'list_box_list':
                localD[name] = self.selection_textD[ name ]
                #print 'In get_IO_values',name,'=',localD[name]
                
            elif widget_type == 'spin_box':
                localD[name] = str( widget.value() )
            
            elif widget_type == 'combo_box':
                localD[name] = str( widget.currentText() )
        
        self.inputD.update( localD )
        return self.inputD
        

    def set_IO_values( self ):
        # Iterate through all the I/O widgets
        for name,val in self.inputD.items():
            val = '%s'%val
            if DEBUG_LEVEL > 2:
                print 'set_IO_values %s = %s'%(name, val)
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
                
                elif widget_type == 'check_box':
                    widget.setChecked( val=='yes' )
                
                elif widget_type == 'radio_btn_list':
                    for i,radio in enumerate(widget): # NOTE... widget is actually a list of QRadioButton objects
                        if val == str( radio.text() ):
                            radio.setChecked(True)
                                
                elif widget_type == 'list_box_list':
                    for i in range( widget.count() ):
                        item = widget.item(i)
                        if str( item.text() ) == val:
                            widget.setItemSelected( item, True )
                            self.list_box_changed( '%s_list_box'%name )
                
                elif widget_type == 'spin_box':
                    try:
                        spin_val = int( val )
                        widget.setValue( spin_val )
                    except:
                        print 'ERROR setting Spin Box named',name
                        
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
        if DEBUG_LEVEL > 2:
            print 'Spin Box "%s" Changed To:'%spin_box_name, sbox_val
        
        self.onChange_function( widget=self.objectD[spin_box_name], widget_name=spin_box_name )

    def combo_box_changed(self, combo_box_name ):
        
        cbox_text = self.objectD[combo_box_name].currentText()
        if DEBUG_LEVEL > 2:
            print 'Combo Box "%s" Changed To:'%combo_box_name, cbox_text
        
        self.onChange_function( widget=self.objectD[combo_box_name], widget_name=combo_box_name )

    def line_edit_changed(self, lineEditName):
        
        ledit_text = str(self.objectD[lineEditName].text()).strip()
        if DEBUG_LEVEL > 2:
            print 'Line Edit "%s" Changed To:'%lineEditName, ledit_text
        
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
                
        self.onChange_function( widget=self.objectD[radio_btn_name], widget_name=radio_btn_name )

    def check_box_changed(self, check_box_name ):
        
        if DEBUG_LEVEL > 2:
            print 'Check Box "%s" changed'%check_box_name,'  checked=', self.objectD[check_box_name].isChecked()
        
        self.onChange_function( widget=self.objectD[check_box_name], widget_name=check_box_name )


    def add_some_vertical_space( self , parent=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        

        # Add some space in the middle ================================
        NRow = parent.get_next_row_number(advance_n=True)
        
        vbox = QVBoxLayout()
        vbox.addStretch()
        widget = QWidget()
        widget.setLayout(vbox)
        parent.grid.addWidget(widget, NRow, 0)

    def add_some_horizontal_space(self, col=10, stretch=1, parent=None, row=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        if row is None:
            NRow = max(0, parent.NextRowNumber-1) # add to current row
        else:
            NRow = int( row )
        
        hbox = QHBoxLayout()
        hbox.addStretch(stretch)
        widget = QWidget()
        widget.setLayout(hbox)
        
        parent.grid.addWidget(widget, NRow, col+1)
    
        

    def add_list_box(self, choicesL, 
                          name='isBell', init_val=3, layout=None,
                          advance_n=True, fulldesc='Nozzle Geometry', 
                          connect_function=None, text_font=ARIAL_10, col=0,
                          parent=None, fit_size_to_contents=True,  width=1, height=1):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
            # Need to change next row number by length of choicesL
            #if advance_n:
            #    for i in range(1, len(choicesL)):
            #        parent.get_next_row_number(advance_n)
        
        self.selection_textD[name] = ''
        
        listWidget = QListWidget()
        for i,choice in enumerate( choicesL ):
            item = QListWidgetItem(choice)
            listWidget.addItem(item)
            if i == init_val:
                #item.setChecked(True)
                listWidget.setItemSelected( item, True )
                self.selection_textD[name] = choice
        
        if fulldesc:
            vbox = QtGui.QVBoxLayout()
            lbl = QLabel(fulldesc, parent)
            lbl.setFont( text_font )
            vbox.addWidget( lbl )
            
            self.objectD['%s_listbox_label'%name] = lbl
            self.input_widget_by_nameD['%s_listbox_label'%name] = (lbl , 'label')
            
            vbox.addWidget( listWidget )
            grid_child = QtGui.QWidget()
            grid_child.setLayout(vbox)
            
            vbox.addStretch(1)
        else:
            grid_child = listWidget
        
        if layout is None:
            if width==1 and height==1:
                parent.grid.addWidget(grid_child,  NRow, col)
            else:
                parent.grid.addWidget(grid_child,  NRow, col, height, width)
                #parent.grid.addWidget(grid_child,  NRow, col, len(choicesL), 1)
        else:
            layout.addWidget( grid_child )
        
        self.objectD['%s_list_box'%name] = listWidget
        self.input_widget_by_nameD[name] = (listWidget , 'list_box_list')
        
        listWidget.itemClicked.connect( lambda: self.list_box_changed( '%s_list_box'%name ) ) 
            
        if fit_size_to_contents:
            listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            listWidget.setFixedSize(listWidget.sizeHintForColumn(0) + 2 * listWidget.frameWidth(), 
                                    listWidget.sizeHintForRow(0) * listWidget.count() + \
                                    2 * listWidget.frameWidth())
    

    def add_push_button(self, name='test', fulldesc='This is a Test',
                           advance_n=True, text_font=ARIAL_12B, col=0, 
                           connect_function=None, background='', pressed_bgrnd='',
                           parent=None, layout=None):        
                           # springgreen #00FF7F , lightgreen #90EE90 , powderblue #B0E0E6
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
                                            
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        btn = QPushButton(fulldesc, parent)
        btn.setFont( text_font )
        
        if background and pressed_bgrnd:
            btn.setStyleSheet("QPushButton { background-color:%s } "%background +\
                               "QPushButton:pressed { background-color: %s }"%pressed_bgrnd  )
        
        if layout is None:
            parent.grid.addWidget(btn,      NRow, col)
        else:
            layout.addWidget( btn )
        
        self.objectD['%s_push_btn'%name] = btn
        self.input_widget_by_nameD[name] = (btn , 'push_btn')
        
        if connect_function is not None:
            btn.clicked.connect( connect_function )


    def add_image(self, advance_n=True, path_to_image='', name='',
                   image_align='', col=0, width=1, height=1,
                   parent=None, layout=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        lbl = QLabel('', parent)
        pixmap = QPixmap(path_to_image) # should be absolute path
        lbl.setPixmap(pixmap)
        
        if layout is None:
            if width==1 and height==1:
                parent.grid.addWidget(lbl,  NRow, col)
            else:
                parent.grid.addWidget(lbl,  NRow, col, height, width)
        else:
            layout.addWidget( lbl )
        
        if image_align=='right':
            parent.grid.setAlignment(lbl, Qt.AlignRight )

        if name:
            self.objectD['%s_pixmap'%name] = lbl
            self.input_widget_by_nameD[name] = (lbl , 'pixmap')

    def add_label(self, advance_n=True, text='label text', name='',
                   text_align='', text_font=ARIAL_12, col=0, width=1,
                   parent=None, layout=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        lbl = QLabel(text, parent)
        lbl.setFont( text_font )
        
        if layout is None:
            if width==1:
                parent.grid.addWidget(lbl,  NRow, col)
            else:
                parent.grid.addWidget(lbl,  NRow, col, 1, width)
        else:
            layout.addWidget( lbl )
        
        if text_align=='right':
            parent.grid.setAlignment(lbl, Qt.AlignRight )

        if name:
            self.objectD['%s_label'%name] = lbl
            self.input_widget_by_nameD[name] = (lbl , 'label')

    def add_check_box(self, advance_n=True, text='label text', name='',
                   text_align='', text_font=ARIAL_12, col=0, width=1,
                   parent=None, layout=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        chkbx = QCheckBox(text, parent)
        chkbx.setFont( text_font )
        
        if layout is None:
            if width==1:
                parent.grid.addWidget(chkbx,  NRow, col)
            else:
                parent.grid.addWidget(chkbx,  NRow, col, 1, width)
        else:
            layout.addWidget( chkbx )
        
        if text_align=='right':
            parent.grid.setAlignment(chkbx, Qt.AlignRight )

        if name:
            self.objectD['%s_check_box'%name] = chkbx
            self.input_widget_by_nameD[name] = (chkbx , 'check_box')
            
        chkbx.stateChanged.connect( lambda: self.check_box_changed( '%s_check_box'%name ) )   


    def add_radio_btns(self, choicesL, 
                          name='isBell', init_val=3, layout=None,
                          advance_n=True, fulldesc='Nozzle Geometry', 
                          text_font=ARIAL_10, col=0, parent=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
                                            
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
            # Need to change next row number by length of choicesL
            if advance_n:
                for i in range(1, len(choicesL)):
                    parent.get_next_row_number(advance_n)
        
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
        
        if layout is None:
            parent.grid.addWidget(groupBox,      NRow, col, len(choicesL), 1)
        else:
            layout.addWidget( groupBox )
        
        self.objectD['%s_radio_group_box'%name] = radio_btnL
        self.input_widget_by_nameD[name] = (radio_btnL , 'radio_btn_list')
    
    

    def add_spin_box(self, name='Number', n_min=1, n_max=99, init_val=1,
                       advance_n=True, fulldesc='Number of Engines', 
                       text_align='right', text_font=ARIAL_10, col=0, width=120,
                       parent=None, layout=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
                            
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        
        lbl = QLabel("    %s "%fulldesc, parent)
        lbl.setFont( text_font )
        
        spin_box =  QSpinBox(parent)    
        spin_box.setFont( text_font )
        spin_box.setFixedWidth( width )
        spin_box.setRange( n_min, n_max)
        spin_box.setValue( init_val )
        
        if layout is None:
            parent.grid.addWidget(lbl,      NRow, col)
        else:
            layout.addWidget( lbl )
            
        hbox = QHBoxLayout()
        hbox.addWidget(spin_box)
        hbox.addStretch(1)
        widget = QWidget()
        widget.setLayout(hbox)
        if layout is None:
            parent.grid.addWidget(widget , NRow, col+1)
            if text_align=='right':
                parent.grid.setAlignment(lbl, Qt.AlignRight )
        else:
            layout.addWidget( widget )
        
        
        self.objectD['%s_spin_box'%name] = spin_box 
        self.input_widget_by_nameD[name] = (spin_box , 'spin_box')
            
        spin_box.valueChanged.connect( lambda: self.spin_box_changed( '%s_spin_box'%name ) )   

    

    def add_combo_box( self, choicesL, index_init=0, name='cycle_desc',
                        advance_n=True, fulldesc='Select Engine Cycle', 
                        text_align='right', text_font=ARIAL_10, col=0, width=100,
                        parent=None, layout=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        
        lbl = QLabel("    %s "%fulldesc, parent)
        combo_box = QComboBox(parent)    
        lbl.setFont( text_font )
        combo_box.setFont( text_font )
        
        self.objectD['%s_combo_box'%name] = combo_box
        for choice in choicesL:
            combo_box.addItem(choice)
        combo_box.setCurrentIndex(index_init)
        if layout is None:
            parent.grid.addWidget(lbl,      NRow, col)
        else:
            layout.addWidget( lbl )
        
        
            
        hbox = QHBoxLayout()
        hbox.addWidget(combo_box)
        hbox.addStretch(1)
        widget = QWidget()
        widget.setLayout(hbox)
        
        if layout is None:
            parent.grid.addWidget(widget, NRow, col+1)
        
            if text_align=='right':
                parent.grid.setAlignment(lbl, Qt.AlignRight )
        else:
            layout.addWidget( widget )
        
        combo_box.setFixedWidth( width )
            
        combo_box.activated[str].connect( lambda: self.combo_box_changed( '%s_combo_box'%name ) )   
            
        self.input_widget_by_nameD[name] = (combo_box, 'combo_box')
    
    

    def add_hbox_lineEdit(self, advance_n=True, text_font=ARIAL_10, onChange_function=None,
                             name='ofcore', fulldesc='Core Mixture Ratio (O/F)',  col=0, width=1,
                             parent=None, layout=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)

        hbox = QHBoxLayout()

        lbl = QLabel(fulldesc, parent )
        lbl.setFont( text_font )
        hbox.addWidget(lbl)
        
        lineEdit = QLineEdit( parent )
        lineEdit.setFont( text_font )
        hbox.addWidget(lineEdit)
        hbox.addStretch(1)
        widget = QWidget()
        widget.setLayout(hbox)
        
        lineEdit.textEdited[str].connect(lambda: self.line_edit_changed('%s_lineEdit'%name))
        
        if layout is None:
            if width > 1:
                parent.grid.addWidget(widget, NRow, col, 1, width)
            else:
                parent.grid.addWidget(widget, NRow, col)
        else:
            layout.addWidget( widget )
        
        self.objectD['%s_lineEdit'%name] = lineEdit
        self.input_widget_by_nameD[name] = (lineEdit, 'line_edit')
    
        if onChange_function:
            self.onChange_functionD[name] = onChange_function
    

    def add_lineEdit(self, advance_n=True, text_font=ARIAL_10, onChange_function=None,
                                name='ofcore', fulldesc='Core Mixture Ratio (O/F)',  col=0, width=1,
                                parent=None, layout=None, fixed_width=100, validator=None):
                       
        # if parent is input, add widget to parent
        if parent is None:
            parent = self
        
        
        if layout is None:
            NRow = parent.get_next_row_number(advance_n)
        
        lbl = QLabel(fulldesc, parent )
        lbl.setFont( text_font )
        if layout is None:
            parent.grid.addWidget(lbl,      NRow, col)
            parent.grid.setAlignment(lbl, Qt.AlignRight )
        else:
            layout.addWidget( lbl )
            
        self.objectD['%s_lineEdit_label'%name] = lbl
        self.input_widget_by_nameD['%s_lineEdit_label'%name] = (lbl , 'label')
        
        lineEdit = QLineEdit( parent )
        lineEdit.setFont( text_font )
        if validator is not None:
            lineEdit.setValidator(validator)
        
        lineEdit.textEdited[str].connect(lambda: self.line_edit_changed('%s_lineEdit'%name))
        
        if layout is None:
            if width > 1:
                parent.grid.addWidget(lineEdit, NRow, col+1, 1, width)
            else:
                lineEdit.setFixedWidth( fixed_width )
                
                hbox = QHBoxLayout()
                hbox.addWidget(lineEdit)
                hbox.addStretch(1)
                widget = QWidget()
                widget.setLayout(hbox)
                
                parent.grid.addWidget(widget, NRow, col+1)
        else:
            layout.addWidget( lineEdit )
            if width <= 1:
                lineEdit.setFixedWidth( fixed_width )
        
        self.objectD['%s_lineEdit'%name] = lineEdit
        self.input_widget_by_nameD[name] = (lineEdit, 'line_edit')
    
        if onChange_function:
            self.onChange_functionD[name] = onChange_function
    
