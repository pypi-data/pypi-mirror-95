from bisect import bisect_left
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QFont, QFontInfo, QBrush
from PyQt5.QtWidgets import QApplication

# Supports both / and \ - current system separator might not match the system the file came from
# so os.path.basename won't do
def strip_path(filename):
    p = filename.rfind("/")
    pbsl = filename.rfind("\\")
    if pbsl >= 0 and (p < 0 or pbsl > p):
        p = pbsl
    return filename[p+1:] if p >= 0 else filename

def top_die_file_name(die):
    if 'DW_AT_name' in die.attributes:
        source_name = die.attributes['DW_AT_name'].value.decode('utf-8', errors='ignore')
        return strip_path(source_name)
    elif 'DW_AT_decl_file' in die.attributes:
        val = die.attributes['DW_AT_decl_file'].value
        if val > 0:
            if die.cu._lineprogram is None:
                die.cu._lineprogram = die.dwarfinfo.line_program_for_CU(self.die.cu)
            return strip_path(die.cu._lineprogram.header.file_entry[val-1].name.decode('utf-8', errors='ignore'))
    return "(no name)"

def cu_sort_key(cu):
    return top_die_file_name(cu.get_top_DIE()).lower()

def die_sort_key(die):
    if 'DW_AT_name' in die.attributes:
        name = die.attributes['DW_AT_name'].value.decode('utf-8', errors='ignore').lower()
    else:
        name = ''
    return (die.tag, name, die.offset)

#------------------------------------------------
# CU tree formatter
#------------------------------------------------    

# Some additional data for every DIE
def decorate_die(die, i):
    die._i = i
    die._children = None
    return die

def load_children(parent_die, sort):
    # Load and cache child DIEs in the parent DIE, if necessary
    # Assumes the check if the DIE has children has been already performed
    if '_children' not in dir(parent_die) or parent_die._children is None:
        # TODO: wait cursor here. It may cause disk I/O
        parent_die._children = [decorate_die(die, i) for (i, die) in enumerate(parent_die.iter_children())]    
        if sort:
            parent_die._children.sort(key = die_sort_key)
            for (i, die) in enumerate(parent_die._children):
                die._i = i

