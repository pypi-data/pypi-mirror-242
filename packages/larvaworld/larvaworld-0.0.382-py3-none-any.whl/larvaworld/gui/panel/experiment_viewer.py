import pandas as pd
import panel as pn
import numpy as np
import holoviews as hv
from panel.template import DarkTheme

pn.extension()

from larvaworld.lib import reg, aux, model, sim, screen
# from larvaworld.lib.param import SimOps

__all__ = [
    'ArenaViewer',
]

class ArenaViewer:

    def __init__(self, img_width=600, experiment='dish',duration=1,**kwargs):
        self.size = img_width
        self.launcher=sim.ExpRun(experiment=experiment,duration=duration,**kwargs)
        self.env=self.launcher.p.env_params
        x, y = self.env.arena.dims
        self.image_kws = {
            'title': f'Arena viewer',
            'xlim': (-x / 2, x / 2),
            'ylim': (-y / 2, y / 2),
            'width': self.size,
            'height': int(self.size*y/x),
            'xlabel': 'X (m)',
            'ylabel': 'Y (m)',
        }

        self.draw_ops=screen.AgentDrawOps(draw_centroid=True, draw_segs=False)
        self.Nfade=int(self.draw_ops.trail_dt / self.launcher.dt)

        #self.app=self.get_app()
        # self.app.servable()

    def get_tank_plot(self):
        a = self.env.arena
        if a.geometry == 'circular':
            tank = hv.Ellipse(0, 0, a.dims[0]).opts(line_width=5, bgcolor='lightgrey')
        elif a.geometry == 'rectangular':
            tank = hv.Box(0, 0, spec=a.dims).opts(line_width=5, bgcolor='lightgrey')
        else:
            raise ValueError('Not implemented')
        return tank

    def draw_imgs(self):
        agents=self.launcher.agents
        sources=self.launcher.sources
        d=aux.AttrDict({
            'draw_segs' : np.multiply([hv.Polygons([seg.vertices for seg in a.segs]).opts(color=a.color) for a in agents]),
            'draw_centroid' : hv.Points(agents.get_position()).opts(size=5, color='black'),
            'draw_head' : hv.Points(agents.head.front_end).opts(size=5, color='red'),
            'draw_midline' : np.multiply([hv.Path(a.midline_xy).opts(color='blue',line_width=2)  for a in agents]),
            'visible_trails' :  hv.Contours([a.trajectory[-self.Nfade:] for a in agents]).opts(color='black'),
        })
        source_img = np.multiply([hv.Ellipse(s.pos[0], s.pos[1], s.radius * 2).opts(line_width=5, color=s.color, bgcolor=s.color) for s in sources])
        return np.multiply([self.tank_plot,source_img]+[img for k,img in d.items() if self.draw_ops[k]]).opts(responsive=False, **self.image_kws)

    def get_app(self):
        self.launcher.sim_setup(steps=self.launcher.p.steps)
        slider_kws = {
            'width': int(self.size/2),
            'start': 0,
            'end': self.launcher.Nsteps-1,
            'interval':  int(1000*self.launcher.dt),
            'value': 0,
            # 'step': 5,
            # 'loop_policy': 'loop',

        }
        progress_kws = {
            'width': int(self.size / 2),
            'max': self.launcher.Nsteps - 1,
            'value': self.launcher.t,
        }
        self.progress_bar = pn.widgets.Progress(bar_color="primary",**progress_kws)
        time_slider = pn.widgets.Player(**slider_kws)
        self.tank_plot=self.get_tank_plot()
        @pn.depends(i=time_slider)
        def get_image(i):
            while i>self.launcher.t :
                self.launcher.sim_step()
                self.progress_bar.value=self.launcher.t
                return self.draw_imgs()


            # overlay = self.tank_plot
            # agents=self.launcher.agents
            # if draw_ops.draw_segs:
            #     for a in agents:
            #         segpolys = hv.Polygons([seg.vertices for seg in a.segs]).opts(color=a.color)
            #         overlay *= segpolys
            # if draw_ops.draw_centroid:
            #     points = hv.Points(agents.get_position()).opts(size=5, color='black')
            #     overlay*=points
            # if draw_ops.draw_head:
            #     hpoints = hv.Points(agents.head.front_end).opts(size=5, color='red')
            #     overlay *= hpoints
            # if draw_ops.draw_midline:
            #     for a in agents:
            #         mid = hv.Path(a.midline_xy).opts(color='blue',line_width=2)
            #         overlay *= mid
            # if draw_ops.trails:
            #     Nfade = int(draw_ops.trajectory_dt / self.launcher.dt)
            #
            #     _paths = [a.trajectory[-Nfade:] for a in agents]
            #     paths = hv.Contours(_paths).opts(color='black')
            #     overlay *= paths
            #
            # for s in self.launcher.sources:
            #     source = hv.Ellipse(s.pos[0], s.pos[1], s.radius*2).opts(line_width=5,color=s.color, bgcolor=s.color)
            #     overlay *= source


            # overlay.opts(responsive=False, **self.image_kws)
            #
            # return overlay

        img_dmap = hv.DynamicMap(get_image)
        app = pn.Row(img_dmap, pn.Column(
            pn.Row(pn.Column('Tick', time_slider)),
            pn.Row(pn.Column('Simulation timestep', self.progress_bar)),
            pn.Param(self.draw_ops),
        ))
        return app


if __name__ == "__main__":
    v=ArenaViewer()
    app = v.get_app()
    app.servable()

