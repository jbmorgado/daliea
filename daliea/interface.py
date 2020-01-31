# -*- coding: utf-8 -*-

from PySide2.QtWidgets import (
    QWidget, QPushButton, QFileDialog, QDesktopWidget, QHBoxLayout,
    QVBoxLayout, QGridLayout, QFormLayout, QGroupBox, QLabel, QComboBox,
    QLineEdit, QSpinBox)
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal, Slot
from PIL import (Image, ImageQt)
import sys
import time

MAX_SIZE = 256


class Interface(QWidget):
    evolve_sig = Signal(object)
    set_stop_flag_sig = Signal(bool)
    set_mtype_flag_sig = Signal(str)

    def __init__(self, chromosome):
        # super().__init__()
        super(self.__class__, self).__init__()
        self.chromosome = chromosome
        self.initUI()

    def initUI(self):
        # Connect the trigger signal to a slot.
        self.omega = None
        self.elp_val = 0
        self.improvements = 0
        self.neutrals = 0
        self.evolution_st = 0.0
        self.evolution_dt = 0.0

        # Omega Group
        omega_gbox = QGroupBox()
        omega_gbox.setTitle("Omega")
        omega_vbox = QVBoxLayout()
        self.omega_label = QLabel()
        omega_vbox.addWidget(self.omega_label)
        self.omega_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        omega_btn_load = QPushButton('Load Image', self)
        omega_btn_load.clicked.connect(self.omega_load)
        omega_vbox.addWidget(omega_btn_load)
        omega_gbox.setLayout(omega_vbox)

        # Alpha Group
        alpha_gbox = QGroupBox()
        alpha_gbox.setTitle("Alpha")
        alpha_vbox = QVBoxLayout()
        self.alpha_label = QLabel()
        alpha_vbox.addWidget(self.alpha_label)
        self.alpha_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        alpha_btn_save = QPushButton('Save', self)
        # alpha_btn_save.clicked.connect(self.alpha_save)
        alpha_vbox.addWidget(alpha_btn_save)
        alpha_gbox.setLayout(alpha_vbox)

        # Configure Group
        config_gbox = QGroupBox()
        config_gbox.setTitle("Configure")
        config_lbox = QFormLayout()
        self.mtype = QComboBox()
        config_lbox.addRow(QLabel("Mutation:"), self.mtype)
        mtype_list = ['Hard', 'Medium', 'Soft', 'Gaussian']
        self.mtype.addItems(mtype_list)
        self.mtype.currentTextChanged.connect(self._mtype_changed)
        config_lbox.addRow(QLabel("Background:"), QLineEdit())
        self.polynum = QSpinBox()
        config_lbox.addRow(QLabel("Polygons:"), self.polynum)
        # self.polynum.valueChanged.connect(self._polynum_changed)
        self.polynum.setMinimum(1)
        self.polynum.setMaximum(1000)
        self.polynum.setValue(50)
        self.vertnum = QSpinBox()
        config_lbox.addRow(QLabel("Vertices:"), self.vertnum)
        self.vertnum.setMinimum(3)
        self.vertnum.setMaximum(10)
        self.vertnum.setValue(4)
        config_gbox.setLayout(config_lbox)

        # Status Group
        status_gbox = QGroupBox()
        status_gbox.setTitle("Status")
        status_vbox = QVBoxLayout()
        status_grid = QGridLayout()
        status_grid.setSpacing(10)
        status_grid.addWidget(QLabel("Fitness:"), 0, 0)
        self.fit_dsp = QLabel()
        status_grid.addWidget(self.fit_dsp, 0, 1)
        status_grid.addWidget(QLabel("Improvements:"), 1, 0)
        self.imp_dsp = QLabel()
        status_grid.addWidget(self.imp_dsp, 1, 1)
        status_grid.addWidget(QLabel("Neutral Imp.:"), 2, 0)
        self.ntr_dsp = QLabel()
        status_grid.addWidget(self.ntr_dsp, 2, 1)
        status_grid.addWidget(QLabel("Mutations:"), 3, 0)
        self.mut_dsp = QLabel()
        status_grid.addWidget(self.mut_dsp, 3, 1)
        status_grid.addWidget(QLabel("Elapsed time (s):"), 4, 0)
        self.elp_dsp = QLabel()
        status_grid.addWidget(self.elp_dsp, 4, 1)
        status_grid.addWidget(QLabel("Mutations/s:"), 5, 0)
        self.mps_dsp = QLabel()
        status_grid.addWidget(self.mps_dsp, 5, 1)
        status_vbox.addLayout(status_grid)
        status_vbox.addStretch()
        self._start_btn = QPushButton('Start', self)
        self._prev_start_btn_status = None
        self._setup_start_btn('Start')
        status_vbox.addWidget(self._start_btn)
        status_gbox.setLayout(status_vbox)

        hbox = QHBoxLayout()
        hbox.addWidget(omega_gbox, 1)
        hbox.addWidget(alpha_gbox, 1)
        hbox.addWidget(config_gbox, 1)
        hbox.addWidget(status_gbox, 1)

        self.setLayout(hbox)
        self.resize(1024, 400)
        self.center()
        self.setWindowTitle('DaliEA')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_img_filename(self):
        """Create dialog for choosing image."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Original Image", "./",
            "Images (*.png *.jpg);;All Files (*)", options=options)

        return filename

    def omega_load(self):
        """Create dialog for choosing image and load it."""
        filename = self.get_img_filename()

        if filename:
            self.omega = Image.open(filename)
            omega_width = self.omega.width
            omega_height = self.omega.height
            omega_ratio = omega_width/omega_height

            if omega_ratio >= 1.:
                new_width = MAX_SIZE
                new_height = int(MAX_SIZE/omega_ratio)
                self.omega = self.omega.resize((new_width, new_height),
                                               Image.LANCZOS)
            else:
                new_height = MAX_SIZE
                new_width = int(MAX_SIZE*omega_ratio)
                self.omega = self.omega.resize((new_width, new_height),
                                               Image.LANCZOS)

            self.omega = self.omega.convert("RGB")

            self.omega_display = ImageQt.ImageQt(self.omega)
            pixmap = QPixmap.fromImage(self.omega_display)
            self.omega_label.setPixmap(pixmap)

    def evolution_start(self):
        """Start the evolution."""
        self.evolution_st = time.time()

        # Exit if there is no omega image.
        # TODO: Do better error checking
        if self.omega is None:
            print("No omega image. Exiting.")
            sys.exit(1)

        if self.chromosome.n_genes is None:
            width = self.omega.width
            height = self.omega.height
            polynum_val = self.polynum.value()
            vertnum_val = self.vertnum.value()
            self.chromosome.setup(width, height, vertnum_val, polynum_val)
            self.chromosome.make_phenotype((0, 0, 0, 255))
            self.chromosome.calc_fitness(self.omega)

            self.fit_dsp.setText(str(0.00))
            self.imp_dsp.setText(str(0))
            self.ntr_dsp.setText(str(0))
            self.mut_dsp.setText(str(0))
            self.elp_dsp.setText(str(0.0))
            self.mps_dsp.setText(str(0.0))

        self._setup_start_btn('Stop')
        self.set_stop_flag_sig.emit(False)
        self.evolve_sig.emit(self.omega)

    def _evolution_stop(self):
        """Send stop signal to evolution."""
        self.evolution_dt = self.evolution_dt + time.time() - self.evolution_st
        self.set_stop_flag_sig.emit(True)
        self._setup_start_btn('Start')

    def _mtype_changed(self):
        """Send mutation type signal to evolution."""
        self.set_mtype_flag_sig.emit(self.mtype.currentText())

    # def _polynum_changed(self):
    #     """Send polynum signal to evolution."""
    #     self.set_polynum_flag_sig.emit(self.polynum.valueFromText())

    @Slot(object)
    def update_status(self, chromosome):
        evolution_dt = self.evolution_dt + time.time() - self.evolution_st
        self.elp_dsp.setText(str(round(evolution_dt, 1)))
        self.mps_dsp.setText(str(round(chromosome.mutations /
                                       evolution_dt, 1)))
        self.mut_dsp.setText(str(chromosome.mutations))
        if chromosome.improvements > self.improvements:
            self.improvements = chromosome.improvements
            self.fit_dsp.setText(str(round(chromosome.fitness_p, 2)))
            self.imp_dsp.setText(str(chromosome.improvements))
            self._update_alpha_display(chromosome.phenotype)
        elif chromosome.neutrals > self.neutrals:
            self.neutrals = chromosome.neutrals
            self.ntr_dsp.setText(str(chromosome.neutrals))

    def make_connection(self, evolution):
        evolution.mutated_sig.connect(self.update_status)

    def _update_alpha_display(self, alpha):
        """Update the alpha image display."""

        self.alpha_display = ImageQt.ImageQt(alpha)
        pixmap = QPixmap.fromImage(self.alpha_display)
        self.alpha_label.setPixmap(pixmap)

    def _setup_start_btn(self, status):
        if status != 'Start' and status != 'Stop':
            raise ValueError("method _setup_start_btn @ interface doesn't accept\
                            attribute %s" % status)

        if self._prev_start_btn_status is None:
            if status == 'Start':
                self._start_btn.setText('Start')
                self._start_btn.clicked.connect(self.evolution_start)
                self._prev_start_btn_status = 'Start'
            elif status == 'Stop':
                self._start_btn.setText('Stop')
                self._start_btn.clicked.connect(self._evolution_stop)
                self._prev_start_btn_status = 'Stop'
        elif self._prev_start_btn_status is 'Start':
            if status == 'Stop':
                self._start_btn.setText('Stop')
                self._start_btn.clicked.disconnect(self.evolution_start)
                self._start_btn.clicked.connect(self._evolution_stop)
                self._prev_start_btn_status = 'Stop'
        elif self._prev_start_btn_status is 'Stop':
            if status == 'Start':
                self._start_btn.setText('Start')
                self._start_btn.clicked.disconnect(self._evolution_stop)
                self._start_btn.clicked.connect(self.evolution_start)
                self._prev_start_btn_status = 'Start'
