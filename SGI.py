import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
import array
from Ponto import Ponto
from Window import Window
from Reta import Reta
from Poligono import Poligono
from Curva import Curva
import math
from Arquivo import Arquivo
from Clipping import Clipping
from copy import deepcopy

lista_pontos = []
lista_retas = []
lista_poligonos = []
lista_curvas = []
lista_ponto_poligono = []
lista_pontos_curva = []

xViewPortMax = 500
xViewPortMin = 0
yViewPortMax = 500
yViewPortMin = 0

surface = None
widget = None

DrawingFrame = None
MainWindow = None
store = Gtk.ListStore(str, str)

tela = Window(xViewPortMin, yViewPortMin, xViewPortMax, yViewPortMax)
area_clipping = False
liang_barsky = False
cohen_sutherland = False
sutherland_hodgmann = False
bezier = False


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()


def transformadaViewPortCoordenadaX(x):
    auxiliar = (x - tela.getXMin()) / (tela.getXMax() - tela.getXMin())

    return auxiliar * (xViewPortMax - xViewPortMin)


def transformadaViewPortCoordenadaY(y):
    auxiliar = (y - tela.getYMin()) / (tela.getYMax() - tela.getYMin())

    return (1 - auxiliar) * (yViewPortMax - yViewPortMin)


def atualizarTela():
    clear_surface()
    redesenha_pontos()
    redesenha_retas()
    redesenha_poligonos()
    redesenha_curvas()
    desenha_area_clippling()
    # atualiza widget do DrawingFrame
    widget.queue_draw()


def redesenha_pontos():
    for ponto in lista_pontos:
        desenhaPonto(ponto)


def redesenha_retas():
    for reta in lista_retas:
        desenhaReta(reta)


def redesenha_poligonos():
    for poligono in lista_poligonos:
        desenha_poligono(poligono)

def redesenha_curvas():
    for curva in lista_curvas:
        desenha_curva(curva)


