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


class SpeechAnalyticsConfigModifiable(object):
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
        'age': 'bool',
        'call_resolution_phrases': 'list[CallResolutionPhrase]',
        'competitor_keyword_groups': 'list[str]',
        'context_id': 'str',
        'entities': 'list[NamedEntityType]',
        'gender': 'bool',
        'keyword_groups': 'list[KeywordSpotGroup]',
        'keywords': 'list[KeywordSpotItem]',
        'moods': 'list[MoodType]',
        'name': 'str',
        'overtalk_single_duration_maximum_threshold': 'float',
        'overtalk_total_percentage_threshold': 'float',
        'phrases': 'list[PhraseSpotItem]',
        'pii_redaction': 'list[PIIRedactionConf]',
        'profanity': 'bool',
        'published': 'bool',
        'sentiment': 'bool',
        'silence_single_duration_maximum_threshold': 'float',
        'silence_total_percentage_threshold': 'float',
        'word_cloud': 'bool'
    }

    attribute_map = {
        'age': 'age',
        'call_resolution_phrases': 'callResolutionPhrases',
        'competitor_keyword_groups': 'competitorKeywordGroups',
        'context_id': 'contextId',
        'entities': 'entities',
        'gender': 'gender',
        'keyword_groups': 'keywordGroups',
        'keywords': 'keywords',
        'moods': 'moods',
        'name': 'name',
        'overtalk_single_duration_maximum_threshold': 'overtalkSingleDurationMaximumThreshold',
        'overtalk_total_percentage_threshold': 'overtalkTotalPercentageThreshold',
        'phrases': 'phrases',
        'pii_redaction': 'piiRedaction',
        'profanity': 'profanity',
        'published': 'published',
        'sentiment': 'sentiment',
        'silence_single_duration_maximum_threshold': 'silenceSingleDurationMaximumThreshold',
        'silence_total_percentage_threshold': 'silenceTotalPercentageThreshold',
        'word_cloud': 'wordCloud'
    }

    def __init__(self, age=None, call_resolution_phrases=None, competitor_keyword_groups=None, context_id=None, entities=None, gender=None, keyword_groups=None, keywords=None, moods=None, name=None, overtalk_single_duration_maximum_threshold=1000, overtalk_total_percentage_threshold=2.5, phrases=None, pii_redaction=None, profanity=None, published=False, sentiment=None, silence_single_duration_maximum_threshold=10000, silence_total_percentage_threshold=10.0, word_cloud=None, local_vars_configuration=None):  # noqa: E501
        """SpeechAnalyticsConfigModifiable - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._age = None
        self._call_resolution_phrases = None
        self._competitor_keyword_groups = None
        self._context_id = None
        self._entities = None
        self._gender = None
        self._keyword_groups = None
        self._keywords = None
        self._moods = None
        self._name = None
        self._overtalk_single_duration_maximum_threshold = None
        self._overtalk_total_percentage_threshold = None
        self._phrases = None
        self._pii_redaction = None
        self._profanity = None
        self._published = None
        self._sentiment = None
        self._silence_single_duration_maximum_threshold = None
        self._silence_total_percentage_threshold = None
        self._word_cloud = None
        self.discriminator = None

        if age is not None:
            self.age = age
        if call_resolution_phrases is not None:
            self.call_resolution_phrases = call_resolution_phrases
        if competitor_keyword_groups is not None:
            self.competitor_keyword_groups = competitor_keyword_groups
        if context_id is not None:
            self.context_id = context_id
        if entities is not None:
            self.entities = entities
        if gender is not None:
            self.gender = gender
        if keyword_groups is not None:
            self.keyword_groups = keyword_groups
        if keywords is not None:
            self.keywords = keywords
        if moods is not None:
            self.moods = moods
        if name is not None:
            self.name = name
        if overtalk_single_duration_maximum_threshold is not None:
            self.overtalk_single_duration_maximum_threshold = overtalk_single_duration_maximum_threshold
        if overtalk_total_percentage_threshold is not None:
            self.overtalk_total_percentage_threshold = overtalk_total_percentage_threshold
        if phrases is not None:
            self.phrases = phrases
        if pii_redaction is not None:
            self.pii_redaction = pii_redaction
        if profanity is not None:
            self.profanity = profanity
        if published is not None:
            self.published = published
        if sentiment is not None:
            self.sentiment = sentiment
        if silence_single_duration_maximum_threshold is not None:
            self.silence_single_duration_maximum_threshold = silence_single_duration_maximum_threshold
        if silence_total_percentage_threshold is not None:
            self.silence_total_percentage_threshold = silence_total_percentage_threshold
        if word_cloud is not None:
            self.word_cloud = word_cloud

    @property
    def age(self):
        """Gets the age of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        set to true to enable speaker age estimation  # noqa: E501

        :return: The age of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._age

    @age.setter
    def age(self, age):
        """Sets the age of this SpeechAnalyticsConfigModifiable.

        set to true to enable speaker age estimation  # noqa: E501

        :param age: The age of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._age = age

    @property
    def call_resolution_phrases(self):
        """Gets the call_resolution_phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(coming soon)_ Phrases from the call script that might indicate call resolution  # noqa: E501

        :return: The call_resolution_phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[CallResolutionPhrase]
        """
        return self._call_resolution_phrases

    @call_resolution_phrases.setter
    def call_resolution_phrases(self, call_resolution_phrases):
        """Sets the call_resolution_phrases of this SpeechAnalyticsConfigModifiable.

        _(coming soon)_ Phrases from the call script that might indicate call resolution  # noqa: E501

        :param call_resolution_phrases: The call_resolution_phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[CallResolutionPhrase]
        """

        self._call_resolution_phrases = call_resolution_phrases

    @property
    def competitor_keyword_groups(self):
        """Gets the competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Set of one or more keyword group tags that should be interpreted as identifying competitor mentions.  # noqa: E501

        :return: The competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[str]
        """
        return self._competitor_keyword_groups

    @competitor_keyword_groups.setter
    def competitor_keyword_groups(self, competitor_keyword_groups):
        """Sets the competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.

        Set of one or more keyword group tags that should be interpreted as identifying competitor mentions.  # noqa: E501

        :param competitor_keyword_groups: The competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[str]
        """

        self._competitor_keyword_groups = competitor_keyword_groups

    @property
    def context_id(self):
        """Gets the context_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        (In request needed only if making request using MAC Authentication. Otherwise will be taken from JWT.)  # noqa: E501

        :return: The context_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._context_id

    @context_id.setter
    def context_id(self, context_id):
        """Sets the context_id of this SpeechAnalyticsConfigModifiable.

        (In request needed only if making request using MAC Authentication. Otherwise will be taken from JWT.)  # noqa: E501

        :param context_id: The context_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                context_id is not None and len(context_id) > 48):
            raise ValueError("Invalid value for `context_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                context_id is not None and len(context_id) < 16):
            raise ValueError("Invalid value for `context_id`, length must be greater than or equal to `16`")  # noqa: E501

        self._context_id = context_id

    @property
    def entities(self):
        """Gets the entities of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Selection of Named Entity types to detect </br> Types of Named Entities: + CARDINAL - Numerals that do not fall under another type. + CC - Credit Card (coming soon) + DATE - Absolute or relative dates or periods. + EVENT - Named hurricanes, battles, wars, sports events, etc. + FAC - Buildings, airports, highways, bridges, etc. + GPE - Countries, cities, states. + NORP - Nationalities or religious or political groups. + MONEY - Monetary values, including unit. + ORDINAL - \"first\", \"second\", etc. + ORG - Companies, agencies, institutions, etc. + PERCENT - Percentage, including \"%\". + PERSON - People, including fictional. + QUANTITY - Measurements, as of weight or distance. + SSN - Social Security number (coming soon) + TIME - Named documents made into laws.          # noqa: E501

        :return: The entities of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[NamedEntityType]
        """
        return self._entities

    @entities.setter
    def entities(self, entities):
        """Sets the entities of this SpeechAnalyticsConfigModifiable.

        Selection of Named Entity types to detect </br> Types of Named Entities: + CARDINAL - Numerals that do not fall under another type. + CC - Credit Card (coming soon) + DATE - Absolute or relative dates or periods. + EVENT - Named hurricanes, battles, wars, sports events, etc. + FAC - Buildings, airports, highways, bridges, etc. + GPE - Countries, cities, states. + NORP - Nationalities or religious or political groups. + MONEY - Monetary values, including unit. + ORDINAL - \"first\", \"second\", etc. + ORG - Companies, agencies, institutions, etc. + PERCENT - Percentage, including \"%\". + PERSON - People, including fictional. + QUANTITY - Measurements, as of weight or distance. + SSN - Social Security number (coming soon) + TIME - Named documents made into laws.          # noqa: E501

        :param entities: The entities of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[NamedEntityType]
        """

        self._entities = entities

    @property
    def gender(self):
        """Gets the gender of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        set to true to enable voice gender classifcation  # noqa: E501

        :return: The gender of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._gender

    @gender.setter
    def gender(self, gender):
        """Sets the gender of this SpeechAnalyticsConfigModifiable.

        set to true to enable voice gender classifcation  # noqa: E501

        :param gender: The gender of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._gender = gender

    @property
    def keyword_groups(self):
        """Gets the keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501


        :return: The keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[KeywordSpotGroup]
        """
        return self._keyword_groups

    @keyword_groups.setter
    def keyword_groups(self, keyword_groups):
        """Sets the keyword_groups of this SpeechAnalyticsConfigModifiable.


        :param keyword_groups: The keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[KeywordSpotGroup]
        """

        self._keyword_groups = keyword_groups

    @property
    def keywords(self):
        """Gets the keywords of this SpeechAnalyticsConfigModifiable.  # noqa: E501


        :return: The keywords of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[KeywordSpotItem]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """Sets the keywords of this SpeechAnalyticsConfigModifiable.


        :param keywords: The keywords of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[KeywordSpotItem]
        """

        self._keywords = keywords

    @property
    def moods(self):
        """Gets the moods of this SpeechAnalyticsConfigModifiable.  # noqa: E501


        :return: The moods of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[MoodType]
        """
        return self._moods

    @moods.setter
    def moods(self, moods):
        """Sets the moods of this SpeechAnalyticsConfigModifiable.


        :param moods: The moods of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[MoodType]
        """

        self._moods = moods

    @property
    def name(self):
        """Gets the name of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        A **unique**, human friendly, name to identify the Speech Analytics configuration.</br> May contain only us-asci letters, digits, and following symbols `.` `-` `_`  </br> Consecutive symbols are not allowed. Must start and end with digit or letter.    # noqa: E501

        :return: The name of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SpeechAnalyticsConfigModifiable.

        A **unique**, human friendly, name to identify the Speech Analytics configuration.</br> May contain only us-asci letters, digits, and following symbols `.` `-` `_`  </br> Consecutive symbols are not allowed. Must start and end with digit or letter.    # noqa: E501

        :param name: The name of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 128):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `128`")  # noqa: E501

        self._name = name

    @property
    def overtalk_single_duration_maximum_threshold(self):
        """Gets the overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Duration-based threshold (in milliseconds) used to determine if an overtalk incident has occured.  Applies to maximun duration of single/individual cases of overtalk.   # noqa: E501

        :return: The overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._overtalk_single_duration_maximum_threshold

    @overtalk_single_duration_maximum_threshold.setter
    def overtalk_single_duration_maximum_threshold(self, overtalk_single_duration_maximum_threshold):
        """Sets the overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.

        Duration-based threshold (in milliseconds) used to determine if an overtalk incident has occured.  Applies to maximun duration of single/individual cases of overtalk.   # noqa: E501

        :param overtalk_single_duration_maximum_threshold: The overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                overtalk_single_duration_maximum_threshold is not None and overtalk_single_duration_maximum_threshold > 60000):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_single_duration_maximum_threshold`, must be a value less than or equal to `60000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                overtalk_single_duration_maximum_threshold is not None and overtalk_single_duration_maximum_threshold < 1):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_single_duration_maximum_threshold`, must be a value greater than or equal to `1`")  # noqa: E501

        self._overtalk_single_duration_maximum_threshold = overtalk_single_duration_maximum_threshold

    @property
    def overtalk_total_percentage_threshold(self):
        """Gets the overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Percentage-based threshold used to determine if an overtalk incident has occured.  Applies to total overtalk expressed as percentage of the call duration.   # noqa: E501

        :return: The overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._overtalk_total_percentage_threshold

    @overtalk_total_percentage_threshold.setter
    def overtalk_total_percentage_threshold(self, overtalk_total_percentage_threshold):
        """Sets the overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.

        Percentage-based threshold used to determine if an overtalk incident has occured.  Applies to total overtalk expressed as percentage of the call duration.   # noqa: E501

        :param overtalk_total_percentage_threshold: The overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                overtalk_total_percentage_threshold is not None and overtalk_total_percentage_threshold > 100.0):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_total_percentage_threshold`, must be a value less than or equal to `100.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                overtalk_total_percentage_threshold is not None and overtalk_total_percentage_threshold < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_total_percentage_threshold`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._overtalk_total_percentage_threshold = overtalk_total_percentage_threshold

    @property
    def phrases(self):
        """Gets the phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(coming soon)_ Phrases detected in the text.  # noqa: E501

        :return: The phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[PhraseSpotItem]
        """
        return self._phrases

    @phrases.setter
    def phrases(self, phrases):
        """Sets the phrases of this SpeechAnalyticsConfigModifiable.

        _(coming soon)_ Phrases detected in the text.  # noqa: E501

        :param phrases: The phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[PhraseSpotItem]
        """

        self._phrases = phrases

    @property
    def pii_redaction(self):
        """Gets the pii_redaction of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        (optional) list specifying the types of entities to be redacted from the transctipt and/or audio  # noqa: E501

        :return: The pii_redaction of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[PIIRedactionConf]
        """
        return self._pii_redaction

    @pii_redaction.setter
    def pii_redaction(self, pii_redaction):
        """Sets the pii_redaction of this SpeechAnalyticsConfigModifiable.

        (optional) list specifying the types of entities to be redacted from the transctipt and/or audio  # noqa: E501

        :param pii_redaction: The pii_redaction of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[PIIRedactionConf]
        """

        self._pii_redaction = pii_redaction

    @property
    def profanity(self):
        """Gets the profanity of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        set to true to enable detection of profanity. will be output together with spotted keywords  # noqa: E501

        :return: The profanity of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._profanity

    @profanity.setter
    def profanity(self, profanity):
        """Sets the profanity of this SpeechAnalyticsConfigModifiable.

        set to true to enable detection of profanity. will be output together with spotted keywords  # noqa: E501

        :param profanity: The profanity of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._profanity = profanity

    @property
    def published(self):
        """Gets the published of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Specifies if Speech Analytics configuration can be used outside its context.  For built-in configurations, specifies if the configuration is visible to end-users of Voicegain. Only user with \"cmp\" role is able to see built-in configurations that are not published.   # noqa: E501

        :return: The published of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published):
        """Sets the published of this SpeechAnalyticsConfigModifiable.

        Specifies if Speech Analytics configuration can be used outside its context.  For built-in configurations, specifies if the configuration is visible to end-users of Voicegain. Only user with \"cmp\" role is able to see built-in configurations that are not published.   # noqa: E501

        :param published: The published of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._published = published

    @property
    def sentiment(self):
        """Gets the sentiment of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        set to true to enable sentiment analytics  # noqa: E501

        :return: The sentiment of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """Sets the sentiment of this SpeechAnalyticsConfigModifiable.

        set to true to enable sentiment analytics  # noqa: E501

        :param sentiment: The sentiment of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._sentiment = sentiment

    @property
    def silence_single_duration_maximum_threshold(self):
        """Gets the silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Duration-based threshold (in milliseconds) used to determine if a silence incident has occured.  Applies to maximun duration of single/individual cases of silence.   # noqa: E501

        :return: The silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._silence_single_duration_maximum_threshold

    @silence_single_duration_maximum_threshold.setter
    def silence_single_duration_maximum_threshold(self, silence_single_duration_maximum_threshold):
        """Sets the silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.

        Duration-based threshold (in milliseconds) used to determine if a silence incident has occured.  Applies to maximun duration of single/individual cases of silence.   # noqa: E501

        :param silence_single_duration_maximum_threshold: The silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                silence_single_duration_maximum_threshold is not None and silence_single_duration_maximum_threshold > 60000):  # noqa: E501
            raise ValueError("Invalid value for `silence_single_duration_maximum_threshold`, must be a value less than or equal to `60000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                silence_single_duration_maximum_threshold is not None and silence_single_duration_maximum_threshold < 1):  # noqa: E501
            raise ValueError("Invalid value for `silence_single_duration_maximum_threshold`, must be a value greater than or equal to `1`")  # noqa: E501

        self._silence_single_duration_maximum_threshold = silence_single_duration_maximum_threshold

    @property
    def silence_total_percentage_threshold(self):
        """Gets the silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Percentage-based threshold used to determine if a silence incident has occured.  Applies to total silence expressed as percentage of the call duration.   # noqa: E501

        :return: The silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._silence_total_percentage_threshold

    @silence_total_percentage_threshold.setter
    def silence_total_percentage_threshold(self, silence_total_percentage_threshold):
        """Sets the silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.

        Percentage-based threshold used to determine if a silence incident has occured.  Applies to total silence expressed as percentage of the call duration.   # noqa: E501

        :param silence_total_percentage_threshold: The silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                silence_total_percentage_threshold is not None and silence_total_percentage_threshold > 100.0):  # noqa: E501
            raise ValueError("Invalid value for `silence_total_percentage_threshold`, must be a value less than or equal to `100.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                silence_total_percentage_threshold is not None and silence_total_percentage_threshold < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `silence_total_percentage_threshold`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._silence_total_percentage_threshold = silence_total_percentage_threshold

    @property
    def word_cloud(self):
        """Gets the word_cloud of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        set to true to enable output of word cloud data  # noqa: E501

        :return: The word_cloud of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._word_cloud

    @word_cloud.setter
    def word_cloud(self, word_cloud):
        """Sets the word_cloud of this SpeechAnalyticsConfigModifiable.

        set to true to enable output of word cloud data  # noqa: E501

        :param word_cloud: The word_cloud of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._word_cloud = word_cloud

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
        if not isinstance(other, SpeechAnalyticsConfigModifiable):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SpeechAnalyticsConfigModifiable):
            return True

        return self.to_dict() != other.to_dict()
