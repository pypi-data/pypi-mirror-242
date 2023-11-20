import random
from typing import Tuple, List
import numpy as np
import param

from .. import reg, aux
from ..aux import nam
from ..param.param_aux import vpar, get_vfunc

__all__ = [
    'SAMPLING_PARS',
    'init2mdict',
    'gConf',
    'get_ks',
    'LarvaworldParam',
    'get_LarvaworldParam',
    'prepare_LarvaworldParam',
    'build_LarvaworldParam',
]


def init2mdict(d0):
    def check(D0):
        D = {}
        for kk, vv in D0.items():
            if not isinstance(vv, dict):
                pass
            elif 'dtype' in vv and vv['dtype'] == dict:
                mdict = check(vv)
                vv0 = {kkk: vvv for kkk, vvv in vv.items() if kkk not in mdict}
                if 'v0' not in vv0:
                    vv0['v0'] = gConf(mdict)
                D[kk] = build_LarvaworldParam(p=kk, mdict=mdict, **vv0)

            elif any([a in vv for a in ['symbol', 'h', 'label', 'disp', 'k']]):
                D[kk] = build_LarvaworldParam(p=kk, **vv)

            else:
                D[kk] = check(vv)
        return D

    d = check(d0)
    return aux.AttrDict(d)


def gConf(mdict, **kwargs):
    if mdict is None:
        return None
    elif isinstance(mdict, param.Parameterized):
        return mdict.v
    elif isinstance(mdict, dict):
        conf = aux.AttrDict()
        for d, p in mdict.items():
            if isinstance(p, param.Parameterized):
                conf[d] = p.v
            else:
                conf[d] = gConf(mdict=p)
            conf.update_existingdict(kwargs)
        return conf
    else:
        return aux.AttrDict(mdict)


def get_ks(d0, k0=None, ks=[]):
    for k, p in d0.items():
        if k0 is not None:
            k = f'{k0}.{k}'
        if isinstance(p, param.Parameterized):
            ks.append(k)
        else:
            ks = get_ks(p, k0=k, ks=ks)
    return ks


