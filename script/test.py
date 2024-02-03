#!/usr/bin/python
# copyright 2021 Joseph J. Pfeiffer, Jr.
# I hereby release this work into the public domain.
# This work is made available with NO WARRANTY WHATEVER.

# fin flutter speed calculations using formulas from Peak of Flight 411
#
# If you change any parameter other than the flutter speed, the flutter
# speed is recalculated.
# If you change the desired flutter speed, the fin thickness is recalculated

from math import sqrt

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Entry3 :
    def __init__(self, grid, row, labelstr, step, unitstr, callback) :
        self.label = Gtk.Label(labelstr)
        self.label.set_hexpand(True)
        self.label.set_halign(Gtk.Align.START)
        grid.attach(self.label, 0, row, 1, 1)
        
        self.value = Gtk.SpinButton()
        self.value.set_range(0, 100*step)

        # formatting of display
        if step < .1 :
            digits = 3
        elif step < 1 :
            digits = 1
        else :
            digits = 0
        self.value.set_digits(digits)
        self.format = "%." + str(digits) + "f"
        
        self.value.set_increments(step, 10*step)
        self.value.set_value(10*step)
        self.value.set_alignment(xalign=1)
        self.value.connect("value-changed", callback)
        grid.attach(self.value, 1, row, 1, 1)

        self.units = Gtk.Label(unitstr)
        self.units.set_hexpand(True)
        self.units.set_halign(Gtk.Align.END)
        grid.attach(self.units, 2, row, 1, 1)
        
    def get_value(self) :
        return float(self.value.get_text())

    def set_value(self, newval) :
        self.value.set_text(self.format % newval)

class MainWindow(Gtk.Window) :
    
    def __init__(self) :
        Gtk.Window.__init__(self, title="Flutter Speed Calculator")

        mainFrame = Gtk.Frame()
        self.add(mainFrame)

        mainGrid = Gtk.Grid()
        mainGrid.set_column_spacing(5)
        mainGrid.set_row_spacing(5)
        mainFrame.add(mainGrid)

        self.modulus      = Entry3(mainGrid, 0, " Shear Modulus",      100000,   "PSI ", self.calculate_speed)
        self.altitude     = Entry3(mainGrid, 1, " Altitude (above MSL)",  100,    "ft ", self.calculate_speed)
        self.root         = Entry3(mainGrid, 2, " Root Chord",              0.1,  "in ", self.calculate_speed)
        self.tip          = Entry3(mainGrid, 3, " Tip Chord",               0.1,  "in ", self.calculate_speed)
        self.semispan     = Entry3(mainGrid, 4, " Semispan",                0.1,  "in ", self.calculate_speed)
        self.thickness    = Entry3(mainGrid, 5, " Thickness",               0.05, "in ", self.calculate_speed)
        self.flutterspeed = Entry3(mainGrid, 6, " Flutter Speed",         100,   "fps ", self.calculate_thickness)

    # OK, here's where we do the work!
    # two callbacks:
    #     calculate_speed calculates flutter speed if you change any input other than the flutter speed
    #     calcualte_thickness calculates required fin thickness if you change the flutter speed

    def calculate_terms(self) :
        G = float(self.modulus.get_value())
        alt = self.altitude.get_value()
        cr = self.root.get_value()
        ct = self.tip.get_value()
        b = self.semispan.get_value()
        
        S = 0.5 * (cr + ct) * b
        AR = b**2 / S
        lam = ct / cr
        
        T = 59.0 - 0.00356 * alt
        P = (2116.0/144.0) * ((T + 459.7)/518.6)**5.256
        a = sqrt(1.4 * 1716.59 * (T + 460))

        return AR, G, P, a, cr, lam
    
    def calculate_speed(self, button) :
        try :
            t = self.thickness.get_value()
            AR, G, P, a, cr, lam = self.calculate_terms()
            
            term1 = 1.337 * (AR**3) * P * (lam + 1)
            term2 = 2 * (AR + 2) * ((t / cr)**3)
            
            Vf = a * sqrt(G / (term1/term2))
            
            Vf = int(Vf / 100) * 100
            self.flutterspeed.set_value(Vf)
        except :
            self.flutterspeed.set_value(0)

    def calculate_thickness(self, button) :
        try :
            Vf = self.flutterspeed.get_value()
            AR, G, P, a, cr, lam = self.calculate_terms()
            
            t = cr * ((1.337 * (Vf/a)**2 * AR**3 * P * (lam + 1)) / (2 * G * (AR + 2))) ** (1.0/3.0)
            self.thickness.set_value(t)
        except :
            self.thickness.set_value(0)
            
win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
win.calculate_speed(None)
Gtk.main()

        
        
