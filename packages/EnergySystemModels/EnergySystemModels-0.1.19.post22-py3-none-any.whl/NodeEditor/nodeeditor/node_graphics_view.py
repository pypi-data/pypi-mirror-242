# -*- coding: utf-8 -*-
"""
A module containing `Graphics View` for NodeEditor
"""
from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from NodeEditor.nodeeditor.node_graphics_socket import QDMGraphicsSocket
from NodeEditor.nodeeditor.node_graphics_edge import QDMGraphicsEdge
from NodeEditor.nodeeditor.node_edge_dragging import EdgeDragging
from NodeEditor.nodeeditor.node_graphics_cutline import QDMCutLine
from NodeEditor.nodeeditor.utils import dumpException


MODE_NOOP = 1               #: Mode representing ready state
MODE_EDGE_DRAG = 2          #: Mode representing when we drag edge state
MODE_EDGE_CUT = 3           #: Mode representing when we draw a cutting edge

#: Distance when click on socket to enable `Drag Edge`
EDGE_DRAG_START_THRESHOLD = 50


DEBUG = False
DEBUG_MMB_SCENE_ITEMS = False
DEBUG_MMB_LAST_SELECTIONS = False


class QDMGraphicsView(QGraphicsView):
    """Class representing NodeEditor's `Graphics View`"""
    #: pyqtSignal emitted when cursor position on the `Scene` has changed
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, grScene:'QDMGraphicsScene', parent:'QWidget'=None):
        """
        :param grScene: reference to the :class:`~nodeeditor.node_graphics_scene.QDMGraphicsScene`
        :type grScene: :class:`~nodeeditor.node_graphics_scene.QDMGraphicsScene`
        :param parent: parent widget
        :type parent: ``QWidget``

        :Instance Attributes:

        - **grScene** - reference to the :class:`~nodeeditor.node_graphics_scene.QDMGraphicsScene`
        - **mode** - state of the `Graphics View`
        - **zoomInFactor**- ``float`` - zoom step scaling, default 1.25
        - **zoomClamp** - ``bool`` - do we clamp zooming or is it infinite?
        - **zoom** - current zoom step
        - **zoomStep** - ``int`` - the relative zoom step when zooming in/out
        - **zoomRange** - ``[min, max]``

        """
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDraggingRectangle = False

        # edge dragging
        self.dragging = EdgeDragging(self)

        # cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)

        self.last_scene_mouse_position = QPoint(0,0)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # listeners
        self._drag_enter_listeners = []
        self._drop_listeners = []


    def initUI(self):
        """Set up this ``QGraphicsView``"""
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        # enable dropping
        self.setAcceptDrops(True)

    def resetMode(self):
        """Helper function to re-set the grView's State Machine state to the default"""
        self.mode = MODE_NOOP

    def dragEnterEvent(self, event:QDragEnterEvent):
        """Trigger our registered `Drag Enter` events"""
        for callback in self._drag_enter_listeners: callback(event)

    def dropEvent(self, event:QDropEvent):
        """Trigger our registered `Drop` events"""
        for callback in self._drop_listeners: callback(event)

    def addDragEnterListener(self, callback:'function'):
        """
        Register callback for `Drag Enter` event

        :param callback: callback function
        """
        self._drag_enter_listeners.append(callback)

    def addDropListener(self, callback:'function'):
        """
        Register callback for `Drop` event

        :param callback: callback function
        """
        self._drop_listeners.append(callback)

    def mousePressEvent(self, event:QMouseEvent):
        """Dispatch Qt's mousePress event to corresponding function below"""
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event:QMouseEvent):
        """Dispatch Qt's mouseRelease event to corresponding function below"""
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPress(self, event:QMouseEvent):
        """When Middle mouse button was pressed"""

        item = self.getItemAtClick(event)

        # debug print out
        if DEBUG_MMB_SCENE_ITEMS:
            if isinstance(item, QDMGraphicsEdge):
                print("MMB DEBUG:", item.edge, "\n\t", item.edge.grEdge if item.edge.grEdge is not None else None)
                return

            if isinstance(item, QDMGraphicsSocket):
                print("MMB DEBUG:", item.socket, "socket_type:", item.socket.socket_type,
                      "has edges:", "no" if item.socket.edges == [] else "")
                if item.socket.edges:
                    for edge in item.socket.edges: print("\t", edge)
                return

        if DEBUG_MMB_SCENE_ITEMS and (item is None):
            print("SCENE:")
            print("  Nodes:")
            for node in self.grScene.scene.nodes: print("\t", node)
            print("  Edges:")
            for edge in self.grScene.scene.edges: print("\t", edge, "\n\t\tgrEdge:", edge.grEdge if edge.grEdge is not None else None)

            if event.modifiers() & Qt.CTRL:
                print("  Graphic Items in GraphicScene:")
                for item in self.grScene.items():
                    print('    ', item)

        if DEBUG_MMB_LAST_SELECTIONS and event.modifiers() & Qt.SHIFT:
            print("scene _last_selected_items:", self.grScene.scene._last_selected_items)
            return

        # faking events for enable MMB dragging the scene
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)



    def middleMouseButtonRelease(self, event:QMouseEvent):
        """When Middle mouse button was released"""
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)


    def leftMouseButtonPress(self, event:QMouseEvent):
        """When Left  mouse button was pressed"""

        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # if DEBUG: print("LMB Click on", item, self.debug_modifiers(event))

        # logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return


        if isinstance(item, QDMGraphicsSocket):
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.dragging.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.dragging.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            else:
                self.rubberBandDraggingRectangle = True

        super().mousePressEvent(event)


    def leftMouseButtonRelease(self, event:QMouseEvent):
        """When Left  mouse button was released"""

        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        try:
            # logic
            if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
                if event.modifiers() & Qt.ShiftModifier:
                    event.ignore()
                    fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                            Qt.LeftButton, Qt.NoButton,
                                            event.modifiers() | Qt.ControlModifier)
                    super().mouseReleaseEvent(fakeEvent)
                    return

            if self.mode == MODE_EDGE_DRAG:
                if self.distanceBetweenClickAndReleaseIsOff(event):
                    res = self.dragging.edgeDragEnd(item)
                    if res: return

            if self.mode == MODE_EDGE_CUT:
                self.cutIntersectingEdges()
                self.cutline.line_points = []
                self.cutline.update()
                QApplication.setOverrideCursor(Qt.ArrowCursor)
                self.mode = MODE_NOOP
                return


            if self.rubberBandDraggingRectangle:
                self.rubberBandDraggingRectangle = False
                current_selected_items = self.grScene.selectedItems()

                if current_selected_items != self.grScene.scene._last_selected_items:
                    if current_selected_items == []:
                        self.grScene.itemsDeselected.emit()
                    else:
                        self.grScene.itemSelected.emit()
                    self.grScene.scene._last_selected_items = current_selected_items

                return

            # otherwise deselect everything
            if item is None:
                self.grScene.itemsDeselected.emit()

        except: dumpException()

        super().mouseReleaseEvent(event)



    def rightMouseButtonPress(self, event:QMouseEvent):
        """When Right mouse button was pressed"""
        super().mousePressEvent(event)


    def rightMouseButtonRelease(self, event:QMouseEvent):
        """When Right mouse button was release"""

        ## cannot be because with dragging RMB we spawn Create New Node Context Menu
        ## However, you could use this if you want to cancel with RMB
        # if self.mode == MODE_EDGE_DRAG:
        #     self.dragging.edgeDragEnd(None)
        #     return

        super().mouseReleaseEvent(event)


    def mouseMoveEvent(self, event:QMouseEvent):
        """Overriden Qt's ``mouseMoveEvent`` handling Scene/View logic"""
        scenepos = self.mapToScene(event.pos())

        if self.mode == MODE_EDGE_DRAG:
            self.dragging.updateDestination(scenepos.x(), scenepos.y())

        if self.mode == MODE_EDGE_CUT and self.cutline is not None:
            self.cutline.line_points.append(scenepos)
            self.cutline.update()

        self.last_scene_mouse_position = scenepos

        self.scenePosChanged.emit( int(scenepos.x()), int(scenepos.y()) )

        super().mouseMoveEvent(event)


    def keyPressEvent(self, event:QKeyEvent):
        """
        .. note::
            This overriden Qt's method was used for handling key shortcuts, before we implemented propper
            ``QWindow`` with Actions and Menu. Still the commented code serves as an example how to handle
            key presses without Qt's framework for Actions and shortcuts. There can be also found an example
            how to solve the problem when Node does contain Text/LineEdit and we press `Delete`
            key (also serving to delete `Node`)

        :param event: Qt's Key event
        :type event: ``QKeyEvent``
        :return:
        """
        # Use this code below if you wanna have shortcuts in this widget.
        # You want to use this, when you don't have a window which handles these shortcuts for you

        # if event.key() == Qt.Key_Delete:
        #     if not self.editingFlag:
        #         self.deleteSelected()
        #     else:
        #         super().keyPressEvent(event)
        # elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
        #     self.grScene.scene.saveToFile("graph.json")
        # elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
        #     self.grScene.scene.loadFromFile("graph.json")
        # elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
        #     self.grScene.scene.history.undo()
        # elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
        #     self.grScene.scene.history.redo()
        # elif event.key() == Qt.Key_H:
        #     print("HISTORY:     len(%d)" % len(self.grScene.scene.history.history_stack),
        #           " -- current_step", self.grScene.scene.history.history_current_step)
        #     ix = 0
        #     for item in self.grScene.scene.history.history_stack:
        #         print("#", ix, "--", item['desc'])
        #         ix += 1
        # else:
        super().keyPressEvent(event)


    def cutIntersectingEdges(self):
        """Compare which `Edges` intersect with current `Cut line` and delete them safely"""
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            # @TODO: we could collect all touched nodes, and notify them once after all edges removed
            # we could cut 3 edges leading to a single nodeeditor this will notify it 3x
            # maybe we could use some Notifier class with methods collect() and dispatch()
            for edge in self.grScene.scene.edges.copy():
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()
        self.grScene.scene.history.storeHistory("Delete cutted edges", setModified=True)



    def deleteSelected(self):
        """Shortcut for safe deleting every object selected in the `Scene`."""
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()
        self.grScene.scene.history.storeHistory("Delete selected", setModified=True)



    def debug_modifiers(self, event):
        """Helper function get string if we hold Ctrl, Shift or Alt modifier keys"""
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out

    def getItemAtClick(self, event:QEvent) -> 'QGraphicsItem':
        """Return the object on which we've clicked/release mouse button

        :param event: Qt's mouse or key event
        :type event: ``QEvent``
        :return: ``QGraphicsItem`` which the mouse event happened or ``None``
        """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj


    def distanceBetweenClickAndReleaseIsOff(self, event:QMouseEvent) -> bool:
        """ Measures if we are too far from the last Mouse button click scene position.
        This is used for detection if we release too far after we clicked on a `Socket`

        :param event: Qt's mouse event
        :type event: ``QMouseEvent``
        :return: ``True`` if we released too far from where we clicked before
        """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq



    def wheelEvent(self, event:QWheelEvent):
        """overriden Qt's ``wheelEvent``. This handles zooming"""
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep


        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

