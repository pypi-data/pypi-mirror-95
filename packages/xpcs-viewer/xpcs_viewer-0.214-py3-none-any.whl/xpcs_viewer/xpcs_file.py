import os
import numpy as np
from .fileIO.hdf_reader import get, put, get_type, create_id
from .plothandler.pyqtgraph_handler import ImageViewDev
from .plothandler.matplot_qt import MplCanvasBarV
from .module import saxs2d, g2mod, saxs1d, intt, stability
from .module.g2mod import  create_slice
from .helper.fitting import fit_with_fixed
import pyqtgraph as pg
from .fileIO.hdf_to_str import get_hdf_info
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtGui, QtCore
from scipy.optimize import curve_fit


def single_exp_all(x, a, b, c, d):
    return a * np.exp( -2 * (x / b) ** c) + d

def power_law(x, a, b):
    return a * x ** b

class XpcsFile(object):
    def __init__(self, fname, cwd='.', fields=None):
        self.fname = fname
        self.full_path = os.path.join(cwd, fname)
        self.cwd = cwd

        self.type = get_type(self.full_path)
        self.keys, attr = self.load(fields)
        self.__dict__.update(attr)
        self.label = create_id(fname)
        self.hdf_info = None
        self.fit_summary = None

    def __str__(self):
        ans = ['File:' + str(self.full_path)]
        for key, val in self.__dict__.items():
            if key in ['hdf_key', "hdf_info"]:
                continue
            elif isinstance(val, np.ndarray) and val.size > 1:
                val = str(val.shape)
            else:
                val = str(val)
            ans.append(f"   {key.ljust(12)}: {val.ljust(30)}")

        return '\n'.join(ans)
    
    def __repr__(self):
        ans = str(type(self))
        ans = '\n'.join([ans, self.__str__()])
        return ans

    def __add__(self, other):
        pass

    def get_hdf_info(self):
        if self.hdf_info is None:
            self.hdf_info = get_hdf_info(self.cwd, self.fname)
        return self.hdf_info

    def load(self, extra_fields=None):
        # default fields;
        fields = ['saxs_2d', "saxs_1d", 'Iqp', 'ql_sta', 'Int_t',
                  't0', 't1', 'ql_dyn', 'type', 'dqmap']

        if self.type == 'Twotime':
            fields = fields + ['g2_full', 'g2_partials']
        # multitau
        else:
            fields = fields + ['tau', 'g2', 'g2_err']

        # append extra fields, eg 'G2', 'IP', 'IF'
        if isinstance(extra_fields, list):
            fields += extra_fields

        # avoid multiple keys
        fields = list(set(fields))

        ret = get(self.full_path, fields, 'alias')
        ret['dqmap'] = ret['dqmap'].astype(np.uint16)

        if 't0' in ret and 'tau' in ret:
            ret['t_el'] = ret['t0'] * ret['tau']

        if self.type == 'Twotime':
            ret['g2'] = ret['g2_full']
            ret['t_el'] = np.arange(ret['g2'].shape[0]) * ret['t0']
        else:
            ret['g2_err_mod'] = self.correct_g2_err(ret['g2_err'])

        return ret.keys(), ret

    def at(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

    def get_time_scale(self, group='xpcs'):
        # acquire time scale for twotime analysis
        key_frames = [
            '/'.join([group, 'stride_frames']),
            '/'.join([group, 'avg_frames'])
        ]
        stride, avg = get(self.full_path,
                          key_frames,
                          mode='raw',
                          ret_type='list')
        time_scale = max(self.t0, self.t1) * stride * avg
        return time_scale

    def get_twotime_maps(self, group='xpcs'):
        rpath = '/'.join([group, 'output_data'])
        rpath = get(self.full_path, [rpath], mode='raw')[rpath]

        key_dqmap = '/'.join([group, 'dqmap'])
        key_saxs = '/'.join([rpath, 'pixelSum'])

        dqmap, saxs = get(self.full_path, [key_dqmap, key_saxs],
                          mode='raw',
                          ret_type='list')

        if self.type == 'Twotime':
            key_c2t = '/'.join([rpath, 'C2T_all'])
            idlist = get(self.full_path, [key_c2t], mode='raw')[key_c2t]
            idlist = [int(x[3:]) for x in idlist]
        else:
            idlist = [None]
        return dqmap, saxs, rpath, idlist

    def get_twotime_c2(self, twotime_key, plot_index):
        c2_key = '/'.join([twotime_key, 'C2T_all/g2_%05d' % plot_index])

        c2_half = get(self.full_path, [c2_key], mode='raw')[c2_key]

        if c2_half is None:
            return None

        c2 = c2_half + np.transpose(c2_half)
        c2_translate = np.zeros(c2.shape)
        c2_translate[:, 0] = c2[:, -1]
        c2_translate[:, 1:] = c2[:, :-1]
        c2 = np.where(c2 > 1.3, c2_translate, c2)
        return c2

    def get_detector_extent(self):
        fields = [
            'ccd_x0', 'ccd_y0', 'det_dist', 'pix_dim', 'X_energy', 'xdim',
            'ydim'
        ]
        res = get(self.full_path, fields, mode='alias', ret_type='dict')

        wlength = 12.398 / res['X_energy']
        pix2q = res['pix_dim'] / res['det_dist'] * (2 * np.pi / wlength)

        qy_min = (0 - res['ccd_x0']) * pix2q
        qy_max = (res['xdim'] - res['ccd_x0']) * pix2q

        qx_min = (0 - res['ccd_y0']) * pix2q
        qx_max = (res['ydim'] - res['ccd_y0']) * pix2q
        extent = (qy_min, qy_max, qx_min, qx_max)

        return extent

    def plot_saxs2d(self, *args, **kwargs):
        app = QtGui.QApplication([])
        win = QtGui.QMainWindow()
        win.resize(1024, 600)
        hdl = ImageViewDev()
        win.setCentralWidget(hdl)
        win.show()
        win.setWindowTitle(self.label + ': ' + self.fname)
        saxs2d.plot([self.saxs_2d], hdl, *args, **kwargs)
        app.exec_()

    def plot_saxs1d(self, *args, **kwargs):
        app = QtGui.QApplication([])
        win = QtGui.QMainWindow()
        win.resize(1024, 600)
        canvas = MplCanvasBarV()
        win.setCentralWidget(canvas)
        win.show()
        win.setWindowTitle(self.label + ': ' + self.fname)
        saxs1d.plot([self], canvas.hdl, *args, **kwargs)
        app.exec_()

    def plot_intt(self, window=1, sampling=1, **kwargs):
        app = QtGui.QApplication([])
        win = pg.GraphicsLayoutWidget(show=True, title=self.label + '_intt')
        win.resize(1024, 600)
        intt.plot([self], win, [self.label], enable_zoom=True,
                  xlabel='Frame Index', rows=None, window=window,
                  sampling=sampling, **kwargs)
        app.exec_()

    def plot_stability(self, **kwargs):
        app = QtGui.QApplication([])
        win = QtGui.QMainWindow()
        win.resize(1024, 600)
        canvas = MplCanvasBarV()
        win.setCentralWidget(canvas)
        win.show()
        stability.plot(self, canvas.hdl,
                       title='stability plot for %s' % self.label, **kwargs)
        app.exec_()

    def get_pg_tree(self):
        data = self.load()
        n = 0
        for key, val in data.items():
            if isinstance(val, np.ndarray):
                if val.size > 4096:
                    data[key] = 'data size is too large'
                # suqeeze one-element array
                if val.size == 1:
                    data[key] = float(val)

        data['type'] = self.type
        data['label'] = self.label

        tree = pg.DataTreeWidget(data=data)
        tree.setWindowTitle(self.fname)
        tree.resize(600, 800)
        return tree
    
    def fit_g2(self,
               q_range=None,
               t_range=None, 
               bounds=None,
               fit_flag=[True, True, True, True]):

        if q_range is None:
            q_range = [np.min(self.ql_dyn) * 0.95, np.max(self.ql_dyn) * 1.05]
        
        if t_range is None:
            q_range = [np.min(self.t_el) * 0.95, np.max(self.t_el) * 1.05]
        
        # create a data slice for given range;    
        t_slice = create_slice(self.t_el, t_range)
        q_slice = create_slice(self.ql_dyn, q_range)

        t_el = self.t_el[t_slice]
        q = self.ql_dyn[q_slice]
        g2 = self.g2[t_slice, q_slice]
        sigma = self.g2_err_mod[t_slice, q_slice]

        p0 = np.array(bounds).mean(axis=0)
        p0[1] = np.sqrt(bounds[0][1] * bounds[1][1])

        fit_x = np.logspace(np.log10(np.min(t_el)) - 0.5,
                            np.log10(np.max(t_el)) + 0.5, 128)
        fit_line, fit_val = fit_with_fixed(single_exp_all, t_el, g2, sigma,
                                           bounds, fit_flag, fit_x, p0=p0)

        self.fit_summary = {
            'fit_val': fit_val,
            't_el': t_el,
            'q_val': q,
            # 'g2': g2,
            # 'sigma': sigma,
            'q_range': str(q_range),
            't_range': str(t_range),
            'bounds': bounds,
            'fit_flag': str(fit_flag),
            'fit_line': fit_line
        }

        return self.fit_summary

    def correct_g2_err(self, g2_err=None, threshold=1E-6):
        # correct the err for some data points with really small error, which
        # may cause the fitting to blowup

        g2_err_mod = np.copy(g2_err)
        for n in range(g2_err.shape[1]):
            data = g2_err[:, n]
            idx = data > threshold
            avg = np.mean(data[idx])
            g2_err_mod[np.logical_not(idx), n] = avg 

        return g2_err_mod
    
    def fit_tauq(self, q_range, bounds, fit_flag):
        if self.fit_summary is None:
            return
        
        data = self.fit_summary['fit_val']

        x = self.fit_summary['q_val']
        q_slice = create_slice(x, q_range)
        x = x[q_slice]

        y = self.fit_summary['fit_val'][q_slice, 0, 1]
        sigma = self.fit_summary['fit_val'][q_slice, 1, 1]

        y = y.reshape(-1, 1)
        sigma = sigma.reshape(-1, 1)

        p0 = [1.0e-7, -2.0]

        fit_x = np.logspace(np.log10(np.min(x) / 1.1),
                            np.log10(np.max(x) * 1.1), 128)

        fit_line, fit_val = fit_with_fixed(power_law, x, y, sigma, bounds, 
                                           fit_flag, fit_x, p0=p0) 

        # fit_line and fit_val are lists with just one element;
        self.fit_summary['tauq_fit_line'] = fit_line[0]
        self.fit_summary['tauq_fit_val'] = fit_val[0]


def test1():
    cwd = '../../../xpcs_data'
    af = XpcsFile(fname='N077_D100_att02_0128_0001-100000.hdf', cwd=cwd)
    af.plot_saxs2d()


if __name__ == '__main__':
    test1()
