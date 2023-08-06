# coding: utf-8

"""
    Voicegain API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + RTC Callback APIs which in addition to speech-to-text allow for control of RTC session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.  # RTC Callback API   Voicegain Real Time Communication (RTC) Callback APIs work on audio data that is part of an RTC session (a telephone call for example).   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Pagination  For methods that support pagination Voicegain has standardized on using the following query parameters: + page={page number} + per_page={number items per page}  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?page=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=2&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=3&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"last\" ```  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.24.0 - updated February 20, 2021
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from voicegain_speech.api_client import ApiClient
from voicegain_speech.exceptions import (
    ApiTypeError,
    ApiValueError
)


class SaApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def sa_config_get(self, sa_config_id, **kwargs):  # noqa: E501
        """Get Sp. Analytics Cfg.  # noqa: E501

        Get Speech Analytics configuration for given id.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_get(sa_config_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_config_id: Configuration ID for Speech Analytics (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SpeechAnalyticsConfig
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_config_get_with_http_info(sa_config_id, **kwargs)  # noqa: E501

    def sa_config_get_with_http_info(self, sa_config_id, **kwargs):  # noqa: E501
        """Get Sp. Analytics Cfg.  # noqa: E501

        Get Speech Analytics configuration for given id.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_get_with_http_info(sa_config_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_config_id: Configuration ID for Speech Analytics (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SpeechAnalyticsConfig, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_config_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_config_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_config_id' is set
        if self.api_client.client_side_validation and ('sa_config_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_config_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_config_id` when calling `sa_config_get`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_config_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_config_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_config_id` when calling `sa_config_get`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_config_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_config_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_config_id` when calling `sa_config_get`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_config_id' in local_var_params:
            path_params['saConfigId'] = local_var_params['sa_config_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/config/{saConfigId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SpeechAnalyticsConfig',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_config_post(self, **kwargs):  # noqa: E501
        """New Sp. Analytics Cfg.  # noqa: E501

        Create new Speech Analytics Configuration    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param bool built_in: Set to true to indicate that a built-in Built-In Speech Analytics config is to be created. Only users with \"cmp\" permission are allowed to create built-in configs. 
        :param SpeechAnalyticsConfig speech_analytics_config: Configuration for Speech Analytics
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SpeechAnalyticsConfig
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_config_post_with_http_info(**kwargs)  # noqa: E501

    def sa_config_post_with_http_info(self, **kwargs):  # noqa: E501
        """New Sp. Analytics Cfg.  # noqa: E501

        Create new Speech Analytics Configuration    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param bool built_in: Set to true to indicate that a built-in Built-In Speech Analytics config is to be created. Only users with \"cmp\" permission are allowed to create built-in configs. 
        :param SpeechAnalyticsConfig speech_analytics_config: Configuration for Speech Analytics
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SpeechAnalyticsConfig, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['built_in', 'speech_analytics_config']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_config_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'built_in' in local_var_params and local_var_params['built_in'] is not None:  # noqa: E501
            query_params.append(('builtIn', local_var_params['built_in']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'speech_analytics_config' in local_var_params:
            body_params = local_var_params['speech_analytics_config']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/config', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SpeechAnalyticsConfig',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_config_put(self, sa_config_id, **kwargs):  # noqa: E501
        """Mod Sp. Analytics Cfg.  # noqa: E501

        Modify new Speech Analytics Configuration    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_put(sa_config_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_config_id: Configuration ID for Speech Analytics (required)
        :param SpeechAnalyticsConfigModifiable speech_analytics_config_modifiable: Modifications to Speech Analytics Configuration
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SpeechAnalyticsConfig
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_config_put_with_http_info(sa_config_id, **kwargs)  # noqa: E501

    def sa_config_put_with_http_info(self, sa_config_id, **kwargs):  # noqa: E501
        """Mod Sp. Analytics Cfg.  # noqa: E501

        Modify new Speech Analytics Configuration    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_put_with_http_info(sa_config_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_config_id: Configuration ID for Speech Analytics (required)
        :param SpeechAnalyticsConfigModifiable speech_analytics_config_modifiable: Modifications to Speech Analytics Configuration
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SpeechAnalyticsConfig, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_config_id', 'speech_analytics_config_modifiable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_config_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_config_id' is set
        if self.api_client.client_side_validation and ('sa_config_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_config_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_config_id` when calling `sa_config_put`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_config_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_config_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_config_id` when calling `sa_config_put`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_config_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_config_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_config_id` when calling `sa_config_put`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_config_id' in local_var_params:
            path_params['saConfigId'] = local_var_params['sa_config_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'speech_analytics_config_modifiable' in local_var_params:
            body_params = local_var_params['speech_analytics_config_modifiable']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/config/{saConfigId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SpeechAnalyticsConfig',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_config_query(self, **kwargs):  # noqa: E501
        """Query Sp. Analytics Cfg.  # noqa: E501

        Get Speech Analytics configurations that match filters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param str name: Name to match. If the provided name ends with a star `*` then a prefix match will be performed.</br> Note - the star is allowed only in the last position (arbitrary wildcard matching is not supported). 
        :param bool incl_other_context_published: If true then will also retrieve Speech Analytics Configurations from other contexts on this account which have been published.
        :param SAConfType type: Speech Analytics Configuration Type - `user`, `built-in`, or `any` (any is a union of user and built-in)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[SpeechAnalyticsConfig]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_config_query_with_http_info(**kwargs)  # noqa: E501

    def sa_config_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query Sp. Analytics Cfg.  # noqa: E501

        Get Speech Analytics configurations that match filters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_config_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param str name: Name to match. If the provided name ends with a star `*` then a prefix match will be performed.</br> Note - the star is allowed only in the last position (arbitrary wildcard matching is not supported). 
        :param bool incl_other_context_published: If true then will also retrieve Speech Analytics Configurations from other contexts on this account which have been published.
        :param SAConfType type: Speech Analytics Configuration Type - `user`, `built-in`, or `any` (any is a union of user and built-in)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[SpeechAnalyticsConfig], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'name', 'incl_other_context_published', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_config_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `sa_config_query`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `sa_config_query`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and ('name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['name']) > 512):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `name` when calling `sa_config_query`, length must be less than or equal to `512`")  # noqa: E501
        if self.api_client.client_side_validation and ('name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['name']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `name` when calling `sa_config_query`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'name' in local_var_params and local_var_params['name'] is not None:  # noqa: E501
            query_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'incl_other_context_published' in local_var_params and local_var_params['incl_other_context_published'] is not None:  # noqa: E501
            query_params.append(('inclOtherContextPublished', local_var_params['incl_other_context_published']))  # noqa: E501
        if 'type' in local_var_params and local_var_params['type'] is not None:  # noqa: E501
            query_params.append(('type', local_var_params['type']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/config', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[SpeechAnalyticsConfig]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_data_get(self, sa_session_id, **kwargs):  # noqa: E501
        """Get Sp. Analytics Data  # noqa: E501

        Retrieve Speech Analytics result data. Note: original audio was mono and diarization had to be used to return the speaker channels,  then the returned decibel and audio zone data will be approximate - it will de extracted from mono channel using diarization zones. If requested we will also return simulated stereo audio in such cases.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_data_get(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param bool audio: If `true` then original or simulated (if diarization was used) multichannel (stereo) audio will be returned.
        :param float decibels: If this parameter has a value then the result will contain an array of decibel values for the audio data.</br> Each value in the array will reflect the power of the audio over the specified millisecond interval.</br> For example, if `decibels=25` then each value will be the power of the audio signal in **dbFS** (sinusoid) over the interval of 25 msec. 
        :param bool audio_zones: If `true` then audioZones information will be returned
        :param bool word_cloud: If `true` then word cloud data for the transcript will be returned
        :param bool emotion: If `true` then emotion (mood and sentiment) information will be returned
        :param bool keywords: If `true` then keywords spotted in the text will be returned
        :param bool entities: If `true` then named entities spotted in the text will be returned
        :param bool phrases: _(coming soon)_ If `true` then phrases spotted in the text will be returned
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SpeechAnalyticsResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_data_get_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_data_get_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """Get Sp. Analytics Data  # noqa: E501

        Retrieve Speech Analytics result data. Note: original audio was mono and diarization had to be used to return the speaker channels,  then the returned decibel and audio zone data will be approximate - it will de extracted from mono channel using diarization zones. If requested we will also return simulated stereo audio in such cases.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_data_get_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param bool audio: If `true` then original or simulated (if diarization was used) multichannel (stereo) audio will be returned.
        :param float decibels: If this parameter has a value then the result will contain an array of decibel values for the audio data.</br> Each value in the array will reflect the power of the audio over the specified millisecond interval.</br> For example, if `decibels=25` then each value will be the power of the audio signal in **dbFS** (sinusoid) over the interval of 25 msec. 
        :param bool audio_zones: If `true` then audioZones information will be returned
        :param bool word_cloud: If `true` then word cloud data for the transcript will be returned
        :param bool emotion: If `true` then emotion (mood and sentiment) information will be returned
        :param bool keywords: If `true` then keywords spotted in the text will be returned
        :param bool entities: If `true` then named entities spotted in the text will be returned
        :param bool phrases: _(coming soon)_ If `true` then phrases spotted in the text will be returned
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SpeechAnalyticsResult, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id', 'audio', 'decibels', 'audio_zones', 'word_cloud', 'emotion', 'keywords', 'entities', 'phrases']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_data_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_data_get`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_data_get`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_data_get`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and 'decibels' in local_var_params and local_var_params['decibels'] < 10:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `decibels` when calling `sa_data_get`, must be a value greater than or equal to `10`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []
        if 'audio' in local_var_params and local_var_params['audio'] is not None:  # noqa: E501
            query_params.append(('audio', local_var_params['audio']))  # noqa: E501
        if 'decibels' in local_var_params and local_var_params['decibels'] is not None:  # noqa: E501
            query_params.append(('decibels', local_var_params['decibels']))  # noqa: E501
        if 'audio_zones' in local_var_params and local_var_params['audio_zones'] is not None:  # noqa: E501
            query_params.append(('audioZones', local_var_params['audio_zones']))  # noqa: E501
        if 'word_cloud' in local_var_params and local_var_params['word_cloud'] is not None:  # noqa: E501
            query_params.append(('wordCloud', local_var_params['word_cloud']))  # noqa: E501
        if 'emotion' in local_var_params and local_var_params['emotion'] is not None:  # noqa: E501
            query_params.append(('emotion', local_var_params['emotion']))  # noqa: E501
        if 'keywords' in local_var_params and local_var_params['keywords'] is not None:  # noqa: E501
            query_params.append(('keywords', local_var_params['keywords']))  # noqa: E501
        if 'entities' in local_var_params and local_var_params['entities'] is not None:  # noqa: E501
            query_params.append(('entities', local_var_params['entities']))  # noqa: E501
        if 'phrases' in local_var_params and local_var_params['phrases'] is not None:  # noqa: E501
            query_params.append(('phrases', local_var_params['phrases']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/{saSessionId}/data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SpeechAnalyticsResult',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_get_transcript(self, sa_session_id, **kwargs):  # noqa: E501
        """SA Transcript Content  # noqa: E501

        Retrieve transcript from Speech Analytics session (after transcription is complete) in one of several possible formats.</br> **NOTE: currently only `json` and `text` formats are supported.** </br> The response will contain the final content of the transcription of the provided audio.</br> Note, if the transcription is still in progress then 400 error will be returned.</br>   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_get_transcript(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param str format: Format of the transcript to be returned: + json - complete transcript data with all detail for each word + text - plaint text transcript with optional timing information + srt - transcript in SRT caption format + vtt - transcript in WebVTT caption format + ttml - transcript in TTML (XML) caption format 
        :param float width: Applicable only to captions. Determines max caption width in number of characters.
        :param float interval: Applicable only to plain text transcript. Determines interval (in seconds) between time stamps.</br> If absent, no time stamps will be provided.<br> 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[WordsSection]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_get_transcript_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_get_transcript_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """SA Transcript Content  # noqa: E501

        Retrieve transcript from Speech Analytics session (after transcription is complete) in one of several possible formats.</br> **NOTE: currently only `json` and `text` formats are supported.** </br> The response will contain the final content of the transcription of the provided audio.</br> Note, if the transcription is still in progress then 400 error will be returned.</br>   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_get_transcript_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param str format: Format of the transcript to be returned: + json - complete transcript data with all detail for each word + text - plaint text transcript with optional timing information + srt - transcript in SRT caption format + vtt - transcript in WebVTT caption format + ttml - transcript in TTML (XML) caption format 
        :param float width: Applicable only to captions. Determines max caption width in number of characters.
        :param float interval: Applicable only to plain text transcript. Determines interval (in seconds) between time stamps.</br> If absent, no time stamps will be provided.<br> 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[WordsSection], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id', 'format', 'width', 'interval']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_get_transcript" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_get_transcript`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_get_transcript`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_get_transcript`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and 'width' in local_var_params and local_var_params['width'] > 120:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `width` when calling `sa_get_transcript`, must be a value less than or equal to `120`")  # noqa: E501
        if self.api_client.client_side_validation and 'width' in local_var_params and local_var_params['width'] < 10:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `width` when calling `sa_get_transcript`, must be a value greater than or equal to `10`")  # noqa: E501
        if self.api_client.client_side_validation and 'interval' in local_var_params and local_var_params['interval'] < 5:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `interval` when calling `sa_get_transcript`, must be a value greater than or equal to `5`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []
        if 'format' in local_var_params and local_var_params['format'] is not None:  # noqa: E501
            query_params.append(('format', local_var_params['format']))  # noqa: E501
        if 'width' in local_var_params and local_var_params['width'] is not None:  # noqa: E501
            query_params.append(('width', local_var_params['width']))  # noqa: E501
        if 'interval' in local_var_params and local_var_params['interval'] is not None:  # noqa: E501
            query_params.append(('interval', local_var_params['interval']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain', 'text/srt', 'text/vtt', 'text/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/{saSessionId}/transcript', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[WordsSection]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_post(self, **kwargs):  # noqa: E501
        """New Sp. Analytics Ses.  # noqa: E501

        Create new Speech Analytics Session    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param NewSpeechAnalyticsSession new_speech_analytics_session: Data for new started Speech Analytics Session
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: NewSpeechAnalyticsSessionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_post_with_http_info(**kwargs)  # noqa: E501

    def sa_post_with_http_info(self, **kwargs):  # noqa: E501
        """New Sp. Analytics Ses.  # noqa: E501

        Create new Speech Analytics Session    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param NewSpeechAnalyticsSession new_speech_analytics_session: Data for new started Speech Analytics Session
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(NewSpeechAnalyticsSessionResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['new_speech_analytics_session']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'new_speech_analytics_session' in local_var_params:
            body_params = local_var_params['new_speech_analytics_session']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NewSpeechAnalyticsSessionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_query(self, **kwargs):  # noqa: E501
        """Query Sp. Analytics Data  # noqa: E501

        Get Speech Analytics data that matches filters.</br> This method returns the bare-bones Speech Analytics data, to get the detail for each one of those use [GET /sa/{saSessionId}](#operation/saDataGet) with the parameters that it offers.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[SpeechAnalyticsResult]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_query_with_http_info(**kwargs)  # noqa: E501

    def sa_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query Sp. Analytics Data  # noqa: E501

        Get Speech Analytics data that matches filters.</br> This method returns the bare-bones Speech Analytics data, to get the detail for each one of those use [GET /sa/{saSessionId}](#operation/saDataGet) with the parameters that it offers.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[SpeechAnalyticsResult], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `sa_query`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `sa_query`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[SpeechAnalyticsResult]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
