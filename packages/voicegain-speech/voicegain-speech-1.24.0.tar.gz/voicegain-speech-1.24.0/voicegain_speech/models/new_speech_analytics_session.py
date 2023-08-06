# coding: utf-8

"""
    Voicegain API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + RTC Callback APIs which in addition to speech-to-text allow for control of RTC session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.  # RTC Callback API   Voicegain Real Time Communication (RTC) Callback APIs work on audio data that is part of an RTC session (a telephone call for example).   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Pagination  For methods that support pagination Voicegain has standardized on using the following query parameters: + page={page number} + per_page={number items per page}  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?page=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=2&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=3&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"last\" ```  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.24.0 - updated February 20, 2021
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from voicegain_speech.configuration import Configuration


class NewSpeechAnalyticsSession(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'asr': 'AsrSettingsTranscriptionSA',
        'async_mode': 'AsyncModeSpeechAnalytics',
        'audio': 'AudioInputAsync',
        'call_review_config': 'str',
        'label': 'str',
        'sa_config': 'str',
        'speaker_channels': 'list[SpeechAnalyticsChannel]',
        'topic_discovery_config': 'str'
    }

    attribute_map = {
        'asr': 'asr',
        'async_mode': 'asyncMode',
        'audio': 'audio',
        'call_review_config': 'callReviewConfig',
        'label': 'label',
        'sa_config': 'saConfig',
        'speaker_channels': 'speakerChannels',
        'topic_discovery_config': 'topicDiscoveryConfig'
    }

    def __init__(self, asr=None, async_mode=None, audio=None, call_review_config=None, label=None, sa_config=None, speaker_channels=None, topic_discovery_config=None, local_vars_configuration=None):  # noqa: E501
        """NewSpeechAnalyticsSession - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._asr = None
        self._async_mode = None
        self._audio = None
        self._call_review_config = None
        self._label = None
        self._sa_config = None
        self._speaker_channels = None
        self._topic_discovery_config = None
        self.discriminator = None

        if asr is not None:
            self.asr = asr
        if async_mode is not None:
            self.async_mode = async_mode
        if audio is not None:
            self.audio = audio
        if call_review_config is not None:
            self.call_review_config = call_review_config
        if label is not None:
            self.label = label
        self.sa_config = sa_config
        if speaker_channels is not None:
            self.speaker_channels = speaker_channels
        if topic_discovery_config is not None:
            self.topic_discovery_config = topic_discovery_config

    @property
    def asr(self):
        """Gets the asr of this NewSpeechAnalyticsSession.  # noqa: E501


        :return: The asr of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: AsrSettingsTranscriptionSA
        """
        return self._asr

    @asr.setter
    def asr(self, asr):
        """Sets the asr of this NewSpeechAnalyticsSession.


        :param asr: The asr of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: AsrSettingsTranscriptionSA
        """

        self._asr = asr

    @property
    def async_mode(self):
        """Gets the async_mode of this NewSpeechAnalyticsSession.  # noqa: E501


        :return: The async_mode of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: AsyncModeSpeechAnalytics
        """
        return self._async_mode

    @async_mode.setter
    def async_mode(self, async_mode):
        """Sets the async_mode of this NewSpeechAnalyticsSession.


        :param async_mode: The async_mode of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: AsyncModeSpeechAnalytics
        """

        self._async_mode = async_mode

    @property
    def audio(self):
        """Gets the audio of this NewSpeechAnalyticsSession.  # noqa: E501


        :return: The audio of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: AudioInputAsync
        """
        return self._audio

    @audio.setter
    def audio(self, audio):
        """Sets the audio of this NewSpeechAnalyticsSession.


        :param audio: The audio of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: AudioInputAsync
        """

        self._audio = audio

    @property
    def call_review_config(self):
        """Gets the call_review_config of this NewSpeechAnalyticsSession.  # noqa: E501

        _(coming soon)_ (optional) id of the Call Review (Score Card) configuration to use.  The Call Review Config will be used to guide the generation of autopopulated Call Review Answers.   # noqa: E501

        :return: The call_review_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._call_review_config

    @call_review_config.setter
    def call_review_config(self, call_review_config):
        """Sets the call_review_config of this NewSpeechAnalyticsSession.

        _(coming soon)_ (optional) id of the Call Review (Score Card) configuration to use.  The Call Review Config will be used to guide the generation of autopopulated Call Review Answers.   # noqa: E501

        :param call_review_config: The call_review_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                call_review_config is not None and len(call_review_config) > 48):
            raise ValueError("Invalid value for `call_review_config`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                call_review_config is not None and len(call_review_config) < 16):
            raise ValueError("Invalid value for `call_review_config`, length must be greater than or equal to `16`")  # noqa: E501

        self._call_review_config = call_review_config

    @property
    def label(self):
        """Gets the label of this NewSpeechAnalyticsSession.  # noqa: E501

        Short labels to assign to the speech Analytics session. May be displayed in a table to make identifying a session easier.  # noqa: E501

        :return: The label of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this NewSpeechAnalyticsSession.

        Short labels to assign to the speech Analytics session. May be displayed in a table to make identifying a session easier.  # noqa: E501

        :param label: The label of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                label is not None and len(label) > 64):
            raise ValueError("Invalid value for `label`, length must be less than or equal to `64`")  # noqa: E501

        self._label = label

    @property
    def sa_config(self):
        """Gets the sa_config of this NewSpeechAnalyticsSession.  # noqa: E501

        id of the Speech Analytics configuration to use. If not provided then default SA Config for the context will be used.   # noqa: E501

        :return: The sa_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._sa_config

    @sa_config.setter
    def sa_config(self, sa_config):
        """Sets the sa_config of this NewSpeechAnalyticsSession.

        id of the Speech Analytics configuration to use. If not provided then default SA Config for the context will be used.   # noqa: E501

        :param sa_config: The sa_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and sa_config is None:  # noqa: E501
            raise ValueError("Invalid value for `sa_config`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sa_config is not None and len(sa_config) > 48):
            raise ValueError("Invalid value for `sa_config`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sa_config is not None and len(sa_config) < 16):
            raise ValueError("Invalid value for `sa_config`, length must be greater than or equal to `16`")  # noqa: E501

        self._sa_config = sa_config

    @property
    def speaker_channels(self):
        """Gets the speaker_channels of this NewSpeechAnalyticsSession.  # noqa: E501

        For stereo audio this is used to map audio channels to processing sessions and to identify which one is Agent.</br> For mono audio, specify just one session. Diarization will be automatically turned on.  Determination of which speaker is Agent will be attempted from the transcript.          # noqa: E501

        :return: The speaker_channels of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: list[SpeechAnalyticsChannel]
        """
        return self._speaker_channels

    @speaker_channels.setter
    def speaker_channels(self, speaker_channels):
        """Sets the speaker_channels of this NewSpeechAnalyticsSession.

        For stereo audio this is used to map audio channels to processing sessions and to identify which one is Agent.</br> For mono audio, specify just one session. Diarization will be automatically turned on.  Determination of which speaker is Agent will be attempted from the transcript.          # noqa: E501

        :param speaker_channels: The speaker_channels of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: list[SpeechAnalyticsChannel]
        """

        self._speaker_channels = speaker_channels

    @property
    def topic_discovery_config(self):
        """Gets the topic_discovery_config of this NewSpeechAnalyticsSession.  # noqa: E501

        _(coming soon)_ (optional) id of the Topic Discovery configuration to use.  If not provided then default Topic Discovery Config for the context will be used.   # noqa: E501

        :return: The topic_discovery_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._topic_discovery_config

    @topic_discovery_config.setter
    def topic_discovery_config(self, topic_discovery_config):
        """Sets the topic_discovery_config of this NewSpeechAnalyticsSession.

        _(coming soon)_ (optional) id of the Topic Discovery configuration to use.  If not provided then default Topic Discovery Config for the context will be used.   # noqa: E501

        :param topic_discovery_config: The topic_discovery_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                topic_discovery_config is not None and len(topic_discovery_config) > 48):
            raise ValueError("Invalid value for `topic_discovery_config`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                topic_discovery_config is not None and len(topic_discovery_config) < 16):
            raise ValueError("Invalid value for `topic_discovery_config`, length must be greater than or equal to `16`")  # noqa: E501

        self._topic_discovery_config = topic_discovery_config

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NewSpeechAnalyticsSession):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewSpeechAnalyticsSession):
            return True

        return self.to_dict() != other.to_dict()
