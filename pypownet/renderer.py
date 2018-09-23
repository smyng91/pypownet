from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Rectangle

__author__ = 'marvinler'
# Copyright (C) 2017-2018 RTE and INRIA (France)
# Authors: Marvin Lerousseau <marvin.lerousseau@gmail.com>
# This file is under the LGPL-v3 license and is part of PyPowNet.
import pygame
import math
from pygame import gfxdraw
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import pylab
from copy import deepcopy

case_layouts = {
    14: [(-280, -81), (-100, -270), (366, -270), (366, -54), (-64, -54), (-64, 54), (366, 0), (438, 0), (326, 54),
         (222, 108), (79, 162), (-152, 270), (-64, 270), (222, 216)],

    30: [(-320, -217), (-188, -306), (-191, -221), (-64, -220), (156, -307), (223, -232), (217, -274), (401, -236),
         (200, -145), (238, -125), (87, -143), (-60, -113), (-185, -114), (-159, -60), (-62, 12), (-13, -73),
         (102, -54), (89, 26), (281, 37), (240, 9), (278, -27), (322, -44), (99, 74), (328, 74), (219, 144), (97, 147),
         (101, 215), (400, 195), (-179, 211), (-181, 136)]
    ,

    96: [(49.0, -243.0), (95.5, -242.5), (24.5, -195.5), (41.5, -216.0), (87.5, -220.5), (154.0, -205.0),
         (132.0, -243.0), (154.5, -228.0), (80.0, -196.5), (121.5, -197.0), (77.0, -163.5), (121.0, -163.0),
         (164.0, -120.0), (65.5, -125.0), (29.5, -143.0), (25.5, -116.0), (13.5, -84.0), (44.0, -64.5),
         (83.0, -106.5), (111.0, -105.5), (80.0, -65.5), (117.5, -65.5), (149.0, -93.0), (24.5, -163.5),
         (252.0, -242.0), (295.0, -241.5), (221.5, -195.5), (245.0, -216.0), (291.0, -219.5), (357.5, -203.5),
         (335.0, -240.5), (357.5, -227.0), (283.0, -196.5), (326.0, -195.5), (281.5, -163.0), (325.5, -162.5),
         (367.5, -120.5), (268.0, -125.0), (230.0, -142.5), (225.0, -115.5), (216.5, -81.5), (248.0, -64.0),
         (285.5, -105.0), (318.5, -105.0), (282.5, -64.0), (322.0, -64.0), (352.0, -93.0), (226.0, -164.0),
         (449.0, -243.0), (493.0, -243.0), (427.0, -196.5), (444.0, -216.0), (490.5, -219.5), (555.5, -205.0),
         (532.0, -242.5), (557.5, -224.5), (481.0, -197.0), (524.5, -196.0), (480.5, -163.5), (540.5, -162.5),
         (566.5, -121.0), (467.5, -126.0), (431.0, -143.5), (426.0, -114.5), (415.5, -83.5), (447.5, -64.0),
         (484.5, -106.0), (517.5, -106.0), (483.0, -64.0), (520.0, -64.5), (553.0, -94.0), (426.0, -164.0),
         (379.0, -28.0)],

    118:
        [(-403, -311), (-355, -311), (-380, -275), (-355, -245), (-369, -191), (-330, -193), (-299, -190), (-366, -88),
         (-364, -44), (-366, -7), (-320, -247), (-266, -266), (-241, -198), (-203, -231), (-188, -201), (-282, -153),
         (-221, -123), (-161, -123), (-131, -156), (-139, -142), (-131, -27), (-123, -3), (-131, 29), (-18, -46),
         (-162, 67), (-203, 39), (-324, 21), (-332, -15), (-331, -52), (-212, -88), (-292, -52), (-259, -29),
         (-4, -254), (32, -203), (-34, -148), (51, -155), (74, -221), (88, -127), (59, -265), (86, -296), (129, -296),
         (161, -296), (124, -198), (140, -226), (147, -163), (133, -138), (162, -134), (187, -173), (221, -125),
         (268, -215), (287, -225), (199, -258), (202, -296), (237, -295), (329, -296), (283, -297), (268, -248),
         (287, -248), (372, -277), (372, -197), (372, -153), (340, -74), (348, -254), (342, -168), (298, -29),
         (283, -74), (297, -92), (213, -62), (184, -50), (61, -45), (40, -73), (25, -52), (61, -84), (43, 53), (61, 73),
         (151, 73), (176, 99), (195, 53), (221, 33), (227, 73), (230, 56), (149, 131), (57, 154), (46, 171), (43, 205),
         (43, 229), (57, 245), (78, 205), (119, 207), (122, 241), (191, 243), (196, 207), (219, 186), (245, 154),
         (212, 154), (221, 132), (220, 110), (262, 94), (294, 74), (288, 154), (273, 230), (226, 229), (326, 230),
         (330, 152), (365, 154), (364, 91), (404, 154), (370, 191), (373, 212), (361, 253), (330, 260), (403, 253),
         (-256, -102), (-270, 0), (-236, 1), (229, -32), (-211, -266), (99, 74)]
}


