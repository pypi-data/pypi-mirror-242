import unittest

from switcore.action.schemas import SwitResponse, ViewCallbackType, View, Body, AttachmentCallbackTypes, AttachmentView, \
    AttachmentBody, SuggestionsCallbackTypes, SuggestionsResult, SuggestionsTypes, NoSuggestionsReason
from switcore.ui.divider import Divider
from switcore.ui.header import Header, AttachmentHeader
from switcore.ui.image import Image
from switcore.ui.select import Option, OptionGroup
from switcore.ui.text_paragraph import TextParagraph


class SwitViewResponseTest(unittest.TestCase):

    def test_swit_response_view(self):
        body = Body(
            elements=[TextParagraph(content="test content"), Divider()],
        )
        swit_response = SwitResponse(
            callback_type=ViewCallbackType.update,
            new_view=View(
                view_id="test01",
                state="test state",
                header=Header(title="this is Header"),
                body=body,
            )
        )
        expected: dict = {
            'callback_type': ViewCallbackType.update,
            'new_view': {
                'view_id': 'test01',
                'state': "test state",
                'header': {'title': 'this is Header'},
                'body': {
                    'elements': [
                        {
                            'content': 'test content',
                            'markdown': False,
                            'type': 'text'
                        },
                        {
                            'type': 'divider'
                        }
                    ],
                }
            }
        }
        self.assertEqual(expected, swit_response.dict(exclude_none=True))

    def test_swit_response_attachments(self):
        swit_response = SwitResponse(
            callback_type=AttachmentCallbackTypes.share_channel,
            attachments=[AttachmentView(
                view_id="test01",
                state="test state",
                header=AttachmentHeader(
                    title="this is Header",
                    app_id="test app id",
                    icon=Image(
                        image_url="https://example.com/image.png",
                    )
                ),
                body=AttachmentBody(
                    elements=[TextParagraph(content="test content")],
                ),
            )]
        )
        expected: dict = {
            'callback_type': AttachmentCallbackTypes.share_channel,
            'attachments': [{
                'view_id': 'test01',
                'state': "test state",
                'header': {
                    'title': 'this is Header',
                    'app_id': 'test app id',
                    'icon': {
                        'type': 'image',
                        'image_url': 'https://example.com/image.png'
                    }
                },
                'body': {
                    'elements': [
                        {
                            'content': 'test content',
                            'markdown': False,
                            'type': 'text'
                        }
                    ],
                }
            }]
        }
        self.assertEqual(expected, swit_response.dict(exclude_none=True))

    def test_swit_response_query_suggestion01(self):
        swit_response = SwitResponse(
            callback_type=SuggestionsCallbackTypes.query_suggestions,
            result=SuggestionsResult(
                type=SuggestionsTypes.options,
                options=[Option(
                    label="Search 성공!",
                    action_id="success_option_action_id",
                )],
            )
        )

        expected: dict = {
            'callback_type': SuggestionsCallbackTypes.query_suggestions,
            'result': {
                'type': SuggestionsTypes.options,
                'options': [{
                    'label': 'Search 성공!',
                    'action_id': 'success_option_action_id'
                }]
            }
        }
        self.assertEqual(expected, swit_response.dict(exclude_none=True))

    def test_swit_response_query_suggestions02(self):
        with self.assertRaises(ValueError):
            SwitResponse(
                callback_type=SuggestionsCallbackTypes.query_suggestions,
                result=SuggestionsResult(
                    type=SuggestionsTypes.options,
                    options=[Option(
                        label="Search 성공!",
                        action_id="success_option_action_id",
                    )],
                    option_groups=[
                        OptionGroup(
                            label="test group",
                            options=[Option(
                                label="test label",
                                action_id="test action id",
                            )]
                        )
                    ]
                )
            )

    def test_swit_response_query_suggestions03(self):
        with self.assertRaises(ValueError):
            SwitResponse(
                callback_type=SuggestionsCallbackTypes.query_suggestions,
                result=SuggestionsResult(
                    type=SuggestionsTypes.option_groups,
                    options=[Option(
                        label="Search 성공!",
                        action_id="success_option_action_id",
                    )]
                )
            )

    def test_swit_response_query_suggestion04(self):
        swit_response = SwitResponse(
            callback_type=SuggestionsCallbackTypes.query_suggestions,
            result=SuggestionsResult(
                type=SuggestionsTypes.option_groups,
                option_groups=[
                    OptionGroup(
                        label="test group1",
                        options=[Option(
                            label="test label1",
                            action_id="test action id1",
                        )]
                    ),
                    OptionGroup(
                        label="test group2",
                        options=[Option(
                            label="test label2",
                            action_id="test action id2",
                        )]
                    ),
                ]
            )
        )

        expected: dict = {
            'callback_type': SuggestionsCallbackTypes.query_suggestions,
            'result': {
                'type': SuggestionsTypes.option_groups,
                'option_groups': [
                    {
                        'label': 'test group1',
                        'options': [{
                            'label': 'test label1',
                            'action_id': 'test action id1'
                        }]
                    },
                    {
                        'label': 'test group2',
                        'options': [{
                            'label': 'test label2',
                            'action_id': 'test action id2'
                        }]
                    }
                ]
            }
        }
        self.assertEqual(expected, swit_response.dict(exclude_none=True))

    def test_swit_response_query_suggestion05(self):
        swit_response = SwitResponse(
            callback_type=SuggestionsCallbackTypes.query_suggestions,
            result=SuggestionsResult(
                type=SuggestionsTypes.no_suggestions_reason,
                no_suggestions_reason=NoSuggestionsReason(
                    message="test message",
                )

            )
        )

        expected: dict = {
            'callback_type': SuggestionsCallbackTypes.query_suggestions,
            'result': {
                'type': SuggestionsTypes.no_suggestions_reason,
                'no_suggestions_reason': {
                    'message': 'test message'
                }
            }
        }
        self.assertEqual(expected, swit_response.dict(exclude_none=True))
