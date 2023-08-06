import time
import json

from PySide2.QtCore import Qt, QPointF, QPoint, QRectF, QSizeF, Signal, QTimer
from PySide2.QtGui import QPainter, QPen, QColor, QKeySequence, QTabletEvent, QImage, QGuiApplication, QFont
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QShortcut, QMenu, QGraphicsItem, QUndoStack

from .Flow import Flow
from .FlowCommands import MoveComponents_Command, PlaceNode_Command, \
    PlaceDrawing_Command, RemoveComponents_Command, ConnectPorts_Command, Paste_Command, FlowUndoCommand
from .FlowViewProxyWidget import FlowViewProxyWidget
from .FlowViewStylusModesWidget import FlowViewStylusModesWidget
from .FlowSessionThreadInterface import FlowSessionThreadInterface
from .FlowViewZoomWidget import FlowViewZoomWidget
from .Node import Node
from .NodeObjPort import NodeObjPort
from .node_selection_widget.PlaceNodeWidget import PlaceNodeWidget
from .NodeItem import NodeItem
from .PortItem import PortItemPin, PortItem
from .Connection import Connection, DataConnection
from .ConnectionItem import default_cubic_connection_path, ConnectionItem, DataConnectionItem, ExecConnectionItem
from .DrawingObject import DrawingObject
from .InfoMsgs import InfoMsgs
from .RC import PortObjPos
from .RC import FlowVPUpdateMode as VPUpdateMode


