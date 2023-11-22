from typing import Optional, Sequence, Tuple, Union

from telegram.files.inputfile import InputFile
from telegram.files.sticker import MaskPosition
from telegram import TelegramObject

from telegram.utils.files import parse_file_input
from telegram.utils.types import FileInput, JSONDict

from typing import  TypeVar

T = TypeVar("T")


def parse_sequence_arg(arg: Optional[Sequence[T]]) -> Tuple[T, ...]:
    """Parses an optional sequence into a tuple

    Args:
        arg (:obj:`Sequence`): The sequence to parse.

    Returns:
        :obj:`Tuple`: The sequence converted to a tuple or an empty tuple.
    """
    return tuple(arg) if arg else ()

class InputSticker(TelegramObject):
    """
    This object describes a sticker to be added to a sticker set.

    .. versionadded:: NEXT.VERSION

    Args:
        sticker (:obj:`str` | :term:`file object` | :obj:`bytes` | :class:`pathlib.Path`): The
            added sticker. |uploadinputnopath| Animated and video stickers can't be uploaded via
            HTTP URL.
        emoji_list (Sequence[:obj:`str`]): Sequence of
            :tg-const:`telegram.constants.StickerLimit.MIN_STICKER_EMOJI` -
            :tg-const:`telegram.constants.StickerLimit.MAX_STICKER_EMOJI` emoji associated with the
            sticker.
        mask_position (:obj:`telegram.MaskPosition`, optional): Position where the mask should be
            placed on faces. For ":tg-const:`telegram.constants.StickerType.MASK`" stickers only.
        keywords (Sequence[:obj:`str`], optional): Sequence of
            0-:tg-const:`telegram.constants.StickerLimit.MAX_SEARCH_KEYWORDS` search keywords
            for the sticker with the total length of up to
            :tg-const:`telegram.constants.StickerLimit.MAX_KEYWORD_LENGTH` characters. For
            ":tg-const:`telegram.constants.StickerType.REGULAR`" and
            ":tg-const:`telegram.constants.StickerType.CUSTOM_EMOJI`" stickers only.

    Attributes:
        sticker (:obj:`str` | :class:`telegram.InputFile`): The added sticker.
        emoji_list (Tuple[:obj:`str`]): Tuple of
            :tg-const:`telegram.constants.StickerLimit.MIN_STICKER_EMOJI` -
            :tg-const:`telegram.constants.StickerLimit.MAX_STICKER_EMOJI` emoji associated with the
            sticker.
        mask_position (:obj:`telegram.MaskPosition`): Optional. Position where the mask should be
            placed on faces. For ":tg-const:`telegram.constants.StickerType.MASK`" stickers only.
        keywords (Tuple[:obj:`str`]): Optional. Tuple of
            0-:tg-const:`telegram.constants.StickerLimit.MAX_SEARCH_KEYWORDS` search keywords
            for the sticker with the total length of up to
            :tg-const:`telegram.constants.StickerLimit.MAX_KEYWORD_LENGTH` characters. For
            ":tg-const:`telegram.constants.StickerType.REGULAR`" and
            ":tg-const:`telegram.constants.StickerType.CUSTOM_EMOJI`" stickers only.

    """

    __slots__ = ("sticker", "emoji_list", "mask_position", "keywords")

    def __init__(
        self,
        sticker: FileInput,
        emoji_list: Sequence[str],
        mask_position: MaskPosition = None,
        keywords: Sequence[str] = None,
        *,
        api_kwargs: JSONDict = None,
    ):
        super().__init__(api_kwargs=api_kwargs)

        # We use local_mode=True because we don't have access to the actual setting and want
        # things to work in local mode.
        self.sticker: Union[str, InputFile] = parse_file_input(
            sticker,
            local_mode=True,
            attach=True,
        )
        self.emoji_list: Tuple[str, ...] = parse_sequence_arg(emoji_list)
        self.mask_position: Optional[MaskPosition] = mask_position
        self.keywords: Tuple[str, ...] = parse_sequence_arg(keywords)

        self._freeze()