class DWARFTreeModel(QAbstractItemModel):
    def __init__(self, di, prefix, sortcus, sortdies):
        QAbstractItemModel.__init__(self)
        self.prefix = prefix
        self.top_dies = [decorate_die(CU.get_top_DIE(), i) for (i, CU) in enumerate(di._CUs)]
        self.highlight_condition = None
        fi = QFontInfo(QApplication.font())
        self.bold_font = QFont(fi.family(), fi.pointSize(), QFont.Bold)
        self.blue_brush = QBrush(Qt.GlobalColor.blue)
        self.sortcus = sortcus
        self.sortdies = sortdies

    # Qt callbacks. QTreeView supports progressive loading, as long as you feed it the "item has children" bit in advance

    def index(self, row, col, parent):
        if parent.isValid():
            parent_die = parent.internalPointer()
            # print("child of %s" % parent_die.tag)
            load_children(parent_die, self.sortdies)
            return self.createIndex(row, col, parent_die._children[row])
        else:
            return self.createIndex(row, col, self.top_dies[row])
        return QModelIndex()

    def flags(self, index):
        f = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.isValid() and not index.internalPointer().has_children:
            f = f | Qt.ItemNeverHasChildren
        return f

    def hasChildren(self, index):
        return not index.isValid() or index.internalPointer().has_children

    def rowCount(self, parent):
        if parent.isValid():
            parent_die = parent.internalPointer()
            # print('rcount of %s' % parent_die.tag)
            if not parent_die.has_children: # Legitimately nothing
                return 0
            else:
                load_children(parent_die, self.sortdies)
                return len(parent_die._children)
        else:
            return len(self.top_dies)

    def columnCount(self, parent):
        return 1

    def parent(self, index):
        if index.isValid():
            parent = index.internalPointer().get_parent()
            if parent:
                return self.createIndex(parent._i, 0, parent)
        return QModelIndex()

    def data(self, index, role):
        die = index.internalPointer()
        if role == Qt.DisplayRole:
            if die.tag == 'DW_TAG_compile_unit' or die.tag == 'DW_TAG_partial_unit': # CU/top die: return file name
                return top_die_file_name(die)
            else: # Return tag, with name if possible
                s = die.tag if self.prefix or not str(die.tag).startswith('DW_TAG_') else die.tag[7:]
                if 'DW_AT_name' in die.attributes:
                    s += ": " + die.attributes['DW_AT_name'].value.decode('utf-8', errors='ignore')
                return s
        elif role == Qt.ToolTipRole:
            if die.tag == 'DW_TAG_compile_unit' or die.tag == 'DW_TAG_partial_unit':
                return die.attributes['DW_AT_name'].value.decode('utf-8', errors='ignore')
        elif role == Qt.ForegroundRole and self.highlight_condition and self.highlight_condition(die):
            return self.blue_brush
        elif role == Qt.FontRole and self.highlight_condition and self.highlight_condition(die):
            return self.bold_font

    # The rest is not Qt callbacks

    def highlight(self, condition):
        self.highlight_condition = condition
        self.dataChanged.emit(self.createIndex(0, 0, self.top_dies[0]), self.createIndex(len(self.top_dies)-1, 0, self.top_dies[-1]), (Qt.ForegroundRole, Qt.FontRole))

    def set_prefix(self, prefix):
        if prefix != self.prefix:
            self.prefix = prefix
            self.dataChanged.emit(
                self.createIndex(0, 0, self.top_dies[0]),
                self.createIndex(len(self.top_dies)-1, 0, self.top_dies[-1]))    

    # returns the model index of the selection
    def set_sortcus(self, sortcus, sel):
        if sortcus != self.sortcus:
            sel_die = sel.internalPointer()
            self.beginResetModel()
            self.sortcus = sortcus
            #Resort the CUs, reload the top_dies
            di = self.top_dies[0].dwarfinfo
            sort_key = cu_sort_key if self.sortcus else lambda cu: cu.cu_offset
            di._CUs.sort(key = sort_key)
            for (i, cu) in enumerate(di._CUs):
                cu._i = i
                self.top_dies[i] = cu.get_top_DIE() # Already decorated, but the index is off
                self.top_dies[i]._i = i
            # Reload
            self.endResetModel()
            if sel_die.get_parent(): # Not a top level
                return sel
            else:
                return self.createIndex(0, sel_die._i, sel_die)

    def set_sortdies(self, sortdies):
        if sortdies != self.sortdies:
            self.sortdies = sortdies
            self.beginResetModel()
            for (i, die) in enumerate(self.top_dies):
                # Fragile! We invalidate the children in the decorated DIEs in the CU DIE cache
                # To force reloading and sorting
                for top_die in self.top_dies:
                    for die in top_die.cu._dielist:
                        die._children = None
            self.endResetModel()
            return self.createIndex(0, 0, self.top_dies[0])

    # Identifier for the current tree node that you can navigate to
    # For the back-forward logic
    # Specifically, (cu, offset within the info section)
    def get_navitem(self, index):
        die = index.internalPointer()
        return (die.cu, die.offset)

    # navitem is (CU, offset within the info section)
    # returns an index within the tree
    def index_for_navitem(self, navitem):
        target_cu, target_offset = navitem
        # Random access is a tricky proposition in the current version. Parse the whole CU.
        for die in target_cu.iter_DIEs():
            pass

        i = bisect_left(target_cu._diemap, target_offset)
        target_die = target_cu._dielist[i]
        return self.index_for_die(target_die)

    # Takes a die that might not have an _i
    # Restores the _i
    # Assumes all parent DIEs of the current one are already parsed
    # and cached in the CU, so get_parent will always return a valid parent DIE
    def index_for_die(self, die):
        if '_i' in dir(die): # DIE already iterated over
            return self.createIndex(die._i, 0, die)
        else: # Found the DIE, but the tree was never opened this deep. Read the tree along the path to the target DIE
            index = False
            while '_i' not in dir(die):
                parent_die = die.get_parent()
                load_children(parent_die, self.sortdies) # This will populate the _i in all children of parent_die, including die
                if not index: # After the first iteration, the one in the direct parent of target_die, target_die will have _i
                    index = self.createIndex(die._i, 0, die)
                die = parent_die
            return index

    # Returns the index of the found item, or False
    # start_pos is the index of the current item, or an invalid one
    # cond is a condition function
    # cu_cond is the same for CUs - hook for find by IP
    def find(self, start_pos, cond, cu_cond = False):
        have_start_pos = start_pos.isValid()
        if have_start_pos: # Searching from a specific position, with wrap-around
            start_die = start_pos.internalPointer()
            start_die_offset = start_die.offset # In the current die, before the next one
            start_cu = start_die.cu
            start_cu_offset = start_cu.cu_offset
            cu = start_cu
            wrapped = False
        else:
            cu = self.top_dies[0].cu

        while True:
            cu_offset = cu.cu_offset
            # Parse all DIEs in the current CU
            if cu_cond(cu) if cu_cond else True:
                for die in cu.iter_DIEs():
                    # Quit condition with search from position - quit once we go past the starting position after the wrap
                    if cu_offset >= start_cu_offset and die.offset > start_die_offset and wrapped:
                        break
                    if (not have_start_pos or cu_offset != start_cu_offset or (not wrapped and die.offset > start_die_offset)) and cond(die):
                        return self.index_for_die(die)

            # We're at the end of the CU. What next?
            if cu._i < len(self.top_dies) - 1: # More CUs to scan
                cu = self.top_dies[cu._i + 1].cu
            elif have_start_pos and not wrapped: # Scanned the last CU, wrap around
                cu = self.top_dies[0].cu
                wrapped = True
            else:
                break

        return False

# Highlighter function(s)
def has_code_location(die):
    return 'DW_AT_low_pc' in die.attributes or 'DW_AT_ranges' in die.attributes