class FlowView(QGraphicsView):
    """Manages the GUI of flows"""

    nodes_selection_changed = Signal(list)
    node_placed = Signal(Node)

    create_node_request = Signal(object, dict)
    remove_node_request = Signal(Node)

    check_connection_validity_request = Signal(NodeObjPort, NodeObjPort)
    connect_request = Signal(NodeObjPort, NodeObjPort)

    get_nodes_config_request = Signal(list)
    get_connections_config_request = Signal(list)
    get_flow_config_data_request = Signal()

    viewport_update_mode_changed = Signal(str)


    def __init__(self, session, script, flow, config=None, flow_size: list = None, parent=None):
        super(FlowView, self).__init__(parent=parent)


        # UNDO/REDO
        self._undo_stack = QUndoStack(self)
        self._undo_action = self._undo_stack.createUndoAction(self, 'undo')
        self._undo_action.setShortcuts(QKeySequence.Undo)
        self._redo_action = self._undo_stack.createRedoAction(self, 'redo')
        self._redo_action.setShortcuts(QKeySequence.Redo)

        # SHORTCUTS
        self._init_shortcuts()

        # GENERAL ATTRIBUTES
        self.session = session
        self.script = script
        self.flow: Flow = flow
        self.node_items: dict = {}  # {Node: NodeItem}
        self.node_items__cache: dict = {}
        self.connection_items: dict = {}  # {Connection: ConnectionItem}
        self.connection_items__cache: dict = {}

        # PRIVATE FIELDS
        self._temp_config_data = None
        self._selected_pin: PortItemPin = None
        self._dragging_connection = False
        self._temp_connection_ports = None
        self.mouse_event_taken = False  # for stylus - see tablet event
        self._showing_framerate = False
        self._last_mouse_move_pos: QPointF = None
        self._node_place_pos = QPointF()
        self._left_mouse_pressed_in_flow = False
        self._right_mouse_pressed_in_flow = False
        self._mouse_press_pos: QPointF = None
        self._auto_connection_pin = None  # stores the gate that we may try to auto connect to a newly placed NI
        self._panning = False
        self._pan_last_x = None
        self._pan_last_y = None
        self._current_scale = 1
        self._total_scale_div = 1

        # CONNECTIONS TO FLOW
        self.create_node_request.connect(self.flow.create_node)
        self.remove_node_request.connect(self.flow.remove_node)
        self.node_placed.connect(self.flow.node_placed)
        self.check_connection_validity_request.connect(self.flow.check_connection_validity)
        self.get_nodes_config_request.connect(self.flow.generate_nodes_config)
        self.get_connections_config_request.connect(self.flow.generate_connections_config)
        self.get_flow_config_data_request.connect(self.flow.generate_config_data)

        # CONNECTIONS FROM FLOW
        self.flow.node_added.connect(self.add_node)
        self.flow.node_removed.connect(self.remove_node)
        self.flow.connection_added.connect(self.add_connection)
        self.flow.connection_removed.connect(self.remove_connection)
        self.flow.connection_request_valid.connect(self.connection_request_valid)
        # self.flow.nodes_config_generated.connect(self._abstract_nodes_config_generated)
        # self.flow.connections_config_generated.connect(self._abstract_connections_config_generated)

        # SESSION THREAD
        if self.session.threaded:
            self.thread_interface = FlowSessionThreadInterface()
            self.thread_interface.moveToThread(self.session.thread())

        # SETTINGS
        self.vp_update_mode: VPUpdateMode = VPUpdateMode.SYNC

        # CREATE UI
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        if flow_size is None:
            scene.setSceneRect(0, 0, 10 * self.width(), 10 * self.height())
        else:
            scene.setSceneRect(0, 0, flow_size[0], flow_size[1])

        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        scene.selectionChanged.connect(self._scene_selection_changed)
        self.setAcceptDrops(True)

        self.centerOn(QPointF(self.viewport().width() / 2, self.viewport().height() / 2))

        # PLACE NODE WIDGET
        self._place_node_widget_proxy = FlowViewProxyWidget(self)
        self._place_node_widget_proxy.setZValue(1000)
        self._place_node_widget = PlaceNodeWidget(self, self.session.nodes)
        self._place_node_widget_proxy.setWidget(self._place_node_widget)
        self.scene().addItem(self._place_node_widget_proxy)
        self.hide_place_node_widget()

        # ZOOM WIDGET
        self._zoom_proxy = FlowViewProxyWidget(self)
        self._zoom_proxy.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        self._zoom_proxy.setZValue(1001)
        self._zoom_widget = FlowViewZoomWidget(self)
        self._zoom_proxy.setWidget(self._zoom_widget)
        self.scene().addItem(self._zoom_proxy)
        self.set_zoom_proxy_pos()

        # STYLUS
        self.stylus_mode = ''
        self._current_drawing = None
        self._drawing = False
        self.drawings = []
        self._stylus_modes_proxy = FlowViewProxyWidget(self)
        self._stylus_modes_proxy.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        self._stylus_modes_proxy.setZValue(1001)
        self._stylus_modes_widget = FlowViewStylusModesWidget(self)
        self._stylus_modes_proxy.setWidget(self._stylus_modes_widget)
        self.scene().addItem(self._stylus_modes_proxy)
        self.set_stylus_proxy_pos()
        self.setAttribute(Qt.WA_TabletTracking)

        # # TOUCH GESTURES
        # recognizer = PanGestureRecognizer()
        # pan_gesture_id = QGestureRecognizer.registerRecognizer(recognizer) <--- CRASH HERE
        # self.grabGesture(pan_gesture_id)

        # DESIGN
        self.session.design.flow_theme_changed.connect(self._theme_changed)

        # FRAMERATE TRACKING
        self.num_frames = 0
        self.framerate = 0
        self.framerate_timer = QTimer(self)
        self.framerate_timer.timeout.connect(self._on_framerate_timer_timeout)

        # self.show_framerate(m_sec_interval=100)  # for testing

        # CONFIG
        if config is not None:
            # viewport update mode
            vpum = config['viewport update mode']
            if vpum == 'sync':  # vpum == VPUpdateMode.SYNC
                # self.vp_update_mode = VPUpdateMode.SYNC
                self.set_viewport_update_mode('sync')
            elif vpum == 'async':  # vpum == VPUpdateMode.ASYNC
                # self.vp_update_mode = VPUpdateMode.ASYNC
                self.set_viewport_update_mode('async')

            if 'drawings' in config:  # not all (old) project files have drawings arr
                self.place_drawings_from_config(config['drawings'])

            if 'view size' in config:
                self.setSceneRect(0, 0, config['view size'][0], config['view size'][1])

            self._undo_stack.clear()


    def show_framerate(self, show: bool = True, m_sec_interval: int = 1000):
        self._showing_framerate = show
        self.framerate_timer.setInterval(m_sec_interval)
        self.framerate_timer.start()

    def _on_framerate_timer_timeout(self):
        self.framerate = self.num_frames
        self.num_frames = 0

    def _init_shortcuts(self):
        place_new_node_shortcut = QShortcut(QKeySequence('Shift+P'), self)
        place_new_node_shortcut.activated.connect(self._place_new_node_by_shortcut)
        move_selected_components_left_shortcut = QShortcut(QKeySequence('Shift+Left'), self)
        move_selected_components_left_shortcut.activated.connect(self._move_selected_comps_left)
        move_selected_components_up_shortcut = QShortcut(QKeySequence('Shift+Up'), self)
        move_selected_components_up_shortcut.activated.connect(self._move_selected_comps_up)
        move_selected_components_right_shortcut = QShortcut(QKeySequence('Shift+Right'), self)
        move_selected_components_right_shortcut.activated.connect(self._move_selected_comps_right)
        move_selected_components_down_shortcut = QShortcut(QKeySequence('Shift+Down'), self)
        move_selected_components_down_shortcut.activated.connect(self._move_selected_comps_down)
        select_all_shortcut = QShortcut(QKeySequence('Ctrl+A'), self)
        select_all_shortcut.activated.connect(self.select_all)
        copy_shortcut = QShortcut(QKeySequence.Copy, self)
        copy_shortcut.activated.connect(self._copy)
        cut_shortcut = QShortcut(QKeySequence.Cut, self)
        cut_shortcut.activated.connect(self._cut)
        paste_shortcut = QShortcut(QKeySequence.Paste, self)
        paste_shortcut.activated.connect(self._paste)

        undo_shortcut = QShortcut(QKeySequence.Undo, self)
        undo_shortcut.activated.connect(self._undo_activated)
        redo_shortcut = QShortcut(QKeySequence.Redo, self)
        redo_shortcut.activated.connect(self._redo_activated)

    def _theme_changed(self, t):
        # TODO: repaint background. how?
        self.viewport().update()

    def _scene_selection_changed(self):
        self.nodes_selection_changed.emit(self.selected_nodes())

    def contextMenuEvent(self, event):
        QGraphicsView.contextMenuEvent(self, event)
        # in the case of the menu already being shown by a widget under the mouse, the event is accepted here
        if event.isAccepted():
            return

        for i in self.items(event.pos()):
            if isinstance(i, NodeItem):
                ni: NodeItem = i
                menu: QMenu = ni.get_context_menu()
                menu.exec_(event.globalPos())
                event.accept()

    def _push_undo(self, cmd: FlowUndoCommand):
        self._undo_stack.push(cmd)
        cmd.activate()

    def _undo_activated(self):
        """Triggered by ctrl+z"""
        self._undo_stack.undo()
        self.viewport().update()

    def _redo_activated(self):
        """Triggered by ctrl+y"""
        self._undo_stack.redo()
        self.viewport().update()

    def mousePressEvent(self, event):
        # InfoMsgs.write('mouse press event received, point:', event.pos())

        # to catch tablet events (for some reason, it results in a mousePrEv too)
        if self.mouse_event_taken:
            self.mouse_event_taken = False
            return

        QGraphicsView.mousePressEvent(self, event)

        # don't process the event if it has been processed by a specific component in the scene
        # this includes node items, node port pins, proxy widgets etc.
        if self.mouse_event_taken:
            self.mouse_event_taken = False
            return

        if event.button() == Qt.LeftButton:
            if self._place_node_widget_proxy.isVisible():
                self.hide_place_node_widget()

        elif event.button() == Qt.RightButton:
            self._right_mouse_pressed_in_flow = True
            event.accept()

        self._mouse_press_pos = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):

        QGraphicsView.mouseMoveEvent(self, event)

        if self._right_mouse_pressed_in_flow:    # PAN

            if not self._panning:
                self._panning = True
                self._pan_last_x = event.x()
                self._pan_last_y = event.y()

            self.pan(event.pos())
            event.accept()

        self._last_mouse_move_pos = self.mapToScene(event.pos())

        if self._dragging_connection:
            self.viewport().repaint()

    def mouseReleaseEvent(self, event):
        # there might be a proxy widget meant to receive the event instead of the flow
        QGraphicsView.mouseReleaseEvent(self, event)

        node_item_at_event_pos = None
        for item in self.items(event.pos()):
            if isinstance(item, NodeItem):
                node_item_at_event_pos = item

        if self.mouse_event_taken:
            self.mouse_event_taken = False
            self.viewport().repaint()
            return

        elif self._panning:
            self._panning = False

        elif event.button() == Qt.RightButton:
            self._right_mouse_pressed_in_flow = False
            if self._mouse_press_pos == self._last_mouse_move_pos:

                self._place_node_widget.reset_list()
                self.show_place_node_widget(event.pos())
                return


        if self._dragging_connection:

            # connection dropped over port item
            port_items = {i: isinstance(i, PortItem) for i in self.items(event.pos())}
            if any(port_items.values()):

                p_i = list(port_items.keys())[list(port_items.values()).index(True)]  # gets the first PortItem

                # the validity of the connection is checked in connect_node_ports__cmd
                self.connect_node_ports__cmd(
                    self._selected_pin.port,
                    p_i.port
                )

            # connection dropped above NodeItem -> auto connect
            elif node_item_at_event_pos:
                # find node item
                ni_under_drop = None
                for item in self.items(event.pos()):
                    if isinstance(item, NodeItem):
                        ni_under_drop = item
                        self.auto_connect(self._selected_pin.port, ni_under_drop.node)
                        break

            # connection dropped somewhere else -> show node choice widget
            else:
                self._auto_connection_pin = self._selected_pin
                self.show_place_node_widget(event.pos())

            self._dragging_connection = False
            self._selected_pin = None

        # if event.button() == Qt.LeftButton:
        #     self._left_mouse_pressed_in_flow = False
        elif event.button() == Qt.RightButton:
            self._right_mouse_pressed_in_flow = False

        self.viewport().repaint()

    def keyPressEvent(self, event):
        QGraphicsView.keyPressEvent(self, event)

        if event.isAccepted():
            return

        if event.key() == Qt.Key_Escape:  # do I need that... ?
            self.clearFocus()
            self.setFocus()
            return True

        elif event.key() == Qt.Key_Delete:
            self.remove_selected_components__cmd()

    def wheelEvent(self, event):

        # ZOOM
        if event.modifiers() == Qt.CTRL and event.angleDelta().x() == 0:
            self.zoom(event.pos(), self.mapToScene(event.pos()), event.angleDelta().y())
            event.accept()
            return True

        QGraphicsView.wheelEvent(self, event)

    def tabletEvent(self, event):
        """tabletEvent gets called by stylus operations.
        LeftButton: std, no button pressed
        RightButton: upper button pressed"""

        # if in edit mode and not panning or starting a pan, pass on to std mouseEvent handlers above
        if self.stylus_mode == 'edit' and not self._panning and not \
                (event.type() == QTabletEvent.TabletPress and event.button() == Qt.RightButton):
            return  # let the mousePress/Move/Release-Events handle it

        scaled_event_pos: QPointF = event.posF()/self._current_scale

        if event.type() == QTabletEvent.TabletPress:
            self.mouse_event_taken = True

            if event.button() == Qt.LeftButton:
                if self.stylus_mode == 'comment':
                    view_pos = self.mapToScene(self.viewport().pos())
                    new_drawing = self._create_and_place_drawing__cmd(
                        view_pos + scaled_event_pos,
                        config={**self._stylus_modes_widget.get_pen_settings(), 'viewport pos': view_pos}
                    )
                    self._current_drawing = new_drawing
                    self._drawing = True
            elif event.button() == Qt.RightButton:
                self._panning = True
                self._pan_last_x = event.x()
                self._pan_last_y = event.y()

        elif event.type() == QTabletEvent.TabletMove:
            self.mouse_event_taken = True
            if self._panning:
                self.pan(event.pos())

            elif event.pointerType() == QTabletEvent.Eraser:
                if self.stylus_mode == 'comment':
                    for i in self.items(event.pos()):
                        if isinstance(i, DrawingObject):
                            self.remove_drawing(i)
                            break
            elif self.stylus_mode == 'comment' and self._drawing:
                if self._current_drawing.append_point(scaled_event_pos):
                    self._current_drawing.stroke_weights.append(event.pressure())
                self._current_drawing.update()
                self.viewport().update()

        elif event.type() == QTabletEvent.TabletRelease:
            if self._panning:
                self._panning = False
            if self.stylus_mode == 'comment' and self._drawing:
                InfoMsgs.write('drawing obj finished')
                self._current_drawing.finish()
                self._current_drawing = None
                self._drawing = False

    # https://forum.qt.io/topic/121473/qgesturerecognizer-registerrecognizer-crashes-using-pyside2
    #
    # def event(self, event) -> bool:
    #     # if event.type() == QEvent.Gesture:
    #     #     if event.gesture(PanGesture) is not None:
    #     #         return self.pan_gesture(event)
    #
    #     return QGraphicsView.event(self, event)
    #
    # def pan_gesture(self, event: QGestureEvent) -> bool:
    #     pan: PanGesture = event.gesture(PanGesture)
    #     print(pan)
    #     return True

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()

    # def dropEvent(self, event):
    #     text = event.mimeData().text()
    #     item: QListWidgetItem = event.mimeData()
    #     InfoMsgs.write('drop received in Flow:', text)
    #
    #     j_obj = None
    #     type = ''
    #     try:
    #         j_obj = json.loads(text)
    #         type = j_obj['type']
    #     except Exception:
    #         return
    #
    #     if type == 'variable':
    #         self.show_node_choice_widget(event.pos(),  # only show get_var and set_var nodes
    #                                      [n for n in self.session.nodes if find_type_in_object(n, GetVar_Node) or
    #                                       find_type_in_object(n, SetVar_Node)])

    # PAINTING
    def drawBackground(self, painter, rect):

        painter.setBrush(self.session.design.flow_theme.flow_background_brush)
        painter.drawRect(rect.intersected(self.sceneRect()))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.sceneRect())

        if self.session.design.performance_mode == 'pretty':
            theme = self.session.design.flow_theme
            if theme.flow_background_grid and self._current_scale >= 0.7:
                if theme.flow_background_grid[0] == 'points':
                    color = theme.flow_background_grid[1]
                    pen_width = theme.flow_background_grid[2]
                    diff_x = theme.flow_background_grid[3]
                    diff_y = theme.flow_background_grid[4]

                    pen = QPen(color)
                    pen.setWidthF(pen_width)
                    painter.setPen(pen)

                    for x in range(diff_x, self.sceneRect().toRect().width(), diff_x):
                        for y in range(diff_y, self.sceneRect().toRect().height(), diff_y):
                            painter.drawPoint(x, y)


        self.set_stylus_proxy_pos()  # has to be called here instead of in drawForeground to prevent lagging
        self.set_zoom_proxy_pos()

    def drawForeground(self, painter, rect):

        if self._showing_framerate:
            self.num_frames += 1
            pen = QPen(QColor('#A9D5EF'))
            pen.setWidthF(2)
            painter.setPen(pen)

            pos = self.mapToScene(10, 23)
            painter.setFont(QFont('Poppins', round(11 * self._total_scale_div)))
            painter.drawText(pos, "{:.2f}".format(self.framerate))


        # DRAW CURRENTLY DRAGGED CONNECTION
        if self._dragging_connection:
            pen = QPen('#101520')
            pen.setWidth(3)
            pen.setStyle(Qt.DotLine)
            painter.setPen(pen)

            pin_pos = self._selected_pin.get_scene_center_pos()
            spp = self._selected_pin.port
            cursor_pos = self._last_mouse_move_pos

            pos1 = pin_pos if spp.io_pos == PortObjPos.OUTPUT else cursor_pos
            pos2 = pin_pos if spp.io_pos == PortObjPos.INPUT else cursor_pos

            painter.drawPath(
                default_cubic_connection_path(pos1, pos2)
            )


        # DRAW SELECTED NIs BORDER
        for ni in self.selected_node_items():
            pen = QPen(self.session.design.flow_theme.flow_highlight_pen_color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            size_factor = 1.2
            x = ni.pos().x() - ni.boundingRect().width() / 2 * size_factor
            y = ni.pos().y() - ni.boundingRect().height() / 2 * size_factor
            w = ni.boundingRect().width() * size_factor
            h = ni.boundingRect().height() * size_factor
            painter.drawRoundedRect(x, y, w, h, 10, 10)


        # DRAW SELECTED DRAWINGS BORDER
        for p_o in self.selected_drawings():
            pen = QPen(QColor('#a3cc3b'))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            size_factor = 1.05
            x = p_o.pos().x() - p_o.width / 2 * size_factor
            y = p_o.pos().y() - p_o.height / 2 * size_factor
            w = p_o.width * size_factor
            h = p_o.height * size_factor
            painter.drawRoundedRect(x, y, w, h, 6, 6)
            painter.drawEllipse(p_o.pos().x(), p_o.pos().y(), 2, 2)

    def get_viewport_img(self) -> QImage:
        """Returns a clear image of the viewport"""

        self.hide_proxies()
        img = QImage(self.viewport().rect().width(), self.viewport().height(), QImage.Format_ARGB32)
        img.fill(Qt.transparent)

        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)
        self.render(painter, self.viewport().rect(), self.viewport().rect())
        self.show_proxies()
        return img

    def get_whole_scene_img(self) -> QImage:
        """Returns an image of the whole scene, scaled accordingly to current scale factor.
        Due to a bug this only works from the viewport position down and right, so the user has to scroll to
        the top left corner in order to get the full scene"""

        self.hide_proxies()
        img = QImage(self.sceneRect().width() / self._total_scale_div, self.sceneRect().height() / self._total_scale_div,
                     QImage.Format_RGB32)
        img.fill(Qt.transparent)

        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF()
        rect.setLeft(-self.viewport().pos().x())
        rect.setTop(-self.viewport().pos().y())
        rect.setWidth(img.rect().width())
        rect.setHeight(img.rect().height())
        # rect is right... but it only renders from the viewport's point down-and rightwards, not from topleft (0,0) ...
        self.render(painter, rect, rect.toRect())
        self.show_proxies()
        return img

    # PROXY POSITIONS
    def set_zoom_proxy_pos(self):
        self._zoom_proxy.setPos(self.mapToScene(self.viewport().width() - self._zoom_widget.width(), 0))

    def set_stylus_proxy_pos(self):
        self._stylus_modes_proxy.setPos(
            self.mapToScene(self.viewport().width() - self._stylus_modes_widget.width() - self._zoom_widget.width(), 0))

    def hide_proxies(self):
        self._stylus_modes_proxy.hide()
        self._zoom_proxy.hide()

    def show_proxies(self):
        self._stylus_modes_proxy.show()
        self._zoom_proxy.show()

    # PLACE NODE WIDGET
    def show_place_node_widget(self, pos, nodes=None):
        """Opens the place node dialog in the scene."""

        # calculating position
        self._node_place_pos = self.mapToScene(pos)
        dialog_pos = QPoint(pos.x() + 1, pos.y() + 1)

        # ensure that the node_selection_widget stays in the viewport
        if dialog_pos.x() + self._place_node_widget.width() / self._total_scale_div > self.viewport().width():
            dialog_pos.setX(dialog_pos.x() - (
                    dialog_pos.x() + self._place_node_widget.width() / self._total_scale_div - self.viewport().width()))
        if dialog_pos.y() + self._place_node_widget.height() / self._total_scale_div > self.viewport().height():
            dialog_pos.setY(dialog_pos.y() - (
                    dialog_pos.y() + self._place_node_widget.height() / self._total_scale_div - self.viewport().height()))
        dialog_pos = self.mapToScene(dialog_pos)

        # open nodes dialog
        # the dialog emits 'node_chosen' which is connected to self.place_node,
        # so this all continues at self.place_node below
        self._place_node_widget.update_list(nodes if nodes is not None else self.session.nodes)
        self._place_node_widget.update_view()
        self._place_node_widget_proxy.setPos(dialog_pos)
        self._place_node_widget_proxy.show()
        self._place_node_widget.refocus()

    def hide_place_node_widget(self):
        self._place_node_widget_proxy.hide()
        self._place_node_widget.clearFocus()
        self._auto_connection_pin = None

    def _place_new_node_by_shortcut(self):  # Shift+P
        point_in_viewport = None
        selected_NIs = self.selected_node_items()
        if len(selected_NIs) > 0:
            x = selected_NIs[-1].pos().x() + 150
            y = selected_NIs[-1].pos().y()
            self._node_place_pos = QPointF(x, y)
            point_in_viewport = self.mapFromScene(QPoint(x, y))
        else:  # place in center
            viewport_x = self.viewport().width() / 2
            viewport_y = self.viewport().height() / 2
            point_in_viewport = QPointF(viewport_x, viewport_y).toPoint()
            self._node_place_pos = self.mapToScene(point_in_viewport)

        self._place_node_widget.reset_list()
        self.show_place_node_widget(point_in_viewport)

    # PAN
    def pan(self, new_pos):
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (new_pos.x() - self._pan_last_x))
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (new_pos.y() - self._pan_last_y))
        self._pan_last_x = new_pos.x()
        self._pan_last_y = new_pos.y()

    # ZOOM
    def zoom_in(self, amount):
        local_viewport_center = QPoint(self.viewport().width() / 2, self.viewport().height() / 2)
        self.zoom(local_viewport_center, self.mapToScene(local_viewport_center), amount)

    def zoom_out(self, amount):
        local_viewport_center = QPoint(self.viewport().width() / 2, self.viewport().height() / 2)
        self.zoom(local_viewport_center, self.mapToScene(local_viewport_center), -amount)

    def zoom(self, p_abs, p_mapped, angle):
        by = 0
        velocity = 2 * (1 / self._current_scale) + 0.5
        if velocity > 3:
            velocity = 3

        direction = ''
        if angle > 0:
            by = 1 + (angle / 360 * 0.1 * velocity)
            direction = 'in'
        elif angle < 0:
            by = 1 - (-angle / 360 * 0.1 * velocity)
            direction = 'out'
        else:
            by = 1

        scene_rect_width = self.mapFromScene(self.sceneRect()).boundingRect().width()
        scene_rect_height = self.mapFromScene(self.sceneRect()).boundingRect().height()

        if direction == 'in':
            if self._current_scale * by < 3:
                self.scale(by, by)
                self._current_scale *= by
        elif direction == 'out':
            if scene_rect_width * by >= self.viewport().size().width() and scene_rect_height * by >= self.viewport().size().height():
                self.scale(by, by)
                self._current_scale *= by

        w = self.viewport().width()
        h = self.viewport().height()
        wf = self.mapToScene(QPoint(w - 1, 0)).x() - self.mapToScene(QPoint(0, 0)).x()
        hf = self.mapToScene(QPoint(0, h - 1)).y() - self.mapToScene(QPoint(0, 0)).y()
        lf = p_mapped.x() - p_abs.x() * wf / w
        tf = p_mapped.y() - p_abs.y() * hf / h

        self.ensureVisible(lf, tf, wf, hf, 0, 0)

        target_rect = QRectF(QPointF(lf, tf),
                             QSizeF(wf, hf))
        self._total_scale_div = target_rect.width() / self.viewport().width()

        self.ensureVisible(target_rect, 0, 0)




    # NODES
    def create_node__cmd(self, node_class):
        self._push_undo(
            PlaceNode_Command(self, node_class, self._node_place_pos)
        )

    def add_node(self, node):

        # create item
        item: NodeItem = None

        if node in self.node_items__cache.keys():  # load from cache
            # print('using a cached item')
            item = self.node_items__cache[node]
            self._add_node_item(item)

        else:  # create new item
            item_config = node.init_config
            item = NodeItem(node, params=(self, self.session.design, item_config))
            node.item = item
            item.initialize()
            self.node_placed.emit(node)

            pos = None
            if item_config is not None:
                if 'pos x' in item_config:
                    pos = QPointF(item_config['pos x'], item_config['pos y'])
                elif 'position x' in item_config:  # backwards compatibility
                    pos = QPointF(item_config['position x'], item_config['position y'])
            else:
                pos = self._node_place_pos

            self._add_node_item(item, pos)

        # auto connect
        if self._auto_connection_pin:
            self.auto_connect(self._auto_connection_pin.port,
                              node)

    def _add_node_item(self, item: NodeItem, pos=None):
        self.node_items[item.node] = item

        self.scene().addItem(item)
        if pos:
            item.setPos(pos)

        # select new item
        self.clear_selection()
        item.setSelected(True)

    def remove_node(self, node):
        item = self.node_items[node]
        self._remove_node_item(item)
        del self.node_items[node]

    def _remove_node_item(self, item: NodeItem):
        # store item in case the remove action gets undone later
        self.node_items__cache[item.node] = item
        self.scene().removeItem(item)

    # CONNECTIONS
    def connect_node_ports__cmd(self, p1: NodeObjPort, p2: NodeObjPort):
        self._temp_connection_ports = (p1, p2)
        self.check_connection_validity_request.emit(p1, p2)

    def connection_request_valid(self, valid: bool):
        """
        Triggered after the abstract flow evaluated validity of pending connect request.
        This can also lead to a disconnect!
        """

        if valid:
            out, inp = self._temp_connection_ports
            if out.io_pos == PortObjPos.INPUT:
                out, inp = inp, out

            # remove forbidden connections
            if inp.type_ == 'data':
                for c in inp.connections:

                    if c.out == out:
                        # if the exact connection exists, we want to remove it by command
                        continue

                    self._push_undo(
                        ConnectPorts_Command(self, out=c.out, inp=inp)
                    )

            self._push_undo(
                ConnectPorts_Command(self, out=out, inp=inp)
            )

    def add_connection(self, c: Connection):

        item: ConnectionItem = None
        if c in self.connection_items__cache.keys():
            item = self.connection_items__cache[c]

        else:
            if isinstance(c, DataConnection):
                item = DataConnectionItem(c, self.session.design)
            else:
                item = ExecConnectionItem(c, self.session.design)



        self._add_connection_item(item)

    def _add_connection_item(self, item: ConnectionItem):
        self.connection_items[item.connection] = item
        self.scene().addItem(item)
        item.setZValue(10)
        # self.viewport().repaint()

    def remove_connection(self, c: Connection):
        item = self.connection_items[c]
        self._remove_connection_item(item)
        del self.connection_items[c]

    def _remove_connection_item(self, item: ConnectionItem):
        self.connection_items__cache[item.connection] = item
        self.scene().removeItem(item)

    def auto_connect(self, p: NodeObjPort, n: Node):
        if p.io_pos == PortObjPos.OUTPUT:
            for inp in n.inputs:
                if p.type_ == inp.type_:
                    # connect exactly once
                    self.connect_node_ports__cmd(p, inp)
                    return
        elif p.io_pos == PortObjPos.INPUT:
            for out in n.outputs:
                if p.type_ == out.type_:
                    # connect exactly once
                    self.connect_node_ports__cmd(p, out)
                    return

    # DRAWINGS
    def create_drawing(self, config=None) -> DrawingObject:
        """Creates and returns a new DrawingObject."""

        new_drawing = DrawingObject(self, config)
        return new_drawing

    def add_drawing(self, drawing_obj, posF=None):
        """Adds a DrawingObject to the scene."""

        self.scene().addItem(drawing_obj)
        if posF:
            drawing_obj.setPos(posF)
        self.drawings.append(drawing_obj)

    def add_drawings(self, drawings):
        """Adds a list of DrawingObjects to the scene."""

        for d in drawings:
            self.add_drawing(d)

    def remove_drawing(self, drawing):
        """Removes a drawing from the scene."""

        self.scene().removeItem(drawing)
        self.drawings.remove(drawing)

    def place_drawings_from_config(self, drawings_config: list, offset_pos=QPoint(0, 0)):
        """Creates and places drawings from drawings. The same list is returned by the config_data() method
        at 'drawings'."""

        new_drawings = []
        for d_config in drawings_config:
            x = d_config['pos x']+offset_pos.x()
            y = d_config['pos y']+offset_pos.y()
            new_drawing = self.create_drawing(config=d_config)
            self.add_drawing(new_drawing, QPointF(x, y))
            new_drawings.append(new_drawing)

        return new_drawings

    def _create_and_place_drawing__cmd(self, posF, config=None):
        new_drawing_obj = self.create_drawing(config)
        place_command = PlaceDrawing_Command(self, posF, new_drawing_obj)
        self._push_undo(place_command)
        return new_drawing_obj

    # ADDING/REMOVING COMPONENTS
    def add_component(self, e: QGraphicsItem):
        if isinstance(e, NodeItem):
            self.add_node(e.node)
            self.add_node_item(e)
        elif isinstance(e, DrawingObject):
            self.add_drawing(e)

    def remove_components(self, comps: [QGraphicsItem]):
        for c in comps:
            self.remove_component(c)

    def remove_component(self, e: QGraphicsItem):
        if isinstance(e, NodeItem):
            self.remove_node(e.node)
            self.remove_node_item(e)
        elif isinstance(e, DrawingObject):
            self.remove_drawing(e)

    def remove_selected_components__cmd(self):
        self._push_undo(
            RemoveComponents_Command(self, self.scene().selectedItems())
        )

        self.viewport().update()

    # MOVING COMPONENTS
    def _move_selected_copmonents__cmd(self, x, y):
        new_rel_pos = QPointF(x, y)

        # if one node item would leave the scene (f.ex. pos.x < 0), stop
        left = False
        for i in self.scene().selectedItems():
            new_pos = i.pos() + new_rel_pos
            w = i.boundingRect().width()
            h = i.boundingRect().height()
            if new_pos.x() - w / 2 < 0 or \
                    new_pos.x() + w / 2 > self.scene().width() or \
                    new_pos.y() - h / 2 < 0 or \
                    new_pos.y() + h / 2 > self.scene().height():
                left = True
                break

        if not left:
            # moving the items
            items_group = self.scene().createItemGroup(self.scene().selectedItems())
            items_group.moveBy(new_rel_pos.x(), new_rel_pos.y())
            self.scene().destroyItemGroup(items_group)

            # saving the command
            self._push_undo(
                MoveComponents_Command(self, self.scene().selectedItems(), p_from=-new_rel_pos, p_to=QPointF(0, 0))
            )

        self.viewport().repaint()

    def _move_selected_comps_left(self):
        self._move_selected_copmonents__cmd(-40, 0)

    def _move_selected_comps_up(self):
        self._move_selected_copmonents__cmd(0, -40)

    def _move_selected_comps_right(self):
        self._move_selected_copmonents__cmd(+40, 0)

    def _move_selected_comps_down(self):
        self._move_selected_copmonents__cmd(0, +40)

    # SELECTION
    def selected_components_moved(self, pos_diff):
        items_list = self.scene().selectedItems()

        self._push_undo(
            MoveComponents_Command(self, items_list, p_from=-pos_diff, p_to=QPointF(0, 0))
        )

    def selected_node_items(self) -> [NodeItem]:
        """Returns a list of the currently selected NodeItems."""

        selected_NIs = []
        for i in self.scene().selectedItems():
            if isinstance(i, NodeItem):
                selected_NIs.append(i)
        return selected_NIs

    def selected_nodes(self) -> [Node]:
        return [item.node for item in self.selected_node_items()]

    def selected_drawings(self) -> [DrawingObject]:
        """Returns a list of the currently selected drawings."""

        selected_drawings = []
        for i in self.scene().selectedItems():
            if isinstance(i, DrawingObject):
                selected_drawings.append(i)
        return selected_drawings

    def select_all(self):
        for i in self.scene().items():
            if i.ItemIsSelectable:
                i.setSelected(True)
        self.viewport().repaint()

    def clear_selection(self):
        self.scene().clearSelection()

    def select_components(self, comps):
        self.scene().clearSelection()
        for c in comps:
            c.setSelected(True)

    # ACTIONS
    def _copy(self):  # ctrl+c
        data = {'nodes': self._get_nodes_config_data(self.selected_nodes()),
                'connections': self._get_connections_config_data(self.selected_nodes()),
                'drawings': self._get_drawings_config_data(self.selected_drawings())}
        QGuiApplication.clipboard().setText(json.dumps(data))

    def _cut(self):  # ctrl+x
        data = {'nodes': self._get_nodes_config_data(self.selected_nodes()),
                'connections': self._get_connections_config_data(self.selected_nodes()),
                'drawings': self._get_drawings_config_data(self.selected_drawings())}
        QGuiApplication.clipboard().setText(json.dumps(data))
        self.remove_selected_components__cmd()

    def _paste(self):
        data = {}
        try:
            data = json.loads(QGuiApplication.clipboard().text())
        except Exception as e:
            return

        self.clear_selection()

        # calculate offset
        positions = []
        for d in data['drawings']:
            positions.append({'x': d['pos x'],
                              'y': d['pos y']})
        for n in data['nodes']:
            positions.append({'x': n['pos x'],
                              'y': n['pos y']})

        offset_for_middle_pos = QPointF(0, 0)
        if len(positions) > 0:
            rect = QRectF(positions[0]['x'], positions[0]['y'], 0, 0)
            for p in positions:
                x = p['x']
                y = p['y']
                if x < rect.left():
                    rect.setLeft(x)
                if x > rect.right():
                    rect.setRight(x)
                if y < rect.top():
                    rect.setTop(y)
                if y > rect.bottom():
                    rect.setBottom(y)

            offset_for_middle_pos = self._last_mouse_move_pos - rect.center()

        self._push_undo(
            Paste_Command(self, data, offset_for_middle_pos)
        )

    # VIEWPORT UPDATE MODE
    def viewport_update_mode(self) -> str:
        """Returns the current viewport update mode as string (sync or async) of the flow"""
        return VPUpdateMode.stringify(self.vp_update_mode)

    def set_viewport_update_mode(self, mode: str):
        """
        Sets the viewport update mode of the flow
        :mode: 'sync' or 'async'
        """
        if mode == 'sync':
            self.vp_update_mode = VPUpdateMode.SYNC
        elif mode == 'async':
            self.vp_update_mode = VPUpdateMode.ASYNC

        self.viewport_update_mode_changed.emit(self.viewport_update_mode())

    # CONFIG
    def generate_config_data(self, abstract_flow_data):

        # # wait for abstract flow
        # self.flow._temp_config_data = None
        # self.get_flow_config_data_request.emit()
        # while self.flow._temp_config_data is None:
        #     time.sleep(0.001)
        # flow_config, nodes_cfg, connections_cfg = self.flow._temp_config_data

        flow_config, nodes_cfg, connections_cfg = abstract_flow_data

        final_flow_config = {
            **flow_config,
            'nodes': self.complete_nodes_config_data(nodes_cfg),
            'connections': self.complete_connections_config_data(connections_cfg),
        }
        self_config = {
            'viewport update mode': VPUpdateMode.stringify(self.vp_update_mode),
            'drawings': self._get_drawings_config_data(self.drawings),
            'view size': [self.sceneRect().size().width(), self.sceneRect().size().height()]
        }

        # self.config_generated.emit(data)
        self._temp_config_data = (final_flow_config, self_config)
        return final_flow_config, self_config

    def complete_nodes_config_data(self, nodes_config_dict):
        """
        Adds the item config (scene pos etc.) to the config of the nodes.
        """

        nodes_config_list = []
        for n in list(nodes_config_dict.keys()):
            cfg = nodes_config_dict[n]

            item = self.node_items[n]
            nodes_config_list.append(item.complete_config(cfg))


        self._temp_config_data = nodes_config_list
        return nodes_config_list

    def complete_connections_config_data(self, conn_config_dict):
        """
        Adds the item config to the config of the connections
        """

        # TODO: add custom config when implementing custom connection items later

        conns_config_list = []
        for c in list(conn_config_dict.keys()):
            conns_config_list.append(conn_config_dict[c])

        self._temp_config_data = conns_config_list
        return conns_config_list

    def _get_nodes_config_data(self, nodes):

        # wait for abstract flow
        self.flow._temp_config_data = None
        self.get_nodes_config_request.emit(nodes)
        while self.flow._temp_config_data is None:
            time.sleep(0.001)

        return self.complete_nodes_config_data(self.flow._temp_config_data)

    def _get_connections_config_data(self, nodes):

        # wait for abstract flow
        self.flow._temp_config_data = None
        self.get_connections_config_request.emit(nodes)
        while self.flow._temp_config_data is None:
            time.sleep(0.001)

        return self.complete_connections_config_data(self.flow._temp_config_data)

    def _get_drawings_config_data(self, drawings):
        drawings_list = []
        for drawing in drawings:
            drawing_dict = drawing.config_data()

            drawings_list.append(drawing_dict)

        return drawings_list
