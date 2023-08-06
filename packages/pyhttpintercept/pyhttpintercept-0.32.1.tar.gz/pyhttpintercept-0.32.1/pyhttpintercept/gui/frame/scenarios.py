# encoding: utf-8

import logging_helper
import pyperclip
import json
from uiutil import (BaseFrame,
                    BaseScrollFrame,
                    nice_grid,
                    Button,
                    Label,
                    Position,
                    Separator,
                    RadioButton,
                    HeadingsFrame)
from uiutil.tk_names import askquestion, showerror, W, NSEW, E, S
from ...config.intercept import InterceptConfig
from ...config.intercept_scenarios import Scenarios
from ...intercept._updater import InterceptUpdaters
from ..window.scenario import AddEditScenarioWindow

logging = logging_helper.setup_logging()

BLUE_TEXT = dict(foreground=u"blue")
BLUE_TEXT_RADIO_BUTTON = u"BlueText.TRadiobutton"
BLUE_TEXT_BUTTON = u"BlueText.TButton"
BLUE_TEXT_LABEL = u"BlueText.TLabel"


class ScenariosConfigFrame(BaseFrame):
    STYLES = {BLUE_TEXT_RADIO_BUTTON: BLUE_TEXT,
              BLUE_TEXT_BUTTON: BLUE_TEXT,
              BLUE_TEXT_LABEL: BLUE_TEXT,
              }

    DESCRIPTION_DISPLAY_MAX_CHARS = 80

    CANVAS_HEIGHT = 300
    CANVAS_WIDTH = 700

    def __init__(self,
                 intercept_server=None,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self, *args, **kwargs)

        self.intercept_server = intercept_server

        self._cfg = InterceptConfig()
        self._scenarios = Scenarios()
        self._updaters = InterceptUpdaters()

        # self.columnconfigure(self.column.start(), weight=1)

        self.headings = HeadingsFrame(headings=['Scenario', 'Description'],
                                      padx=0)

        self.SCENARIO_ROW = self.row.next()
        # self.rowconfigure(self.SCENARIO_ROW, weight=1)
        self.BUTTON_ROW = self.row.next()

        self.__build_scenarios_frame()
        self.__build_button_frame()

    @property
    def _active_scenario(self):
        return self._cfg.selected_scenario

    def __build_scenarios_frame(self):

        self.headings.set_widths((max([len(scenario_name) for scenario_name in sorted(self._scenarios)]),
                                  self.DESCRIPTION_DISPLAY_MAX_CHARS))
        try:
            self.scenario_row
        except AttributeError:
            self.scenario_row = self.row.next()

        self.scenarios_frame = BaseScrollFrame(parent=self,
                                               canvas_height=self.CANVAS_HEIGHT,
                                               canvas_width=self.CANVAS_WIDTH,
                                               row=self.scenario_row)

        for scenario_name in sorted(self._scenarios):

            scenario = self._scenarios[scenario_name]

            if scenario.name == self._active_scenario:
                label_style = BLUE_TEXT_LABEL
                radio_button_style = BLUE_TEXT_RADIO_BUTTON

            else:
                label_style = u'TLabel'
                radio_button_style = u'TRadiobutton'

            self.selected_scenario = RadioButton(frame=self.scenarios_frame,
                                                 text=scenario.name,
                                                 value=scenario.name,
                                                 style=radio_button_style,
                                                 row=Position.NEXT,
                                                 column=Position.START,
                                                 sticky=W)

            description_text = (scenario.description[:self.DESCRIPTION_DISPLAY_MAX_CHARS].replace(u'\n', u' ') + u"…"
                                if len(scenario.description) > self.DESCRIPTION_DISPLAY_MAX_CHARS
                                else scenario.description.replace(u'\n', u' '))

            description_tooltip = (dict(text=scenario.description,
                                        max_width=self.DESCRIPTION_DISPLAY_MAX_CHARS / 2,
                                        justify="left")
                                   if len(scenario.description) > self.DESCRIPTION_DISPLAY_MAX_CHARS
                                   else None)

            Label(frame=self.scenarios_frame,
                  text=description_text,
                  style=label_style,
                  column=Position.NEXT,
                  sticky=W,
                  tooltip=description_tooltip)

        self.selected_scenario.value = self._cfg.selected_scenario

        Separator()

        self.scenarios_frame.nice_grid()

    def __build_button_frame(self):

        button_width = 12

        buttons = BaseFrame(row=Position.NEXT,
                            column=Position.START,
                            sticky=(E, W, S))

        Button(frame=buttons,
               text=u'Set Active',
               width=button_width,
               command=self._set_active,
               style=BLUE_TEXT_BUTTON,
               tooltip=(u'Set selected\n'
                        u'scenario as\n'
                        u'active'))

        Button(frame=buttons,
               text=u'Delete',
               width=button_width,
               command=self._delete_scenario,
               column=Position.NEXT,
               tooltip=(u'Delete\n'
                        u'selected\n'
                        u'scenario'))

        Button(frame=buttons,
               text=u'Add',
               width=button_width,
               command=self._add_scenario,
               column=Position.NEXT,
               tooltip=(u'Add scenario\n'
                        u'to scenarios\n'
                        u'list'))

        Button(frame=buttons,
               text=u'Edit',
               width=button_width,
               command=self._edit_scenario,
               column=Position.NEXT,
               tooltip=(u'Edit\n'
                        u'selected\n'
                        u'scenario'))

        Button(frame=buttons,
               text=u'Copy',
               width=button_width,
               command=self._copy,
               column=Position.NEXT,
               tooltip=(u'Copy the selected\n'
                        u'scenario to the\n'
                        u'Clipboard'))

        Button(frame=buttons,
               text=u'Paste',
               width=button_width,
               command=self._paste,
               column=Position.NEXT,
               tooltip=(u'Add a scenario\n'
                        u'from the\n'
                        u'Clipboard'))

        Button(frame=buttons,
               text=u'Update',
               width=button_width,
               command=self._update,
               column=Position.NEXT,
               tooltip=(u'Update scenarios and\n'
                        u'supporting test data'))

        nice_grid(buttons)

    def _redraw_scenarios_frame(self):
        # TODO: Fix broken redrawing is broken.
        self.scenarios_frame.destroy()

        try:
            self.intercept_server.reload_config()
        except AttributeError as e:
            logging.exception(e)

        self.__build_scenarios_frame()
        self.parent.master.update_geometry()

    def _add_scenario(self):
        window = AddEditScenarioWindow(fixed=True,
                                       intercept_server=self.intercept_server,
                                       parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)
        self._redraw_scenarios_frame()

    def _edit_scenario(self):
        window = AddEditScenarioWindow(selected_record=self.selected_scenario.value,
                                       edit=True,
                                       fixed=True,
                                       intercept_server=self.intercept_server,
                                       parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)
        self._redraw_scenarios_frame()

    def _delete_scenario(self):
        result = askquestion(u"Delete Scenario",
                             u"Are you sure you want to delete {t}?".format(t=self.selected_scenario.value),
                             icon=u'warning',
                             parent=self)

        if result == u'yes':
            # Delete selected scenario
            self._scenarios.delete(key_attr=self.selected_scenario.value)

            self._redraw_scenarios_frame()

    def _set_active(self):
        # Set new active scenario
        self._cfg.selected_scenario = self.selected_scenario.value
        self._redraw_scenarios_frame()

    def _copy(self):
        selected_scenario_dict = dict(name=self.selected_scenario.value,
                                      scenario=self._scenarios[self.selected_scenario.value].raw_items)
        pyperclip.copy(json.dumps(selected_scenario_dict,
                                  indent=4))
        logging_helper.LogLines(pyperclip.paste())

    def _paste(self):
        try:
            new_scenario = json.loads(pyperclip.paste())
        except Exception as e:
            logging.exception(e)
            showerror(u"Paste Error",
                      u'Error pasting scenario:{e}'.format(e=e),
                      icon=u'error',
                      parent=self)
            return
        try:
            name = new_scenario[u'name']
            if name in self._scenarios.keys():
                result = askquestion(u"Paste Scenario",
                                     u"Are you sure you want to replace {t}?".format(t=name),
                                     icon=u'warning',
                                     parent=self)
                if result != u"yes":
                    return
            self._scenarios.add(key_attr=name,
                                config=new_scenario[u'scenario'])
        except Exception as e:
            logging.exception(e)
            showerror(u"Paste Error",
                      u'Invalid Scenario:{e}'.format(e=e),
                      icon=u'error',
                      parent=self)
            return

        self._redraw_scenarios_frame()

    def _update(self):
        scenarios = self._updaters.run_updaters()

        for scenario in scenarios:
            try:
                self._scenarios.add(key_attr=scenario[u'name'],
                                    config=scenario[u'scenario'])
            except Exception as e:
                logging.exception(e)
                logging.warning(u'Invalid scenario: {scenario}'.format(scenario=scenario))

        self._redraw_scenarios_frame()