class LarvaworldParam(param.Parameterized):
    p = param.String(default='', doc='Name of the parameter')
    d = param.String(default='', doc='Dataset name of the parameter')
    disp = param.String(default='', doc='Displayed name of the parameter')
    k = param.String(default='', doc='Key of the parameter')
    sym = param.String(default='', doc='Symbol of the parameter')
    codename = param.String(default='', doc='Name of the parameter in code')
    flatname = param.String(default=None, doc='Name of the parameter in model configuration')
    dtype = param.Parameter(default=float, doc='Data type of the parameter value')
    mdict = param.Dict(default=None, doc='The parameter dict in case of a dict header', allow_None=True)
    func = param.Callable(default=None, doc='Function to get the parameter from a dataset', allow_None=True)
    required_ks = param.List(default=[], doc='Keys of prerequired parameters for computation in a dataset')

    @property
    def s(self):
        return self.disp

    @property
    def l(self):
        return self.disp + '  ' + self.ulabel

    @property
    def symunit(self):
        return self.sym + '  ' + self.ulabel

    @property
    def ulabel(self):
        if self.u == reg.units.dimensionless:
            return ''
        else:
            return '(' + self.unit + ')'

    @property
    def unit(self):
        if self.u == reg.units.dimensionless:
            return '-'
        else:
            return fr'${self.u}$'

    @property
    def upint(self):
        try:
            from pint_pandas import PintType
            ustring = f'pint[{self.u}]'
            return PintType(ustring)
        except:
            return self.u

    @property
    def short(self):
        return self.k

    @property
    def gConf(self):
        if self.mdict is None:
            return None
        else:
            return gConf(self.mdict)

    @property
    def v0(self):
        return self.param.v.default

    @property
    def initial_value(self):
        return self.param.v.default

    @property
    def value(self):
        return self.v

    @property
    def symbol(self):
        return self.sym

    @property
    def label(self):
        return self.param.v.label

    @property
    def parameter(self):
        return self.disp

    # @property
    # def lab(self):
    #     return self.l

    @property
    def tooltip(self):
        return self.param.v.doc

    @property
    def description(self):
        return self.param.v.doc

    @property
    def help(self):
        return self.param.v.doc

    @property
    def parclass(self):
        return type(self.param.v)

    @property
    def min(self):
        try:
            vmin, vmax = self.param.v.bounds
            return vmin
        except:
            return None

    @property
    def max(self):
        try:
            vmin, vmax = self.param.v.bounds
            return vmax
        except:
            return None

    @property
    def lim(self):
        try:
            lim = self.param.v.bounds
            return lim
        except:
            return None

    @property
    def step(self):
        if self.parclass in [param.Number, param.Range] and self.param.v.step is not None:
            return self.param.v.step
        elif self.parclass == param.Magnitude:
            return 0.01
        elif self.dtype in [float, List[float], List[Tuple[float]], Tuple[float]]:
            return 0.01
        else:
            return None

    @property
    def Ndec(self):
        if self.step is not None:
            return str(self.step)[::-1].find('.')
        else:
            return None

    def exists(self, dataset):
        return aux.AttrDict({'step': self.d in dataset.step_ps, 'end': self.d in dataset.end_ps})

    def get(self, dataset, compute=True):
        res = self.exists(dataset)
        for key, exists in res.items():
            if exists:
                return dataset.get_par(key=key, par=self.d)

        if compute:
            self.compute(dataset)
            return self.get(dataset, compute=False)
        else:
            print(f'Parameter {self.disp} not found')

    def compute(self, dataset):
        if self.func is not None:
            self.func(dataset)
        else:
            print(f'Function to compute parameter {self.disp} is not defined')

    def randomize(self):
        p = self.parclass
        if p == param.Number:
            vmin, vmax = self.param.v.bounds
            self.v = self.param.v.crop_to_bounds(np.round(random.uniform(vmin, vmax), self.Ndec))
        elif p == param.Integer:
            vmin, vmax = self.param.v.bounds
            self.v = random.randint(vmin, vmax)
        elif p == param.Magnitude:
            self.v = np.round(random.uniform(0.0, 1.0), self.Ndec)
        elif p == param.Selector:
            self.v = random.choice(self.param.v.objects)
        elif p == param.Boolean:
            self.v = random.choice([True, False])
        elif p == param.Range:
            vmin, vmax = self.param.v.bounds
            vv0 = np.round(random.uniform(vmin, vmax), self.Ndec)
            vv1 = np.round(random.uniform(vv0, vmax), self.Ndec)

            self.v = (vv0, vv1)

    def mutate(self, Pmut, Cmut):
        if random.random() < Pmut:
            if self.parclass in [param.Magnitude] +param.Magnitude.__subclasses__():
                v0 = self.v if self.v is not None else 0.5
                vv = random.gauss(v0, Cmut)
                self.v = self.param.v.crop_to_bounds(np.round(vv, self.Ndec))
                # self.v = np.round(self.v, self.Ndec)
            elif self.parclass in [param.Integer] +param.Integer.__subclasses__():
                vmin, vmax = self.param.v.bounds
                vr = np.abs(vmax - vmin)
                v0 = self.v if self.v is not None else int(vmin + vr / 2)
                vv = random.gauss(v0, Cmut * vr)
                self.v = self.param.v.crop_to_bounds(int(vv))
            elif self.parclass in [param.Number] +param.Number.__subclasses__():

                vmin, vmax = self.param.v.bounds
                vr = np.abs(vmax - vmin)
                v0 = self.v if self.v is not None else vmin + vr / 2
                vv = random.gauss(v0, Cmut * vr)
                self.v = self.param.v.crop_to_bounds(np.round(vv, self.Ndec))
            elif self.parclass in [param.Selector] +param.Selector.__subclasses__():
                self.v = random.choice(self.param.v.objects)
            elif self.parclass == param.Boolean:
                self.v = random.choice([True, False])
            elif self.parclass in [param.Range] +param.Range.__subclasses__():
                vmin, vmax = self.param.v.bounds
                vr = np.abs(vmax - vmin)
                v0, v1 = self.v if self.v is not None else (vmin, vmax)
                vv0 = random.gauss(v0, Cmut * vr)
                vv1 = random.gauss(v1, Cmut * vr)
                vv0 = np.round(np.clip(vv0, a_min=vmin, a_max=vmax), self.Ndec)
                vv1 = np.round(np.clip(vv1, a_min=vv0, a_max=vmax), self.Ndec)
                self.v = (vv0, vv1)


