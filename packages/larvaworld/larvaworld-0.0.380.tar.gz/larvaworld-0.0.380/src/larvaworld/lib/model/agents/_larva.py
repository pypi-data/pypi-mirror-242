import math
from copy import deepcopy
import numpy as np

from ... import reg, aux
from . import Source, MobileAgent
from ...param import SegmentedBodySensored, Contour

__all__ = [
    'Larva',
    'LarvaContoured',
    'LarvaSegmented',
    'LarvaMotile',
]

__displayname__ = 'Larva agent'


class Larva(MobileAgent):
    """A Larva as a mobile agent.

    Args:
        model (larvaworld.lib.model.Model) : The model containing this agent.
        unique_id (str) : The unique identifier for this agent.
        **kwargs (dict) : Additional keyword arguments.

    """

    def __init__(self, model=None, unique_id=None, **kwargs):
        if unique_id is None and model:
            unique_id = model.next_id(type='Larva')
        super().__init__(unique_id=unique_id, model=model, **kwargs)
        self.trajectory = [self.initial_pos]
        self.orientation_trajectory = [self.initial_orientation]
        self.cum_dur = 0

    def draw(self, v, **kwargs):
        p, c, r, l = self.get_position(), self.color, self.radius, self.length
        mid = self.midline_xy
        if np.isnan(p).all():
            return
        if v.manager.draw_centroid:
            v.draw_circle(p, r / 4, c, True, r / 10)

        if v.manager.draw_midline:
            if not any(np.isnan(np.array(mid).flatten())):
                Nmid = len(mid)
                v.draw_polyline(mid, color=(0, 0, 255), closed=False, width=l / 20)
                for i, xy in enumerate(mid):
                    c = 255 * i / (Nmid - 1)
                    v.draw_circle(xy, l / 30, color=(c, 255 - c, 0), width=l / 40)

        if v.manager.draw_head:
            v.draw_circle(mid[0], l / 4, color=(255, 0, 0), width=l / 12)

        if v.manager.visible_trails:
            Nfade = int(v.manager.trail_dt / self.model.dt)
            traj = self.trajectory[-Nfade:]
            or_traj = self.orientation_trajectory[-Nfade:]
            if not np.isnan(traj).any():
                parsed_traj = [traj]
                parsed_or_traj = [or_traj]
            elif np.isnan(traj).all():
                return
            # This is the case for larva trajectories derived from experiments where some values are np.nan
            else:
                ds, de = aux.parse_array_at_nans(np.array(traj)[:, 0])
                parsed_traj = [traj[s:e] for s, e in zip(ds, de)]
                parsed_or_traj = [or_traj[s:e] for s, e in zip(ds, de)]
            Npars = len(parsed_traj)
            for i in range(Npars):
                t = parsed_traj[i]
                or_t = parsed_or_traj[i]
                # If trajectory has one point, skip
                if len(t) < 2:
                    pass
                else:
                    if v.manager.trail_color == 'normal':
                        color = self.color
                    elif v.manager.trail_color == 'linear':
                        color = aux.scaled_velocity_to_col(aux.eudist(np.array(t)) / self.length / self.model.dt)
                    elif v.manager.trail_color == 'angular':
                        color = aux.angular_velocity_to_col(np.diff(np.array(or_t)) / self.model.dt)
                    else:
                        raise

                    try:
                        v.draw_polyline(t, color=color, width=0.0005)
                    except:
                        pass

        if v.manager.draw_orientations:
            p02 = [p[0] + math.cos(self.front_orientation) * l,
                   p[1] + math.sin(self.front_orientation) * l]
            v.draw_line(p, p02, color='green', width=l / 10)
            p12 = [p[0] - math.cos(self.rear_orientation) * l,
                   p[1] - math.sin(self.rear_orientation) * l]
            v.draw_line(p, p12, color='red', width=l / 10)
        super().draw(v, **kwargs)


