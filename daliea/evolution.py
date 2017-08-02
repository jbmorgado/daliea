# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
import copy


class Evolution(QObject):
    mutated_sig = pyqtSignal(object)

    def __init__(self, chromosome):
        QObject.__init__(self)
        self.chromosome = chromosome
        self._stop_flag = None
        self._mtype_flag = 'Hard'

    @pyqtSlot(object)
    def evolve(self, omega):
        c_descendant = copy.deepcopy(self.chromosome)

        while self._stop_flag is False:
            c_descendant.mutate(self._mtype_flag)
            c_descendant.mutations = c_descendant.mutations + 1
            self.chromosome.mutations = self.chromosome.mutations + 1
            c_descendant.make_phenotype((0, 0, 0, 255))
            c_descendant.calc_fitness(omega)
            # If descendant is less fit than parent keep parent
            if c_descendant.fitness > self.chromosome.fitness:
                c_descendant = copy.deepcopy(self.chromosome)
            # If descendant as fit as parent keep descendant
            elif c_descendant.fitness == self.chromosome.fitness:
                self.chromosome = copy.deepcopy(c_descendant)
                self.chromosome.neutrals = self.chromosome.neutrals + 1
                c_descendant.neutrals = c_descendant.neutrals + 1
            # If descendant fitter than parent keep descendant
            else:
                self.chromosome = copy.deepcopy(c_descendant)
                self.chromosome.improvements = self.chromosome.improvements + 1
                c_descendant.improvements = c_descendant.improvements + 1

            self.mutated_sig.emit(self.chromosome)
            QApplication.processEvents()

    @pyqtSlot(bool)
    def _set_stop_flag(self, value):
        if value is not True and value is not False:
            raise ValueError("method _set_stop_flag @ evolution doesn't accept\
                              attribute %s" % value)
        self._stop_flag = value

    @pyqtSlot(str)
    def _set_mtype_flag(self, value):
        # TODO: Error checking
        self._mtype_flag = value

    def make_connection(self, interface):
        interface.evolve_sig.connect(self.evolve)
        interface.set_stop_flag_sig.connect(self._set_stop_flag)
        interface.set_mtype_flag_sig.connect(self._set_mtype_flag)
