from django.db import models

from .actions import *
from .event import Event
from .mind import Mind
from .block import Block
from .none_object import NoneObject
from .buttons.reply_button import ReplyButton
from .buttons.inline_button import InlineButton


class Action(models.Model):
    title = models.CharField(max_length=64, default="Action")
    created_at = models.DateTimeField(auto_now_add=True)

    text_message = models.ForeignKey(TextMessage, on_delete=models.SET_NULL, null=True, blank=True)

    photo_message = models.ForeignKey(PhotoMessage, on_delete=models.SET_NULL, null=True, blank=True)

    audio_message = models.ForeignKey(AudioMessage, on_delete=models.SET_NULL, null=True, blank=True)

    document_message = models.ForeignKey(DocumentMessage, on_delete=models.SET_NULL, null=True, blank=True)

    video_message = models.ForeignKey(VideoMessage, on_delete=models.SET_NULL, null=True, blank=True)

    animation_message = models.ForeignKey(AnimationMessage, on_delete=models.SET_NULL, null=True, blank=True)

    voice_message = models.ForeignKey(VoiceMessage, on_delete=models.SET_NULL, null=True, blank=True)

    video_note_message = models.ForeignKey(VideoNoteMessage, on_delete=models.SET_NULL, null=True, blank=True)

    media_group_message = models.ForeignKey(MediaGroupMessage, on_delete=models.SET_NULL, null=True, blank=True)

    chat_action = models.ForeignKey(ChatAction, on_delete=models.SET_NULL, null=True, blank=True)

    approve_request = models.ForeignKey(ApproveRequest, on_delete=models.SET_NULL, null=True, blank=True)

    http_request_action = models.ForeignKey(
        HttpRequestAction, on_delete=models.SET_NULL, null=True, blank=True)

    reply_buttons = models.ManyToManyField(ReplyButton, blank=True)

    inline_buttons = models.ManyToManyField(InlineButton, blank=True)

    remove_reply_buttons = models.BooleanField(default=False)

    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    mind = models.ForeignKey(Mind, on_delete=models.SET_NULL, null=True, blank=True, related_name="minds")

    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)

    none_object = models.ForeignKey(NoneObject, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "action"
