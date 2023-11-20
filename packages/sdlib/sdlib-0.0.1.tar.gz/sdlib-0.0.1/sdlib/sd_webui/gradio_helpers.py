from gradio.context import Context as GradioContext


class GradioContextSwitch:
    def __init__(self, block):
        self.block = block

    def __enter__(self):
        self.previous_block = GradioContext.block
        GradioContext.block = self.block
        return self

    def __exit__(self, *args, **kwargs):
        GradioContext.block = self.previous_block
