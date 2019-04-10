from wagtail.core import blocks
from .ColumnsBlock import ColumnsBlock
from .CommonBlocks import CommonBlocks


class GridBlock(blocks.StreamBlock):
    column_1_1 = ColumnsBlock(
        CommonBlocks(),
        ratios=(1, 1),
        label="Two halves",
        group="Columns",
    )
    column_2_1 = ColumnsBlock(
        CommonBlocks(),
        ratios=(2, 1),
        label="Two thirds/One third",
        group="Columns",
    )
    column_1_1_1 = ColumnsBlock(
        CommonBlocks(),
        ratios=(1, 1, 1),
        label="Three thirds",
        group="Columns",
    )

    class Meta:
        icon = "fa-th-large"
