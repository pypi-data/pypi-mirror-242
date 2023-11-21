from dataclasses import dataclass
import functools

from .api_impl import webui_api
import gradio as gr
from gradio.blocks import Block as GradioBlock
from .gradio_helpers import GradioContext, GradioContextSwitch
from modules.scripts import script_callbacks


all_custom_tabs = webui_api.host_plugin.create_component_list(name='create_img2img_tab')


@dataclass
class TabData:
    tab_index: int
    ui_params: GradioBlock


class Img2imgTabExtender:
    img2img_tabs_block = None
    ui_params_block = None
    inpaint_params_block = None
    amount_of_default_tabs = None
    tab_data_list = []

    @classmethod
    def on_after_component(cls, component, **kwargs):
        elem_id = kwargs.get('elem_id', None)

        if elem_id == 'img2img_batch_inpaint_mask_dir':
            cls.register_img2img_tabs_block(component)

        if elem_id == 'img2img_mask_blur':
            cls.register_inpaint_params_block(component)
            cls.register_custom_ui_params_block(component)
            cls.register_default_amount_of_tabs()

            cls.create_custom_tabs()
            cls.setup_navigation_events()

    @classmethod
    def register_img2img_tabs_block(cls, component):
        cls.img2img_tabs_block = component.parent.parent

    @classmethod
    def register_inpaint_params_block(cls, component):
        cls.inpaint_params_block = component.parent.parent

    @classmethod
    def register_custom_ui_params_block(cls, component):
        cls.ui_params_block = component.parent.parent.parent

    @classmethod
    def register_default_amount_of_tabs(cls):
        cls.amount_of_default_tabs = len(
            [
                child
                for child in cls.img2img_tabs_block.children
                if isinstance(child, gr.TabItem)
            ]
        )

    @classmethod
    def create_custom_tabs(cls):
        for tab_class in all_custom_tabs():
            tab_index = cls._find_tab_index()
            custom_tab_object = tab_class(tab_index)

            with GradioContextSwitch(cls.img2img_tabs_block):
                custom_tab_object.tab()
            with GradioContextSwitch(cls.ui_params_block):
                with gr.Group() as tab_ui_params:
                    custom_tab_object.section()

            custom_tab_object.gradio_events()

            cls.register_custom_tab_data(tab_index, tab_ui_params)

    @classmethod
    def register_custom_tab_data(cls, tab_index, tab_ui_params):
        cls.tab_data_list.append(TabData(tab_index, tab_ui_params))

    @classmethod
    def setup_navigation_events(cls):
        img2img_tabs = [
            child
            for child in cls.img2img_tabs_block.children
            if isinstance(child, gr.TabItem)
        ]
        for custom_tab in cls.tab_data_list:
            for i, tab in enumerate(img2img_tabs):
                def update_func(tab_id, custom_tab_data):
                    return gr.update(visible=tab_id == custom_tab_data.tab_index)

                tab.select(
                    fn=functools.partial(update_func, tab_id=i, custom_tab_data=custom_tab),
                    inputs=[],
                    outputs=[custom_tab.ui_params]
                )

                # extend the behavior of hiding the default inpaint_params
                if i >= cls.amount_of_default_tabs:
                    tab.select(
                        fn=lambda tab_id=i: gr.update(visible=False),
                        inputs=[],
                        outputs=[cls.inpaint_params_block]
                    )

    @classmethod
    def _find_tab_index(cls):
        img2img_tabs = [
            child
            for child in cls.img2img_tabs_block.children
            if isinstance(child, gr.TabItem)
        ]
        return len(img2img_tabs)


script_callbacks.on_after_component(Img2imgTabExtender.on_after_component)