# noinspection PyArgumentList
class Renderer(object):
    def __init__(self, grid_case, or_ids, ex_ids, are_prods, are_loads):
        self.grid_case = grid_case
        self.grid_layout = np.asarray(case_layouts[grid_case])

        self.video_width, self.video_height = 1300, 800

        self.screen = pygame.display.set_mode((self.video_width, self.video_height), pygame.RESIZABLE)
        pygame.display.set_caption('pypownet - render mode')  # Window title
        # Set default background color
        self.background_color = [70, 70, 73]
        self.screen.fill(self.background_color)

        self.topology_layout_shape = [1000, 800]
        self.topology_layout = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        # Substations layer
        self.nodes_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.nodes_outer_radius = 8
        self.nodes_inner_radius = 5
        #node_img = pygame.image.load(os.path.join(media_path, 'substation.png')).convert_alpha()
        #self.node_img = pygame.transform.scale(node_img, (20, 20))
        self.injections_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.are_prods = are_prods
        self.are_loads = are_loads

        # Lines layer
        self.lines_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.lines_ids_or = or_ids
        self.lines_ids_ex = ex_ids

        # Lines labels (e.g. mW) layer
        self.lines_labels_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA,
                                                   32).convert_alpha()

        self.left_menu_shape = [300, 800]
        self.left_menu = pygame.Surface(self.left_menu_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.left_menu_tile_color = [e + 10 for e in self.background_color]

        # Helpers for printing or plotting
        pygame.font.init()
        font = 'Arial'
        self.default_font = pygame.font.SysFont(font, 15)
        text_color = (180, 180, 180)
        value_color = (220, 220, 220)
        self.text_render = lambda s: self.default_font.render(s, False, text_color)
        self.value_render = lambda s: self.default_font.render(s, False, value_color)
        big_value_font = pygame.font.SysFont('Arial', 18)
        self.big_value_render = lambda s: big_value_font.render(s, False, value_color)

        self.bold_white_font = pygame.font.SysFont(font, 15)
        bold_white = (220, 220, 220)
        self.bold_white_font.set_bold(True)
        self.bold_white_render = lambda s: self.bold_white_font.render(s, False, bold_white)
        # Containers for plotting prods and loads curves
        self.loads = []
        self.relative_thermal_limits = []

        self.black_bold_font = pygame.font.SysFont(font, 15)
        blackish = (70, 70, 70)
        self.black_bold_font.set_bold(True)
        self.black_bold_font_render = lambda s: self.black_bold_font.render(s, False, blackish)

        self.last_rewards_surface = None

        self.game_over_surface = self.draw_plot_game_over()

        self.boolean_dynamic_arrows = True

    def draw_surface_nodes_headers(self, scenario_id, date, cascading_result_frame):
        surface = self.nodes_surface

        # Print some scenario stats
        surface.blit(self.text_render('Date'), (25, 15))
        surface.blit(self.big_value_render(date.strftime("%A %d %b  %H:%M")), (75, 12))
        surface.blit(self.text_render('Timestep id'), (330, 15))
        surface.blit(self.big_value_render(str(scenario_id)), (425, 12))

        width = 400
        height = 25
        x_offset = 25
        y_offset = 40
        if cascading_result_frame == -1:
            gfxdraw.filled_polygon(surface,
                                   ((x_offset, y_offset + height), (x_offset, y_offset), (x_offset + width, y_offset),
                                    (x_offset + width, y_offset + height)),
                                   (250, 200, 150, 240))
            surface.blit(
                self.black_bold_font_render('result of applying action frame'),
                (x_offset + 85, y_offset + 4))
        elif cascading_result_frame is not None:
            gfxdraw.filled_polygon(surface,
                                   ((x_offset, y_offset + height), (x_offset, y_offset), (x_offset + width, y_offset),
                                    (x_offset + width, y_offset + height)),
                                   (250, 200, 200, 240))
            surface.blit(
                self.black_bold_font_render('result of cascading simulation depth %d frame' % cascading_result_frame),
                (x_offset + 40, y_offset + 4))
        else:
            gfxdraw.filled_polygon(surface,
                                   ((x_offset, y_offset + height), (x_offset, y_offset), (x_offset + width, y_offset),
                                    (x_offset + width, y_offset + height)),
                                   (200, 250, 200, 240))
            surface.blit(
                self.black_bold_font_render('new observation frame'),
                (x_offset + 120, y_offset + 4))

    def plot_lines_nodes_matplotlib(self, relative_thermal_limits, lines_por, lines_service_status, prods, loads,
                                    are_substations_changed):
        layout = self.grid_layout
        my_dpi = 200
        fig = plt.figure(figsize=(1000 / my_dpi, 700 / my_dpi), dpi=my_dpi,
                         facecolor=[c / 255. for c in self.background_color], clear=True)
        l = []

        layout = np.asarray(deepcopy(layout))
        min_x = np.min(layout[:, 0])
        min_y = np.min(layout[:, 1])
        layout[:, 0] -= (min_x + 890)
        layout[:, 0] *= -1
        layout[:, 1] -= min_y
        if self.grid_case == 14:
            layout[:, 0] -= 120
            layout[:, 1] += 30
        color_low = np.asarray((51, 204, 51))
        color_middle = np.asarray((255, 93, 0))
        color_high = np.asarray((255, 50, 30))
        for or_id, ex_id, rtl, line_por, is_on in zip(self.lines_ids_or, self.lines_ids_ex, relative_thermal_limits,
                                                      lines_por, lines_service_status):
            # Compute line thickness + color based on its thermal usage
            thickness = .6 + .25 * (min(1., rtl) // .1)

            if rtl < .5:
                color = color_low + 2. * rtl * (color_middle - color_low)
            elif rtl < 1.:
                #color = (51, 204, 51) if rtl < .7 else (255, 165, 0) if rtl < 1. else (214, 0, 0)
                color = color_low + min(1., rtl) * (color_high - color_low)
            else:
                color = (255, 20, 20)

            # Compute the true origin of the flow (lines always fixed or -> dest in IEEE files)
            if line_por >= 0:
                ori = layout[or_id]
                ext = layout[ex_id]
            else:
                ori = layout[ex_id]
                ext = layout[or_id]

            if not is_on:
                l.append(lines.Line2D([ori[0], ext[0]], [50 + ori[1], 50 + ext[1]], linewidth=.8,
                                      color=[.8, .8, .8], figure=fig, linestyle='dashed'))
            else:
                l.append(lines.Line2D([ori[0], ext[0]], [50 + ori[1], 50 + ext[1]], linewidth=thickness,
                                      color=[c / 255. for c in color], figure=fig,
                                      linestyle='--' if rtl > 1. else '-',
                                      dashes=(2., .8) if rtl > 1. else (None, None)))
        fig.lines.extend(l)

        ######## Draw nodes
        ax = fig.gca(frame_on=False, autoscale_on=False, zorder=10)
        ax.set_xlim(0, 1000)
        ax.set_ylim(-50, 650)
        fig.subplots_adjust(0, 0, 1, 1, 0, 0)
        ax.set_xticks([])
        ax.set_yticks([])

        # Loop to compute prods minus loads
        prods_iter, loads_iter = iter(prods), iter(loads)
        prods_minus_loads = []
        for is_prod, is_load in zip(self.are_prods, self.are_loads):
            prod = next(prods_iter) if is_prod else 0.
            load = next(loads_iter) if is_load else 0.
            prods_minus_loads.append(prod - load)
        max_diff = max(abs(np.max(prods_minus_loads)), abs(np.min(prods_minus_loads)))

        prods_iter, loads_iter = iter(prods), iter(loads)
        for i, ((x, y), is_prod, is_load, is_changed) in enumerate(
                zip(layout, self.are_prods, self.are_loads, are_substations_changed)):
            prod = next(prods_iter) if is_prod else 0.
            load = next(loads_iter) if is_load else 0.
            prod_minus_load = prod - load
            # Determine color of filled circle based on the amount of production - consumption
            linewidth_min = 1.
            if prod_minus_load > 0:  # Draw production
                color = [c / 255. for c in (0, 153, 255)]
                inner_circle_color = (255, 255, 0) if is_changed else self.background_color
                inner_circle_color = [c / 255. for c in inner_circle_color]
                linewidth = linewidth_min + 2. * prod_minus_load / max_diff
                outer_radius = self.nodes_outer_radius + 3. * prod_minus_load / max_diff

                c = Circle((x, y), outer_radius, linewidth=0, fill=True, color=inner_circle_color, zorder=9)
                ax.add_artist(c)
                c = Circle((x, y), outer_radius, linewidth=linewidth, fill=False, color=color, zorder=10)
                ax.add_artist(c)
            elif prod_minus_load < 0:  # Draw consumption
                color = [c / 255. for c in (210, 77, 255)]
                inner_circle_color = (255, 255, 0) if is_changed else self.background_color
                inner_circle_color = [c / 255. for c in inner_circle_color]
                linewidth = linewidth_min - 2. * prod_minus_load / max_diff
                outer_radius = self.nodes_outer_radius - 3. * prod_minus_load / max_diff

                # c = Circle((x, y), outer_radius, linewidth=0, fill=True, color=inner_circle_color, zorder=9)
                # ax.add_artist(c)
                # c = Circle((x, y), outer_radius, linewidth=linewidth, fill=False, color=color, zorder=10)
                # ax.add_artist(c)

                c = Rectangle((x - outer_radius, y - outer_radius), 2. * outer_radius, 2. * outer_radius,
                              linewidth=0, fill=True, color=inner_circle_color, zorder=9)
                ax.add_artist(c)
                c = Rectangle((x - outer_radius, y - outer_radius), 2. * outer_radius, 2. * outer_radius,
                              linewidth=linewidth, fill=False, color=color, zorder=10)
                ax.add_artist(c)
            else:
                color = [c / 255. for c in (255, 255, 255)]
                inner_circle_color = (255, 255, 0) if is_changed else self.background_color
                inner_circle_color = [c / 255. for c in inner_circle_color]
                linewidth = linewidth_min
                outer_radius = self.nodes_outer_radius

                c = Rectangle((x, y - math.sqrt(2.) * outer_radius), 2. * outer_radius, 2. * outer_radius,
                              linewidth=0, fill=True, color=inner_circle_color, zorder=9, angle=45.)
                ax.add_artist(c)
                c = Rectangle((x, y - math.sqrt(2.) * outer_radius), 2. * outer_radius, 2. * outer_radius,
                              linewidth=linewidth, fill=False, color=color, zorder=10, angle=45.)
                ax.add_artist(c)
                #Circle((x, y), self.nodes_inner_radius, fill=True, color=inner_circle_color)

        l = []
        for or_id, ex_id, rtl, line_por, is_on in zip(self.lines_ids_or, self.lines_ids_ex, relative_thermal_limits,
                                                      lines_por, lines_service_status):
            if not is_on:
                continue
            # Compute line thickness + color based on its thermal usage
            thickness = .6 + .04 * (min(1., rtl) // .1)

            if rtl < .5:
                color = color_low + 2. * rtl * (color_middle - color_low)
            elif rtl < 1.:
                #color = (51, 204, 51) if rtl < .7 else (255, 165, 0) if rtl < 1. else (214, 0, 0)
                color = color_low + min(1., rtl) * (color_high - color_low)
            else:
                color = (255, 20, 20)

            # Compute the true origin of the flow (lines always fixed or -> dest in IEEE files)
            if line_por >= 0:
                ori = layout[or_id]
                ext = layout[ex_id]
            else:
                ori = layout[ex_id]
                ext = layout[or_id]

            # Compute the line characteristics: draxing is done by plotting two lines starting from the center
            # with a specific angle and semi-length
            length = math.sqrt((ori[0] - ext[0]) ** 2. + (ori[1] - ext[1]) ** 2.) - 2. * self.nodes_outer_radius
            center = ((ori[0] + ext[0]) / 2., (ori[1] + ext[1]) / 2.)
            angle = math.atan2(ori[1] - ext[1], ori[0] - ext[0])

            # First, draw the arrow heads; lines will be drawn on top
            distance_arrow_heads = 25
            n_arrow_heads = int(max(1, length // distance_arrow_heads))
            for a in range(n_arrow_heads):
                if n_arrow_heads != 1:
                    offset = a + .25 if self.boolean_dynamic_arrows else a + .75
                    x = center[0] + (offset * distance_arrow_heads - length / 2.) * math.cos(angle)
                    y = center[1] + (offset * distance_arrow_heads - length / 2.) * math.sin(angle)
                else:
                    x = center[0]
                    y = center[1]

                #draw_arrow_head(x, y, angle, color, thickness)
                head_angle = math.pi / 6.
                width = 8 + 20 * (thickness - .6)
                x -= width / 2. * math.cos(angle)
                y -= width / 2. * math.sin(angle)
                x1 = x + width * math.cos(angle + head_angle)
                y1 = y + width * math.sin(angle + head_angle)
                x2 = x + width * math.cos(angle - head_angle)
                y2 = y + width * math.sin(angle - head_angle)
                l.append(lines.Line2D([x, x2], [50 + y, 50 + y2], linewidth=thickness,
                                      color=[c / 255. for c in color], figure=fig, linestyle='-'))
                l.append(lines.Line2D([x, x1], [50 + y, 50 + y1], linewidth=thickness,
                                      color=[c / 255. for c in color], figure=fig, linestyle='-'))
        fig.lines.extend(l)

        #p.set_array(np.array(color*len(patches)))
        # Export plot into something readable by pygame
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        return pygame.image.fromstring(raw_data, size, "RGB")

    def draw_surface_lines(self, relative_thermal_limits, lines_por, lines_service_status, prods, loads,
                           are_substations_changed):
        img_loads_curve_week = self.plot_lines_nodes_matplotlib(relative_thermal_limits, lines_por,
                                                                lines_service_status, prods, loads,
                                                                are_substations_changed)
        loads_curve_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        loads_curve_surface.fill(self.background_color)
        loads_curve_surface.blit(img_loads_curve_week, (0, 30) if self.grid_case != 30 else (-100, 0))

        return loads_curve_surface

    def create_plot_loads_curve(self, n_timesteps, left_xlabel):
        facecolor_asfloat = np.asarray(self.left_menu_tile_color) / 255.
        layout_config = {'pad': 0.2}
        fig = pylab.figure(figsize=[3, 1.5], dpi=100, facecolor=facecolor_asfloat, tight_layout=layout_config)
        ax = fig.gca()
        # Retrieve data for the specified time
        data = np.sum(self.loads, axis=-1)
        data = data[-min(len(data), n_timesteps):]
        n_data = len(data)
        ax.plot(np.linspace(n_data, 0, num=n_data), data, '#d24dff')
        # Ticks and labels
        ax.set_xlim([n_timesteps, 1])
        ax.set_xticks([1, n_timesteps])
        ax.set_xticklabels(['now', left_xlabel])
        ax.set_ylim([0, np.max(data) * 1.05])
        ax.set_yticks([0, np.max(data)])
        ax.set_yticklabels(['', '%.0f MW' % (np.max(data))])
        label_color_hexa = '#D2D2D2'
        ax.tick_params(axis='y', labelsize=6, pad=-30, labelcolor=label_color_hexa, direction='in')
        ax.tick_params(axis='x', labelsize=6, labelcolor=label_color_hexa)
        # Top and right axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.set_facecolor(np.asarray(self.background_color) / 255.)
        fig.tight_layout()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        return pygame.image.fromstring(raw_data, size, "RGB")

    def create_plot_relative_thermal_limits(self, n_timesteps, left_xlabel):
        facecolor_asfloat = np.asarray(self.left_menu_tile_color) / 255.
        layout_config = {'pad': 0.2}
        fig = pylab.figure(figsize=[3, 1.5], dpi=100, facecolor=facecolor_asfloat, tight_layout=layout_config)
        ax = fig.gca()
        # Retrieve data for the specified time
        data = self.relative_thermal_limits
        data = data[-min(len(data), n_timesteps):]
        n_data = len(data)
        medians = np.median(data, axis=-1)
        p25 = np.percentile(data, 25, axis=-1)
        p75 = np.percentile(data, 75, axis=-1)
        p90 = np.percentile(data, 90, axis=-1)
        p10 = np.percentile(data, 10, axis=-1)
        ax.fill_between(np.linspace(n_data, 0, num=n_data), p10, p90, color='#16AA16')
        ax.fill_between(np.linspace(n_data, 0, num=n_data), p25, p75, color='#16DC16')
        ax.plot(np.linspace(n_data, 0, num=n_data), medians, '#AAFFAA')
        # ax.plot(np.linspace(n_data, 0, num=n_data), percentiles_10, '#33cc33')
        # ax.plot(np.linspace(n_data, 0, num=n_data), percentiles_90, '#33cc33')
        # Ticks and labels
        ax.set_xlim([n_timesteps, 1])
        ax.set_xticks([1, n_timesteps])
        ax.set_xticklabels(['now', left_xlabel])
        ax.set_ylim([0, max(1.05, min(2., np.max([medians, p90, p10]) * 1.05))])
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['', '100%'])
        label_color_hexa = '#D2D2D2'
        ax.tick_params(axis='y', labelsize=6, pad=-22, labelcolor=label_color_hexa, direction='in')
        ax.tick_params(axis='x', labelsize=6, labelcolor=label_color_hexa)
        # Top and right axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.set_facecolor(np.asarray(self.background_color) / 255.)
        fig.tight_layout()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        return pygame.image.fromstring(raw_data, size, "RGB")

    def create_plot_number_overflows(self, n_timesteps, left_xlabel):
        facecolor_asfloat = np.asarray(self.left_menu_tile_color) / 255.
        layout_config = {'pad': 0.2}
        fig = pylab.figure(figsize=[3, 1], dpi=100, facecolor=facecolor_asfloat, tight_layout=layout_config)
        ax = fig.gca()
        # Retrieve data for the specified time
        data = np.sum(np.asarray(self.relative_thermal_limits) >= 1., axis=-1)
        data = data[-min(len(data), n_timesteps):]
        n_data = len(data)
        ax.plot(np.linspace(n_data, 0, num=n_data), data, '#ff3333')
        # Ticks and labels
        ax.set_xlim([n_timesteps, 1])
        ax.set_xticks([1, n_timesteps])
        ax.set_xticklabels(['now', left_xlabel])
        ax.set_ylim([0, max(1, np.max(data) * 1.05)])
        ax.set_yticks([0, max(1, np.max(data))])
        ax.set_yticklabels(['', '%d' % max(1, np.max(data))])
        label_color_hexa = '#D2D2D2'
        ax.tick_params(axis='y', labelsize=6, pad=-12, labelcolor=label_color_hexa, direction='in')
        ax.tick_params(axis='x', labelsize=6, labelcolor=label_color_hexa)
        # Top and right axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.set_facecolor(np.asarray(self.background_color) / 255.)
        fig.tight_layout()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        return pygame.image.fromstring(raw_data, size, "RGB")

    def draw_surface_diagnosis(self, number_loads_cut, number_prods_cut, number_nodes_splitting, number_lines_switches,
                               distance_initial_grid, line_capacity_usage, n_offlines_lines, number_unavailable_lines,
                               max_number_isolated_loads, max_number_isolated_prods):
        my_dpi = 100
        height = 220
        fig = plt.figure(figsize=(self.left_menu_shape[0] / my_dpi, height / my_dpi), dpi=my_dpi,
                         facecolor=[c / 255. for c in self.left_menu_tile_color], clear=True, tight_layout={'pad': 0.2})
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        plt.axis('off')
        plt.ylim(0, height)
        plt.xlim(0, self.left_menu_shape[0])

        string_color = (180 / 255., 180 / 255., 180 / 255.)
        header_color = (220 / 255., 220 / 255., 220 / 255.)
        value_color = (1., 1., 1.)
        plt.text(0, height - 20, 'Live diagnosis', fontdict={'size': 12}, color=header_color)

        string_offset = 65
        value_offset = 10
        plt.text(string_offset, height - 60, '# of isolated loads', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 61, '%d' % number_loads_cut,
                 fontdict={'size': 8.5},
                 color=(1., 0.3, 0.3) if number_loads_cut > max_number_isolated_loads else value_color)
        plt.text(value_offset, height - 60, '   / %d' % max_number_isolated_loads,
                 fontdict={'size': 8.5}, color=value_color)
        plt.text(string_offset, height - 80, '# of isolated productions', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 81, '%d' % number_prods_cut,
                 fontdict={'size': 8.5},
                 color=(1., 0.3, 0.3) if number_prods_cut > max_number_isolated_prods else value_color)
        plt.text(value_offset, height - 80, '   / %d' % max_number_isolated_prods,
                 fontdict={'size': 8.5}, color=value_color)

        plt.text(string_offset, height - 110, '# of node switches of last action', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 110, '%d' % number_nodes_splitting, fontdict={'size': 8.5}, color=value_color)
        plt.text(string_offset, height - 130, '# of line switches of last action', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 130, '%d' % number_lines_switches, fontdict={'size': 8.5}, color=value_color)

        plt.text(string_offset, height - 160, 'average line capacity usage', fontdict={'size': 8.5}, color=string_color)
        usage = 100. * np.mean(line_capacity_usage)
        plt.text(value_offset, height - 160, '%d%%' % usage if usage < 5000 else '∞', fontdict={'size': 8.5},
                 color=value_color)
        plt.text(string_offset, height - 180, '# of OFF lines', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 180, '%d' % n_offlines_lines, fontdict={'size': 8.5}, color=value_color)
        plt.text(string_offset, height - 200, '# of unavailable lines', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 200, '%d' % number_unavailable_lines, fontdict={'size': 8.5}, color=value_color)

        plt.text(string_offset, height - 230, 'distance to reference grid', fontdict={'size': 8.5}, color=string_color)
        plt.text(value_offset, height - 230, '%d' % distance_initial_grid, fontdict={'size': 8.5}, color=value_color)

        fig.tight_layout()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        img = pygame.image.fromstring(raw_data, size, "RGB")
        last_rewards_surface_shape = (self.left_menu_shape[0], height)
        last_rewards_surface = pygame.Surface(last_rewards_surface_shape, pygame.SRCALPHA, 32).convert_alpha()
        last_rewards_surface.fill(self.left_menu_tile_color)

        #last_rewards_surface.blit(img, (0, 30) if self.grid_case != 30 else (-100, 0))
        last_rewards_surface.blit(img, (-20, 0))
        gfxdraw.hline(last_rewards_surface, 0, last_rewards_surface_shape[0], 0, (64, 64, 64))
        gfxdraw.hline(last_rewards_surface, 0, last_rewards_surface_shape[0], last_rewards_surface_shape[1] - 1,
                      (64, 64, 64))
        gfxdraw.vline(last_rewards_surface, 0, last_rewards_surface_shape[1] - 1, 0, (64, 64, 64))
        gfxdraw.vline(last_rewards_surface, last_rewards_surface_shape[0], 0, last_rewards_surface_shape[1] - 1,
                      (64, 64, 64))
        return last_rewards_surface

        last_rewards_surface.blit(self.bold_white_render('Last timestep reward'), (30, 20))

        reward_offset = (50, 40)
        string_offset = 180
        line_spacing = 20

        rewards_labels = ['Loads cut', 'Productions cut', 'Last action cost', 'Distance to initial grid',
                          'Line capacity usage']
        for i, (reward, label) in enumerate(zip(rewards, rewards_labels)):
            last_rewards_surface.blit(self.text_render(label), (reward_offset[0], reward_offset[1] + i * line_spacing))
            last_rewards_surface.blit(self.value_render('%.2f' % reward if reward else '0'),
                                      (reward_offset[0] + string_offset if reward >= 0 else reward_offset[0] + string_offset - 7
                                       , reward_offset[1] + i * line_spacing))
        last_rewards_surface.blit(self.text_render('Total'),
                                  (reward_offset[0], reward_offset[1] + (i + 1) * line_spacing))
        last_rewards_surface.blit(self.value_render('%.2f' % np.sum(rewards)),
                                  (reward_offset[0] + string_offset - 7, reward_offset[1] + (i + 1) * line_spacing))

        return last_rewards_surface

    def draw_surface_loads_curves(self):
        # Loads curve surface: retrieve images surfaces, stack them into a common surface, plot horizontal lines
        # at top and bottom of latter surface
        img_loads_curve_week = self.create_plot_loads_curve(n_timesteps=7 * 24, left_xlabel=' 7 days ago  ')
        img_loads_curve_day = self.create_plot_loads_curve(n_timesteps=24, left_xlabel='24 hours ago')
        loads_curve_surface = pygame.Surface(
            (img_loads_curve_week.get_width(), 2 * img_loads_curve_week.get_height() + 30),
            pygame.SRCALPHA, 32).convert_alpha()
        loads_curve_surface.fill(self.left_menu_tile_color)
        loads_curve_surface.blit(self.bold_white_render('Historical total consumption'), (30, 10))
        loads_curve_surface.blit(img_loads_curve_day, (0, 30))
        loads_curve_surface.blit(img_loads_curve_week, (0, 30 + img_loads_curve_day.get_height()))
        gfxdraw.hline(loads_curve_surface, 0, loads_curve_surface.get_width(), 0, (64, 64, 64))
        gfxdraw.hline(loads_curve_surface, 0, loads_curve_surface.get_width(), loads_curve_surface.get_height() - 1,
                      (64, 64, 64))

        return loads_curve_surface

    def draw_surface_relative_thermal_limits(self):
        img_rtl = self.create_plot_relative_thermal_limits(n_timesteps=24, left_xlabel='24 hours ago')
        rtl_curves_surface = pygame.Surface((img_rtl.get_width(), 2 * img_rtl.get_height() + 30),
                                            pygame.SRCALPHA, 32).convert_alpha()
        rtl_curves_surface.fill(self.left_menu_tile_color)
        rtl_curves_surface.blit(self.bold_white_render('Last 24h lines capacity usage'), (30, 10))
        rtl_curves_surface.blit(img_rtl, (0, 30))
        gfxdraw.hline(rtl_curves_surface, 0, rtl_curves_surface.get_width(), 0, (64, 64, 64))
        gfxdraw.hline(rtl_curves_surface, 0, rtl_curves_surface.get_width(), rtl_curves_surface.get_height() - 1,
                      (64, 64, 64))

        return rtl_curves_surface

    def draw_surface_n_overflows(self):
        img_rtl = self.create_plot_number_overflows(n_timesteps=7 * 24, left_xlabel=' 7 days ago  ')
        n_overflows_surface = pygame.Surface((img_rtl.get_width(), 2 * img_rtl.get_height() + 30),
                                             pygame.SRCALPHA, 32).convert_alpha()
        n_overflows_surface.fill(self.left_menu_tile_color)
        n_overflows_surface.blit(self.bold_white_render('Number of overflows'), (30, 10))
        n_overflows_surface.blit(img_rtl, (0, 30))
        gfxdraw.hline(n_overflows_surface, 0, n_overflows_surface.get_width(), 0, (64, 64, 64))
        gfxdraw.hline(n_overflows_surface, 0, n_overflows_surface.get_width(), n_overflows_surface.get_height() - 1,
                      (64, 64, 64))

        return n_overflows_surface

    def draw_surface_legend(self):
        surface_shape = (self.left_menu_shape[0], 100)
        surface = pygame.Surface(surface_shape, pygame.SRCALPHA, 32).convert_alpha()
        surface.fill(self.left_menu_tile_color)
        surface.blit(self.bold_white_render('Legend'), (15, 10))

        # Lines legend
        xs, ys, thi, lrg = 30, 30, 1, 40
        gfxdraw.filled_polygon(surface, ((xs, ys), (xs + lrg, ys), (xs + lrg, ys + thi), (xs, ys + thi)), (51, 204, 51))
        xs, ys, thi, lrg = xs + lrg, 30, 2, 40
        gfxdraw.filled_polygon(surface, ((xs, ys), (xs + lrg, ys), (xs + lrg, ys + thi), (xs, ys + thi)), (51, 204, 51))
        xs, ys, thi, lrg = xs + lrg, 30, 4, 40
        gfxdraw.filled_polygon(surface, ((xs, ys), (xs + lrg, ys), (xs + lrg, ys + thi), (xs, ys + thi)), (51, 204, 51))

        return surface

    @staticmethod
    def draw_plot_pause():
        pause_font = pygame.font.SysFont("Arial", 25)
        yellow = (255, 255, 179)
        txt_surf = pause_font.render('pause', False, (80., 80., 80.))
        alpha_img = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
        alpha_img.fill(yellow + (72,))
        #txt_surf.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        pause_surface = pygame.Surface((200, 70), pygame.SRCALPHA, 32).convert_alpha()
        pause_surface.fill(yellow + (128,))
        pause_surface.blit(txt_surf, (64, 18))

        return pause_surface

    @staticmethod
    def draw_plot_game_over():
        game_over_font = pygame.font.SysFont("Arial", 25)
        red = (255, 26, 26)
        txt_surf = game_over_font.render('game over', False, (255, 255, 255))
        alpha_img = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
        alpha_img.fill(red + (128,))
        #txt_surf.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        game_over_surface = pygame.Surface((200, 70), pygame.SRCALPHA, 32).convert_alpha()
        game_over_surface.fill(red + (128,))
        game_over_surface.blit(txt_surf, (38, 18))

        return game_over_surface

    def _update_left_menu(self, epoch, timestep):
        self.left_menu = pygame.Surface(self.left_menu_shape, pygame.SRCALPHA, 32).convert_alpha()

        # Top info about epoch and timestep
        self.left_menu.blit(self.text_render('Epoch'), (30, 10))
        self.left_menu.blit(self.text_render('Timestep'), (150, 10))
        self.left_menu.blit(self.value_render(str(epoch)), (100, 10))
        self.left_menu.blit(self.value_render(str(timestep)), (250, 10))

        # Last reward surface
        #last_rewards_surface = self.draw_surface_rewards(rewards)

        # Loads curve surface
        loads_curve_surface = self.draw_surface_loads_curves()

        # Relative thermal limits curves
        rtl_curves_surface = self.draw_surface_relative_thermal_limits()

        # Number of overflowed lines curves
        n_overflows_surface = self.draw_surface_n_overflows()

        gfxdraw.vline(self.left_menu, self.left_menu_shape[0] - 1, 0, self.left_menu_shape[1], (128, 128, 128))
        #self.left_menu.blit(last_rewards_surface, (0, 50))
        self.left_menu.blit(loads_curve_surface, (0, 50))
        self.left_menu.blit(rtl_curves_surface, (0, 380))
        self.left_menu.blit(n_overflows_surface, (0, 560))

    # noinspection PyArgumentList
    def _update_topology(self, scenario_id, date, relative_thermal_limits, lines_por, lines_service_status,
                         prods, loads, rewards, are_substations_changed, game_over, cascading_frame_id,
                         number_loads_cut, number_prods_cut, number_nodes_splitting, number_lines_switches,
                         distance_initial_grid, line_capacity_usage, number_off_lines, number_unavailable_lines,
                         max_number_isolated_loads, max_number_isolated_prods):
        self.topology_layout = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.nodes_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.injections_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        self.lines_surface = pygame.Surface(self.topology_layout_shape, pygame.SRCALPHA, 32).convert_alpha()
        gfxdraw.vline(self.topology_layout, 0, 0, self.left_menu_shape[1], (20, 20, 20))

        # Lines
        if self.relative_thermal_limits:
            if cascading_frame_id is None:
                self.relative_thermal_limits.append(relative_thermal_limits)
        else:
            self.relative_thermal_limits.append(relative_thermal_limits)

        lines_surf = self.draw_surface_lines(relative_thermal_limits, lines_por, lines_service_status,
                                             prods, loads, are_substations_changed)
        self.topology_layout.blit(lines_surf, (0, 0))
        # arrow_surf = self.draw_surface_arrows(relative_thermal_limits, lines_por, lines_service_status)
        # self.topology_layout.blit(arrow_surf, (0, 0))

        # Dirty
        if not rewards:
            rewards = [0] * 5

        diagnosis_reward = self.draw_surface_diagnosis(number_loads_cut, number_prods_cut, number_nodes_splitting,
                                                       number_lines_switches, distance_initial_grid,
                                                       line_capacity_usage, number_off_lines, number_unavailable_lines,
                                                       max_number_isolated_loads, max_number_isolated_prods)
        self.last_rewards_surface = diagnosis_reward

        # Legend
        #legend_surface = self.draw_surface_legend()

        # Dirty
        if self.loads:
            if cascading_frame_id is None:
                self.loads.append(loads)
        else:
            self.loads.append(loads)
        # Nodes
        self.draw_surface_nodes_headers(scenario_id, date, cascading_result_frame=cascading_frame_id)

        #self.topology_layout.blit(self.lines_surface, (0, 0))
        self.topology_layout.blit(self.last_rewards_surface, (690, 1))
        #self.topology_layout.blit(legend_surface, (1, 470))
        self.topology_layout.blit(self.nodes_surface, (0, 0))

        # Print a game over message if game has been lost
        if game_over:
            self.topology_layout.blit(self.game_over_surface, (320, 320))

    def render(self, lines_capacity_usage, lines_por, lines_service_status, epoch, timestep, scenario_id, prods,
               loads, last_timestep_rewards, date, are_substations_changed, number_loads_cut, number_prods_cut,
               number_nodes_splitting, number_lines_switches, distance_initial_grid,
               number_off_lines, number_unavailable_lines, max_number_isolated_loads, max_number_isolated_prods,
               game_over=False, cascading_frame_id=None):
        plt.close('all')

        def event_looper(force=False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_SPACE:
                        pause_surface = self.draw_plot_pause()
                        self.screen.blit(pause_surface, (320 + self.left_menu_shape[0], 320))
                        pygame.display.flip()
                        return not force
            return force

        force = event_looper(force=False)
        while event_looper(force=force):
            pass

        # The game is not paused anymore (or never has been), I can render the next surface
        self.screen.fill(self.background_color)

        # Execute full plotting mechanism: order is important
        self._update_topology(scenario_id, date, lines_capacity_usage, lines_por, lines_service_status,
                              prods, loads, last_timestep_rewards, are_substations_changed, game_over,
                              cascading_frame_id, number_loads_cut, number_prods_cut, number_nodes_splitting,
                              number_lines_switches, distance_initial_grid, lines_capacity_usage, number_off_lines,
                              number_unavailable_lines, max_number_isolated_loads, max_number_isolated_prods)

        if cascading_frame_id is None:
            self._update_left_menu(epoch, timestep)

        # Blit all macro surfaces on screen
        self.screen.blit(self.topology_layout, (self.left_menu_shape[0], 0))
        self.screen.blit(self.left_menu, (0, 0))
        pygame.display.flip()
        # Bugfix for mac
        #pygame.event.get()

        self.boolean_dynamic_arrows = not self.boolean_dynamic_arrows


def scale(u, z, t):
    for k, v in case_layouts.items():
        print(k)
        print([(int(a * u + -0), int(b * z + -40)) for a, b in v])


def recenter():
    for k, v in case_layouts.items():
        print(k)
        arr = np.asarray(np.absolute(v))
        minix = np.min(arr[:, 0])
        miniy = np.min(arr[:, 1])
        maxix = np.max(arr[:, 0])
        maxiy = np.max(arr[:, 1])

        x = (maxix - minix) / 2.
        y = (maxiy - miniy) / 2.
        print([(int(a - x), int(-b - y)) for a, b in v])


if __name__ == '__main__':
    a = np.asarray(case_layouts[30])
    print(np.min(a[:, 0]))
    print(np.max(a[:, 0]))
    print(np.min(a[:, 1]))
    print(np.max(a[:, 1]))
    a = np.asarray(case_layouts[14])
    print()
    print(np.min(a[:, 0]))
    print(np.max(a[:, 0]))
    print(np.min(a[:, 1]))
    print(np.max(a[:, 1]))
    scale(1.01, 1., 0)