class LarvaContoured(Larva, Contour):
    """A larva surrounded by a contour."""

    __displayname__ = 'Contoured larva'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self, v, **kwargs):
        if v.manager.draw_contour:
            Contour.draw(self, v, **kwargs)
        super().draw(v, **kwargs)

    def draw_selected(self, v, **kwargs):
        v.draw_polygon(vertices=self.vertices, color=v.manager.selection_color,
                       filled=False, width=0.0002)


class LarvaSegmented(Larva, SegmentedBodySensored):
    """A larva with a segmented body, possibly bearing sensors."""

    __displayname__ = 'Segmented larva'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_color(self.default_color)

    def draw(self, v, **kwargs):
        if v.manager.draw_sensors:
            self.draw_sensors(v, **kwargs)
        if v.manager.draw_contour:
            self.draw_segs(v, **kwargs)
        super().draw(v, **kwargs)

    def set_default_color(self, color):
        super().set_default_color(color)
        self.segs.set_default_color(color)

    def invert_default_color(self):
        super().invert_default_color()
        self.segs.set_default_color(self.default_color)

    def draw_selected(self, v, **kwargs):
        v.draw_polygon(vertices=self.get_shape(), color=v.manager.selection_color,
                       filled=False, width=0.0002)


class LarvaMotile(LarvaSegmented):
    """ A larva with a segmented body, sensors, a brain, energetics, and life history.

    Args:
        brain (larvaworld.lib.model.modules.brain.BrainConfiguration) :
        The configuration for the larva's brain.
        energetics (larvaworld.lib.model.deb.deb.EnergeticsParameters) :
        The energetics parameters for the larva. Defaults to None.
        life_history  (dict) : The life history of the larva. Defaults to None.
        **kwargs (dict) : Additional keyword arguments.
    """

    __displayname__ = 'Behaving & growing larva'

    def __init__(self, brain, energetics, life_history, body, **kwargs):
        super().__init__(**body, **kwargs)
        self.carried_objects = []
        self.brain = self.build_brain(brain)
        self.build_energetics(energetics, life_history=life_history)
        self.food_detected, self.feeder_motion = None, False
        self.cum_food_detected, self.amount_eaten = 0, 0

    def build_brain(self, conf):
        """Build the brain for the larva agent."""

        if conf.nengo:
            from larvaworld.lib.model.modules.nengobrain import NengoBrain
            return NengoBrain(agent=self, conf=conf, dt=self.model.dt)
        else:
            from larvaworld.lib.model.modules.brain import DefaultBrain
            return DefaultBrain(agent=self, conf=conf, dt=self.model.dt)

    def feed(self, source, motion):

        def get_max_V_bite():
            return self.brain.locomotor.feeder.V_bite * self.V * 1000  # ** (2 / 3)

        if motion:
            a_max = get_max_V_bite()
            if source is not None:
                grid = self.model.food_grid
                if grid:
                    V = -grid.add_cell_value(source, -a_max)
                else:
                    V = source.subtract_amount(a_max)

                return V
            else:
                return 0
        else:
            return 0

    def build_energetics(self, energetic_pars, life_history):
        from larvaworld.lib.model.deb.deb import DEB_runner
        if energetic_pars is not None:
            self.deb = DEB_runner(model=self.model, id=self.unique_id,
                                  life_history=life_history, gut_params=energetic_pars.gut,
                                  **energetic_pars.DEB)
            self.length = self.deb.Lw * 10 / 1000
            self.mass = self.deb.Ww
            self.V = self.deb.V
            try:
                self.deb.set_intermitter(self.brain.locomotor.intermitter)
            except:
                pass
        else:
            self.deb = None
            self.V = self.length ** 3
            self.mass = None
            self.length = None

    def run_energetics(self, V_eaten):
        self.deb.update(V_eaten)
        self.length = self.deb.Lw * 10 / 1000
        self.mass = self.deb.Ww
        self.V = self.deb.V
        # TODO add this again
        # self.adjust_body_vertices()

    def get_feed_success(self, t):
        if self.feeder_motion:
            if self.on_food:
                return 1
            else:
                return -1
        else:
            return 0

    @property
    def on_food_dur_ratio(self):
        return self.cum_food_detected * self.model.dt / self.cum_dur if self.cum_dur != 0 else 0

    @property
    def on_food(self):
        return self.food_detected is not None

    def get_on_food(self, t):
        return self.on_food

    @property
    def scaled_amount_eaten(self):
        return self.amount_eaten / self.mass

    def resolve_carrying(self, food):
        gain_for_base_odor = 100.0
        if food is None or not isinstance(food, Source):
            return
        if food.can_be_carried and food not in self.carried_objects:
            if food.is_carried_by is not None:
                prev_carrier = food.is_carried_by
                if prev_carrier == self:
                    return
                prev_carrier.carried_objects.remove(food)
                prev_carrier.brain.olfactor.reset_all_gains()
            food.is_carried_by = self
            self.carried_objects.append(food)
            if self.model.experiment == 'capture_the_flag':
                self.brain.olfactor.set_gain(gain_for_base_odor, f'{self.group}_base_odor')
            elif self.model.experiment == 'keep_the_flag':
                carrier_group = self.group
                carrier_group_odor_id = self.odor.id
                if carrier_group == 'Left':
                    opponent_group = 'Right'
                elif carrier_group == 'Right':
                    opponent_group = 'Left'
                else:
                    raise ValueError(f'Argument {carrier_group} is neither Left nor Right')

                opponent_group_odor_id = f'{opponent_group}_odor'
                for f in self.model.agents:
                    if f.group == carrier_group:
                        f.brain.olfactor.set_gain(gain_for_base_odor, opponent_group_odor_id)
                    else:
                        f.brain.olfactor.set_gain(0.0, carrier_group_odor_id)
                self.brain.olfactor.set_gain(-gain_for_base_odor, opponent_group_odor_id)

        for o in self.carried_objects:
            o.pos = self.pos

    def update_behavior_dict(self, mode='lin'):
        inter = self.brain.locomotor.intermitter
        if mode == 'lin' and inter is not None:
            s, f, p, r = inter.active_bouts
            if s or r:
                color = np.array([0, 150, 0])
            elif p:
                color = np.array([255, 0, 0])
            elif f:
                color = np.array([0, 0, 255])
            else:
                raise
        elif mode == 'ang':
            color = deepcopy(self.default_color)
            orvel = self.front_orientation_vel
            if orvel > 0:
                color[2] = 150
            elif orvel < 0:
                color[2] = 50
        else:
            raise
        self.set_color(color)

    def sense(self):
        pass

    # @profile
    def step(self):
        self.cum_dur += self.model.dt
        self.sense()
        pos = self.olfactor_pos

        if self.model.space.accessible_sources:
            self.food_detected = self.model.space.accessible_sources[self]

        elif self.brain.locomotor.feeder or self.brain.toucher:
            self.food_detected = aux.sense_food(pos, sources=self.model.sources, grid=self.model.food_grid,
                                                radius=self.radius)
        self.resolve_carrying(self.food_detected)

        lin, ang, self.feeder_motion = self.brain.step(pos, length=self.length, on_food=self.on_food)
        self.prepare_motion(lin=lin, ang=ang)

        V = self.feed(self.food_detected, self.feeder_motion)
        self.amount_eaten += V * 1000
        self.cum_food_detected += int(self.on_food)
        if self.deb is not None:
            self.run_energetics(V)

        try:
            if self.model.screen_manager.color_behavior:
                self.update_behavior_dict()
            else:
                self.color = self.default_color
        except:
            pass

    def prepare_motion(self, lin, ang):
        pass
        # Overriden by subclasses
