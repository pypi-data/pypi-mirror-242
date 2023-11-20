import random
import numpy as np
import pandas as pd

from ... import reg, aux
from ...param import Larva_Distro
from .larva_robot import LarvaRobot

__all__ = [
    'LarvaOffline',
    'sim_model',
    'sim_models',
]

__displayname__ = 'Offline simulations'


class LarvaOffline(LarvaRobot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fo = self.orientation
        self.ro = self.orientation

    def step(self):
        dt = self.model.dt
        self.cum_dur += dt

        lin, ang, feed = self.brain.locomotor.step(A_in=0, length=self.length)
        self.lin_vel = lin * self.lin_vel_coef
        self.ang_vel = self.compute_ang_vel(ang)

        ang_vel_min, ang_vel_max = (-np.pi + self.body_bend) / self.model.dt, (np.pi + self.body_bend) / self.model.dt
        if self.ang_vel < ang_vel_min:
            self.ang_vel = ang_vel_min
        elif self.ang_vel > ang_vel_max:
            self.ang_vel = ang_vel_max

        self.fo = (self.fo + self.ang_vel * dt) % (2 * np.pi)
        self.dst = self.lin_vel * dt
        delta_ro = self.compute_delta_rear_angle(self.body_bend, self.dst, self.length)

        self.ro = (self.ro + delta_ro) % (2 * np.pi)
        self.body_bend = aux.wrap_angle_to_0(self.fo - self.ro)
        self.cum_dst += self.dst
        k1 = np.array([np.cos(self.fo), np.sin(self.fo)])

        self.set_position(tuple(self.pos + k1 * self.dst))
        self.set_orientation(self.fo)
        self.set_angularvelocity(self.ang_vel)
        self.set_linearvelocity(self.lin_vel)

        self.trajectory.append(self.pos)


def sim_models(modelIDs, colors=None, groupIDs=None, lgs=None, data_dir=None, **kwargs):
    N = len(modelIDs)
    if colors is None:
        colors = aux.N_colors(N)
    if groupIDs is None:
        groupIDs = modelIDs
    if lgs is None:
        lgs = [None] * N
    if data_dir is None:
        dirs = [None] * N
    else:
        dirs = [f'{data_dir}/{dID}' for dID in groupIDs]
    ds = [sim_model(mID=modelIDs[i], color=colors[i], dataset_id=groupIDs[i], lg=lgs[i], dir=dirs[i], **kwargs) for i in
          range(N)]
    return ds


def sim_model(mID, Nids=1, refID=None, refDataset=None, imitation=False,
              tor_durs=[], dsp_starts=[0], dsp_stops=[40], enrichment=True, parameter_dict={},
              lg=None, env_params={}, dir=None, duration=3, dt=1 / 16, color='blue', dataset_id=None,
              **kwargs):
    Nticks = int(duration * 60 / dt)
    if refDataset is None and refID is not None:
        refID = refDataset.refID
    if lg is None:
        lg = reg.generators.LarvaGroup(group_id=dataset_id, model=mID, color=color,
                                       distribution=Larva_Distro(N=Nids), sample=refID,
                                       imitation=imitation)
    ids, p0s, fo0s, ms = lg.generate_agent_attrs(parameter_dict)
    s, e = sim_multi_agents(Nticks, Nids, ms, lg.group_id, dt=dt, ids=ids, p0s=p0s, fo0s=fo0s)

    c_kws = {
        'dir': dir,
        'id': lg.group_id,
        'larva_group': lg,
        'env_params': env_params,
        'Npoints': 3,
        'Ncontour': 0,
        'fr': 1 / dt,
    }
    from ...process.dataset import LarvaDataset
    d = LarvaDataset(**c_kws, load_data=False)
    d.set_data(step=s, end=e)
    if enrichment:
        d = d.enrich(proc_keys=['spatial', 'angular', 'dispersion', 'tortuosity'],
                     anot_keys=['bout_detection', 'bout_distribution', 'interference'],
                     dsp_starts=dsp_starts, dsp_stops=dsp_stops, tor_durs=tor_durs)

    return d


def sim_single_agent(m, Nticks=1000, dt=0.1, df_columns=None, p0=None, fo0=None):
    from ..modules.locomotor import DefaultLocomotor
    from ._larva_sim import BaseController
    if fo0 is None:
        fo0 = 0.0
    if p0 is None:
        p0 = (0.0, 0.0)
    x0, y0 = p0
    if df_columns is None:
        df_columns = reg.getPar(['b', 'fo', 'ro', 'fov', 'I_T', 'x', 'y', 'd', 'v', 'A_T'])
    AA = np.ones([Nticks, len(df_columns)]) * np.nan

    controller = BaseController(**m.physics)
    l = m.body.length
    bend_errors = 0
    DL = DefaultLocomotor(dt=dt, conf=m.brain)
    for qq in range(100):
        if random.uniform(0, 1) < 0.5:
            DL.step(A_in=0, length=l)
    b, fo, ro, fov, x, y, dst, v = 0, fo0, 0, 0, x0, y0, 0, 0
    for i in range(Nticks):
        lin, ang, feed = DL.step(A_in=0, length=l)
        v = lin * controller.lin_vel_coef
        fov += (-controller.ang_damping * fov - controller.body_spring_k * b + ang * controller.torque_coef) * dt

        d_or = fov * dt
        if np.abs(d_or) > np.pi:
            bend_errors += 1
        dst = v * dt
        d_ro = controller.compute_delta_rear_angle(b, dst, l)
        b = aux.wrap_angle_to_0(b + d_or - d_ro)
        fo = (fo + d_or) % (2 * np.pi)
        ro = (ro + d_ro) % (2 * np.pi)
        x += dst * np.cos(fo)
        y += dst * np.sin(fo)

        AA[i, :] = [b, fo, ro, fov, DL.turner.input, x, y, dst, v, DL.turner.output]

    AA[:, :4] = np.rad2deg(AA[:, :4])
    return AA


def sim_multi_agents(Nticks, Nids, ms, group_id, dt=0.1, ids=None, p0s=None, fo0s=None):
    df_columns = reg.getPar(['b', 'fo', 'ro', 'fov', 'I_T', 'x', 'y', 'd', 'v', 'A_T'])
    if ids is None:
        ids = [f'{group_id}{j}' for j in range(Nids)]
    if p0s is None:
        p0s = [(0.0, 0.0) for j in range(Nids)]
    if fo0s is None:
        fo0s = [0.0 for j in range(Nids)]
    my_index = pd.MultiIndex.from_product([np.arange(Nticks), ids], names=['Step', 'AgentID'])
    AA = np.ones([Nticks, Nids, len(df_columns)]) * np.nan

    for j, id in enumerate(ids):
        m = ms[j]
        AA[:, j, :] = sim_single_agent(m, Nticks, dt=dt, df_columns=df_columns, p0=p0s[j], fo0=fo0s[j])

    AA = AA.reshape(Nticks * Nids, len(df_columns))
    s = pd.DataFrame(AA, index=my_index, columns=df_columns)
    s = s.astype(float)

    e = pd.DataFrame(index=ids)
    e['cum_dur'] = Nticks * dt
    e['num_ticks'] = Nticks
    e['length'] = [m.body.length for m in ms]

    from ...process.spatial import scale_to_length
    scale_to_length(s, e, keys=['v'])
    return s, e
