
__all__ = ("FancyMDSwitch")

import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from kivymd.color_definitions import colors
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
    FakeCircularElevationBehavior,
)
from kivymd.uix.label import MDIcon

from kivymd.uix.selectioncontrol import Thumb


Builder.load_string(
"""
<FancyMDSwitch>
    canvas.before:
        Color:
            rgba:
                self._track_color_disabled if self.disabled else \
                ( \
                self._track_color_active \
                if self.active else self._track_color_normal \
                )
        RoundedRectangle:
            size:
                (self.width + dp(12), dp(24)) \
                if root.widget_style == "ios" else \
                (self.width - dp(8), dp(16))
            pos:
                (self.x - dp(2), self.center_y - dp(12)) \
                if root.widget_style == "ios" else \
                (self.x + dp(8), self.center_y - dp(8))
            radius:
                [dp(12)] if root.widget_style == "ios" else [dp(7)]
        Color:
            rgba:
                ( \
                self.theme_cls.disabled_hint_text_color[:-1] + [.2] \
                if not root.active else (0, 0, 0, 0) \
                ) \
                if root.widget_style == "ios" else (0, 0, 0, 0)
        Line:
            width: 1
            rounded_rectangle:
                ( \
                self.x - dp(2), self.center_y - dp(14), self.width + dp(14), \
                dp(28), dp(14), dp(14), dp(14), dp(14), dp(28) \
                ) \
                if root.widget_style == "ios" else \
                (1, 1, 1, 1, 1, 1, 1, 1, 1)

    Thumb:
        id: thumb
        size_hint: (None, None)
        size: root._thumb_size
        pos: root.pos[0] + root._thumb_pos[0], root.pos[1] + root._thumb_pos[1]
        color:
            root.thumb_color_disabled if root.disabled else \
            (root.thumb_color_down if root.active else root.thumb_color)
        elevation: 8 if root.active else 5
        on_release: setattr(root, "active", not root.active)

"""
)


class FancyMDSwitch(ThemableBehavior, ButtonBehavior, FloatLayout):
    active = BooleanProperty(False)
    """
    Indicates if the switch is active or inactive.
    :attr:`active` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    _thumb_color = ColorProperty(get_color_from_hex(colors["Gray"]["50"]))

    def _get_thumb_color(self):
        return self._thumb_color

    def _set_thumb_color(self, color, alpha=None):
        if len(color) == 2:
            self._thumb_color = get_color_from_hex(colors[color[0]][color[1]])
            if alpha:
                self._thumb_color[3] = alpha
        elif len(color) == 4:
            self._thumb_color = color

    thumb_color = AliasProperty(
        _get_thumb_color, _set_thumb_color, bind=["_thumb_color"]
    )
    """
    Get thumb color ``rgba`` format.
    :attr:`thumb_color` is an :class:`~kivy.properties.AliasProperty`
    and property is readonly.
    """

    _thumb_color_down = ColorProperty([1, 1, 1, 1])

    def _get_thumb_color_down(self):
        return self._thumb_color_down

    def _set_thumb_color_down(self, color, alpha=None):
        if len(color) == 2:
            self._thumb_color_down = get_color_from_hex(
                colors[color[0]][color[1]]
            )
            if alpha:
                self._thumb_color_down[3] = alpha
            else:
                self._thumb_color_down[3] = 1
        elif len(color) == 4:
            self._thumb_color_down = color

    _thumb_color_disabled = ColorProperty(
        get_color_from_hex(colors["Gray"]["400"])
    )

    # thumb_color_disabled = get_color_from_hex(colors["Gray"]["800"])
    thumb_color_disabled = (0.5,0.5,0.5,1)
    """
    Get thumb color disabled ``rgba`` format.
    :attr:`thumb_color_disabled` is an :class:`~kivy.properties.AliasProperty`
    and property is readonly.
    """

    def _get_thumb_color_disabled(self):
        return self._thumb_color_disabled

    def _set_thumb_color_disabled(self, color, alpha=None):
        if len(color) == 2:
            self._thumb_color_disabled = get_color_from_hex(
                colors[color[0]][color[1]]
            )
            if alpha:
                self._thumb_color_disabled[3] = alpha
        elif len(color) == 4:
            self._thumb_color_disabled = color

    thumb_color_down = AliasProperty(
        _get_thumb_color_disabled,
        _set_thumb_color_disabled,
        bind=["_thumb_color_disabled"],
    )
    """
    Get thumb color down ``rgba`` format.
    :attr:`thumb_color_down` is an :class:`~kivy.properties.AliasProperty`
    and property is readonly.
    """

    theme_thumb_color = OptionProperty("Primary", options=["Primary", "Custom"])
    """
    Thumb color scheme name
    :attr:`theme_thumb_color` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `Primary`.
    """

    theme_thumb_down_color = OptionProperty(
        "Primary", options=["Primary", "Custom"]
    )
    """
    Thumb Down color scheme name
    :attr:`theme_thumb_down_color` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `Primary`.
    """

    _track_color_active = ColorProperty([0, 0, 0, 0])
    _track_color_normal = ColorProperty([0, 0, 0, 0])
    _track_color_disabled = ColorProperty([0, 0, 0, 0])
    _thumb_pos = ListProperty([0, 0])

    _thumb_size = ListProperty([dp(18),dp(18)])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(
            theme_style=self._set_colors,
            primary_color=self._set_colors,
            primary_palette=self._set_colors,
        )
        self.bind(active=self._update_thumb_pos)
        Clock.schedule_once(self._set_colors)
        self.size_hint = (None, None)
        self.size = (dp(36), dp(48))

    def _set_colors(self, *args):
        self._track_color_normal = self.theme_cls.disabled_hint_text_color
        self._track_color_disabled = self.theme_cls.disabled_hint_text_color
        self.thumb_color_down = (0.77,0.55,0.17,1)
        self._track_color_active = (1,0.75,0.25,0.5)

    def _update_thumb_pos(self, *args, animation=True):
        if self.active:
            _thumb_pos = (self.width - dp(14), self.height / 2 - 0.5*self._thumb_size[1]) # 0.5*self.ids['thumb'].size[1]) #dp(12))
        else:
            _thumb_pos = (0, self.height / 2  - 0.5*self._thumb_size[1]) #self.ids['thumb'].size[1]) # - dp(12))
        Animation.cancel_all(self, "_thumb_pos")
        if animation:
            Animation(_thumb_pos=_thumb_pos, duration=0.2, t="out_quad").start(
                self
            )
        else:
            self._thumb_pos = _thumb_pos

    def on_size(self, *args):
        self._update_thumb_pos(animation=False)