def desenhaPonto(ponto):
    ctx = cairo.Context(surface)
    ctx.save()
    ctx.set_line_width(2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(0.3, 0.3, 0.3)

    if ponto.selecionado == True:
        ctx.set_line_width(4)
        ctx.set_source_rgb(0, 1, 0)

    if liang_barsky == True:
        clipped = deepcopy(ponto)
        reta = Reta(clipped.x, clipped.y, clipped.x, clipped.y)
        lb = Clipping(tela)
        pontos = lb.liang_barsky_clipping(reta)
        if len(pontos) == 0:
            pass
        else:
            reta.x1 = pontos[0]
            reta.y1 = pontos[1]
            reta.x2 = pontos[2]
            reta.y2 = pontos[3]
            ctx.move_to(transformadaViewPortCoordenadaX(reta.x1), transformadaViewPortCoordenadaY(reta.y1))
            ctx.line_to(transformadaViewPortCoordenadaX(reta.x2), transformadaViewPortCoordenadaY(reta.y2))
            ctx.stroke()
            ctx.restore()
            return
    if cohen_sutherland == True:
        clipped = deepcopy(ponto)
        reta = Reta(clipped.x, clipped.y, clipped.x, clipped.y)
        lb = Clipping(tela)
        pontos = lb.cohen_sutherland_clipping(reta)
        if len(pontos) == 0:
            pass
        else:
            reta.x1 = pontos[0]
            reta.y1 = pontos[1]
            reta.x2 = pontos[2]
            reta.y2 = pontos[3]
            ctx.move_to(transformadaViewPortCoordenadaX(reta.x1), transformadaViewPortCoordenadaY(reta.y1))
            ctx.line_to(transformadaViewPortCoordenadaX(reta.x2), transformadaViewPortCoordenadaY(reta.y2))
            ctx.stroke()
            ctx.restore()
            return
    else:
        ctx.move_to(transformadaViewPortCoordenadaX(ponto.x), transformadaViewPortCoordenadaY(ponto.y))
        ctx.line_to(transformadaViewPortCoordenadaX(ponto.x), transformadaViewPortCoordenadaY(ponto.y))
        ctx.stroke()
        ctx.restore()


def desenhaReta(reta):
    ctx = cairo.Context(surface)
    ctx.save()
    ctx.set_line_width(2)
    ctx.set_line_cap(cairo.LINE_CAP_SQUARE)
    ctx.set_source_rgb(0.3, 0.3, 0.3)

    if reta.selecionado == True:
        ctx.set_source_rgb(0, 1, 0)
    if liang_barsky == True:
        clipped = deepcopy(reta)
        lb = Clipping(tela)
        pontos = lb.liang_barsky_clipping(clipped)
        if len(pontos) == 0:
            pass
        else:
            clipped.x1 = pontos[0]
            clipped.y1 = pontos[1]
            clipped.x2 = pontos[2]
            clipped.y2 = pontos[3]
            ctx.move_to(transformadaViewPortCoordenadaX(clipped.x1), transformadaViewPortCoordenadaY(clipped.y1))
            ctx.line_to(transformadaViewPortCoordenadaX(clipped.x2), transformadaViewPortCoordenadaY(clipped.y2))
            ctx.stroke()
            ctx.restore()
            return
    if cohen_sutherland == True:
        clipped = deepcopy(reta)
        lb = Clipping(tela)
        pontos = lb.cohen_sutherland_clipping(clipped)
        if len(pontos) == 0:
            pass
        else:
            clipped.x1 = pontos[0]
            clipped.y1 = pontos[1]
            clipped.x2 = pontos[2]
            clipped.y2 = pontos[3]
            ctx.move_to(transformadaViewPortCoordenadaX(clipped.x1), transformadaViewPortCoordenadaY(clipped.y1))
            ctx.line_to(transformadaViewPortCoordenadaX(clipped.x2), transformadaViewPortCoordenadaY(clipped.y2))
            ctx.stroke()
            ctx.restore()
            return
    else:
        ctx.move_to(transformadaViewPortCoordenadaX(reta.x1), transformadaViewPortCoordenadaY(reta.y1))
        ctx.line_to(transformadaViewPortCoordenadaX(reta.x2), transformadaViewPortCoordenadaY(reta.y2))
        ctx.stroke()
        ctx.restore()

def desenha_poligono(poligono):
    ctx = cairo.Context(surface)
    ctx.save()
    ctx.set_line_width(2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(0.3, 0.3, 0.3)

    if poligono.selecionado == True:
        ctx.set_source_rgb(0, 1, 0)

    if sutherland_hodgmann == True:
        clipped = deepcopy(poligono)
        lb = Clipping(tela)

        _pontos = lb.sutherland_hodgman_clipping(clipped)
        if len(_pontos) == 0:
            pass
        else:
            _ponto = _pontos[0]

            ctx.move_to(transformadaViewPortCoordenadaX(_ponto.x), transformadaViewPortCoordenadaY(_ponto.y))

            for p in _pontos:
                ctx.line_to(transformadaViewPortCoordenadaX(p.x), transformadaViewPortCoordenadaY(p.y))

            ctx.line_to(transformadaViewPortCoordenadaX(_ponto.x), transformadaViewPortCoordenadaY(_ponto.y))

            ctx.stroke()
            ctx.restore()

    else:
        _ponto = poligono.pontos[0]
        ctx.move_to(transformadaViewPortCoordenadaX(_ponto.x), transformadaViewPortCoordenadaY(_ponto.y))

        for p in poligono.pontos:
            ctx.line_to(transformadaViewPortCoordenadaX(p.x), transformadaViewPortCoordenadaY(p.y))

        ctx.line_to(transformadaViewPortCoordenadaX(_ponto.x), transformadaViewPortCoordenadaY(_ponto.y))

        ctx.stroke()
        ctx.restore()

def desenha_curva(curva):
    ctx = cairo.Context(surface)
    ctx.save()
    ctx.set_line_width(2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(0.3, 0.3, 0.3)

    if curva.selecionado == True:
        ctx.set_source_rgb(0, 1, 0)

    if cohen_sutherland == True:
        clipped = deepcopy(curva)
        lb = Clipping(tela)

        _pontos = []

        for clip in clipped.pontos_curva:
            r = Reta(clip.x, clip.y, clip.x, clip.y)
            pontos_aux = lb.cohen_sutherland_clipping(r)
            if len(pontos_aux) != 0:
                p = Ponto(pontos_aux[0], pontos_aux[1])
                _pontos.append(p)

        if len(_pontos) == 0:
            pass
        else:
            _ponto = _pontos[0]

            ctx.move_to(transformadaViewPortCoordenadaX(_ponto.x), transformadaViewPortCoordenadaY(_ponto.y))

            for p in _pontos:
                ctx.line_to(transformadaViewPortCoordenadaX(p.x), transformadaViewPortCoordenadaY(p.y))

            ctx.stroke()
            ctx.restore()

    else:
        _ponto = curva.pontos_curva[0]

        ctx.move_to(transformadaViewPortCoordenadaX(_ponto.x), transformadaViewPortCoordenadaY(_ponto.y))

        for p in curva.pontos_curva:
            ctx.line_to(transformadaViewPortCoordenadaX(p.x), transformadaViewPortCoordenadaY(p.y))

        ctx.stroke()
        ctx.restore()

def desenha_area_clippling():
    global area_clipping
    ctx = cairo.Context(surface)
    if area_clipping == True:
        ctx.save()
        ctx.set_line_width(1)
        ctx.set_source_rgb(0,0,1)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.move_to(50, 50)
        ctx.line_to(50, 450)
        ctx.line_to(450, 450)
        ctx.line_to(450, 50)
        ctx.line_to(50, 50)
        ctx.stroke()
        ctx.restore()
        widget.queue_draw()
    else:
        pass


def clear_surface():
    cr = cairo.Context(surface)
    cr.set_source_rgb(1, 1, 1)
    cr.paint()

    del cr


def configure_event_cb(wid, evt):
    global surface

    if surface is not None:
        del surface
        surface = None

    win = wid.get_window()
    width = wid.get_allocated_width()
    height = wid.get_allocated_height()

    surface = win.create_similar_surface(
        cairo.CONTENT_COLOR,
        width,
        height)

    clear_surface()
    return True


def draw_cb(wid, cr):
    global surface
    global widget
    widget = wid

    cr.set_source_surface(surface, 0, 0)
    cr.paint()
    return False


# carregando interface Glade
class MainWindow(Gtk.Window):

    def __init__(self):

        # p = Ponto(50, 50, 'q')
        # q = Ponto(10, 10, 'r')
        # s = Ponto(70, 90, 'r')
        # r = Reta(100, 100, 300, 300, 'w')
        #
        # listaPontos.append(p)
        # listaPontos.append(q)
        # listaRetas.append(r)
        #
        # poly = Poligono([p, q, s], 's')
        # lista_poligonos.append(poly)
        # poly = Poligono([Ponto(50, 50), Ponto(150, 150), Ponto(300, 50), Ponto(400,450), Ponto(450, 1)], 'poly')
        # lista_poligonos.append(poly)
        curve_bezier = Curva([Ponto(50, 50), Ponto(150, 150), Ponto(300, 50), Ponto(400,450), Ponto(450, 1)], 'bezier', True)
        curve = Curva([Ponto(50, 50), Ponto(150, 150), Ponto(300, 50), Ponto(400,450), Ponto(450, 1)], 'normal', False)
        lista_curvas.append(curve)
        lista_curvas.append(curve_bezier)

        builder = Gtk.Builder()
        builder.add_from_file("view.glade")
        builder.connect_signals(self)

        # carregando elementos
        MainWindow = builder.get_object("MainWindow")

        self.PontoWindow = builder.get_object("PontoWindow")
        self.RetaWindow = builder.get_object("RetaWindow")
        self.PoligonoWindow = builder.get_object("PoligonoWindow")
        self.ExclusaoWindow = builder.get_object("ExclusaoWindow")
        self.AlertaWindow = builder.get_object("AlertaWindow")
        self.DrawingFrame = builder.get_object("DrawingFrame")
        self.EditarWindow = builder.get_object("WindowEditarObjeto")
        self.CurvaWindow = builder.get_object("CurvaWindow")

        self.objectTreeView = builder.get_object("objectTreeView")
        self.objectTreeView.set_model(store)

        self.objectsCellRenderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Nome", self.objectsCellRenderer, text=0)
        self.objectTreeView.append_column(column)
        column = Gtk.TreeViewColumn("Tipo", self.objectsCellRenderer, text=1)
        self.objectTreeView.append_column(column)

        # regra de selecao de objeto na lista
        self.objeto_selecionado = self.objectTreeView.get_selection()
        self.objeto_selecionado.connect("changed", self.on_btn_deleta_selected)
        self.atual_selecao = None
        self.treeiter = None

        # acao do mouse
        self.objectTreeView.connect("button_press_event", self.mouse_click)

        # store.append(p.get_attributes())
        # store.append(q.get_attributes())
        # store.append(r.get_sttributes())
        # store.append(poly.get_attributes())
        store.append(curve.get_attributes())
        store.append(curve_bezier.get_attributes())

        # botoes janela MainWindow
        self.btnAbrirArquivo = builder.get_object("btnAbrirArquivo")
        self.btnSalvarArquivo = builder.get_object("btnSalvarArquivo")
        self.btnPonto = builder.get_object("btnPonto")
        self.btnReta = builder.get_object("btnReta")
        self.btnPoligono = builder.get_object("btnPoligono")
        self.btnCurva = builder.get_object("btnCurva")
        self.btnUp = builder.get_object("btnUp")
        self.btnDown = builder.get_object("btnDown")
        self.btnLeft = builder.get_object("btnLeft")
        self.btnRight = builder.get_object("btnRight")
        self.btnZoomIn = builder.get_object("btnZoomIn")
        self.btnZoomOut = builder.get_object("btnZoomOut")
        self.btnLimpaTela = builder.get_object("btnLimpaTela")
        self.btnRotacionarDireita = builder.get_object("btnRotacionarDireita")
        self.btnRotacionarEsquerda = builder.get_object("btnRotacionarEsquerda")
        # radio buttons
        self.radioRotacionarWindow = builder.get_object("radioRotacionarWindow")
        self.radioRotacionarObjeto = builder.get_object("radioRotacionarCentroObj")
        self.radioRotacionarMundo = builder.get_object("radioRotacionarCentroMundo")
        # switches
        self.switchAreaClipping = builder.get_object('switchAreaClipping')
        self.switchLiangBarsky = builder.get_object('switchLiangBarsky')
        self.switchCohen = builder.get_object('switchCohen')
        self.switchHodgmann = builder.get_object('switchHodgmann')


        self.btnDeletaItem = builder.get_object("btnDeletaItem")

        # botoes janela novo ponto
        self.btnSalvarPonto = builder.get_object("btnSalvarPonto")
        self.btnCancelaPonto = builder.get_object("btnCancelaPonto")
        self.btnSpinX = builder.get_object("btnSpinX")
        self.btnSpinY = builder.get_object("btnSpinY")
        self.textFieldNome = builder.get_object("textFieldNome")

        # botoes janela nova reta
        self.btnSalvarReta = builder.get_object("btnSalvarReta")
        self.btnCancelarReta = builder.get_object("btnCancelarReta")
        self.spinRetaX1 = builder.get_object("spinRetaX1")
        self.spinRetaY1 = builder.get_object("spinRetaY1")
        self.spinRetaX2 = builder.get_object("spinRetaX2")
        self.spinRetaY2 = builder.get_object("spinRetaY2")
        self.textFieldRetaNome = builder.get_object("textFieldRetaNome")

        self.btnConfirmaExclusao = builder.get_object("btnConfirmaExclusao")
        self.btnCancelaExclusao = builder.get_object("btnCancelaExclusao")

        # botoes janela novo poligono
        self.poligonoX = builder.get_object("poligonoX")
        self.poligonoY = builder.get_object("poligonoY")
        self.poligonoZ = builder.get_object("poligonoZ")
        self.btnSalvarPoligono = builder.get_object("btnSalvarPoligono")
        self.btnCancelarPoligono = builder.get_object("btnCancelarPoligono")
        self.textFieldPoligonoName = builder.get_object("textFieldPoligonoName")
        self.btnAdicionaPontoPoligono = builder.get_object("btnAdicionaPontoPoligono")

        # botoes janela nova curva
        self.curvaX = builder.get_object("curvaX")
        self.curvaY = builder.get_object("curvaY")
        self.curvaZ = builder.get_object("curvaZ")
        self.btnSalvarCurva = builder.get_object("btnSalvarCurva")
        self.btnCancelarCurva = builder.get_object("btnCancelarCurva")
        self.textFieldCurvaName = builder.get_object("textFieldCurvaName")
        self.btnAdicionaPontoCurva = builder.get_object("btnAdicionaPontoCurva")
        self.switchBezier = builder.get_object("switchBezier")

        # botoes janela alerta
        self.btnWindowAlerta = builder.get_object("btnWindowAlerta")
        self.mensagemTituloAviso = builder.get_object("mensagemTituloAviso")
        self.mensagemAviso = builder.get_object("mensagemAviso")

        # botoes janela edicao
        self.buttonSalvarEdicao = builder.get_object("buttonSalvarEdicao")
        self.buttonCancelarEdicao = builder.get_object("buttonCancelarEdicao")
        self.radioTransladar = builder.get_object("radioTransladar")
        self.radioEscalonar = builder.get_object("radioEscalonar")
        self.textFieldEditarX = builder.get_object("textFieldEditarX")
        self.textFieldEditarY = builder.get_object("textFieldEditarY")
        self.textFieldEditarEscalonar = builder.get_object("textFieldEditarEscalonar")

        # acao click de janelas Ponto
        self.btnPonto.connect("clicked", self.onBtnPontoClicked)
        self.btnSalvarPonto.connect("clicked", self.onBtnSalvarPontoClicked)
        self.btnCancelaPonto.connect("clicked", self.onBtnCancelaPontoClicked)

        # acao click de janelas Reta
        self.btnReta.connect("clicked", self.onBtnRetaClicked)
        self.btnSalvarReta.connect("clicked", self.onBtnSalvarRetaClicked)
        self.btnCancelarReta.connect("clicked", self.onBtnCancelaRetaClicked)

        # acao click janela Poligono
        self.btnPoligono.connect("clicked", self.onBtnPoligonoClicked)
        self.btnAdicionaPontoPoligono.connect("clicked", self.onBtnAdicionaPontoPoligonoClicked)
        self.btnSalvarPoligono.connect("clicked", self.onBtnSalvarPoligonoClicked)
        self.btnCancelarPoligono.connect("clicked", self.onBtnCancelaPoligonoClicked)

        # acao click janela Curva
        self.btnCurva.connect("clicked", self.on_btn_curva_clicked)
        self.btnAdicionaPontoCurva.connect("clicked", self.on_btn_adiciona_ponto_curva_clicked)
        self.btnSalvarCurva.connect("clicked", self.on_btn_salvar_curva_clicked)
        self.btnCancelarCurva.connect("clicked", self.on_btn_cancela_curva_clicked)
        self.switchBezier.connect('notify::active', self.on_switch_activate_bezier)

        # acao click janela principal
        self.btnAbrirArquivo.connect("clicked", self.on_btn_abrir_arquivo_clicked)
        self.btnSalvarArquivo.connect("clicked", self.on_btn_salvar_arquivo_clicked)
        self.btnDeletaItem.connect("clicked", self.on_btn_deleta_clicked)
        self.btnLimpaTela.connect("clicked", self.on_btn_limpa_tela_clicked)
        self.btnDown.connect("clicked", self.onBtnDownClicked)
        self.btnUp.connect("clicked", self.onBtnUpClicked)
        self.btnLeft.connect("clicked", self.onBtnLeftClicked)
        self.btnRight.connect("clicked", self.onBtnRightClicked)

        self.btnZoomIn.connect("clicked", self.onBtnZoomInClicked)
        self.btnZoomOut.connect("clicked", self.onBtnZoomOutClicked)

        self.btnRotacionarEsquerda.connect("clicked", self.on_btn_rotaciona_esquerda_clicked)
        self.btnRotacionarDireita.connect("clicked", self.on_btn_rotaciona_direita_clicked)

        # self.radioRotacionarObjeto.connect("toggled", self.on_editable_toggled)
        self.buttonSalvarEdicao.connect("clicked", self.on_btn_salvar_edicao_clicked)
        self.buttonCancelarEdicao.connect("clicked", self.on_btn_cancelar_edicao_clicked)

        self.switchAreaClipping.connect('notify::active', self.on_switch_activate_clipping)
        self.switchLiangBarsky.connect('notify::active', self.on_switch_activate_liang)
        self.switchCohen.connect('notify::active', self.on_switch_activate_cohen)
        self.switchHodgmann.connect('notify::active', self.on_switch_activate_hodgmann)

        self.DrawingFrame.connect('draw', draw_cb)
        self.DrawingFrame.connect('configure-event', configure_event_cb)

        builder.connect_signals(Handler())

        # exibe tela inicial SGI
        MainWindow.show_all()
        Gtk.main()

    def on_switch_activate_clipping(self, switch, gparam):
        global area_clipping
        if switch.get_active():
            area_clipping = True
            desenha_area_clippling()
        else:
            area_clipping = False
            desenha_area_clippling()

    def on_switch_activate_liang(self, switch, gparam):
        global liang_barsky
        global cohen_sutherland
        if switch.get_active():
            liang_barsky = True
            cohen_sutherland = False
            self.switchCohen.set_active(False)
        else:
            liang_barsky = False

    def on_switch_activate_cohen(self, switch, gparam):
        global cohen_sutherland
        global liang_barsky
        if switch.get_active():
            cohen_sutherland = True
            liang_barsky = False
            self.switchLiangBarsky.set_active(False)
        else:
            cohen_sutherland = False

    def on_switch_activate_hodgmann(self, switch, gparam):
        global sutherland_hodgmann
        if switch.get_active():
            sutherland_hodgmann = True
        else:
            sutherland_hodgmann = False


    def on_editable_toggled(self, button):
        value = button.get_active()
        print(value)

    def on_btn_cancelar_edicao_clicked(self, button):
        self.EditarWindow.hide()

    def on_btn_abrir_arquivo_clicked(self, button):
        arquivo = Arquivo('teste')
        global lista_poligonos
        global lista_pontos
        global lista_retas
        lista_objetos = arquivo.abrir()

        lista_pontos = lista_objetos[0]
        lista_retas = lista_objetos[1]
        lista_poligonos = lista_objetos[2]

        for p in lista_pontos:
            store.append(p.get_attributes())
        for r in lista_retas:
            store.append(r.get_sttributes())
        for y in lista_poligonos:
            store.append(y.get_attributes())

        atualizarTela()

    def on_btn_salvar_arquivo_clicked(self, button):
        arquivo = Arquivo("teste", lista_pontos, lista_retas, lista_poligonos)
        arquivo.salvar()

    def on_btn_salvar_edicao_clicked(self, button):
        model = self.objeto_selecionado[0]
        iter = self.objeto_selecionado[1]
        objeto = model[iter]
        # escalonar
        if self.radioEscalonar.get_active() == True:
            if objeto[0] == 'Ponto':
                for p in lista_pontos:
                    if objeto[1] == p.nome:
                        pass
            if objeto[0] == 'Reta':
                for p in lista_retas:
                    if objeto[1] == p.nome:
                        self.escalonar_reta(p)
            if objeto[0] == 'Poligono':
                for p in lista_poligonos:
                    if objeto[1] == p.nome:
                        self.escalonar_poligono(p)
            if objeto[0] == 'Curva':
                for p in lista_curvas:
                    if objeto[1] == p.nome:
                        self.escalonar_curva(p)
        # transladar
        else:
            if objeto[0] == 'Ponto':
                for p in lista_pontos:
                    if objeto[1] == p.nome:
                        self.transladar_ponto(p)
            if objeto[0] == 'Reta':
                for p in lista_retas:
                    if objeto[1] == p.nome:
                        self.translatar_reta(p)
            if objeto[0] == 'Poligono':
                for p in lista_poligonos:
                    if objeto[1] == p.nome:
                        self.transladar_poligono(p)
            if objeto[0] == 'Curva':
                for p in lista_curvas:
                    if objeto[1] == p.nome:
                        self.transladar_curva(p)

        self.EditarWindow.hide()

    def on_btn_limpa_tela_clicked(self, button):
        global lista_pontos
        global lista_retas
        global lista_poligonos
        global lista_curvas
        global store

        lista_pontos.clear()
        lista_retas.clear()
        lista_poligonos.clear()
        lista_curvas.clear()
        store.clear()

        atualizarTela()

    # Ações de botões Curva #

    def on_btn_curva_clicked(self, button):
        self.CurvaWindow.show_all()

    def on_btn_adiciona_ponto_curva_clicked(self, button):
        global lista_pontos_curva
        x = float(self.curvaX.get_value_as_int())
        y = float(self.curvaY.get_value_as_int())
        p = Ponto(x, y)
        lista_pontos_curva.append(p)

    def on_btn_salvar_curva_clicked(self, button):
        global lista_ponto_curva
        nome = self.textFieldPoligonoName.get_text()
        curva = Curva(lista_pontos_curva, nome)
        store.append(curva.get_attributes())
        lista_curvas.append(curva)
        desenha_curva(curva)
        self.CurvaWindow.hide()
        lista_ponto_curva = []

    def on_btn_cancela_curva_clicked(self, button):
        self.CurvaWindow.hide()

    def on_switch_activate_bezier(self, switch, gparam):
        global bezier
        if switch.get_active():
            bezier = True
        else:
            bezier = False

    ###########################################

    # Ações de botões Ponto #

    def onBtnPontoClicked(self, button):
        self.PontoWindow.show_all()

    def onBtnSalvarPontoClicked(self, button):
        x = float(self.btnSpinX.get_value_as_int())
        y = float(self.btnSpinY.get_value_as_int())
        nome = self.textFieldNome.get_text()
        ponto = Ponto(x, y, nome)
        store.append(ponto.get_attributes())
        lista_pontos.append(ponto)
        desenhaPonto(ponto)
        self.PontoWindow.hide()

    def onBtnCancelaPontoClicked(self, button):
        self.PontoWindow.hide()

    ############################################

    # Ações de botões Reta #
    def onBtnRetaClicked(self, button):
        self.RetaWindow.show_all()

    def onBtnSalvarRetaClicked(self, button):
        print('teste')
        x1 = float(self.spinRetaX1.get_value_as_int())
        y1 = float(self.spinRetaY1.get_value_as_int())
        x2 = float(self.spinRetaX2.get_value_as_int())
        y2 = float(self.spinRetaY2.get_value_as_int())
        nome = self.textFieldRetaNome.get_text()
        reta = Reta(x1, y1, x2, y2, nome)
        store.append(reta.get_sttributes())
        lista_retas.append(reta)
        desenhaReta(reta)
        self.RetaWindow.hide()


    def onBtnCancelaRetaClicked(self, button):
        self.RetaWindow.hide()

    #########################################

    # Ações de botões Poligono #
    def onBtnPoligonoClicked(self, button):
        self.PoligonoWindow.show_all()

    def onBtnAdicionaPontoPoligonoClicked(self, button):
        global lista_ponto_poligono
        x = float(self.poligonoX.get_value_as_int())
        y = float(self.poligonoY.get_value_as_int())
        p = Ponto(x, y)
        lista_ponto_poligono.append(p)

    def onBtnSalvarPoligonoClicked(self, button):
        global lista_ponto_poligono
        nome = self.textFieldPoligonoName.get_text()
        poligono = Poligono(lista_ponto_poligono, nome)
        store.append(poligono.get_attributes())
        lista_poligonos.append(poligono)
        desenha_poligono(poligono)
        self.PoligonoWindow.hide()
        lista_ponto_poligono = []

    def onBtnCancelaPoligonoClicked(self, button):
        self.PoligonoWindow.hide()

    ############################################


    def on_btn_deleta_selected(self, selecao):
        model, iter = selecao.get_selected()
        if iter is not None:
            print("You selected", model[iter][0])
            self.atual_selecao = model, iter
            self.highlight_objeto(model[iter])

    def on_btn_deleta_clicked(self, button):
        if len(store) != 0:
            (model, iter) = self.atual_selecao
            if iter is not None:
                print("%s foi removido" % (model[iter][0]))
                self.atualiza_objetos(model[iter])
                store.remove(iter)
        else:
            print("Lista Vazia")

        atualizarTela()

    def highlight_objeto(self, objeto):
        for p in lista_pontos:
            p.selecionado = False
        for p in lista_retas:
            p.selecionado = False
        for p in lista_poligonos:
            p.selecionado = False
        for p in lista_curvas:
            p.selecionado = False

        if objeto[0] == 'Ponto':
            for p in lista_pontos:
                p.selecionado = False
                if objeto[1] == p.nome:
                    p.selecionado = True

        if objeto[0] == 'Reta':
            for p in lista_retas:
                p.selecionado = False
                if objeto[1] == p.nome:
                    p.selecionado = True

        if objeto[0] == 'Poligono':
            for p in lista_poligonos:
                p.selecionado = False
                if objeto[1] == p.nome:
                    p.selecionado = True

        if objeto[0] == 'Curva':
            for p in lista_curvas:
                p.selecionado = False
                if objeto[1] == p.nome:
                    p.selecionado = True

        atualizarTela()

    def atualiza_objetos(self, objeto):
        if objeto[0] == 'Ponto':
            for p in lista_pontos:
                if objeto[1] == p.nome:
                    lista_pontos.remove(p)
        if objeto[0] == 'Reta':
            for p in lista_retas:
                if objeto[1] == p.nome:
                    lista_retas.remove(p)
        if objeto[0] == 'Poligono':
            for p in lista_poligonos:
                if objeto[1] == p.nome:
                    lista_poligonos.remove(p)
        if objeto[0] == 'Curva':
            for p in lista_curvas:
                if objeto[1] == p.nome:
                    lista_curvas.remove(p)

    def onBtnDownClicked(self, button):
        xMaximo = tela.getXMax()
        xMinimo = tela.getXMin()
        yMaximo = tela.getYMax()
        yMinimo = tela.getYMin()

        yMaximo += 10
        yMinimo += 10

        tela.setCoordenadasMaximo(xMaximo, yMaximo)
        tela.setCoordenadasMinimo(xMinimo, yMinimo)

        atualizarTela()

    def onBtnUpClicked(self, button):
        xMaximo = tela.getXMax()
        xMinimo = tela.getXMin()
        yMaximo = tela.getYMax()
        yMinimo = tela.getYMin()

        yMaximo -= 10
        yMinimo -= 10

        tela.setCoordenadasMaximo(xMaximo, yMaximo)
        tela.setCoordenadasMinimo(xMinimo, yMinimo)

        atualizarTela()

    def onBtnLeftClicked(self, button):
        xMaximo = tela.getXMax()
        xMinimo = tela.getXMin()
        yMaximo = tela.getYMax()
        yMinimo = tela.getYMin()

        xMaximo += 10
        xMinimo += 10

        tela.setCoordenadasMaximo(xMaximo, yMaximo)
        tela.setCoordenadasMinimo(xMinimo, yMinimo)

        atualizarTela()

    def onBtnRightClicked(self, button):
        xMaximo = tela.getXMax()
        xMinimo = tela.getXMin()
        yMaximo = tela.getYMax()
        yMinimo = tela.getYMin()

        xMaximo -= 10
        xMinimo -= 10

        tela.setCoordenadasMaximo(xMaximo, yMaximo)
        tela.setCoordenadasMinimo(xMinimo, yMinimo)

        atualizarTela()

    def onBtnZoomInClicked(self, button):
        xMaximo = tela.getXMax()
        xMinimo = tela.getXMin()
        yMaximo = tela.getYMax()
        yMinimo = tela.getYMin()

        xMaximo -= 5
        xMinimo += 5
        yMaximo -= 5
        yMinimo += 5

        tela.setCoordenadasMaximo(xMaximo, yMaximo)
        tela.setCoordenadasMinimo(xMinimo, yMinimo)

        atualizarTela()

    def onBtnZoomOutClicked(self, button):
        xMaximo = tela.getXMax()
        xMinimo = tela.getXMin()
        yMaximo = tela.getYMax()
        yMinimo = tela.getYMin()

        xMaximo += 5
        xMinimo -= 5
        yMaximo += 5
        yMinimo -= 5

        tela.setCoordenadasMaximo(xMaximo, yMaximo)
        tela.setCoordenadasMinimo(xMinimo, yMinimo)

        atualizarTela()

    def mouse_click(self, tv, event):
        if event.button == 3:
            # Begin added code
            pthinfo = self.objectTreeView.get_path_at_pos(event.x, event.y)
            if pthinfo != None:
                path, col, cellx, celly = pthinfo
                self.objectTreeView.grab_focus()
                self.objectTreeView.set_cursor(path, col, 0)
            # End added code

            selection = self.objectTreeView.get_selection()
            (model, iter) = selection.get_selected()
            self.objeto_selecionado = (model, iter)
            # dispara window
            self.EditarWindow.show_all()

    def on_btn_rotaciona_esquerda_clicked(self, button):
        if self.radioRotacionarWindow.get_active() == True:
            self.rotaciona_window_esquerda()
            return
        if len(store) != 0:
            (model, iter) = self.atual_selecao
            objeto = model[iter]
            if objeto is not None:
                if objeto[0] == 'Ponto':
                    # chama func rotaciona ponto
                    for p in lista_pontos:
                        if objeto[1] == p.nome:
                            self.rotaciona_ponto(p, 'l')
                if objeto[0] == 'Reta':
                    # chama func rotaciona reta
                    for p in lista_retas:
                        if objeto[1] == p.nome:
                            self.rotaciona_reta(p, 'l')
                if objeto[0] == 'Poligono':
                    # chama func rotaciona poligono
                    for p in lista_poligonos:
                        if objeto[1] == p.nome:
                            self.rotaciona_poligono(p, 'l')
                if objeto[0] == 'Curva':
                    # chama func rotaciona curva
                    for p in lista_curvas:
                        if objeto[1] == p.nome:
                            self.rotaciona_curva(p, 'l')

    def on_btn_rotaciona_direita_clicked(self, button):
        if self.radioRotacionarWindow.get_active() == True:
            self.rotaciona_window_direita()
            return
        if len(store) != 0:
            (model, iter) = self.atual_selecao
            objeto = model[iter]
            if objeto is not None:
                if objeto[0] == 'Ponto':
                    # chama func rotaciona ponto
                    for p in lista_pontos:
                        if objeto[1] == p.nome:
                            self.rotaciona_ponto(p, 'r')
                if objeto[0] == 'Reta':
                    # chama func rotaciona reta
                    for p in lista_retas:
                        if objeto[1] == p.nome:
                            self.rotaciona_reta(p, 'r')
                if objeto[0] == 'Poligono':
                    # chama func rotaciona poligono
                    for p in lista_poligonos:
                        if objeto[1] == p.nome:
                            self.rotaciona_poligono(p, 'r')
                if objeto[0] == 'Curva':
                    # chama func rotaciona curva
                    for p in lista_curvas:
                        if objeto[1] == p.nome:
                            self.rotaciona_curva(p, 'r')

    def rotaciona_ponto(self, ponto, direcao):
        if direcao == 'l':
            theta = 10 * math.pi / 180
        if direcao == 'r':
            theta = - 10 * math.pi / 180

        if self.radioRotacionarObjeto.get_active() == True:
            x, y = ponto.get_centro_gravidade()
        if self.radioRotacionarMundo.get_active() == True or self.radioRotacionarWindow.get_active() == True:
            x, y = tela.get_centro()

        _x = (ponto.x - x) * math.cos(theta) + (ponto.y - y) * math.sin(theta) + x
        _y = (ponto.x - x) * -math.sin(theta) + (ponto.y - y) * math.cos(theta) + y

        ponto.x = _x
        ponto.y = _y

        atualizarTela()

    def rotaciona_reta(self, reta, direcao):
        if direcao == 'l':
            theta = 10 * math.pi / 180
        if direcao == 'r':
            theta = - 10 * math.pi / 180

        if self.radioRotacionarObjeto.get_active() == True:
            x, y = reta.get_centro_gravidade()
        if self.radioRotacionarMundo.get_active() == True or self.radioRotacionarWindow.get_active() == True:
            x, y = tela.get_centro()

        _x1 = (reta.x1 - x) * math.cos(theta) + (reta.y1 - y) * math.sin(theta) + x
        _y1 = (reta.x1 - x) * -math.sin(theta) + (reta.y1 - y) * math.cos(theta) + y
        _x2 = (reta.x2 - x) * math.cos(theta) + (reta.y2 - y) * math.sin(theta) + x
        _y2 = (reta.x2 - x) * -math.sin(theta) + (reta.y2 - y) * math.cos(theta) + y

        reta.x1 = _x1
        reta.x2 = _x2
        reta.y1 = _y1
        reta.y2 = _y2

        atualizarTela()

    def rotaciona_poligono(self, poligono, direcao):
        if direcao == 'l':
            theta = 10 * math.pi / 180
        if direcao == 'r':
            theta = - 10 * math.pi / 180

        if self.radioRotacionarObjeto.get_active() == True:
            x, y = poligono.get_centro_gravidade()
        if self.radioRotacionarMundo.get_active() == True or self.radioRotacionarWindow.get_active() == True:
            x, y = tela.get_centro()

        for p in poligono.pontos:
            _x = (p.x - x) * math.cos(theta) + (p.y - y) * math.sin(theta) + x
            _y = (p.x - x) * -math.sin(theta) + (p.y - y) * math.cos(theta) + y
            p.x = _x
            p.y = _y

        atualizarTela()

    def rotaciona_curva(self, curva, direcao):
        if direcao == 'l':
            theta = 10 * math.pi / 180
        if direcao == 'r':
            theta = - 10 * math.pi / 180

        if self.radioRotacionarObjeto.get_active() == True:
            x, y = curva.get_centro_gravidade()
        if self.radioRotacionarMundo.get_active() == True or self.radioRotacionarWindow.get_active() == True:
            x, y = tela.get_centro()

        for p in curva.pontos_curva:
            _x = (p.x - x) * math.cos(theta) + (p.y - y) * math.sin(theta) + x
            _y = (p.x - x) * -math.sin(theta) + (p.y - y) * math.cos(theta) + y
            p.x = _x
            p.y = _y

        atualizarTela()

    def transladar_ponto(self, ponto):
        x = float(self.textFieldEditarX.get_text())
        y = float(self.textFieldEditarY.get_text())

        ponto.x = ponto.x + x
        ponto.y = ponto.y + y

        for p in lista_pontos:
            if p == ponto:
                p = ponto

        atualizarTela()

    def translatar_reta(self, reta):
        x = float(self.textFieldEditarX.get_text())
        y = float(self.textFieldEditarY.get_text())

        reta.x1 = reta.x1 + x
        reta.x2 = reta.x2 + x
        reta.y1 = reta.y1 + y
        reta.y2 = reta.y2 + y

        for p in lista_retas:
            if p == reta:
                p = reta

        atualizarTela()

    def transladar_poligono(self, poligono):
        x = float(self.textFieldEditarX.get_text())
        y = float(self.textFieldEditarY.get_text())

        for p in poligono.pontos:
            p.x = p.x + x
            p.y = p.y + y

        for p in lista_poligonos:
            if p == poligono:
                p = poligono

        atualizarTela()

    def transladar_curva(self, curva):
        x = float(self.textFieldEditarX.get_text())
        y = float(self.textFieldEditarY.get_text())

        for p in curva.pontos_curva:
            p.x = p.x + x
            p.y = p.y + y

        for p in lista_curvas:
            if p == curva:
                p = curva

        atualizarTela()

    def escalonar_reta(self, reta):
        porcentagem = int(self.textFieldEditarEscalonar.get_text()) / 100

        centro_reta_x, centro_reta_y = reta.get_centro_gravidade()

        reta.x1 = (reta.x1 - centro_reta_x) * porcentagem + centro_reta_x
        reta.y1 = (reta.y1 - centro_reta_y) * porcentagem + centro_reta_y
        reta.x2 = (reta.x2 - centro_reta_x) * porcentagem + centro_reta_x
        reta.y2 = (reta.y2 - centro_reta_y) * porcentagem + centro_reta_y

        atualizarTela()

    def escalonar_poligono(self, poligono):
        porcentagem = int(self.textFieldEditarEscalonar.get_text()) / 100

        centro_poligono_x, centro_poligono_y = poligono.get_centro_gravidade()

        for p in poligono.pontos:
            p.x = (p.x - centro_poligono_x) * porcentagem + centro_poligono_x
            p.y = (p.y - centro_poligono_y) * porcentagem + centro_poligono_y

        atualizarTela()

    def escalonar_curva(self, curva):
        porcentagem = int(self.textFieldEditarEscalonar.get_text()) / 100

        centro_curva_x, centro_curva_y = curva.get_centro_gravidade()

        for p in curva.pontos_curva:
            p.x = (p.x - centro_curva_x) * porcentagem + centro_curva_x
            p.y = (p.y - centro_curva_y) * porcentagem + centro_curva_y

        atualizarTela()

    def rotaciona_window_esquerda(self):
        for p in lista_pontos:
            self.rotaciona_ponto(p, 'l')

        for r in lista_retas:
            self.rotaciona_reta(r, 'l')

        for y in lista_poligonos:
            self.rotaciona_poligono(y, 'l')

        for y in lista_curvas:
            self.rotaciona_curva(y, 'l')

    def rotaciona_window_direita(self):
        for p in lista_pontos:
            self.rotaciona_ponto(p, 'r')

        for r in lista_retas:
            self.rotaciona_reta(r, 'r')

        for y in lista_poligonos:
            self.rotaciona_poligono(y, 'r')

        for y in lista_curvas:
            self.rotaciona_curva(y, 'r')


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