def get_LarvaworldParam(vparfunc, v0=None, dv=None, u_name=None, **kws):
    class _LarvaworldParam(LarvaworldParam):
        v = vparfunc
        u = param.Parameter(default=reg.units.dimensionless, doc='Unit of the parameter values', label=u_name)

    par = _LarvaworldParam(**kws)
    return par


SAMPLING_PARS = aux.bidict(
    aux.AttrDict(
        {
            'length': 'body.length',
            nam.freq(nam.scal(nam.vel(''))): 'brain.crawler_params.freq',
            nam.mean(nam.scal(nam.chunk_track('stride', nam.dst('')))): 'brain.crawler_params.stride_dst_mean',
            nam.std(nam.scal(nam.chunk_track('stride', nam.dst('')))): 'brain.crawler_params.stride_dst_std',
            nam.freq('feed'): 'brain.feeder_params.freq',
            nam.max(nam.chunk_track('stride', nam.scal(nam.vel('')))): 'brain.crawler_params.max_scaled_vel',
            aux.nam.phi(aux.nam.max(aux.nam.scal(aux.nam.vel('')))): 'brain.crawler_params.max_vel_phase',
            'attenuation': 'brain.interference_params.attenuation',
            nam.max('attenuation'): 'brain.interference_params.attenuation_max',
            nam.freq(nam.vel(nam.orient(('front')))): 'brain.turner_params.freq',
            aux.nam.phi(nam.max('attenuation')): 'brain.interference_params.max_attenuation_phase',
        }
    )
)


def prepare_LarvaworldParam(p, k=None, dtype=float, d=None, disp=None, sym=None, symbol=None, codename=None, lab=None,
                            h=None,
                            u_name=None, mdict=None, flatname=None,
                            required_ks=[], u=reg.units.dimensionless, v0=None, v=None, lim=None, dv=None, vs=None,
                            vfunc=None, vparfunc=None, func=None, **kwargs):
    '''
    Method that formats the dictionary of attributes for a parameter in order to create a LarvaworldParam instance
    '''
    codename = p if codename is None else codename
    d = p if d is None else d
    disp = d if disp is None else disp
    k = k if k is not None else d
    v0 = v if v is not None else v0

    if flatname is None :
        if p in SAMPLING_PARS:
            flatname = SAMPLING_PARS[p]
        else:
            flatname = p

    if sym is None:
        if symbol is not None:
            sym = symbol
        else:
            sym = k

    if lab is None:
        if u == reg.units.dimensionless:
            lab = f'{disp}'
        else:
            ulab = fr'${u}$'
            lab = fr'{disp} ({ulab})'
    if dv is None and dtype in [float, List[float], List[Tuple[float]], Tuple[float]]:
        dv = 0.01
    h = lab if h is None else h

    if vparfunc is None:

        if vfunc is None:
            vfunc = get_vfunc(dtype=dtype, lim=lim, vs=vs)
        vparfunc = vpar(vfunc, v0, h, lab, lim, dv, vs)
    else:
        vparfunc = vparfunc()

    return aux.AttrDict({
        'name': p,
        'p': p,
        'd': d,
        'k': k,
        'disp': disp,
        'sym': sym,
        'codename': codename,
        'flatname': flatname,
        'dtype': dtype,
        'func': func,
        'u': u,
        'u_name': u_name,
        'required_ks': required_ks,
        'vparfunc': vparfunc,
        'mdict': mdict,
        'dv': dv,
        'v0': v0,

    })


def build_LarvaworldParam(p, **kwargs):
    pre_p = prepare_LarvaworldParam(p=p, **kwargs)
    return get_LarvaworldParam(**pre_p)
