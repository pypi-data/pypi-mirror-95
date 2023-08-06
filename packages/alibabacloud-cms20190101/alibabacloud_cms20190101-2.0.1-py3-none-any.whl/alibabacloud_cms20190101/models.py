# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict


class AddTagsRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class AddTagsRequest(TeaModel):
    def __init__(
        self,
        tag: List[AddTagsRequestTag] = None,
        group_ids: List[str] = None,
    ):
        self.tag = tag
        self.group_ids = group_ids

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        if self.group_ids is not None:
            result['GroupIds'] = self.group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = AddTagsRequestTag()
                self.tag.append(temp_model.from_map(k))
        if m.get('GroupIds') is not None:
            self.group_ids = m.get('GroupIds')
        return self


class AddTagsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class AddTagsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddTagsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddTagsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ApplyMetricRuleTemplateRequest(TeaModel):
    def __init__(
        self,
        silence_time: int = None,
        group_id: int = None,
        template_ids: str = None,
        enable_start_time: int = None,
        enable_end_time: int = None,
        notify_level: int = None,
        apply_mode: str = None,
        webhook: str = None,
    ):
        self.silence_time = silence_time
        self.group_id = group_id
        self.template_ids = template_ids
        self.enable_start_time = enable_start_time
        self.enable_end_time = enable_end_time
        self.notify_level = notify_level
        self.apply_mode = apply_mode
        self.webhook = webhook

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.template_ids is not None:
            result['TemplateIds'] = self.template_ids
        if self.enable_start_time is not None:
            result['EnableStartTime'] = self.enable_start_time
        if self.enable_end_time is not None:
            result['EnableEndTime'] = self.enable_end_time
        if self.notify_level is not None:
            result['NotifyLevel'] = self.notify_level
        if self.apply_mode is not None:
            result['ApplyMode'] = self.apply_mode
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('TemplateIds') is not None:
            self.template_ids = m.get('TemplateIds')
        if m.get('EnableStartTime') is not None:
            self.enable_start_time = m.get('EnableStartTime')
        if m.get('EnableEndTime') is not None:
            self.enable_end_time = m.get('EnableEndTime')
        if m.get('NotifyLevel') is not None:
            self.notify_level = m.get('NotifyLevel')
        if m.get('ApplyMode') is not None:
            self.apply_mode = m.get('ApplyMode')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        return self


class ApplyMetricRuleTemplateResponseBodyResourceAlertResults(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        success: bool = None,
        code: str = None,
        message: str = None,
        rule_id: str = None,
        rule_name: str = None,
    ):
        self.group_id = group_id
        self.success = success
        self.code = code
        self.message = message
        self.rule_id = rule_id
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.success is not None:
            result['Success'] = self.success
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class ApplyMetricRuleTemplateResponseBodyResource(TeaModel):
    def __init__(
        self,
        alert_results: List[ApplyMetricRuleTemplateResponseBodyResourceAlertResults] = None,
        group_id: int = None,
    ):
        self.alert_results = alert_results
        self.group_id = group_id

    def validate(self):
        if self.alert_results:
            for k in self.alert_results:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertResults'] = []
        if self.alert_results is not None:
            for k in self.alert_results:
                result['AlertResults'].append(k.to_map() if k else None)
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_results = []
        if m.get('AlertResults') is not None:
            for k in m.get('AlertResults'):
                temp_model = ApplyMetricRuleTemplateResponseBodyResourceAlertResults()
                self.alert_results.append(temp_model.from_map(k))
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class ApplyMetricRuleTemplateResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        resource: ApplyMetricRuleTemplateResponseBodyResource = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.resource = resource
        self.code = code
        self.success = success

    def validate(self):
        if self.resource:
            self.resource.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource is not None:
            result['Resource'] = self.resource.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Resource') is not None:
            temp_model = ApplyMetricRuleTemplateResponseBodyResource()
            self.resource = temp_model.from_map(m['Resource'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ApplyMetricRuleTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ApplyMetricRuleTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ApplyMetricRuleTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateCmsCallNumOrderRequest(TeaModel):
    def __init__(
        self,
        period: int = None,
        period_unit: str = None,
        auto_renew_period: int = None,
        auto_pay: bool = None,
        auto_use_coupon: bool = None,
        phone_count: str = None,
    ):
        self.period = period
        self.period_unit = period_unit
        self.auto_renew_period = auto_renew_period
        self.auto_pay = auto_pay
        self.auto_use_coupon = auto_use_coupon
        self.phone_count = phone_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.period is not None:
            result['Period'] = self.period
        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit
        if self.auto_renew_period is not None:
            result['AutoRenewPeriod'] = self.auto_renew_period
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.phone_count is not None:
            result['PhoneCount'] = self.phone_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')
        if m.get('AutoRenewPeriod') is not None:
            self.auto_renew_period = m.get('AutoRenewPeriod')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('PhoneCount') is not None:
            self.phone_count = m.get('PhoneCount')
        return self


class CreateCmsCallNumOrderResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        order_id: str = None,
    ):
        self.request_id = request_id
        self.order_id = order_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        return self


class CreateCmsCallNumOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateCmsCallNumOrderResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateCmsCallNumOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateCmsOrderRequest(TeaModel):
    def __init__(
        self,
        period: int = None,
        period_unit: str = None,
        auto_renew_period: int = None,
        auto_pay: bool = None,
        auto_use_coupon: bool = None,
        pay_type: str = None,
        suggest_type: str = None,
        api_count: str = None,
        site_operator_num: str = None,
        event_store_time: str = None,
        log_monitor_stream: str = None,
        site_task_num: str = None,
        event_store_num: str = None,
        site_ecs_num: str = None,
        custom_time_series: str = None,
        sms_count: str = None,
        phone_count: str = None,
    ):
        self.period = period
        self.period_unit = period_unit
        self.auto_renew_period = auto_renew_period
        self.auto_pay = auto_pay
        self.auto_use_coupon = auto_use_coupon
        self.pay_type = pay_type
        self.suggest_type = suggest_type
        self.api_count = api_count
        self.site_operator_num = site_operator_num
        self.event_store_time = event_store_time
        self.log_monitor_stream = log_monitor_stream
        self.site_task_num = site_task_num
        self.event_store_num = event_store_num
        self.site_ecs_num = site_ecs_num
        self.custom_time_series = custom_time_series
        self.sms_count = sms_count
        self.phone_count = phone_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.period is not None:
            result['Period'] = self.period
        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit
        if self.auto_renew_period is not None:
            result['AutoRenewPeriod'] = self.auto_renew_period
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.suggest_type is not None:
            result['SuggestType'] = self.suggest_type
        if self.api_count is not None:
            result['ApiCount'] = self.api_count
        if self.site_operator_num is not None:
            result['SiteOperatorNum'] = self.site_operator_num
        if self.event_store_time is not None:
            result['EventStoreTime'] = self.event_store_time
        if self.log_monitor_stream is not None:
            result['LogMonitorStream'] = self.log_monitor_stream
        if self.site_task_num is not None:
            result['SiteTaskNum'] = self.site_task_num
        if self.event_store_num is not None:
            result['EventStoreNum'] = self.event_store_num
        if self.site_ecs_num is not None:
            result['SiteEcsNum'] = self.site_ecs_num
        if self.custom_time_series is not None:
            result['CustomTimeSeries'] = self.custom_time_series
        if self.sms_count is not None:
            result['SmsCount'] = self.sms_count
        if self.phone_count is not None:
            result['PhoneCount'] = self.phone_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')
        if m.get('AutoRenewPeriod') is not None:
            self.auto_renew_period = m.get('AutoRenewPeriod')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('SuggestType') is not None:
            self.suggest_type = m.get('SuggestType')
        if m.get('ApiCount') is not None:
            self.api_count = m.get('ApiCount')
        if m.get('SiteOperatorNum') is not None:
            self.site_operator_num = m.get('SiteOperatorNum')
        if m.get('EventStoreTime') is not None:
            self.event_store_time = m.get('EventStoreTime')
        if m.get('LogMonitorStream') is not None:
            self.log_monitor_stream = m.get('LogMonitorStream')
        if m.get('SiteTaskNum') is not None:
            self.site_task_num = m.get('SiteTaskNum')
        if m.get('EventStoreNum') is not None:
            self.event_store_num = m.get('EventStoreNum')
        if m.get('SiteEcsNum') is not None:
            self.site_ecs_num = m.get('SiteEcsNum')
        if m.get('CustomTimeSeries') is not None:
            self.custom_time_series = m.get('CustomTimeSeries')
        if m.get('SmsCount') is not None:
            self.sms_count = m.get('SmsCount')
        if m.get('PhoneCount') is not None:
            self.phone_count = m.get('PhoneCount')
        return self


class CreateCmsOrderResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        order_id: str = None,
    ):
        self.request_id = request_id
        self.order_id = order_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        return self


class CreateCmsOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateCmsOrderResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateCmsOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateCmsSmspackageOrderRequest(TeaModel):
    def __init__(
        self,
        period: int = None,
        period_unit: str = None,
        auto_renew_period: int = None,
        auto_pay: bool = None,
        auto_use_coupon: bool = None,
        sms_count: str = None,
    ):
        self.period = period
        self.period_unit = period_unit
        self.auto_renew_period = auto_renew_period
        self.auto_pay = auto_pay
        self.auto_use_coupon = auto_use_coupon
        self.sms_count = sms_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.period is not None:
            result['Period'] = self.period
        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit
        if self.auto_renew_period is not None:
            result['AutoRenewPeriod'] = self.auto_renew_period
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.sms_count is not None:
            result['SmsCount'] = self.sms_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')
        if m.get('AutoRenewPeriod') is not None:
            self.auto_renew_period = m.get('AutoRenewPeriod')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('SmsCount') is not None:
            self.sms_count = m.get('SmsCount')
        return self


class CreateCmsSmspackageOrderResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        order_id: str = None,
    ):
        self.request_id = request_id
        self.order_id = order_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        return self


class CreateCmsSmspackageOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateCmsSmspackageOrderResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateCmsSmspackageOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateDynamicTagGroupRequestMatchExpress(TeaModel):
    def __init__(
        self,
        tag_value_match_function: str = None,
        tag_value: str = None,
    ):
        self.tag_value_match_function = tag_value_match_function
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag_value_match_function is not None:
            result['TagValueMatchFunction'] = self.tag_value_match_function
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagValueMatchFunction') is not None:
            self.tag_value_match_function = m.get('TagValueMatchFunction')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class CreateDynamicTagGroupRequest(TeaModel):
    def __init__(
        self,
        tag_key: str = None,
        enable_subscribe_event: bool = None,
        enable_install_agent: bool = None,
        match_express_filter_relation: str = None,
        match_express: List[CreateDynamicTagGroupRequestMatchExpress] = None,
        contact_group_list: List[str] = None,
        template_id_list: List[str] = None,
    ):
        self.tag_key = tag_key
        self.enable_subscribe_event = enable_subscribe_event
        self.enable_install_agent = enable_install_agent
        self.match_express_filter_relation = match_express_filter_relation
        self.match_express = match_express
        self.contact_group_list = contact_group_list
        self.template_id_list = template_id_list

    def validate(self):
        if self.match_express:
            for k in self.match_express:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.enable_subscribe_event is not None:
            result['EnableSubscribeEvent'] = self.enable_subscribe_event
        if self.enable_install_agent is not None:
            result['EnableInstallAgent'] = self.enable_install_agent
        if self.match_express_filter_relation is not None:
            result['MatchExpressFilterRelation'] = self.match_express_filter_relation
        result['MatchExpress'] = []
        if self.match_express is not None:
            for k in self.match_express:
                result['MatchExpress'].append(k.to_map() if k else None)
        if self.contact_group_list is not None:
            result['ContactGroupList'] = self.contact_group_list
        if self.template_id_list is not None:
            result['TemplateIdList'] = self.template_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('EnableSubscribeEvent') is not None:
            self.enable_subscribe_event = m.get('EnableSubscribeEvent')
        if m.get('EnableInstallAgent') is not None:
            self.enable_install_agent = m.get('EnableInstallAgent')
        if m.get('MatchExpressFilterRelation') is not None:
            self.match_express_filter_relation = m.get('MatchExpressFilterRelation')
        self.match_express = []
        if m.get('MatchExpress') is not None:
            for k in m.get('MatchExpress'):
                temp_model = CreateDynamicTagGroupRequestMatchExpress()
                self.match_express.append(temp_model.from_map(k))
        if m.get('ContactGroupList') is not None:
            self.contact_group_list = m.get('ContactGroupList')
        if m.get('TemplateIdList') is not None:
            self.template_id_list = m.get('TemplateIdList')
        return self


class CreateDynamicTagGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateDynamicTagGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateDynamicTagGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateDynamicTagGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateGroupMetricRulesRequestGroupMetricRulesEscalationsInfo(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        times: int = None,
        statistics: str = None,
        comparison_operator: str = None,
    ):
        self.threshold = threshold
        self.times = times
        self.statistics = statistics
        self.comparison_operator = comparison_operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        return self


class CreateGroupMetricRulesRequestGroupMetricRulesEscalationsWarn(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        comparison_operator: str = None,
        times: int = None,
        statistics: str = None,
    ):
        self.threshold = threshold
        self.comparison_operator = comparison_operator
        self.times = times
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class CreateGroupMetricRulesRequestGroupMetricRulesEscalationsCritical(TeaModel):
    def __init__(
        self,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
        comparison_operator: str = None,
    ):
        self.times = times
        self.threshold = threshold
        self.statistics = statistics
        self.comparison_operator = comparison_operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        return self


class CreateGroupMetricRulesRequestGroupMetricRulesEscalations(TeaModel):
    def __init__(
        self,
        info: CreateGroupMetricRulesRequestGroupMetricRulesEscalationsInfo = None,
        warn: CreateGroupMetricRulesRequestGroupMetricRulesEscalationsWarn = None,
        critical: CreateGroupMetricRulesRequestGroupMetricRulesEscalationsCritical = None,
    ):
        self.info = info
        self.warn = warn
        self.critical = critical

    def validate(self):
        self.validate_required(self.info, 'info')
        if self.info:
            self.info.validate()
        self.validate_required(self.warn, 'warn')
        if self.warn:
            self.warn.validate()
        self.validate_required(self.critical, 'critical')
        if self.critical:
            self.critical.validate()

    def to_map(self):
        result = dict()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Info') is not None:
            temp_model = CreateGroupMetricRulesRequestGroupMetricRulesEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = CreateGroupMetricRulesRequestGroupMetricRulesEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        if m.get('Critical') is not None:
            temp_model = CreateGroupMetricRulesRequestGroupMetricRulesEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        return self


class CreateGroupMetricRulesRequestGroupMetricRules(TeaModel):
    def __init__(
        self,
        escalations: CreateGroupMetricRulesRequestGroupMetricRulesEscalations = None,
        metric_name: str = None,
        no_effective_interval: str = None,
        effective_interval: str = None,
        rule_id: str = None,
        dimensions: str = None,
        silence_time: int = None,
        webhook: str = None,
        namespace: str = None,
        email_subject: str = None,
        period: str = None,
        rule_name: str = None,
        interval: str = None,
        category: str = None,
    ):
        self.escalations = escalations
        self.metric_name = metric_name
        self.no_effective_interval = no_effective_interval
        self.effective_interval = effective_interval
        self.rule_id = rule_id
        self.dimensions = dimensions
        self.silence_time = silence_time
        self.webhook = webhook
        self.namespace = namespace
        self.email_subject = email_subject
        self.period = period
        self.rule_name = rule_name
        self.interval = interval
        self.category = category

    def validate(self):
        self.validate_required(self.escalations, 'escalations')
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.email_subject is not None:
            result['EmailSubject'] = self.email_subject
        if self.period is not None:
            result['Period'] = self.period
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Escalations') is not None:
            temp_model = CreateGroupMetricRulesRequestGroupMetricRulesEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('EmailSubject') is not None:
            self.email_subject = m.get('EmailSubject')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class CreateGroupMetricRulesRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        group_metric_rules: List[CreateGroupMetricRulesRequestGroupMetricRules] = None,
    ):
        self.group_id = group_id
        self.group_metric_rules = group_metric_rules

    def validate(self):
        if self.group_metric_rules:
            for k in self.group_metric_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        result['GroupMetricRules'] = []
        if self.group_metric_rules is not None:
            for k in self.group_metric_rules:
                result['GroupMetricRules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        self.group_metric_rules = []
        if m.get('GroupMetricRules') is not None:
            for k in m.get('GroupMetricRules'):
                temp_model = CreateGroupMetricRulesRequestGroupMetricRules()
                self.group_metric_rules.append(temp_model.from_map(k))
        return self


class CreateGroupMetricRulesResponseBodyResourcesAlertResult(TeaModel):
    def __init__(
        self,
        success: bool = None,
        code: int = None,
        message: str = None,
        rule_name: str = None,
        rule_id: str = None,
    ):
        self.success = success
        self.code = code
        self.message = message
        self.rule_name = rule_name
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.success is not None:
            result['Success'] = self.success
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class CreateGroupMetricRulesResponseBodyResources(TeaModel):
    def __init__(
        self,
        alert_result: List[CreateGroupMetricRulesResponseBodyResourcesAlertResult] = None,
    ):
        self.alert_result = alert_result

    def validate(self):
        if self.alert_result:
            for k in self.alert_result:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertResult'] = []
        if self.alert_result is not None:
            for k in self.alert_result:
                result['AlertResult'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_result = []
        if m.get('AlertResult') is not None:
            for k in m.get('AlertResult'):
                temp_model = CreateGroupMetricRulesResponseBodyResourcesAlertResult()
                self.alert_result.append(temp_model.from_map(k))
        return self


class CreateGroupMetricRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        resources: CreateGroupMetricRulesResponseBodyResources = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.resources = resources
        self.code = code
        self.success = success

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Resources') is not None:
            temp_model = CreateGroupMetricRulesResponseBodyResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateGroupMetricRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateGroupMetricRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateGroupMetricRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateGroupMonitoringAgentProcessRequestMatchExpress(TeaModel):
    def __init__(
        self,
        value: str = None,
        function: str = None,
        name: str = None,
    ):
        self.value = value
        self.function = function
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.function is not None:
            result['Function'] = self.function
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Function') is not None:
            self.function = m.get('Function')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class CreateGroupMonitoringAgentProcessRequestAlertConfig(TeaModel):
    def __init__(
        self,
        silence_time: str = None,
        comparison_operator: str = None,
        webhook: str = None,
        times: str = None,
        escalations_level: str = None,
        no_effective_interval: str = None,
        effective_interval: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.silence_time = silence_time
        self.comparison_operator = comparison_operator
        self.webhook = webhook
        self.times = times
        self.escalations_level = escalations_level
        self.no_effective_interval = no_effective_interval
        self.effective_interval = effective_interval
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.times is not None:
            result['Times'] = self.times
        if self.escalations_level is not None:
            result['EscalationsLevel'] = self.escalations_level
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('EscalationsLevel') is not None:
            self.escalations_level = m.get('EscalationsLevel')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class CreateGroupMonitoringAgentProcessRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        process_name: str = None,
        match_express_filter_relation: str = None,
        match_express: List[CreateGroupMonitoringAgentProcessRequestMatchExpress] = None,
        alert_config: List[CreateGroupMonitoringAgentProcessRequestAlertConfig] = None,
    ):
        self.group_id = group_id
        self.process_name = process_name
        self.match_express_filter_relation = match_express_filter_relation
        self.match_express = match_express
        self.alert_config = alert_config

    def validate(self):
        if self.match_express:
            for k in self.match_express:
                if k:
                    k.validate()
        if self.alert_config:
            for k in self.alert_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.match_express_filter_relation is not None:
            result['MatchExpressFilterRelation'] = self.match_express_filter_relation
        result['MatchExpress'] = []
        if self.match_express is not None:
            for k in self.match_express:
                result['MatchExpress'].append(k.to_map() if k else None)
        result['AlertConfig'] = []
        if self.alert_config is not None:
            for k in self.alert_config:
                result['AlertConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('MatchExpressFilterRelation') is not None:
            self.match_express_filter_relation = m.get('MatchExpressFilterRelation')
        self.match_express = []
        if m.get('MatchExpress') is not None:
            for k in m.get('MatchExpress'):
                temp_model = CreateGroupMonitoringAgentProcessRequestMatchExpress()
                self.match_express.append(temp_model.from_map(k))
        self.alert_config = []
        if m.get('AlertConfig') is not None:
            for k in m.get('AlertConfig'):
                temp_model = CreateGroupMonitoringAgentProcessRequestAlertConfig()
                self.alert_config.append(temp_model.from_map(k))
        return self


class CreateGroupMonitoringAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateGroupMonitoringAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateGroupMonitoringAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateGroupMonitoringAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateHostAvailabilityRequestTaskOption(TeaModel):
    def __init__(
        self,
        http_uri: str = None,
        telnet_or_ping_host: str = None,
        http_response_charset: str = None,
        http_post_content: str = None,
        http_response_match_content: str = None,
        http_method: str = None,
        http_negative: bool = None,
    ):
        self.http_uri = http_uri
        self.telnet_or_ping_host = telnet_or_ping_host
        self.http_response_charset = http_response_charset
        self.http_post_content = http_post_content
        self.http_response_match_content = http_response_match_content
        self.http_method = http_method
        self.http_negative = http_negative

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.http_uri is not None:
            result['HttpURI'] = self.http_uri
        if self.telnet_or_ping_host is not None:
            result['TelnetOrPingHost'] = self.telnet_or_ping_host
        if self.http_response_charset is not None:
            result['HttpResponseCharset'] = self.http_response_charset
        if self.http_post_content is not None:
            result['HttpPostContent'] = self.http_post_content
        if self.http_response_match_content is not None:
            result['HttpResponseMatchContent'] = self.http_response_match_content
        if self.http_method is not None:
            result['HttpMethod'] = self.http_method
        if self.http_negative is not None:
            result['HttpNegative'] = self.http_negative
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HttpURI') is not None:
            self.http_uri = m.get('HttpURI')
        if m.get('TelnetOrPingHost') is not None:
            self.telnet_or_ping_host = m.get('TelnetOrPingHost')
        if m.get('HttpResponseCharset') is not None:
            self.http_response_charset = m.get('HttpResponseCharset')
        if m.get('HttpPostContent') is not None:
            self.http_post_content = m.get('HttpPostContent')
        if m.get('HttpResponseMatchContent') is not None:
            self.http_response_match_content = m.get('HttpResponseMatchContent')
        if m.get('HttpMethod') is not None:
            self.http_method = m.get('HttpMethod')
        if m.get('HttpNegative') is not None:
            self.http_negative = m.get('HttpNegative')
        return self


class CreateHostAvailabilityRequestAlertConfig(TeaModel):
    def __init__(
        self,
        notify_type: int = None,
        start_time: int = None,
        end_time: int = None,
        silence_time: int = None,
        web_hook: str = None,
    ):
        self.notify_type = notify_type
        self.start_time = start_time
        self.end_time = end_time
        self.silence_time = silence_time
        self.web_hook = web_hook

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.notify_type is not None:
            result['NotifyType'] = self.notify_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.web_hook is not None:
            result['WebHook'] = self.web_hook
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NotifyType') is not None:
            self.notify_type = m.get('NotifyType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('WebHook') is not None:
            self.web_hook = m.get('WebHook')
        return self


class CreateHostAvailabilityRequestAlertConfigEscalationList(TeaModel):
    def __init__(
        self,
        value: str = None,
        metric_name: str = None,
        times: int = None,
        operator: str = None,
        aggregate: str = None,
    ):
        self.value = value
        self.metric_name = metric_name
        self.times = times
        self.operator = operator
        self.aggregate = aggregate

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.times is not None:
            result['Times'] = self.times
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.aggregate is not None:
            result['Aggregate'] = self.aggregate
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Aggregate') is not None:
            self.aggregate = m.get('Aggregate')
        return self


class CreateHostAvailabilityRequest(TeaModel):
    def __init__(
        self,
        task_option: CreateHostAvailabilityRequestTaskOption = None,
        alert_config: CreateHostAvailabilityRequestAlertConfig = None,
        group_id: int = None,
        task_name: str = None,
        task_scope: str = None,
        task_type: str = None,
        alert_config_escalation_list: List[CreateHostAvailabilityRequestAlertConfigEscalationList] = None,
        instance_list: List[str] = None,
    ):
        self.task_option = task_option
        self.alert_config = alert_config
        self.group_id = group_id
        self.task_name = task_name
        self.task_scope = task_scope
        self.task_type = task_type
        self.alert_config_escalation_list = alert_config_escalation_list
        self.instance_list = instance_list

    def validate(self):
        if self.task_option:
            self.task_option.validate()
        if self.alert_config:
            self.alert_config.validate()
        if self.alert_config_escalation_list:
            for k in self.alert_config_escalation_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.task_option is not None:
            result['TaskOption'] = self.task_option.to_map()
        if self.alert_config is not None:
            result['AlertConfig'] = self.alert_config.to_map()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_scope is not None:
            result['TaskScope'] = self.task_scope
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        result['AlertConfigEscalationList'] = []
        if self.alert_config_escalation_list is not None:
            for k in self.alert_config_escalation_list:
                result['AlertConfigEscalationList'].append(k.to_map() if k else None)
        if self.instance_list is not None:
            result['InstanceList'] = self.instance_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskOption') is not None:
            temp_model = CreateHostAvailabilityRequestTaskOption()
            self.task_option = temp_model.from_map(m['TaskOption'])
        if m.get('AlertConfig') is not None:
            temp_model = CreateHostAvailabilityRequestAlertConfig()
            self.alert_config = temp_model.from_map(m['AlertConfig'])
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskScope') is not None:
            self.task_scope = m.get('TaskScope')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        self.alert_config_escalation_list = []
        if m.get('AlertConfigEscalationList') is not None:
            for k in m.get('AlertConfigEscalationList'):
                temp_model = CreateHostAvailabilityRequestAlertConfigEscalationList()
                self.alert_config_escalation_list.append(temp_model.from_map(k))
        if m.get('InstanceList') is not None:
            self.instance_list = m.get('InstanceList')
        return self


class CreateHostAvailabilityResponseBody(TeaModel):
    def __init__(
        self,
        task_id: int = None,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.task_id = task_id
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateHostAvailabilityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateHostAvailabilityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateHostAvailabilityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMetricRuleResourcesRequest(TeaModel):
    def __init__(
        self,
        rule_id: str = None,
        overwrite: str = None,
        resources: str = None,
    ):
        self.rule_id = rule_id
        self.overwrite = overwrite
        self.resources = resources

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.overwrite is not None:
            result['Overwrite'] = self.overwrite
        if self.resources is not None:
            result['Resources'] = self.resources
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Overwrite') is not None:
            self.overwrite = m.get('Overwrite')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        return self


class CreateMetricRuleResourcesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateMetricRuleResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMetricRuleResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMetricRuleResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMetricRuleTemplateRequestAlertTemplatesEscalationsInfo(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        statistics: str = None,
        comparison_operator: str = None,
        times: int = None,
    ):
        self.threshold = threshold
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class CreateMetricRuleTemplateRequestAlertTemplatesEscalationsWarn(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        times: int = None,
        comparison_operator: str = None,
        statistics: str = None,
    ):
        self.threshold = threshold
        self.times = times
        self.comparison_operator = comparison_operator
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class CreateMetricRuleTemplateRequestAlertTemplatesEscalationsCritical(TeaModel):
    def __init__(
        self,
        times: int = None,
        threshold: str = None,
        comparison_operator: str = None,
        statistics: str = None,
    ):
        self.times = times
        self.threshold = threshold
        self.comparison_operator = comparison_operator
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class CreateMetricRuleTemplateRequestAlertTemplatesEscalations(TeaModel):
    def __init__(
        self,
        info: CreateMetricRuleTemplateRequestAlertTemplatesEscalationsInfo = None,
        warn: CreateMetricRuleTemplateRequestAlertTemplatesEscalationsWarn = None,
        critical: CreateMetricRuleTemplateRequestAlertTemplatesEscalationsCritical = None,
    ):
        self.info = info
        self.warn = warn
        self.critical = critical

    def validate(self):
        self.validate_required(self.info, 'info')
        if self.info:
            self.info.validate()
        self.validate_required(self.warn, 'warn')
        if self.warn:
            self.warn.validate()
        self.validate_required(self.critical, 'critical')
        if self.critical:
            self.critical.validate()

    def to_map(self):
        result = dict()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Info') is not None:
            temp_model = CreateMetricRuleTemplateRequestAlertTemplatesEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = CreateMetricRuleTemplateRequestAlertTemplatesEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        if m.get('Critical') is not None:
            temp_model = CreateMetricRuleTemplateRequestAlertTemplatesEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        return self


class CreateMetricRuleTemplateRequestAlertTemplates(TeaModel):
    def __init__(
        self,
        escalations: CreateMetricRuleTemplateRequestAlertTemplatesEscalations = None,
        metric_name: str = None,
        webhook: str = None,
        namespace: str = None,
        rule_name: str = None,
        period: int = None,
        selector: str = None,
        category: str = None,
    ):
        self.escalations = escalations
        self.metric_name = metric_name
        self.webhook = webhook
        self.namespace = namespace
        self.rule_name = rule_name
        self.period = period
        self.selector = selector
        self.category = category

    def validate(self):
        self.validate_required(self.escalations, 'escalations')
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.period is not None:
            result['Period'] = self.period
        if self.selector is not None:
            result['Selector'] = self.selector
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Escalations') is not None:
            temp_model = CreateMetricRuleTemplateRequestAlertTemplatesEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Selector') is not None:
            self.selector = m.get('Selector')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class CreateMetricRuleTemplateRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        description: str = None,
        alert_templates: List[CreateMetricRuleTemplateRequestAlertTemplates] = None,
    ):
        self.name = name
        self.description = description
        self.alert_templates = alert_templates

    def validate(self):
        if self.alert_templates:
            for k in self.alert_templates:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        result['AlertTemplates'] = []
        if self.alert_templates is not None:
            for k in self.alert_templates:
                result['AlertTemplates'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        self.alert_templates = []
        if m.get('AlertTemplates') is not None:
            for k in m.get('AlertTemplates'):
                temp_model = CreateMetricRuleTemplateRequestAlertTemplates()
                self.alert_templates.append(temp_model.from_map(k))
        return self


class CreateMetricRuleTemplateResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        id: int = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.id = id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.id is not None:
            result['Id'] = self.id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateMetricRuleTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMetricRuleTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMetricRuleTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMonitorAgentProcessRequest(TeaModel):
    def __init__(
        self,
        process_name: str = None,
        instance_id: str = None,
        process_user: str = None,
    ):
        self.process_name = process_name
        self.instance_id = instance_id
        self.process_user = process_user

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.process_user is not None:
            result['ProcessUser'] = self.process_user
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ProcessUser') is not None:
            self.process_user = m.get('ProcessUser')
        return self


class CreateMonitorAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        id: int = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.id = id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.id is not None:
            result['Id'] = self.id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateMonitorAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMonitorAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMonitorAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMonitorGroupRequest(TeaModel):
    def __init__(
        self,
        type: str = None,
        group_name: str = None,
        service_id: int = None,
        bind_url: str = None,
        contact_groups: str = None,
        options: str = None,
    ):
        self.type = type
        self.group_name = group_name
        self.service_id = service_id
        self.bind_url = bind_url
        self.contact_groups = contact_groups
        self.options = options

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.service_id is not None:
            result['ServiceId'] = self.service_id
        if self.bind_url is not None:
            result['BindUrl'] = self.bind_url
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.options is not None:
            result['Options'] = self.options
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('ServiceId') is not None:
            self.service_id = m.get('ServiceId')
        if m.get('BindUrl') is not None:
            self.bind_url = m.get('BindUrl')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Options') is not None:
            self.options = m.get('Options')
        return self


class CreateMonitorGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
        group_id: int = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class CreateMonitorGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMonitorGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMonitorGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMonitorGroupByResourceGroupIdRequest(TeaModel):
    def __init__(
        self,
        enable_subscribe_event: bool = None,
        enable_install_agent: bool = None,
        region_id: str = None,
        resource_group_id: str = None,
        resource_group_name: str = None,
        contact_group_list: List[str] = None,
    ):
        self.enable_subscribe_event = enable_subscribe_event
        self.enable_install_agent = enable_install_agent
        self.region_id = region_id
        self.resource_group_id = resource_group_id
        self.resource_group_name = resource_group_name
        self.contact_group_list = contact_group_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.enable_subscribe_event is not None:
            result['EnableSubscribeEvent'] = self.enable_subscribe_event
        if self.enable_install_agent is not None:
            result['EnableInstallAgent'] = self.enable_install_agent
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.resource_group_name is not None:
            result['ResourceGroupName'] = self.resource_group_name
        if self.contact_group_list is not None:
            result['ContactGroupList'] = self.contact_group_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnableSubscribeEvent') is not None:
            self.enable_subscribe_event = m.get('EnableSubscribeEvent')
        if m.get('EnableInstallAgent') is not None:
            self.enable_install_agent = m.get('EnableInstallAgent')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ResourceGroupName') is not None:
            self.resource_group_name = m.get('ResourceGroupName')
        if m.get('ContactGroupList') is not None:
            self.contact_group_list = m.get('ContactGroupList')
        return self


class CreateMonitorGroupByResourceGroupIdResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateMonitorGroupByResourceGroupIdResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMonitorGroupByResourceGroupIdResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMonitorGroupByResourceGroupIdResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMonitorGroupInstancesRequestInstances(TeaModel):
    def __init__(
        self,
        instance_name: str = None,
        category: str = None,
        instance_id: str = None,
        region_id: str = None,
    ):
        self.instance_name = instance_name
        self.category = category
        self.instance_id = instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.category is not None:
            result['Category'] = self.category
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class CreateMonitorGroupInstancesRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        instances: List[CreateMonitorGroupInstancesRequestInstances] = None,
    ):
        self.group_id = group_id
        self.instances = instances

    def validate(self):
        if self.instances:
            for k in self.instances:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        result['Instances'] = []
        if self.instances is not None:
            for k in self.instances:
                result['Instances'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        self.instances = []
        if m.get('Instances') is not None:
            for k in m.get('Instances'):
                temp_model = CreateMonitorGroupInstancesRequestInstances()
                self.instances.append(temp_model.from_map(k))
        return self


class CreateMonitorGroupInstancesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateMonitorGroupInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMonitorGroupInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMonitorGroupInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMonitorGroupNotifyPolicyRequest(TeaModel):
    def __init__(
        self,
        policy_type: str = None,
        group_id: str = None,
        start_time: int = None,
        end_time: int = None,
    ):
        self.policy_type = policy_type
        self.group_id = group_id
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.policy_type is not None:
            result['PolicyType'] = self.policy_type
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PolicyType') is not None:
            self.policy_type = m.get('PolicyType')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        return self


class CreateMonitorGroupNotifyPolicyResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: str = None,
        result: int = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.result is not None:
            result['Result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        return self


class CreateMonitorGroupNotifyPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMonitorGroupNotifyPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMonitorGroupNotifyPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMonitoringAgentProcessRequest(TeaModel):
    def __init__(
        self,
        process_name: str = None,
        instance_id: str = None,
        process_user: str = None,
    ):
        self.process_name = process_name
        self.instance_id = instance_id
        self.process_user = process_user

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.process_user is not None:
            result['ProcessUser'] = self.process_user
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ProcessUser') is not None:
            self.process_user = m.get('ProcessUser')
        return self


class CreateMonitoringAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        id: int = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.id = id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.id is not None:
            result['Id'] = self.id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateMonitoringAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateMonitoringAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateMonitoringAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateSiteMonitorRequest(TeaModel):
    def __init__(
        self,
        address: str = None,
        task_type: str = None,
        task_name: str = None,
        interval: str = None,
        isp_cities: str = None,
        options_json: str = None,
        alert_ids: str = None,
    ):
        self.address = address
        self.task_type = task_type
        self.task_name = task_name
        self.interval = interval
        self.isp_cities = isp_cities
        self.options_json = options_json
        self.alert_ids = alert_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.address is not None:
            result['Address'] = self.address
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.isp_cities is not None:
            result['IspCities'] = self.isp_cities
        if self.options_json is not None:
            result['OptionsJson'] = self.options_json
        if self.alert_ids is not None:
            result['AlertIds'] = self.alert_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Address') is not None:
            self.address = m.get('Address')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('IspCities') is not None:
            self.isp_cities = m.get('IspCities')
        if m.get('OptionsJson') is not None:
            self.options_json = m.get('OptionsJson')
        if m.get('AlertIds') is not None:
            self.alert_ids = m.get('AlertIds')
        return self


class CreateSiteMonitorResponseBodyDataAttachAlertResultContact(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: str = None,
        code: str = None,
        message: str = None,
        rule_id: str = None,
    ):
        self.request_id = request_id
        self.success = success
        self.code = code
        self.message = message
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class CreateSiteMonitorResponseBodyDataAttachAlertResult(TeaModel):
    def __init__(
        self,
        contact: List[CreateSiteMonitorResponseBodyDataAttachAlertResultContact] = None,
    ):
        self.contact = contact

    def validate(self):
        if self.contact:
            for k in self.contact:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Contact'] = []
        if self.contact is not None:
            for k in self.contact:
                result['Contact'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact = []
        if m.get('Contact') is not None:
            for k in m.get('Contact'):
                temp_model = CreateSiteMonitorResponseBodyDataAttachAlertResultContact()
                self.contact.append(temp_model.from_map(k))
        return self


class CreateSiteMonitorResponseBodyData(TeaModel):
    def __init__(
        self,
        attach_alert_result: CreateSiteMonitorResponseBodyDataAttachAlertResult = None,
    ):
        self.attach_alert_result = attach_alert_result

    def validate(self):
        if self.attach_alert_result:
            self.attach_alert_result.validate()

    def to_map(self):
        result = dict()
        if self.attach_alert_result is not None:
            result['AttachAlertResult'] = self.attach_alert_result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AttachAlertResult') is not None:
            temp_model = CreateSiteMonitorResponseBodyDataAttachAlertResult()
            self.attach_alert_result = temp_model.from_map(m['AttachAlertResult'])
        return self


class CreateSiteMonitorResponseBodyCreateResultListCreateResultList(TeaModel):
    def __init__(
        self,
        task_name: str = None,
        task_id: str = None,
    ):
        self.task_name = task_name
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class CreateSiteMonitorResponseBodyCreateResultList(TeaModel):
    def __init__(
        self,
        create_result_list: List[CreateSiteMonitorResponseBodyCreateResultListCreateResultList] = None,
    ):
        self.create_result_list = create_result_list

    def validate(self):
        if self.create_result_list:
            for k in self.create_result_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['CreateResultList'] = []
        if self.create_result_list is not None:
            for k in self.create_result_list:
                result['CreateResultList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.create_result_list = []
        if m.get('CreateResultList') is not None:
            for k in m.get('CreateResultList'):
                temp_model = CreateSiteMonitorResponseBodyCreateResultListCreateResultList()
                self.create_result_list.append(temp_model.from_map(k))
        return self


class CreateSiteMonitorResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: CreateSiteMonitorResponseBodyData = None,
        code: str = None,
        create_result_list: CreateSiteMonitorResponseBodyCreateResultList = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.create_result_list = create_result_list
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()
        if self.create_result_list:
            self.create_result_list.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.create_result_list is not None:
            result['CreateResultList'] = self.create_result_list.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = CreateSiteMonitorResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('CreateResultList') is not None:
            temp_model = CreateSiteMonitorResponseBodyCreateResultList()
            self.create_result_list = temp_model.from_map(m['CreateResultList'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateSiteMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateSiteMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateSiteMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteContactRequest(TeaModel):
    def __init__(
        self,
        contact_name: str = None,
    ):
        self.contact_name = contact_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_name is not None:
            result['ContactName'] = self.contact_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactName') is not None:
            self.contact_name = m.get('ContactName')
        return self


class DeleteContactResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteContactResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteContactResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteContactResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteContactGroupRequest(TeaModel):
    def __init__(
        self,
        contact_group_name: str = None,
    ):
        self.contact_group_name = contact_group_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group_name is not None:
            result['ContactGroupName'] = self.contact_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupName') is not None:
            self.contact_group_name = m.get('ContactGroupName')
        return self


class DeleteContactGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteContactGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteContactGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteContactGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteCustomMetricRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        metric_name: str = None,
        md_5: str = None,
        uuid: str = None,
    ):
        self.group_id = group_id
        self.metric_name = metric_name
        self.md_5 = md_5
        self.uuid = uuid

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.md_5 is not None:
            result['Md5'] = self.md_5
        if self.uuid is not None:
            result['UUID'] = self.uuid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Md5') is not None:
            self.md_5 = m.get('Md5')
        if m.get('UUID') is not None:
            self.uuid = m.get('UUID')
        return self


class DeleteCustomMetricResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        return self


class DeleteCustomMetricResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteCustomMetricResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteCustomMetricResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDynamicTagGroupRequest(TeaModel):
    def __init__(
        self,
        dynamic_tag_rule_id: str = None,
    ):
        self.dynamic_tag_rule_id = dynamic_tag_rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dynamic_tag_rule_id is not None:
            result['DynamicTagRuleId'] = self.dynamic_tag_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DynamicTagRuleId') is not None:
            self.dynamic_tag_rule_id = m.get('DynamicTagRuleId')
        return self


class DeleteDynamicTagGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteDynamicTagGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteDynamicTagGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteDynamicTagGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteEventRulesRequest(TeaModel):
    def __init__(
        self,
        rule_names: List[str] = None,
    ):
        self.rule_names = rule_names

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_names is not None:
            result['RuleNames'] = self.rule_names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleNames') is not None:
            self.rule_names = m.get('RuleNames')
        return self


class DeleteEventRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteEventRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteEventRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteEventRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteEventRuleTargetsRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
        ids: List[str] = None,
    ):
        self.rule_name = rule_name
        self.ids = ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.ids is not None:
            result['Ids'] = self.ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Ids') is not None:
            self.ids = m.get('Ids')
        return self


class DeleteEventRuleTargetsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteEventRuleTargetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteEventRuleTargetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteEventRuleTargetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteExporterOutputRequest(TeaModel):
    def __init__(
        self,
        dest_name: str = None,
    ):
        self.dest_name = dest_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dest_name is not None:
            result['DestName'] = self.dest_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DestName') is not None:
            self.dest_name = m.get('DestName')
        return self


class DeleteExporterOutputResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteExporterOutputResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteExporterOutputResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteExporterOutputResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteExporterRuleRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
    ):
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class DeleteExporterRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteExporterRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteExporterRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteExporterRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteGroupMonitoringAgentProcessRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        id: str = None,
    ):
        self.group_id = group_id
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DeleteGroupMonitoringAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteGroupMonitoringAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteGroupMonitoringAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteGroupMonitoringAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteHostAvailabilityRequest(TeaModel):
    def __init__(
        self,
        id: List[int] = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DeleteHostAvailabilityResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteHostAvailabilityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteHostAvailabilityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteHostAvailabilityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteLogMonitorRequest(TeaModel):
    def __init__(
        self,
        log_id: int = None,
    ):
        self.log_id = log_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.log_id is not None:
            result['LogId'] = self.log_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LogId') is not None:
            self.log_id = m.get('LogId')
        return self


class DeleteLogMonitorResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteLogMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteLogMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteLogMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMetricRuleResourcesRequest(TeaModel):
    def __init__(
        self,
        rule_id: str = None,
        resources: str = None,
    ):
        self.rule_id = rule_id
        self.resources = resources

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.resources is not None:
            result['Resources'] = self.resources
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        return self


class DeleteMetricRuleResourcesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMetricRuleResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMetricRuleResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMetricRuleResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMetricRulesRequest(TeaModel):
    def __init__(
        self,
        id: List[str] = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DeleteMetricRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMetricRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMetricRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMetricRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMetricRuleTargetsRequest(TeaModel):
    def __init__(
        self,
        rule_id: str = None,
        target_ids: List[str] = None,
    ):
        self.rule_id = rule_id
        self.target_ids = target_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.target_ids is not None:
            result['TargetIds'] = self.target_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('TargetIds') is not None:
            self.target_ids = m.get('TargetIds')
        return self


class DeleteMetricRuleTargetsResponseBodyFailIdsTargetIds(TeaModel):
    def __init__(
        self,
        target_id: List[str] = None,
    ):
        self.target_id = target_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.target_id is not None:
            result['TargetId'] = self.target_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TargetId') is not None:
            self.target_id = m.get('TargetId')
        return self


class DeleteMetricRuleTargetsResponseBodyFailIds(TeaModel):
    def __init__(
        self,
        target_ids: DeleteMetricRuleTargetsResponseBodyFailIdsTargetIds = None,
    ):
        self.target_ids = target_ids

    def validate(self):
        if self.target_ids:
            self.target_ids.validate()

    def to_map(self):
        result = dict()
        if self.target_ids is not None:
            result['TargetIds'] = self.target_ids.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TargetIds') is not None:
            temp_model = DeleteMetricRuleTargetsResponseBodyFailIdsTargetIds()
            self.target_ids = temp_model.from_map(m['TargetIds'])
        return self


class DeleteMetricRuleTargetsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        fail_ids: DeleteMetricRuleTargetsResponseBodyFailIds = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.fail_ids = fail_ids

    def validate(self):
        if self.fail_ids:
            self.fail_ids.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.fail_ids is not None:
            result['FailIds'] = self.fail_ids.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('FailIds') is not None:
            temp_model = DeleteMetricRuleTargetsResponseBodyFailIds()
            self.fail_ids = temp_model.from_map(m['FailIds'])
        return self


class DeleteMetricRuleTargetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMetricRuleTargetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMetricRuleTargetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMetricRuleTemplateRequest(TeaModel):
    def __init__(
        self,
        template_id: str = None,
    ):
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DeleteMetricRuleTemplateResponseBodyResource(TeaModel):
    def __init__(
        self,
        template_id: str = None,
    ):
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DeleteMetricRuleTemplateResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        resource: DeleteMetricRuleTemplateResponseBodyResource = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.resource = resource
        self.code = code
        self.success = success

    def validate(self):
        if self.resource:
            self.resource.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource is not None:
            result['Resource'] = self.resource.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Resource') is not None:
            temp_model = DeleteMetricRuleTemplateResponseBodyResource()
            self.resource = temp_model.from_map(m['Resource'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMetricRuleTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMetricRuleTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMetricRuleTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMonitorGroupRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
    ):
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DeleteMonitorGroupResponseBodyGroupContactGroupsContactGroup(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeleteMonitorGroupResponseBodyGroupContactGroups(TeaModel):
    def __init__(
        self,
        contact_group: List[DeleteMonitorGroupResponseBodyGroupContactGroupsContactGroup] = None,
    ):
        self.contact_group = contact_group

    def validate(self):
        if self.contact_group:
            for k in self.contact_group:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContactGroup'] = []
        if self.contact_group is not None:
            for k in self.contact_group:
                result['ContactGroup'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact_group = []
        if m.get('ContactGroup') is not None:
            for k in m.get('ContactGroup'):
                temp_model = DeleteMonitorGroupResponseBodyGroupContactGroupsContactGroup()
                self.contact_group.append(temp_model.from_map(k))
        return self


class DeleteMonitorGroupResponseBodyGroup(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        contact_groups: DeleteMonitorGroupResponseBodyGroupContactGroups = None,
    ):
        self.group_name = group_name
        self.contact_groups = contact_groups

    def validate(self):
        if self.contact_groups:
            self.contact_groups.validate()

    def to_map(self):
        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('ContactGroups') is not None:
            temp_model = DeleteMonitorGroupResponseBodyGroupContactGroups()
            self.contact_groups = temp_model.from_map(m['ContactGroups'])
        return self


class DeleteMonitorGroupResponseBody(TeaModel):
    def __init__(
        self,
        group: DeleteMonitorGroupResponseBodyGroup = None,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.group = group
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        if self.group:
            self.group.validate()

    def to_map(self):
        result = dict()
        if self.group is not None:
            result['Group'] = self.group.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Group') is not None:
            temp_model = DeleteMonitorGroupResponseBodyGroup()
            self.group = temp_model.from_map(m['Group'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMonitorGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMonitorGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMonitorGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMonitorGroupDynamicRuleRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        category: str = None,
    ):
        self.group_id = group_id
        self.category = category

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class DeleteMonitorGroupDynamicRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMonitorGroupDynamicRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMonitorGroupDynamicRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMonitorGroupDynamicRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMonitorGroupInstancesRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        instance_id_list: str = None,
        category: str = None,
    ):
        self.group_id = group_id
        self.instance_id_list = instance_id_list
        self.category = category

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.instance_id_list is not None:
            result['InstanceIdList'] = self.instance_id_list
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('InstanceIdList') is not None:
            self.instance_id_list = m.get('InstanceIdList')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class DeleteMonitorGroupInstancesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMonitorGroupInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMonitorGroupInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMonitorGroupInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMonitorGroupNotifyPolicyRequest(TeaModel):
    def __init__(
        self,
        policy_type: str = None,
        group_id: str = None,
    ):
        self.policy_type = policy_type
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.policy_type is not None:
            result['PolicyType'] = self.policy_type
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PolicyType') is not None:
            self.policy_type = m.get('PolicyType')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DeleteMonitorGroupNotifyPolicyResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: str = None,
        result: int = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.result is not None:
            result['Result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        return self


class DeleteMonitorGroupNotifyPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMonitorGroupNotifyPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMonitorGroupNotifyPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMonitoringAgentProcessRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        process_name: str = None,
        process_id: str = None,
    ):
        self.instance_id = instance_id
        self.process_name = process_name
        self.process_id = process_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.process_id is not None:
            result['ProcessId'] = self.process_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('ProcessId') is not None:
            self.process_id = m.get('ProcessId')
        return self


class DeleteMonitoringAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMonitoringAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteMonitoringAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteMonitoringAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteSiteMonitorsRequest(TeaModel):
    def __init__(
        self,
        task_ids: str = None,
        is_delete_alarms: bool = None,
    ):
        self.task_ids = task_ids
        self.is_delete_alarms = is_delete_alarms

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_ids is not None:
            result['TaskIds'] = self.task_ids
        if self.is_delete_alarms is not None:
            result['IsDeleteAlarms'] = self.is_delete_alarms
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskIds') is not None:
            self.task_ids = m.get('TaskIds')
        if m.get('IsDeleteAlarms') is not None:
            self.is_delete_alarms = m.get('IsDeleteAlarms')
        return self


class DeleteSiteMonitorsResponseBodyData(TeaModel):
    def __init__(
        self,
        count: int = None,
    ):
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        return self


class DeleteSiteMonitorsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: DeleteSiteMonitorsResponseBodyData = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DeleteSiteMonitorsResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteSiteMonitorsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteSiteMonitorsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteSiteMonitorsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeActiveMetricRuleListRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
    ):
        self.product = product

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        return self


class DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsCritical(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        times: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsInfo(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        times: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsWarn(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        times: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalations(TeaModel):
    def __init__(
        self,
        critical: DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsCritical = None,
        info: DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsInfo = None,
        warn: DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsWarn = None,
    ):
        self.critical = critical
        self.info = info
        self.warn = warn

    def validate(self):
        if self.critical:
            self.critical.validate()
        if self.info:
            self.info.validate()
        if self.warn:
            self.warn.validate()

    def to_map(self):
        result = dict()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Critical') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        if m.get('Info') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        return self


class DescribeActiveMetricRuleListResponseBodyAlertListAlert(TeaModel):
    def __init__(
        self,
        silence_time: str = None,
        metric_name: str = None,
        webhook: str = None,
        escalations: DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalations = None,
        contact_groups: str = None,
        namespace: str = None,
        mail_subject: str = None,
        no_effective_interval: str = None,
        effective_interval: str = None,
        rule_name: str = None,
        alert_state: str = None,
        period: str = None,
        rule_id: str = None,
        dimensions: str = None,
        enable_state: bool = None,
        resources: str = None,
    ):
        self.silence_time = silence_time
        self.metric_name = metric_name
        self.webhook = webhook
        self.escalations = escalations
        self.contact_groups = contact_groups
        self.namespace = namespace
        self.mail_subject = mail_subject
        self.no_effective_interval = no_effective_interval
        self.effective_interval = effective_interval
        self.rule_name = rule_name
        self.alert_state = alert_state
        self.period = period
        self.rule_id = rule_id
        self.dimensions = dimensions
        self.enable_state = enable_state
        self.resources = resources

    def validate(self):
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.mail_subject is not None:
            result['MailSubject'] = self.mail_subject
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.alert_state is not None:
            result['AlertState'] = self.alert_state
        if self.period is not None:
            result['Period'] = self.period
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.enable_state is not None:
            result['EnableState'] = self.enable_state
        if self.resources is not None:
            result['Resources'] = self.resources
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Escalations') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBodyAlertListAlertEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MailSubject') is not None:
            self.mail_subject = m.get('MailSubject')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('AlertState') is not None:
            self.alert_state = m.get('AlertState')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('EnableState') is not None:
            self.enable_state = m.get('EnableState')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        return self


class DescribeActiveMetricRuleListResponseBodyAlertList(TeaModel):
    def __init__(
        self,
        alert: List[DescribeActiveMetricRuleListResponseBodyAlertListAlert] = None,
    ):
        self.alert = alert

    def validate(self):
        if self.alert:
            for k in self.alert:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Alert'] = []
        if self.alert is not None:
            for k in self.alert:
                result['Alert'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert = []
        if m.get('Alert') is not None:
            for k in m.get('Alert'):
                temp_model = DescribeActiveMetricRuleListResponseBodyAlertListAlert()
                self.alert.append(temp_model.from_map(k))
        return self


class DescribeActiveMetricRuleListResponseBodyDatapointsAlarm(TeaModel):
    def __init__(
        self,
        silence_time: str = None,
        metric_name: str = None,
        evaluation_count: str = None,
        webhook: str = None,
        state: str = None,
        contact_groups: str = None,
        namespace: str = None,
        period: str = None,
        rule_id: str = None,
        rule_name: str = None,
        end_time: str = None,
        comparison_operator: str = None,
        start_time: str = None,
        threshold: str = None,
        statistics: str = None,
        enable: str = None,
    ):
        self.silence_time = silence_time
        self.metric_name = metric_name
        self.evaluation_count = evaluation_count
        self.webhook = webhook
        self.state = state
        self.contact_groups = contact_groups
        self.namespace = namespace
        self.period = period
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.end_time = end_time
        self.comparison_operator = comparison_operator
        self.start_time = start_time
        self.threshold = threshold
        self.statistics = statistics
        self.enable = enable

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.state is not None:
            result['State'] = self.state
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.period is not None:
            result['Period'] = self.period
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class DescribeActiveMetricRuleListResponseBodyDatapoints(TeaModel):
    def __init__(
        self,
        alarm: List[DescribeActiveMetricRuleListResponseBodyDatapointsAlarm] = None,
    ):
        self.alarm = alarm

    def validate(self):
        if self.alarm:
            for k in self.alarm:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Alarm'] = []
        if self.alarm is not None:
            for k in self.alarm:
                result['Alarm'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alarm = []
        if m.get('Alarm') is not None:
            for k in m.get('Alarm'):
                temp_model = DescribeActiveMetricRuleListResponseBodyDatapointsAlarm()
                self.alarm.append(temp_model.from_map(k))
        return self


class DescribeActiveMetricRuleListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        alert_list: DescribeActiveMetricRuleListResponseBodyAlertList = None,
        datapoints: DescribeActiveMetricRuleListResponseBodyDatapoints = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.alert_list = alert_list
        self.datapoints = datapoints
        self.code = code
        self.success = success

    def validate(self):
        if self.alert_list:
            self.alert_list.validate()
        if self.datapoints:
            self.datapoints.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.alert_list is not None:
            result['AlertList'] = self.alert_list.to_map()
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AlertList') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBodyAlertList()
            self.alert_list = temp_model.from_map(m['AlertList'])
        if m.get('Datapoints') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBodyDatapoints()
            self.datapoints = temp_model.from_map(m['Datapoints'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeActiveMetricRuleListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeActiveMetricRuleListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeActiveMetricRuleListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAlertHistoryListRequest(TeaModel):
    def __init__(
        self,
        rule_id: str = None,
        rule_name: str = None,
        namespace: str = None,
        metric_name: str = None,
        group_id: str = None,
        status: str = None,
        state: str = None,
        ascending: bool = None,
        start_time: str = None,
        end_time: str = None,
        page_size: int = None,
        page: int = None,
    ):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.namespace = namespace
        self.metric_name = metric_name
        self.group_id = group_id
        self.status = status
        self.state = state
        self.ascending = ascending
        self.start_time = start_time
        self.end_time = end_time
        self.page_size = page_size
        self.page = page

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.state is not None:
            result['State'] = self.state
        if self.ascending is not None:
            result['Ascending'] = self.ascending
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page is not None:
            result['Page'] = self.page
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Ascending') is not None:
            self.ascending = m.get('Ascending')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Page') is not None:
            self.page = m.get('Page')
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContacts(TeaModel):
    def __init__(
        self,
        contact: List[str] = None,
    ):
        self.contact = contact

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact is not None:
            result['Contact'] = self.contact
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Contact') is not None:
            self.contact = m.get('Contact')
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactGroups(TeaModel):
    def __init__(
        self,
        contact_group: List[str] = None,
    ):
        self.contact_group = contact_group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group is not None:
            result['ContactGroup'] = self.contact_group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroup') is not None:
            self.contact_group = m.get('ContactGroup')
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactSmses(TeaModel):
    def __init__(
        self,
        contact_sms: List[str] = None,
    ):
        self.contact_sms = contact_sms

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_sms is not None:
            result['ContactSms'] = self.contact_sms
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactSms') is not None:
            self.contact_sms = m.get('ContactSms')
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactALIIMs(TeaModel):
    def __init__(
        self,
        contact_aliim: List[str] = None,
    ):
        self.contact_aliim = contact_aliim

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_aliim is not None:
            result['ContactALIIM'] = self.contact_aliim
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactALIIM') is not None:
            self.contact_aliim = m.get('ContactALIIM')
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactMails(TeaModel):
    def __init__(
        self,
        contact_mail: List[str] = None,
    ):
        self.contact_mail = contact_mail

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_mail is not None:
            result['ContactMail'] = self.contact_mail
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactMail') is not None:
            self.contact_mail = m.get('ContactMail')
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistory(TeaModel):
    def __init__(
        self,
        status: int = None,
        metric_name: str = None,
        contacts: DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContacts = None,
        evaluation_count: int = None,
        state: str = None,
        contact_groups: DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactGroups = None,
        namespace: str = None,
        webhooks: str = None,
        rule_id: str = None,
        rule_name: str = None,
        last_time: int = None,
        value: str = None,
        expression: str = None,
        group_id: str = None,
        alert_time: int = None,
        instance_name: str = None,
        contact_smses: DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactSmses = None,
        dimensions: str = None,
        contact_aliims: DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactALIIMs = None,
        level: str = None,
        contact_mails: DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactMails = None,
    ):
        self.status = status
        self.metric_name = metric_name
        self.contacts = contacts
        self.evaluation_count = evaluation_count
        self.state = state
        self.contact_groups = contact_groups
        self.namespace = namespace
        self.webhooks = webhooks
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.last_time = last_time
        self.value = value
        self.expression = expression
        self.group_id = group_id
        self.alert_time = alert_time
        self.instance_name = instance_name
        self.contact_smses = contact_smses
        self.dimensions = dimensions
        self.contact_aliims = contact_aliims
        self.level = level
        self.contact_mails = contact_mails

    def validate(self):
        if self.contacts:
            self.contacts.validate()
        if self.contact_groups:
            self.contact_groups.validate()
        if self.contact_smses:
            self.contact_smses.validate()
        if self.contact_aliims:
            self.contact_aliims.validate()
        if self.contact_mails:
            self.contact_mails.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.contacts is not None:
            result['Contacts'] = self.contacts.to_map()
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.state is not None:
            result['State'] = self.state
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups.to_map()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.webhooks is not None:
            result['Webhooks'] = self.webhooks
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.last_time is not None:
            result['LastTime'] = self.last_time
        if self.value is not None:
            result['Value'] = self.value
        if self.expression is not None:
            result['Expression'] = self.expression
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.alert_time is not None:
            result['AlertTime'] = self.alert_time
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.contact_smses is not None:
            result['ContactSmses'] = self.contact_smses.to_map()
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.contact_aliims is not None:
            result['ContactALIIMs'] = self.contact_aliims.to_map()
        if self.level is not None:
            result['Level'] = self.level
        if self.contact_mails is not None:
            result['ContactMails'] = self.contact_mails.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Contacts') is not None:
            temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContacts()
            self.contacts = temp_model.from_map(m['Contacts'])
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('ContactGroups') is not None:
            temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactGroups()
            self.contact_groups = temp_model.from_map(m['ContactGroups'])
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Webhooks') is not None:
            self.webhooks = m.get('Webhooks')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('LastTime') is not None:
            self.last_time = m.get('LastTime')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Expression') is not None:
            self.expression = m.get('Expression')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('AlertTime') is not None:
            self.alert_time = m.get('AlertTime')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('ContactSmses') is not None:
            temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactSmses()
            self.contact_smses = temp_model.from_map(m['ContactSmses'])
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('ContactALIIMs') is not None:
            temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactALIIMs()
            self.contact_aliims = temp_model.from_map(m['ContactALIIMs'])
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('ContactMails') is not None:
            temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistoryContactMails()
            self.contact_mails = temp_model.from_map(m['ContactMails'])
        return self


class DescribeAlertHistoryListResponseBodyAlarmHistoryList(TeaModel):
    def __init__(
        self,
        alarm_history: List[DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistory] = None,
    ):
        self.alarm_history = alarm_history

    def validate(self):
        if self.alarm_history:
            for k in self.alarm_history:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlarmHistory'] = []
        if self.alarm_history is not None:
            for k in self.alarm_history:
                result['AlarmHistory'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alarm_history = []
        if m.get('AlarmHistory') is not None:
            for k in m.get('AlarmHistory'):
                temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryListAlarmHistory()
                self.alarm_history.append(temp_model.from_map(k))
        return self


class DescribeAlertHistoryListResponseBody(TeaModel):
    def __init__(
        self,
        alarm_history_list: DescribeAlertHistoryListResponseBodyAlarmHistoryList = None,
        message: str = None,
        request_id: str = None,
        total: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.alarm_history_list = alarm_history_list
        self.message = message
        self.request_id = request_id
        self.total = total
        self.code = code
        self.success = success

    def validate(self):
        if self.alarm_history_list:
            self.alarm_history_list.validate()

    def to_map(self):
        result = dict()
        if self.alarm_history_list is not None:
            result['AlarmHistoryList'] = self.alarm_history_list.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AlarmHistoryList') is not None:
            temp_model = DescribeAlertHistoryListResponseBodyAlarmHistoryList()
            self.alarm_history_list = temp_model.from_map(m['AlarmHistoryList'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeAlertHistoryListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAlertHistoryListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeAlertHistoryListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAlertLogCountRequest(TeaModel):
    def __init__(
        self,
        start_time: int = None,
        end_time: int = None,
        page_number: int = None,
        page_size: int = None,
        search_key: str = None,
        namespace: str = None,
        group_id: str = None,
        product: str = None,
        level: str = None,
        send_status: str = None,
        contact_group: str = None,
        rule_name: str = None,
        metric_name: str = None,
        last_min: str = None,
        group_by: str = None,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        self.search_key = search_key
        self.namespace = namespace
        self.group_id = group_id
        self.product = product
        self.level = level
        self.send_status = send_status
        self.contact_group = contact_group
        self.rule_name = rule_name
        self.metric_name = metric_name
        self.last_min = last_min
        self.group_by = group_by

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search_key is not None:
            result['SearchKey'] = self.search_key
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.product is not None:
            result['Product'] = self.product
        if self.level is not None:
            result['Level'] = self.level
        if self.send_status is not None:
            result['SendStatus'] = self.send_status
        if self.contact_group is not None:
            result['ContactGroup'] = self.contact_group
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.last_min is not None:
            result['LastMin'] = self.last_min
        if self.group_by is not None:
            result['GroupBy'] = self.group_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SearchKey') is not None:
            self.search_key = m.get('SearchKey')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('SendStatus') is not None:
            self.send_status = m.get('SendStatus')
        if m.get('ContactGroup') is not None:
            self.contact_group = m.get('ContactGroup')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('LastMin') is not None:
            self.last_min = m.get('LastMin')
        if m.get('GroupBy') is not None:
            self.group_by = m.get('GroupBy')
        return self


class DescribeAlertLogCountResponseBodyAlertLogCountLogs(TeaModel):
    def __init__(
        self,
        value: str = None,
        name: str = None,
    ):
        self.value = value
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeAlertLogCountResponseBodyAlertLogCount(TeaModel):
    def __init__(
        self,
        logs: List[DescribeAlertLogCountResponseBodyAlertLogCountLogs] = None,
        count: int = None,
    ):
        self.logs = logs
        self.count = count

    def validate(self):
        if self.logs:
            for k in self.logs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Logs'] = []
        if self.logs is not None:
            for k in self.logs:
                result['Logs'].append(k.to_map() if k else None)
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.logs = []
        if m.get('Logs') is not None:
            for k in m.get('Logs'):
                temp_model = DescribeAlertLogCountResponseBodyAlertLogCountLogs()
                self.logs.append(temp_model.from_map(k))
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeAlertLogCountResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        alert_log_count: List[DescribeAlertLogCountResponseBodyAlertLogCount] = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.alert_log_count = alert_log_count
        self.code = code
        self.success = success

    def validate(self):
        if self.alert_log_count:
            for k in self.alert_log_count:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['AlertLogCount'] = []
        if self.alert_log_count is not None:
            for k in self.alert_log_count:
                result['AlertLogCount'].append(k.to_map() if k else None)
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.alert_log_count = []
        if m.get('AlertLogCount') is not None:
            for k in m.get('AlertLogCount'):
                temp_model = DescribeAlertLogCountResponseBodyAlertLogCount()
                self.alert_log_count.append(temp_model.from_map(k))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeAlertLogCountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAlertLogCountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeAlertLogCountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAlertLogHistogramRequest(TeaModel):
    def __init__(
        self,
        start_time: int = None,
        end_time: int = None,
        page_number: int = None,
        page_size: int = None,
        search_key: str = None,
        group_id: str = None,
        product: str = None,
        namespace: str = None,
        level: str = None,
        send_status: str = None,
        contact_group: str = None,
        rule_name: str = None,
        metric_name: str = None,
        last_min: str = None,
        group_by: str = None,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        self.search_key = search_key
        self.group_id = group_id
        self.product = product
        self.namespace = namespace
        self.level = level
        self.send_status = send_status
        self.contact_group = contact_group
        self.rule_name = rule_name
        self.metric_name = metric_name
        self.last_min = last_min
        self.group_by = group_by

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search_key is not None:
            result['SearchKey'] = self.search_key
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.product is not None:
            result['Product'] = self.product
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.level is not None:
            result['Level'] = self.level
        if self.send_status is not None:
            result['SendStatus'] = self.send_status
        if self.contact_group is not None:
            result['ContactGroup'] = self.contact_group
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.last_min is not None:
            result['LastMin'] = self.last_min
        if self.group_by is not None:
            result['GroupBy'] = self.group_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SearchKey') is not None:
            self.search_key = m.get('SearchKey')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('SendStatus') is not None:
            self.send_status = m.get('SendStatus')
        if m.get('ContactGroup') is not None:
            self.contact_group = m.get('ContactGroup')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('LastMin') is not None:
            self.last_min = m.get('LastMin')
        if m.get('GroupBy') is not None:
            self.group_by = m.get('GroupBy')
        return self


class DescribeAlertLogHistogramResponseBodyAlertLogHistogramList(TeaModel):
    def __init__(
        self,
        from_: int = None,
        to: int = None,
        count: int = None,
    ):
        self.from_ = from_
        self.to = to
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_ is not None:
            result['From'] = self.from_
        if self.to is not None:
            result['To'] = self.to
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('From') is not None:
            self.from_ = m.get('From')
        if m.get('To') is not None:
            self.to = m.get('To')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeAlertLogHistogramResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        alert_log_histogram_list: List[DescribeAlertLogHistogramResponseBodyAlertLogHistogramList] = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.alert_log_histogram_list = alert_log_histogram_list
        self.code = code
        self.success = success

    def validate(self):
        if self.alert_log_histogram_list:
            for k in self.alert_log_histogram_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['AlertLogHistogramList'] = []
        if self.alert_log_histogram_list is not None:
            for k in self.alert_log_histogram_list:
                result['AlertLogHistogramList'].append(k.to_map() if k else None)
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.alert_log_histogram_list = []
        if m.get('AlertLogHistogramList') is not None:
            for k in m.get('AlertLogHistogramList'):
                temp_model = DescribeAlertLogHistogramResponseBodyAlertLogHistogramList()
                self.alert_log_histogram_list.append(temp_model.from_map(k))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeAlertLogHistogramResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAlertLogHistogramResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeAlertLogHistogramResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAlertLogListRequest(TeaModel):
    def __init__(
        self,
        start_time: int = None,
        end_time: int = None,
        page_number: int = None,
        page_size: int = None,
        search_key: str = None,
        group_id: str = None,
        namespace: str = None,
        product: str = None,
        level: str = None,
        send_status: str = None,
        contact_group: str = None,
        rule_name: str = None,
        metric_name: str = None,
        last_min: str = None,
        group_by: str = None,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        self.search_key = search_key
        self.group_id = group_id
        self.namespace = namespace
        self.product = product
        self.level = level
        self.send_status = send_status
        self.contact_group = contact_group
        self.rule_name = rule_name
        self.metric_name = metric_name
        self.last_min = last_min
        self.group_by = group_by

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search_key is not None:
            result['SearchKey'] = self.search_key
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.product is not None:
            result['Product'] = self.product
        if self.level is not None:
            result['Level'] = self.level
        if self.send_status is not None:
            result['SendStatus'] = self.send_status
        if self.contact_group is not None:
            result['ContactGroup'] = self.contact_group
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.last_min is not None:
            result['LastMin'] = self.last_min
        if self.group_by is not None:
            result['GroupBy'] = self.group_by
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SearchKey') is not None:
            self.search_key = m.get('SearchKey')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('SendStatus') is not None:
            self.send_status = m.get('SendStatus')
        if m.get('ContactGroup') is not None:
            self.contact_group = m.get('ContactGroup')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('LastMin') is not None:
            self.last_min = m.get('LastMin')
        if m.get('GroupBy') is not None:
            self.group_by = m.get('GroupBy')
        return self


class DescribeAlertLogListResponseBodyAlertLogListExtendedInfo(TeaModel):
    def __init__(
        self,
        value: str = None,
        name: str = None,
    ):
        self.value = value
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeAlertLogListResponseBodyAlertLogListDimensions(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeAlertLogListResponseBodyAlertLogListEscalation(TeaModel):
    def __init__(
        self,
        expression: str = None,
        times: int = None,
        level: str = None,
    ):
        self.expression = expression
        self.times = times
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.expression is not None:
            result['Expression'] = self.expression
        if self.times is not None:
            result['Times'] = self.times
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Expression') is not None:
            self.expression = m.get('Expression')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class DescribeAlertLogListResponseBodyAlertLogList(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        event_name: str = None,
        contact_aliiwwlist: List[str] = None,
        message: str = None,
        level_change: str = None,
        rule_id: str = None,
        extended_info: List[DescribeAlertLogListResponseBodyAlertLogListExtendedInfo] = None,
        dingding_webhook_list: List[str] = None,
        instance_name: str = None,
        contact_mail_list: List[str] = None,
        dimensions: List[DescribeAlertLogListResponseBodyAlertLogListDimensions] = None,
        contact_smslist: List[str] = None,
        send_status: str = None,
        contact_on_call_list: List[str] = None,
        product: str = None,
        contact_groups: List[str] = None,
        namespace: str = None,
        escalation: DescribeAlertLogListResponseBodyAlertLogListEscalation = None,
        instance_id: str = None,
        contact_ding_list: List[str] = None,
        rule_name: str = None,
        webhook_list: List[str] = None,
        group_id: str = None,
        group_name: str = None,
        alert_time: str = None,
        level: str = None,
    ):
        self.metric_name = metric_name
        self.event_name = event_name
        self.contact_aliiwwlist = contact_aliiwwlist
        self.message = message
        self.level_change = level_change
        self.rule_id = rule_id
        self.extended_info = extended_info
        self.dingding_webhook_list = dingding_webhook_list
        self.instance_name = instance_name
        self.contact_mail_list = contact_mail_list
        self.dimensions = dimensions
        self.contact_smslist = contact_smslist
        self.send_status = send_status
        self.contact_on_call_list = contact_on_call_list
        self.product = product
        self.contact_groups = contact_groups
        self.namespace = namespace
        self.escalation = escalation
        self.instance_id = instance_id
        self.contact_ding_list = contact_ding_list
        self.rule_name = rule_name
        self.webhook_list = webhook_list
        self.group_id = group_id
        self.group_name = group_name
        self.alert_time = alert_time
        self.level = level

    def validate(self):
        if self.extended_info:
            for k in self.extended_info:
                if k:
                    k.validate()
        if self.dimensions:
            for k in self.dimensions:
                if k:
                    k.validate()
        if self.escalation:
            self.escalation.validate()

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.event_name is not None:
            result['EventName'] = self.event_name
        if self.contact_aliiwwlist is not None:
            result['ContactALIIWWList'] = self.contact_aliiwwlist
        if self.message is not None:
            result['Message'] = self.message
        if self.level_change is not None:
            result['LevelChange'] = self.level_change
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        result['ExtendedInfo'] = []
        if self.extended_info is not None:
            for k in self.extended_info:
                result['ExtendedInfo'].append(k.to_map() if k else None)
        if self.dingding_webhook_list is not None:
            result['DingdingWebhookList'] = self.dingding_webhook_list
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.contact_mail_list is not None:
            result['ContactMailList'] = self.contact_mail_list
        result['Dimensions'] = []
        if self.dimensions is not None:
            for k in self.dimensions:
                result['Dimensions'].append(k.to_map() if k else None)
        if self.contact_smslist is not None:
            result['ContactSMSList'] = self.contact_smslist
        if self.send_status is not None:
            result['SendStatus'] = self.send_status
        if self.contact_on_call_list is not None:
            result['ContactOnCallList'] = self.contact_on_call_list
        if self.product is not None:
            result['Product'] = self.product
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.escalation is not None:
            result['Escalation'] = self.escalation.to_map()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.contact_ding_list is not None:
            result['ContactDingList'] = self.contact_ding_list
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.webhook_list is not None:
            result['WebhookList'] = self.webhook_list
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.alert_time is not None:
            result['AlertTime'] = self.alert_time
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('EventName') is not None:
            self.event_name = m.get('EventName')
        if m.get('ContactALIIWWList') is not None:
            self.contact_aliiwwlist = m.get('ContactALIIWWList')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('LevelChange') is not None:
            self.level_change = m.get('LevelChange')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        self.extended_info = []
        if m.get('ExtendedInfo') is not None:
            for k in m.get('ExtendedInfo'):
                temp_model = DescribeAlertLogListResponseBodyAlertLogListExtendedInfo()
                self.extended_info.append(temp_model.from_map(k))
        if m.get('DingdingWebhookList') is not None:
            self.dingding_webhook_list = m.get('DingdingWebhookList')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('ContactMailList') is not None:
            self.contact_mail_list = m.get('ContactMailList')
        self.dimensions = []
        if m.get('Dimensions') is not None:
            for k in m.get('Dimensions'):
                temp_model = DescribeAlertLogListResponseBodyAlertLogListDimensions()
                self.dimensions.append(temp_model.from_map(k))
        if m.get('ContactSMSList') is not None:
            self.contact_smslist = m.get('ContactSMSList')
        if m.get('SendStatus') is not None:
            self.send_status = m.get('SendStatus')
        if m.get('ContactOnCallList') is not None:
            self.contact_on_call_list = m.get('ContactOnCallList')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Escalation') is not None:
            temp_model = DescribeAlertLogListResponseBodyAlertLogListEscalation()
            self.escalation = temp_model.from_map(m['Escalation'])
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ContactDingList') is not None:
            self.contact_ding_list = m.get('ContactDingList')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('WebhookList') is not None:
            self.webhook_list = m.get('WebhookList')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('AlertTime') is not None:
            self.alert_time = m.get('AlertTime')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class DescribeAlertLogListResponseBody(TeaModel):
    def __init__(
        self,
        alert_log_list: List[DescribeAlertLogListResponseBodyAlertLogList] = None,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        total: int = None,
        code: str = None,
        success: bool = None,
    ):
        self.alert_log_list = alert_log_list
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.code = code
        self.success = success

    def validate(self):
        if self.alert_log_list:
            for k in self.alert_log_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertLogList'] = []
        if self.alert_log_list is not None:
            for k in self.alert_log_list:
                result['AlertLogList'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_log_list = []
        if m.get('AlertLogList') is not None:
            for k in m.get('AlertLogList'):
                temp_model = DescribeAlertLogListResponseBodyAlertLogList()
                self.alert_log_list.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeAlertLogListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAlertLogListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeAlertLogListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeContactGroupListRequest(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        page_number: int = None,
    ):
        self.page_size = page_size
        self.page_number = page_number

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeContactGroupListResponseBodyContactGroupListContactGroupContacts(TeaModel):
    def __init__(
        self,
        contact: List[str] = None,
    ):
        self.contact = contact

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact is not None:
            result['Contact'] = self.contact
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Contact') is not None:
            self.contact = m.get('Contact')
        return self


class DescribeContactGroupListResponseBodyContactGroupListContactGroup(TeaModel):
    def __init__(
        self,
        describe: str = None,
        update_time: int = None,
        contacts: DescribeContactGroupListResponseBodyContactGroupListContactGroupContacts = None,
        create_time: int = None,
        enabled_weekly_report: bool = None,
        name: str = None,
        enable_subscribed: bool = None,
    ):
        self.describe = describe
        self.update_time = update_time
        self.contacts = contacts
        self.create_time = create_time
        self.enabled_weekly_report = enabled_weekly_report
        self.name = name
        self.enable_subscribed = enable_subscribed

    def validate(self):
        if self.contacts:
            self.contacts.validate()

    def to_map(self):
        result = dict()
        if self.describe is not None:
            result['Describe'] = self.describe
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.contacts is not None:
            result['Contacts'] = self.contacts.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.enabled_weekly_report is not None:
            result['EnabledWeeklyReport'] = self.enabled_weekly_report
        if self.name is not None:
            result['Name'] = self.name
        if self.enable_subscribed is not None:
            result['EnableSubscribed'] = self.enable_subscribed
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Describe') is not None:
            self.describe = m.get('Describe')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('Contacts') is not None:
            temp_model = DescribeContactGroupListResponseBodyContactGroupListContactGroupContacts()
            self.contacts = temp_model.from_map(m['Contacts'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('EnabledWeeklyReport') is not None:
            self.enabled_weekly_report = m.get('EnabledWeeklyReport')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EnableSubscribed') is not None:
            self.enable_subscribed = m.get('EnableSubscribed')
        return self


class DescribeContactGroupListResponseBodyContactGroupList(TeaModel):
    def __init__(
        self,
        contact_group: List[DescribeContactGroupListResponseBodyContactGroupListContactGroup] = None,
    ):
        self.contact_group = contact_group

    def validate(self):
        if self.contact_group:
            for k in self.contact_group:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContactGroup'] = []
        if self.contact_group is not None:
            for k in self.contact_group:
                result['ContactGroup'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact_group = []
        if m.get('ContactGroup') is not None:
            for k in m.get('ContactGroup'):
                temp_model = DescribeContactGroupListResponseBodyContactGroupListContactGroup()
                self.contact_group.append(temp_model.from_map(k))
        return self


class DescribeContactGroupListResponseBodyContactGroups(TeaModel):
    def __init__(
        self,
        contact_group: List[str] = None,
    ):
        self.contact_group = contact_group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group is not None:
            result['ContactGroup'] = self.contact_group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroup') is not None:
            self.contact_group = m.get('ContactGroup')
        return self


class DescribeContactGroupListResponseBody(TeaModel):
    def __init__(
        self,
        contact_group_list: DescribeContactGroupListResponseBodyContactGroupList = None,
        contact_groups: DescribeContactGroupListResponseBodyContactGroups = None,
        message: str = None,
        request_id: str = None,
        total: int = None,
        code: str = None,
        success: bool = None,
    ):
        self.contact_group_list = contact_group_list
        self.contact_groups = contact_groups
        self.message = message
        self.request_id = request_id
        self.total = total
        self.code = code
        self.success = success

    def validate(self):
        if self.contact_group_list:
            self.contact_group_list.validate()
        if self.contact_groups:
            self.contact_groups.validate()

    def to_map(self):
        result = dict()
        if self.contact_group_list is not None:
            result['ContactGroupList'] = self.contact_group_list.to_map()
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupList') is not None:
            temp_model = DescribeContactGroupListResponseBodyContactGroupList()
            self.contact_group_list = temp_model.from_map(m['ContactGroupList'])
        if m.get('ContactGroups') is not None:
            temp_model = DescribeContactGroupListResponseBodyContactGroups()
            self.contact_groups = temp_model.from_map(m['ContactGroups'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeContactGroupListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeContactGroupListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeContactGroupListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeContactListRequest(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        page_number: int = None,
        contact_name: str = None,
        chanel_type: str = None,
        chanel_value: str = None,
    ):
        self.page_size = page_size
        self.page_number = page_number
        self.contact_name = contact_name
        self.chanel_type = chanel_type
        self.chanel_value = chanel_value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.contact_name is not None:
            result['ContactName'] = self.contact_name
        if self.chanel_type is not None:
            result['ChanelType'] = self.chanel_type
        if self.chanel_value is not None:
            result['ChanelValue'] = self.chanel_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('ContactName') is not None:
            self.contact_name = m.get('ContactName')
        if m.get('ChanelType') is not None:
            self.chanel_type = m.get('ChanelType')
        if m.get('ChanelValue') is not None:
            self.chanel_value = m.get('ChanelValue')
        return self


class DescribeContactListResponseBodyContactsContactChannelsState(TeaModel):
    def __init__(
        self,
        ding_web_hook: str = None,
        sms: str = None,
        mail: str = None,
        ali_im: str = None,
    ):
        self.ding_web_hook = ding_web_hook
        self.sms = sms
        self.mail = mail
        self.ali_im = ali_im

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ding_web_hook is not None:
            result['DingWebHook'] = self.ding_web_hook
        if self.sms is not None:
            result['SMS'] = self.sms
        if self.mail is not None:
            result['Mail'] = self.mail
        if self.ali_im is not None:
            result['AliIM'] = self.ali_im
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DingWebHook') is not None:
            self.ding_web_hook = m.get('DingWebHook')
        if m.get('SMS') is not None:
            self.sms = m.get('SMS')
        if m.get('Mail') is not None:
            self.mail = m.get('Mail')
        if m.get('AliIM') is not None:
            self.ali_im = m.get('AliIM')
        return self


class DescribeContactListResponseBodyContactsContactContactGroups(TeaModel):
    def __init__(
        self,
        contact_group: List[str] = None,
    ):
        self.contact_group = contact_group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group is not None:
            result['ContactGroup'] = self.contact_group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroup') is not None:
            self.contact_group = m.get('ContactGroup')
        return self


class DescribeContactListResponseBodyContactsContactChannels(TeaModel):
    def __init__(
        self,
        ding_web_hook: str = None,
        sms: str = None,
        mail: str = None,
        ali_im: str = None,
    ):
        self.ding_web_hook = ding_web_hook
        self.sms = sms
        self.mail = mail
        self.ali_im = ali_im

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ding_web_hook is not None:
            result['DingWebHook'] = self.ding_web_hook
        if self.sms is not None:
            result['SMS'] = self.sms
        if self.mail is not None:
            result['Mail'] = self.mail
        if self.ali_im is not None:
            result['AliIM'] = self.ali_im
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DingWebHook') is not None:
            self.ding_web_hook = m.get('DingWebHook')
        if m.get('SMS') is not None:
            self.sms = m.get('SMS')
        if m.get('Mail') is not None:
            self.mail = m.get('Mail')
        if m.get('AliIM') is not None:
            self.ali_im = m.get('AliIM')
        return self


class DescribeContactListResponseBodyContactsContact(TeaModel):
    def __init__(
        self,
        update_time: int = None,
        channels_state: DescribeContactListResponseBodyContactsContactChannelsState = None,
        create_time: int = None,
        lang: str = None,
        contact_groups: DescribeContactListResponseBodyContactsContactContactGroups = None,
        channels: DescribeContactListResponseBodyContactsContactChannels = None,
        name: str = None,
        desc: str = None,
    ):
        self.update_time = update_time
        self.channels_state = channels_state
        self.create_time = create_time
        self.lang = lang
        self.contact_groups = contact_groups
        self.channels = channels
        self.name = name
        self.desc = desc

    def validate(self):
        if self.channels_state:
            self.channels_state.validate()
        if self.contact_groups:
            self.contact_groups.validate()
        if self.channels:
            self.channels.validate()

    def to_map(self):
        result = dict()
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.channels_state is not None:
            result['ChannelsState'] = self.channels_state.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups.to_map()
        if self.channels is not None:
            result['Channels'] = self.channels.to_map()
        if self.name is not None:
            result['Name'] = self.name
        if self.desc is not None:
            result['Desc'] = self.desc
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('ChannelsState') is not None:
            temp_model = DescribeContactListResponseBodyContactsContactChannelsState()
            self.channels_state = temp_model.from_map(m['ChannelsState'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ContactGroups') is not None:
            temp_model = DescribeContactListResponseBodyContactsContactContactGroups()
            self.contact_groups = temp_model.from_map(m['ContactGroups'])
        if m.get('Channels') is not None:
            temp_model = DescribeContactListResponseBodyContactsContactChannels()
            self.channels = temp_model.from_map(m['Channels'])
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Desc') is not None:
            self.desc = m.get('Desc')
        return self


class DescribeContactListResponseBodyContacts(TeaModel):
    def __init__(
        self,
        contact: List[DescribeContactListResponseBodyContactsContact] = None,
    ):
        self.contact = contact

    def validate(self):
        if self.contact:
            for k in self.contact:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Contact'] = []
        if self.contact is not None:
            for k in self.contact:
                result['Contact'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact = []
        if m.get('Contact') is not None:
            for k in m.get('Contact'):
                temp_model = DescribeContactListResponseBodyContactsContact()
                self.contact.append(temp_model.from_map(k))
        return self


class DescribeContactListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        contacts: DescribeContactListResponseBodyContacts = None,
        total: int = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.contacts = contacts
        self.total = total
        self.code = code
        self.success = success

    def validate(self):
        if self.contacts:
            self.contacts.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.contacts is not None:
            result['Contacts'] = self.contacts.to_map()
        if self.total is not None:
            result['Total'] = self.total
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Contacts') is not None:
            temp_model = DescribeContactListResponseBodyContacts()
            self.contacts = temp_model.from_map(m['Contacts'])
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeContactListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeContactListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeContactListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeContactListByContactGroupRequest(TeaModel):
    def __init__(
        self,
        contact_group_name: str = None,
    ):
        self.contact_group_name = contact_group_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group_name is not None:
            result['ContactGroupName'] = self.contact_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupName') is not None:
            self.contact_group_name = m.get('ContactGroupName')
        return self


class DescribeContactListByContactGroupResponseBodyContactsContactChannels(TeaModel):
    def __init__(
        self,
        ding_web_hook: str = None,
        sms: str = None,
        mail: str = None,
        ali_im: str = None,
    ):
        self.ding_web_hook = ding_web_hook
        self.sms = sms
        self.mail = mail
        self.ali_im = ali_im

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ding_web_hook is not None:
            result['DingWebHook'] = self.ding_web_hook
        if self.sms is not None:
            result['SMS'] = self.sms
        if self.mail is not None:
            result['Mail'] = self.mail
        if self.ali_im is not None:
            result['AliIM'] = self.ali_im
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DingWebHook') is not None:
            self.ding_web_hook = m.get('DingWebHook')
        if m.get('SMS') is not None:
            self.sms = m.get('SMS')
        if m.get('Mail') is not None:
            self.mail = m.get('Mail')
        if m.get('AliIM') is not None:
            self.ali_im = m.get('AliIM')
        return self


class DescribeContactListByContactGroupResponseBodyContactsContact(TeaModel):
    def __init__(
        self,
        update_time: int = None,
        create_time: int = None,
        channels: DescribeContactListByContactGroupResponseBodyContactsContactChannels = None,
        name: str = None,
        desc: str = None,
    ):
        self.update_time = update_time
        self.create_time = create_time
        self.channels = channels
        self.name = name
        self.desc = desc

    def validate(self):
        if self.channels:
            self.channels.validate()

    def to_map(self):
        result = dict()
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.channels is not None:
            result['Channels'] = self.channels.to_map()
        if self.name is not None:
            result['Name'] = self.name
        if self.desc is not None:
            result['Desc'] = self.desc
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Channels') is not None:
            temp_model = DescribeContactListByContactGroupResponseBodyContactsContactChannels()
            self.channels = temp_model.from_map(m['Channels'])
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Desc') is not None:
            self.desc = m.get('Desc')
        return self


class DescribeContactListByContactGroupResponseBodyContacts(TeaModel):
    def __init__(
        self,
        contact: List[DescribeContactListByContactGroupResponseBodyContactsContact] = None,
    ):
        self.contact = contact

    def validate(self):
        if self.contact:
            for k in self.contact:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Contact'] = []
        if self.contact is not None:
            for k in self.contact:
                result['Contact'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact = []
        if m.get('Contact') is not None:
            for k in m.get('Contact'):
                temp_model = DescribeContactListByContactGroupResponseBodyContactsContact()
                self.contact.append(temp_model.from_map(k))
        return self


class DescribeContactListByContactGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        contacts: DescribeContactListByContactGroupResponseBodyContacts = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.contacts = contacts
        self.code = code
        self.success = success

    def validate(self):
        if self.contacts:
            self.contacts.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.contacts is not None:
            result['Contacts'] = self.contacts.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Contacts') is not None:
            temp_model = DescribeContactListByContactGroupResponseBodyContacts()
            self.contacts = temp_model.from_map(m['Contacts'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeContactListByContactGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeContactListByContactGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeContactListByContactGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCustomEventAttributeRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        event_id: str = None,
        group_id: str = None,
        search_keywords: str = None,
        start_time: str = None,
        end_time: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.name = name
        self.event_id = event_id
        self.group_id = group_id
        self.search_keywords = search_keywords
        self.start_time = start_time
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.event_id is not None:
            result['EventId'] = self.event_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.search_keywords is not None:
            result['SearchKeywords'] = self.search_keywords
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EventId') is not None:
            self.event_id = m.get('EventId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('SearchKeywords') is not None:
            self.search_keywords = m.get('SearchKeywords')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeCustomEventAttributeResponseBodyCustomEventsCustomEvent(TeaModel):
    def __init__(
        self,
        time: str = None,
        group_id: str = None,
        name: str = None,
        content: str = None,
        id: str = None,
    ):
        self.time = time
        self.group_id = group_id
        self.name = name
        self.content = content
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.time is not None:
            result['Time'] = self.time
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.name is not None:
            result['Name'] = self.name
        if self.content is not None:
            result['Content'] = self.content
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeCustomEventAttributeResponseBodyCustomEvents(TeaModel):
    def __init__(
        self,
        custom_event: List[DescribeCustomEventAttributeResponseBodyCustomEventsCustomEvent] = None,
    ):
        self.custom_event = custom_event

    def validate(self):
        if self.custom_event:
            for k in self.custom_event:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['CustomEvent'] = []
        if self.custom_event is not None:
            for k in self.custom_event:
                result['CustomEvent'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.custom_event = []
        if m.get('CustomEvent') is not None:
            for k in m.get('CustomEvent'):
                temp_model = DescribeCustomEventAttributeResponseBodyCustomEventsCustomEvent()
                self.custom_event.append(temp_model.from_map(k))
        return self


class DescribeCustomEventAttributeResponseBody(TeaModel):
    def __init__(
        self,
        custom_events: DescribeCustomEventAttributeResponseBodyCustomEvents = None,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: str = None,
    ):
        self.custom_events = custom_events
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        if self.custom_events:
            self.custom_events.validate()

    def to_map(self):
        result = dict()
        if self.custom_events is not None:
            result['CustomEvents'] = self.custom_events.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CustomEvents') is not None:
            temp_model = DescribeCustomEventAttributeResponseBodyCustomEvents()
            self.custom_events = temp_model.from_map(m['CustomEvents'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeCustomEventAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeCustomEventAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeCustomEventAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCustomEventCountRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        event_id: str = None,
        group_id: str = None,
        search_keywords: str = None,
        start_time: str = None,
        end_time: str = None,
    ):
        self.name = name
        self.event_id = event_id
        self.group_id = group_id
        self.search_keywords = search_keywords
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.event_id is not None:
            result['EventId'] = self.event_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.search_keywords is not None:
            result['SearchKeywords'] = self.search_keywords
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EventId') is not None:
            self.event_id = m.get('EventId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('SearchKeywords') is not None:
            self.search_keywords = m.get('SearchKeywords')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        return self


class DescribeCustomEventCountResponseBodyCustomEventCountsCustomEventCount(TeaModel):
    def __init__(
        self,
        time: int = None,
        num: int = None,
        name: str = None,
    ):
        self.time = time
        self.num = num
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.time is not None:
            result['Time'] = self.time
        if self.num is not None:
            result['Num'] = self.num
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeCustomEventCountResponseBodyCustomEventCounts(TeaModel):
    def __init__(
        self,
        custom_event_count: List[DescribeCustomEventCountResponseBodyCustomEventCountsCustomEventCount] = None,
    ):
        self.custom_event_count = custom_event_count

    def validate(self):
        if self.custom_event_count:
            for k in self.custom_event_count:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['CustomEventCount'] = []
        if self.custom_event_count is not None:
            for k in self.custom_event_count:
                result['CustomEventCount'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.custom_event_count = []
        if m.get('CustomEventCount') is not None:
            for k in m.get('CustomEventCount'):
                temp_model = DescribeCustomEventCountResponseBodyCustomEventCountsCustomEventCount()
                self.custom_event_count.append(temp_model.from_map(k))
        return self


class DescribeCustomEventCountResponseBody(TeaModel):
    def __init__(
        self,
        custom_event_counts: DescribeCustomEventCountResponseBodyCustomEventCounts = None,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.custom_event_counts = custom_event_counts
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        if self.custom_event_counts:
            self.custom_event_counts.validate()

    def to_map(self):
        result = dict()
        if self.custom_event_counts is not None:
            result['CustomEventCounts'] = self.custom_event_counts.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CustomEventCounts') is not None:
            temp_model = DescribeCustomEventCountResponseBodyCustomEventCounts()
            self.custom_event_counts = temp_model.from_map(m['CustomEventCounts'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeCustomEventCountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeCustomEventCountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeCustomEventCountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCustomEventHistogramRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        level: str = None,
        event_id: str = None,
        group_id: str = None,
        search_keywords: str = None,
        start_time: str = None,
        end_time: str = None,
    ):
        self.name = name
        self.level = level
        self.event_id = event_id
        self.group_id = group_id
        self.search_keywords = search_keywords
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.level is not None:
            result['Level'] = self.level
        if self.event_id is not None:
            result['EventId'] = self.event_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.search_keywords is not None:
            result['SearchKeywords'] = self.search_keywords
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('EventId') is not None:
            self.event_id = m.get('EventId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('SearchKeywords') is not None:
            self.search_keywords = m.get('SearchKeywords')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        return self


class DescribeCustomEventHistogramResponseBodyEventHistogramsEventHistogram(TeaModel):
    def __init__(
        self,
        end_time: int = None,
        start_time: int = None,
        count: int = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeCustomEventHistogramResponseBodyEventHistograms(TeaModel):
    def __init__(
        self,
        event_histogram: List[DescribeCustomEventHistogramResponseBodyEventHistogramsEventHistogram] = None,
    ):
        self.event_histogram = event_histogram

    def validate(self):
        if self.event_histogram:
            for k in self.event_histogram:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['EventHistogram'] = []
        if self.event_histogram is not None:
            for k in self.event_histogram:
                result['EventHistogram'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.event_histogram = []
        if m.get('EventHistogram') is not None:
            for k in m.get('EventHistogram'):
                temp_model = DescribeCustomEventHistogramResponseBodyEventHistogramsEventHistogram()
                self.event_histogram.append(temp_model.from_map(k))
        return self


class DescribeCustomEventHistogramResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        event_histograms: DescribeCustomEventHistogramResponseBodyEventHistograms = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.event_histograms = event_histograms
        self.success = success

    def validate(self):
        if self.event_histograms:
            self.event_histograms.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.event_histograms is not None:
            result['EventHistograms'] = self.event_histograms.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('EventHistograms') is not None:
            temp_model = DescribeCustomEventHistogramResponseBodyEventHistograms()
            self.event_histograms = temp_model.from_map(m['EventHistograms'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeCustomEventHistogramResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeCustomEventHistogramResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeCustomEventHistogramResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCustomMetricListRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        metric_name: str = None,
        dimension: str = None,
        md_5: str = None,
        page_number: str = None,
        page_size: str = None,
    ):
        self.group_id = group_id
        self.metric_name = metric_name
        self.dimension = dimension
        self.md_5 = md_5
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.dimension is not None:
            result['Dimension'] = self.dimension
        if self.md_5 is not None:
            result['Md5'] = self.md_5
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Dimension') is not None:
            self.dimension = m.get('Dimension')
        if m.get('Md5') is not None:
            self.md_5 = m.get('Md5')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeCustomMetricListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        result: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.result is not None:
            result['Result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        return self


class DescribeCustomMetricListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeCustomMetricListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeCustomMetricListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDynamicTagRuleListRequest(TeaModel):
    def __init__(
        self,
        tag_key: str = None,
        page_number: str = None,
        page_size: str = None,
    ):
        self.tag_key = tag_key
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupMatchExpressMatchExpress(TeaModel):
    def __init__(
        self,
        tag_value_match_function: str = None,
        tag_value: str = None,
    ):
        self.tag_value_match_function = tag_value_match_function
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag_value_match_function is not None:
            result['TagValueMatchFunction'] = self.tag_value_match_function
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagValueMatchFunction') is not None:
            self.tag_value_match_function = m.get('TagValueMatchFunction')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupMatchExpress(TeaModel):
    def __init__(
        self,
        match_express: List[DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupMatchExpressMatchExpress] = None,
    ):
        self.match_express = match_express

    def validate(self):
        if self.match_express:
            for k in self.match_express:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['MatchExpress'] = []
        if self.match_express is not None:
            for k in self.match_express:
                result['MatchExpress'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.match_express = []
        if m.get('MatchExpress') is not None:
            for k in m.get('MatchExpress'):
                temp_model = DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupMatchExpressMatchExpress()
                self.match_express.append(temp_model.from_map(k))
        return self


class DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupTemplateIdList(TeaModel):
    def __init__(
        self,
        template_id_list: List[str] = None,
    ):
        self.template_id_list = template_id_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.template_id_list is not None:
            result['TemplateIdList'] = self.template_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateIdList') is not None:
            self.template_id_list = m.get('TemplateIdList')
        return self


class DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroup(TeaModel):
    def __init__(
        self,
        status: str = None,
        match_express: DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupMatchExpress = None,
        template_id_list: DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupTemplateIdList = None,
        dynamic_tag_rule_id: str = None,
        match_express_filter_relation: str = None,
        region_id: str = None,
        tag_key: str = None,
    ):
        self.status = status
        self.match_express = match_express
        self.template_id_list = template_id_list
        self.dynamic_tag_rule_id = dynamic_tag_rule_id
        self.match_express_filter_relation = match_express_filter_relation
        self.region_id = region_id
        self.tag_key = tag_key

    def validate(self):
        if self.match_express:
            self.match_express.validate()
        if self.template_id_list:
            self.template_id_list.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.match_express is not None:
            result['MatchExpress'] = self.match_express.to_map()
        if self.template_id_list is not None:
            result['TemplateIdList'] = self.template_id_list.to_map()
        if self.dynamic_tag_rule_id is not None:
            result['DynamicTagRuleId'] = self.dynamic_tag_rule_id
        if self.match_express_filter_relation is not None:
            result['MatchExpressFilterRelation'] = self.match_express_filter_relation
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('MatchExpress') is not None:
            temp_model = DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupMatchExpress()
            self.match_express = temp_model.from_map(m['MatchExpress'])
        if m.get('TemplateIdList') is not None:
            temp_model = DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroupTemplateIdList()
            self.template_id_list = temp_model.from_map(m['TemplateIdList'])
        if m.get('DynamicTagRuleId') is not None:
            self.dynamic_tag_rule_id = m.get('DynamicTagRuleId')
        if m.get('MatchExpressFilterRelation') is not None:
            self.match_express_filter_relation = m.get('MatchExpressFilterRelation')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class DescribeDynamicTagRuleListResponseBodyTagGroupList(TeaModel):
    def __init__(
        self,
        tag_group: List[DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroup] = None,
    ):
        self.tag_group = tag_group

    def validate(self):
        if self.tag_group:
            for k in self.tag_group:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['TagGroup'] = []
        if self.tag_group is not None:
            for k in self.tag_group:
                result['TagGroup'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag_group = []
        if m.get('TagGroup') is not None:
            for k in m.get('TagGroup'):
                temp_model = DescribeDynamicTagRuleListResponseBodyTagGroupListTagGroup()
                self.tag_group.append(temp_model.from_map(k))
        return self


class DescribeDynamicTagRuleListResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: str = None,
        page_number: str = None,
        total: int = None,
        tag_group_list: DescribeDynamicTagRuleListResponseBodyTagGroupList = None,
        code: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.tag_group_list = tag_group_list
        self.code = code
        self.success = success

    def validate(self):
        if self.tag_group_list:
            self.tag_group_list.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.tag_group_list is not None:
            result['TagGroupList'] = self.tag_group_list.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('TagGroupList') is not None:
            temp_model = DescribeDynamicTagRuleListResponseBodyTagGroupList()
            self.tag_group_list = temp_model.from_map(m['TagGroupList'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDynamicTagRuleListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDynamicTagRuleListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDynamicTagRuleListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeEventRuleAttributeRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
    ):
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class DescribeEventRuleAttributeResponseBodyResultEventPatternStatusList(TeaModel):
    def __init__(
        self,
        status_list: List[str] = None,
    ):
        self.status_list = status_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status_list is not None:
            result['StatusList'] = self.status_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StatusList') is not None:
            self.status_list = m.get('StatusList')
        return self


class DescribeEventRuleAttributeResponseBodyResultEventPatternLevelList(TeaModel):
    def __init__(
        self,
        level_list: List[str] = None,
    ):
        self.level_list = level_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.level_list is not None:
            result['LevelList'] = self.level_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LevelList') is not None:
            self.level_list = m.get('LevelList')
        return self


class DescribeEventRuleAttributeResponseBodyResultEventPatternNameList(TeaModel):
    def __init__(
        self,
        name_list: List[str] = None,
    ):
        self.name_list = name_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name_list is not None:
            result['NameList'] = self.name_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NameList') is not None:
            self.name_list = m.get('NameList')
        return self


class DescribeEventRuleAttributeResponseBodyResultEventPattern(TeaModel):
    def __init__(
        self,
        status_list: DescribeEventRuleAttributeResponseBodyResultEventPatternStatusList = None,
        product: str = None,
        level_list: DescribeEventRuleAttributeResponseBodyResultEventPatternLevelList = None,
        name_list: DescribeEventRuleAttributeResponseBodyResultEventPatternNameList = None,
    ):
        self.status_list = status_list
        self.product = product
        self.level_list = level_list
        self.name_list = name_list

    def validate(self):
        if self.status_list:
            self.status_list.validate()
        if self.level_list:
            self.level_list.validate()
        if self.name_list:
            self.name_list.validate()

    def to_map(self):
        result = dict()
        if self.status_list is not None:
            result['StatusList'] = self.status_list.to_map()
        if self.product is not None:
            result['Product'] = self.product
        if self.level_list is not None:
            result['LevelList'] = self.level_list.to_map()
        if self.name_list is not None:
            result['NameList'] = self.name_list.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StatusList') is not None:
            temp_model = DescribeEventRuleAttributeResponseBodyResultEventPatternStatusList()
            self.status_list = temp_model.from_map(m['StatusList'])
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('LevelList') is not None:
            temp_model = DescribeEventRuleAttributeResponseBodyResultEventPatternLevelList()
            self.level_list = temp_model.from_map(m['LevelList'])
        if m.get('NameList') is not None:
            temp_model = DescribeEventRuleAttributeResponseBodyResultEventPatternNameList()
            self.name_list = temp_model.from_map(m['NameList'])
        return self


class DescribeEventRuleAttributeResponseBodyResult(TeaModel):
    def __init__(
        self,
        event_type: str = None,
        group_id: str = None,
        description: str = None,
        state: str = None,
        name: str = None,
        event_pattern: DescribeEventRuleAttributeResponseBodyResultEventPattern = None,
    ):
        self.event_type = event_type
        self.group_id = group_id
        self.description = description
        self.state = state
        self.name = name
        self.event_pattern = event_pattern

    def validate(self):
        if self.event_pattern:
            self.event_pattern.validate()

    def to_map(self):
        result = dict()
        if self.event_type is not None:
            result['EventType'] = self.event_type
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.description is not None:
            result['Description'] = self.description
        if self.state is not None:
            result['State'] = self.state
        if self.name is not None:
            result['Name'] = self.name
        if self.event_pattern is not None:
            result['EventPattern'] = self.event_pattern.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventType') is not None:
            self.event_type = m.get('EventType')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EventPattern') is not None:
            temp_model = DescribeEventRuleAttributeResponseBodyResultEventPattern()
            self.event_pattern = temp_model.from_map(m['EventPattern'])
        return self


class DescribeEventRuleAttributeResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        result: DescribeEventRuleAttributeResponseBodyResult = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.result is not None:
            result['Result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Result') is not None:
            temp_model = DescribeEventRuleAttributeResponseBodyResult()
            self.result = temp_model.from_map(m['Result'])
        return self


class DescribeEventRuleAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeEventRuleAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeEventRuleAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeEventRuleListRequest(TeaModel):
    def __init__(
        self,
        name_prefix: str = None,
        page_number: str = None,
        page_size: str = None,
        group_id: str = None,
    ):
        self.name_prefix = name_prefix
        self.page_number = page_number
        self.page_size = page_size
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name_prefix is not None:
            result['NamePrefix'] = self.name_prefix
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NamePrefix') is not None:
            self.name_prefix = m.get('NamePrefix')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternEventTypeList(TeaModel):
    def __init__(
        self,
        event_type_list: List[str] = None,
    ):
        self.event_type_list = event_type_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.event_type_list is not None:
            result['EventTypeList'] = self.event_type_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventTypeList') is not None:
            self.event_type_list = m.get('EventTypeList')
        return self


class DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternLevelList(TeaModel):
    def __init__(
        self,
        level_list: List[str] = None,
    ):
        self.level_list = level_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.level_list is not None:
            result['LevelList'] = self.level_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LevelList') is not None:
            self.level_list = m.get('LevelList')
        return self


class DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternNameList(TeaModel):
    def __init__(
        self,
        name_list: List[str] = None,
    ):
        self.name_list = name_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name_list is not None:
            result['NameList'] = self.name_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NameList') is not None:
            self.name_list = m.get('NameList')
        return self


class DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPattern(TeaModel):
    def __init__(
        self,
        event_type_list: DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternEventTypeList = None,
        product: str = None,
        level_list: DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternLevelList = None,
        name_list: DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternNameList = None,
    ):
        self.event_type_list = event_type_list
        self.product = product
        self.level_list = level_list
        self.name_list = name_list

    def validate(self):
        if self.event_type_list:
            self.event_type_list.validate()
        if self.level_list:
            self.level_list.validate()
        if self.name_list:
            self.name_list.validate()

    def to_map(self):
        result = dict()
        if self.event_type_list is not None:
            result['EventTypeList'] = self.event_type_list.to_map()
        if self.product is not None:
            result['Product'] = self.product
        if self.level_list is not None:
            result['LevelList'] = self.level_list.to_map()
        if self.name_list is not None:
            result['NameList'] = self.name_list.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventTypeList') is not None:
            temp_model = DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternEventTypeList()
            self.event_type_list = temp_model.from_map(m['EventTypeList'])
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('LevelList') is not None:
            temp_model = DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternLevelList()
            self.level_list = temp_model.from_map(m['LevelList'])
        if m.get('NameList') is not None:
            temp_model = DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPatternNameList()
            self.name_list = temp_model.from_map(m['NameList'])
        return self


class DescribeEventRuleListResponseBodyEventRulesEventRuleEventPattern(TeaModel):
    def __init__(
        self,
        event_pattern: List[DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPattern] = None,
    ):
        self.event_pattern = event_pattern

    def validate(self):
        if self.event_pattern:
            for k in self.event_pattern:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['EventPattern'] = []
        if self.event_pattern is not None:
            for k in self.event_pattern:
                result['EventPattern'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.event_pattern = []
        if m.get('EventPattern') is not None:
            for k in m.get('EventPattern'):
                temp_model = DescribeEventRuleListResponseBodyEventRulesEventRuleEventPatternEventPattern()
                self.event_pattern.append(temp_model.from_map(k))
        return self


class DescribeEventRuleListResponseBodyEventRulesEventRule(TeaModel):
    def __init__(
        self,
        event_type: str = None,
        description: str = None,
        group_id: str = None,
        state: str = None,
        name: str = None,
        event_pattern: DescribeEventRuleListResponseBodyEventRulesEventRuleEventPattern = None,
    ):
        self.event_type = event_type
        self.description = description
        self.group_id = group_id
        self.state = state
        self.name = name
        self.event_pattern = event_pattern

    def validate(self):
        if self.event_pattern:
            self.event_pattern.validate()

    def to_map(self):
        result = dict()
        if self.event_type is not None:
            result['EventType'] = self.event_type
        if self.description is not None:
            result['Description'] = self.description
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.state is not None:
            result['State'] = self.state
        if self.name is not None:
            result['Name'] = self.name
        if self.event_pattern is not None:
            result['EventPattern'] = self.event_pattern.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventType') is not None:
            self.event_type = m.get('EventType')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EventPattern') is not None:
            temp_model = DescribeEventRuleListResponseBodyEventRulesEventRuleEventPattern()
            self.event_pattern = temp_model.from_map(m['EventPattern'])
        return self


class DescribeEventRuleListResponseBodyEventRules(TeaModel):
    def __init__(
        self,
        event_rule: List[DescribeEventRuleListResponseBodyEventRulesEventRule] = None,
    ):
        self.event_rule = event_rule

    def validate(self):
        if self.event_rule:
            for k in self.event_rule:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['EventRule'] = []
        if self.event_rule is not None:
            for k in self.event_rule:
                result['EventRule'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.event_rule = []
        if m.get('EventRule') is not None:
            for k in m.get('EventRule'):
                temp_model = DescribeEventRuleListResponseBodyEventRulesEventRule()
                self.event_rule.append(temp_model.from_map(k))
        return self


class DescribeEventRuleListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        total: int = None,
        event_rules: DescribeEventRuleListResponseBodyEventRules = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.total = total
        self.event_rules = event_rules
        self.code = code
        self.success = success

    def validate(self):
        if self.event_rules:
            self.event_rules.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.event_rules is not None:
            result['EventRules'] = self.event_rules.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('EventRules') is not None:
            temp_model = DescribeEventRuleListResponseBodyEventRules()
            self.event_rules = temp_model.from_map(m['EventRules'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeEventRuleListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeEventRuleListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeEventRuleListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeEventRuleTargetListRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
    ):
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class DescribeEventRuleTargetListResponseBodyContactParametersContactParameter(TeaModel):
    def __init__(
        self,
        contact_group_name: str = None,
        level: str = None,
        id: str = None,
    ):
        self.contact_group_name = contact_group_name
        self.level = level
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group_name is not None:
            result['ContactGroupName'] = self.contact_group_name
        if self.level is not None:
            result['Level'] = self.level
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupName') is not None:
            self.contact_group_name = m.get('ContactGroupName')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeEventRuleTargetListResponseBodyContactParameters(TeaModel):
    def __init__(
        self,
        contact_parameter: List[DescribeEventRuleTargetListResponseBodyContactParametersContactParameter] = None,
    ):
        self.contact_parameter = contact_parameter

    def validate(self):
        if self.contact_parameter:
            for k in self.contact_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContactParameter'] = []
        if self.contact_parameter is not None:
            for k in self.contact_parameter:
                result['ContactParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact_parameter = []
        if m.get('ContactParameter') is not None:
            for k in m.get('ContactParameter'):
                temp_model = DescribeEventRuleTargetListResponseBodyContactParametersContactParameter()
                self.contact_parameter.append(temp_model.from_map(k))
        return self


class DescribeEventRuleTargetListResponseBodySlsParametersSlsParameter(TeaModel):
    def __init__(
        self,
        log_store: str = None,
        region: str = None,
        project: str = None,
        arn: str = None,
        id: str = None,
    ):
        self.log_store = log_store
        self.region = region
        self.project = project
        self.arn = arn
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.log_store is not None:
            result['LogStore'] = self.log_store
        if self.region is not None:
            result['Region'] = self.region
        if self.project is not None:
            result['Project'] = self.project
        if self.arn is not None:
            result['Arn'] = self.arn
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LogStore') is not None:
            self.log_store = m.get('LogStore')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('Project') is not None:
            self.project = m.get('Project')
        if m.get('Arn') is not None:
            self.arn = m.get('Arn')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeEventRuleTargetListResponseBodySlsParameters(TeaModel):
    def __init__(
        self,
        sls_parameter: List[DescribeEventRuleTargetListResponseBodySlsParametersSlsParameter] = None,
    ):
        self.sls_parameter = sls_parameter

    def validate(self):
        if self.sls_parameter:
            for k in self.sls_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SlsParameter'] = []
        if self.sls_parameter is not None:
            for k in self.sls_parameter:
                result['SlsParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.sls_parameter = []
        if m.get('SlsParameter') is not None:
            for k in m.get('SlsParameter'):
                temp_model = DescribeEventRuleTargetListResponseBodySlsParametersSlsParameter()
                self.sls_parameter.append(temp_model.from_map(k))
        return self


class DescribeEventRuleTargetListResponseBodyWebhookParametersWebhookParameter(TeaModel):
    def __init__(
        self,
        protocol: str = None,
        url: str = None,
        method: str = None,
        id: str = None,
    ):
        self.protocol = protocol
        self.url = url
        self.method = method
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.url is not None:
            result['Url'] = self.url
        if self.method is not None:
            result['Method'] = self.method
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Method') is not None:
            self.method = m.get('Method')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeEventRuleTargetListResponseBodyWebhookParameters(TeaModel):
    def __init__(
        self,
        webhook_parameter: List[DescribeEventRuleTargetListResponseBodyWebhookParametersWebhookParameter] = None,
    ):
        self.webhook_parameter = webhook_parameter

    def validate(self):
        if self.webhook_parameter:
            for k in self.webhook_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['WebhookParameter'] = []
        if self.webhook_parameter is not None:
            for k in self.webhook_parameter:
                result['WebhookParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.webhook_parameter = []
        if m.get('WebhookParameter') is not None:
            for k in m.get('WebhookParameter'):
                temp_model = DescribeEventRuleTargetListResponseBodyWebhookParametersWebhookParameter()
                self.webhook_parameter.append(temp_model.from_map(k))
        return self


class DescribeEventRuleTargetListResponseBodyFcParametersFCParameter(TeaModel):
    def __init__(
        self,
        function_name: str = None,
        region: str = None,
        service_name: str = None,
        arn: str = None,
        id: str = None,
    ):
        self.function_name = function_name
        self.region = region
        self.service_name = service_name
        self.arn = arn
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.function_name is not None:
            result['FunctionName'] = self.function_name
        if self.region is not None:
            result['Region'] = self.region
        if self.service_name is not None:
            result['ServiceName'] = self.service_name
        if self.arn is not None:
            result['Arn'] = self.arn
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FunctionName') is not None:
            self.function_name = m.get('FunctionName')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ServiceName') is not None:
            self.service_name = m.get('ServiceName')
        if m.get('Arn') is not None:
            self.arn = m.get('Arn')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeEventRuleTargetListResponseBodyFcParameters(TeaModel):
    def __init__(
        self,
        fcparameter: List[DescribeEventRuleTargetListResponseBodyFcParametersFCParameter] = None,
    ):
        self.fcparameter = fcparameter

    def validate(self):
        if self.fcparameter:
            for k in self.fcparameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['FCParameter'] = []
        if self.fcparameter is not None:
            for k in self.fcparameter:
                result['FCParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.fcparameter = []
        if m.get('FCParameter') is not None:
            for k in m.get('FCParameter'):
                temp_model = DescribeEventRuleTargetListResponseBodyFcParametersFCParameter()
                self.fcparameter.append(temp_model.from_map(k))
        return self


class DescribeEventRuleTargetListResponseBodyMnsParametersMnsParameter(TeaModel):
    def __init__(
        self,
        region: str = None,
        queue: str = None,
        arn: str = None,
        id: str = None,
    ):
        self.region = region
        self.queue = queue
        self.arn = arn
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region is not None:
            result['Region'] = self.region
        if self.queue is not None:
            result['Queue'] = self.queue
        if self.arn is not None:
            result['Arn'] = self.arn
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('Queue') is not None:
            self.queue = m.get('Queue')
        if m.get('Arn') is not None:
            self.arn = m.get('Arn')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeEventRuleTargetListResponseBodyMnsParameters(TeaModel):
    def __init__(
        self,
        mns_parameter: List[DescribeEventRuleTargetListResponseBodyMnsParametersMnsParameter] = None,
    ):
        self.mns_parameter = mns_parameter

    def validate(self):
        if self.mns_parameter:
            for k in self.mns_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['MnsParameter'] = []
        if self.mns_parameter is not None:
            for k in self.mns_parameter:
                result['MnsParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.mns_parameter = []
        if m.get('MnsParameter') is not None:
            for k in m.get('MnsParameter'):
                temp_model = DescribeEventRuleTargetListResponseBodyMnsParametersMnsParameter()
                self.mns_parameter.append(temp_model.from_map(k))
        return self


class DescribeEventRuleTargetListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        contact_parameters: DescribeEventRuleTargetListResponseBodyContactParameters = None,
        sls_parameters: DescribeEventRuleTargetListResponseBodySlsParameters = None,
        webhook_parameters: DescribeEventRuleTargetListResponseBodyWebhookParameters = None,
        fc_parameters: DescribeEventRuleTargetListResponseBodyFcParameters = None,
        code: str = None,
        mns_parameters: DescribeEventRuleTargetListResponseBodyMnsParameters = None,
    ):
        self.message = message
        self.request_id = request_id
        self.contact_parameters = contact_parameters
        self.sls_parameters = sls_parameters
        self.webhook_parameters = webhook_parameters
        self.fc_parameters = fc_parameters
        self.code = code
        self.mns_parameters = mns_parameters

    def validate(self):
        if self.contact_parameters:
            self.contact_parameters.validate()
        if self.sls_parameters:
            self.sls_parameters.validate()
        if self.webhook_parameters:
            self.webhook_parameters.validate()
        if self.fc_parameters:
            self.fc_parameters.validate()
        if self.mns_parameters:
            self.mns_parameters.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.contact_parameters is not None:
            result['ContactParameters'] = self.contact_parameters.to_map()
        if self.sls_parameters is not None:
            result['SlsParameters'] = self.sls_parameters.to_map()
        if self.webhook_parameters is not None:
            result['WebhookParameters'] = self.webhook_parameters.to_map()
        if self.fc_parameters is not None:
            result['FcParameters'] = self.fc_parameters.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.mns_parameters is not None:
            result['MnsParameters'] = self.mns_parameters.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ContactParameters') is not None:
            temp_model = DescribeEventRuleTargetListResponseBodyContactParameters()
            self.contact_parameters = temp_model.from_map(m['ContactParameters'])
        if m.get('SlsParameters') is not None:
            temp_model = DescribeEventRuleTargetListResponseBodySlsParameters()
            self.sls_parameters = temp_model.from_map(m['SlsParameters'])
        if m.get('WebhookParameters') is not None:
            temp_model = DescribeEventRuleTargetListResponseBodyWebhookParameters()
            self.webhook_parameters = temp_model.from_map(m['WebhookParameters'])
        if m.get('FcParameters') is not None:
            temp_model = DescribeEventRuleTargetListResponseBodyFcParameters()
            self.fc_parameters = temp_model.from_map(m['FcParameters'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('MnsParameters') is not None:
            temp_model = DescribeEventRuleTargetListResponseBodyMnsParameters()
            self.mns_parameters = temp_model.from_map(m['MnsParameters'])
        return self


class DescribeEventRuleTargetListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeEventRuleTargetListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeEventRuleTargetListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeExporterOutputListRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeExporterOutputListResponseBodyDatapointsDatapointConfigJson(TeaModel):
    def __init__(
        self,
        as_: str = None,
        ak: str = None,
        endpoint: str = None,
        project: str = None,
        logstore: str = None,
    ):
        self.as_ = as_
        self.ak = ak
        self.endpoint = endpoint
        self.project = project
        self.logstore = logstore

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.as_ is not None:
            result['as'] = self.as_
        if self.ak is not None:
            result['ak'] = self.ak
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.project is not None:
            result['project'] = self.project
        if self.logstore is not None:
            result['logstore'] = self.logstore
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('as') is not None:
            self.as_ = m.get('as')
        if m.get('ak') is not None:
            self.ak = m.get('ak')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('project') is not None:
            self.project = m.get('project')
        if m.get('logstore') is not None:
            self.logstore = m.get('logstore')
        return self


class DescribeExporterOutputListResponseBodyDatapointsDatapoint(TeaModel):
    def __init__(
        self,
        create_time: int = None,
        config_json: DescribeExporterOutputListResponseBodyDatapointsDatapointConfigJson = None,
        dest_name: str = None,
        dest_type: str = None,
    ):
        self.create_time = create_time
        self.config_json = config_json
        self.dest_name = dest_name
        self.dest_type = dest_type

    def validate(self):
        if self.config_json:
            self.config_json.validate()

    def to_map(self):
        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.config_json is not None:
            result['ConfigJson'] = self.config_json.to_map()
        if self.dest_name is not None:
            result['DestName'] = self.dest_name
        if self.dest_type is not None:
            result['DestType'] = self.dest_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('ConfigJson') is not None:
            temp_model = DescribeExporterOutputListResponseBodyDatapointsDatapointConfigJson()
            self.config_json = temp_model.from_map(m['ConfigJson'])
        if m.get('DestName') is not None:
            self.dest_name = m.get('DestName')
        if m.get('DestType') is not None:
            self.dest_type = m.get('DestType')
        return self


class DescribeExporterOutputListResponseBodyDatapoints(TeaModel):
    def __init__(
        self,
        datapoint: List[DescribeExporterOutputListResponseBodyDatapointsDatapoint] = None,
    ):
        self.datapoint = datapoint

    def validate(self):
        if self.datapoint:
            for k in self.datapoint:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Datapoint'] = []
        if self.datapoint is not None:
            for k in self.datapoint:
                result['Datapoint'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.datapoint = []
        if m.get('Datapoint') is not None:
            for k in m.get('Datapoint'):
                temp_model = DescribeExporterOutputListResponseBodyDatapointsDatapoint()
                self.datapoint.append(temp_model.from_map(k))
        return self


class DescribeExporterOutputListResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_number: int = None,
        total: int = None,
        datapoints: DescribeExporterOutputListResponseBodyDatapoints = None,
        code: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_number = page_number
        self.total = total
        self.datapoints = datapoints
        self.code = code
        self.success = success

    def validate(self):
        if self.datapoints:
            self.datapoints.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Datapoints') is not None:
            temp_model = DescribeExporterOutputListResponseBodyDatapoints()
            self.datapoints = temp_model.from_map(m['Datapoints'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeExporterOutputListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeExporterOutputListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeExporterOutputListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeExporterRuleListRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeExporterRuleListResponseBodyDatapointsDatapointDstName(TeaModel):
    def __init__(
        self,
        dst_name: List[str] = None,
    ):
        self.dst_name = dst_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dst_name is not None:
            result['DstName'] = self.dst_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DstName') is not None:
            self.dst_name = m.get('DstName')
        return self


class DescribeExporterRuleListResponseBodyDatapointsDatapoint(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        describe: str = None,
        target_windows: str = None,
        create_time: int = None,
        enabled: bool = None,
        dst_name: DescribeExporterRuleListResponseBodyDatapointsDatapointDstName = None,
        dimension: str = None,
        namespace: str = None,
        rule_name: str = None,
    ):
        self.metric_name = metric_name
        self.describe = describe
        self.target_windows = target_windows
        self.create_time = create_time
        self.enabled = enabled
        self.dst_name = dst_name
        self.dimension = dimension
        self.namespace = namespace
        self.rule_name = rule_name

    def validate(self):
        if self.dst_name:
            self.dst_name.validate()

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.describe is not None:
            result['Describe'] = self.describe
        if self.target_windows is not None:
            result['TargetWindows'] = self.target_windows
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.enabled is not None:
            result['Enabled'] = self.enabled
        if self.dst_name is not None:
            result['DstName'] = self.dst_name.to_map()
        if self.dimension is not None:
            result['Dimension'] = self.dimension
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Describe') is not None:
            self.describe = m.get('Describe')
        if m.get('TargetWindows') is not None:
            self.target_windows = m.get('TargetWindows')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Enabled') is not None:
            self.enabled = m.get('Enabled')
        if m.get('DstName') is not None:
            temp_model = DescribeExporterRuleListResponseBodyDatapointsDatapointDstName()
            self.dst_name = temp_model.from_map(m['DstName'])
        if m.get('Dimension') is not None:
            self.dimension = m.get('Dimension')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class DescribeExporterRuleListResponseBodyDatapoints(TeaModel):
    def __init__(
        self,
        datapoint: List[DescribeExporterRuleListResponseBodyDatapointsDatapoint] = None,
    ):
        self.datapoint = datapoint

    def validate(self):
        if self.datapoint:
            for k in self.datapoint:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Datapoint'] = []
        if self.datapoint is not None:
            for k in self.datapoint:
                result['Datapoint'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.datapoint = []
        if m.get('Datapoint') is not None:
            for k in m.get('Datapoint'):
                temp_model = DescribeExporterRuleListResponseBodyDatapointsDatapoint()
                self.datapoint.append(temp_model.from_map(k))
        return self


class DescribeExporterRuleListResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_number: int = None,
        total: int = None,
        datapoints: DescribeExporterRuleListResponseBodyDatapoints = None,
        code: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_number = page_number
        self.total = total
        self.datapoints = datapoints
        self.code = code
        self.success = success

    def validate(self):
        if self.datapoints:
            self.datapoints.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Datapoints') is not None:
            temp_model = DescribeExporterRuleListResponseBodyDatapoints()
            self.datapoints = temp_model.from_map(m['Datapoints'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeExporterRuleListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeExporterRuleListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeExporterRuleListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGroupMonitoringAgentProcessRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        process_name: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.group_id = group_id
        self.process_name = process_name
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessMatchExpressMatchExpress(TeaModel):
    def __init__(
        self,
        value: str = None,
        name: str = None,
        function: str = None,
    ):
        self.value = value
        self.name = name
        self.function = function

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.name is not None:
            result['Name'] = self.name
        if self.function is not None:
            result['Function'] = self.function
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Function') is not None:
            self.function = m.get('Function')
        return self


class DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessMatchExpress(TeaModel):
    def __init__(
        self,
        match_express: List[DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessMatchExpressMatchExpress] = None,
    ):
        self.match_express = match_express

    def validate(self):
        if self.match_express:
            for k in self.match_express:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['MatchExpress'] = []
        if self.match_express is not None:
            for k in self.match_express:
                result['MatchExpress'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.match_express = []
        if m.get('MatchExpress') is not None:
            for k in m.get('MatchExpress'):
                temp_model = DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessMatchExpressMatchExpress()
                self.match_express.append(temp_model.from_map(k))
        return self


class DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessAlertConfigAlertConfig(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        silence_time: str = None,
        webhook: str = None,
        times: str = None,
        escalations_level: str = None,
        no_effective_interval: str = None,
        effective_interval: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.silence_time = silence_time
        self.webhook = webhook
        self.times = times
        self.escalations_level = escalations_level
        self.no_effective_interval = no_effective_interval
        self.effective_interval = effective_interval
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.times is not None:
            result['Times'] = self.times
        if self.escalations_level is not None:
            result['EscalationsLevel'] = self.escalations_level
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('EscalationsLevel') is not None:
            self.escalations_level = m.get('EscalationsLevel')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessAlertConfig(TeaModel):
    def __init__(
        self,
        alert_config: List[DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessAlertConfigAlertConfig] = None,
    ):
        self.alert_config = alert_config

    def validate(self):
        if self.alert_config:
            for k in self.alert_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertConfig'] = []
        if self.alert_config is not None:
            for k in self.alert_config:
                result['AlertConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_config = []
        if m.get('AlertConfig') is not None:
            for k in m.get('AlertConfig'):
                temp_model = DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessAlertConfigAlertConfig()
                self.alert_config.append(temp_model.from_map(k))
        return self


class DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcess(TeaModel):
    def __init__(
        self,
        process_name: str = None,
        match_express: DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessMatchExpress = None,
        group_id: str = None,
        alert_config: DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessAlertConfig = None,
        match_express_filter_relation: str = None,
        id: str = None,
    ):
        self.process_name = process_name
        self.match_express = match_express
        self.group_id = group_id
        self.alert_config = alert_config
        self.match_express_filter_relation = match_express_filter_relation
        self.id = id

    def validate(self):
        if self.match_express:
            self.match_express.validate()
        if self.alert_config:
            self.alert_config.validate()

    def to_map(self):
        result = dict()
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.match_express is not None:
            result['MatchExpress'] = self.match_express.to_map()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.alert_config is not None:
            result['AlertConfig'] = self.alert_config.to_map()
        if self.match_express_filter_relation is not None:
            result['MatchExpressFilterRelation'] = self.match_express_filter_relation
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('MatchExpress') is not None:
            temp_model = DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessMatchExpress()
            self.match_express = temp_model.from_map(m['MatchExpress'])
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('AlertConfig') is not None:
            temp_model = DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcessAlertConfig()
            self.alert_config = temp_model.from_map(m['AlertConfig'])
        if m.get('MatchExpressFilterRelation') is not None:
            self.match_express_filter_relation = m.get('MatchExpressFilterRelation')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeGroupMonitoringAgentProcessResponseBodyProcesses(TeaModel):
    def __init__(
        self,
        process: List[DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcess] = None,
    ):
        self.process = process

    def validate(self):
        if self.process:
            for k in self.process:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Process'] = []
        if self.process is not None:
            for k in self.process:
                result['Process'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.process = []
        if m.get('Process') is not None:
            for k in m.get('Process'):
                temp_model = DescribeGroupMonitoringAgentProcessResponseBodyProcessesProcess()
                self.process.append(temp_model.from_map(k))
        return self


class DescribeGroupMonitoringAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: str = None,
        page_number: str = None,
        total: str = None,
        processes: DescribeGroupMonitoringAgentProcessResponseBodyProcesses = None,
        code: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.processes = processes
        self.code = code
        self.success = success

    def validate(self):
        if self.processes:
            self.processes.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.processes is not None:
            result['Processes'] = self.processes.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Processes') is not None:
            temp_model = DescribeGroupMonitoringAgentProcessResponseBodyProcesses()
            self.processes = temp_model.from_map(m['Processes'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeGroupMonitoringAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGroupMonitoringAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGroupMonitoringAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeHostAvailabilityListRequest(TeaModel):
    def __init__(
        self,
        id: int = None,
        task_name: str = None,
        page_number: int = None,
        page_size: int = None,
        group_id: int = None,
    ):
        self.id = id
        self.task_name = task_name
        self.page_number = page_number
        self.page_size = page_size
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigTaskOption(TeaModel):
    def __init__(
        self,
        http_method: str = None,
        http_uri: str = None,
        telnet_or_ping_host: str = None,
        http_response_charset: str = None,
        http_post_content: str = None,
        http_negative: bool = None,
        http_keyword: str = None,
    ):
        self.http_method = http_method
        self.http_uri = http_uri
        self.telnet_or_ping_host = telnet_or_ping_host
        self.http_response_charset = http_response_charset
        self.http_post_content = http_post_content
        self.http_negative = http_negative
        self.http_keyword = http_keyword

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.http_method is not None:
            result['HttpMethod'] = self.http_method
        if self.http_uri is not None:
            result['HttpURI'] = self.http_uri
        if self.telnet_or_ping_host is not None:
            result['TelnetOrPingHost'] = self.telnet_or_ping_host
        if self.http_response_charset is not None:
            result['HttpResponseCharset'] = self.http_response_charset
        if self.http_post_content is not None:
            result['HttpPostContent'] = self.http_post_content
        if self.http_negative is not None:
            result['HttpNegative'] = self.http_negative
        if self.http_keyword is not None:
            result['HttpKeyword'] = self.http_keyword
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HttpMethod') is not None:
            self.http_method = m.get('HttpMethod')
        if m.get('HttpURI') is not None:
            self.http_uri = m.get('HttpURI')
        if m.get('TelnetOrPingHost') is not None:
            self.telnet_or_ping_host = m.get('TelnetOrPingHost')
        if m.get('HttpResponseCharset') is not None:
            self.http_response_charset = m.get('HttpResponseCharset')
        if m.get('HttpPostContent') is not None:
            self.http_post_content = m.get('HttpPostContent')
        if m.get('HttpNegative') is not None:
            self.http_negative = m.get('HttpNegative')
        if m.get('HttpKeyword') is not None:
            self.http_keyword = m.get('HttpKeyword')
        return self


class DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfigEscalationListEscalationList(TeaModel):
    def __init__(
        self,
        value: str = None,
        metric_name: str = None,
        times: str = None,
        operator: str = None,
        aggregate: str = None,
    ):
        self.value = value
        self.metric_name = metric_name
        self.times = times
        self.operator = operator
        self.aggregate = aggregate

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.times is not None:
            result['Times'] = self.times
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.aggregate is not None:
            result['Aggregate'] = self.aggregate
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Aggregate') is not None:
            self.aggregate = m.get('Aggregate')
        return self


class DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfigEscalationList(TeaModel):
    def __init__(
        self,
        escalation_list: List[DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfigEscalationListEscalationList] = None,
    ):
        self.escalation_list = escalation_list

    def validate(self):
        if self.escalation_list:
            for k in self.escalation_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['escalationList'] = []
        if self.escalation_list is not None:
            for k in self.escalation_list:
                result['escalationList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.escalation_list = []
        if m.get('escalationList') is not None:
            for k in m.get('escalationList'):
                temp_model = DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfigEscalationListEscalationList()
                self.escalation_list.append(temp_model.from_map(k))
        return self


class DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfig(TeaModel):
    def __init__(
        self,
        silence_time: int = None,
        end_time: int = None,
        start_time: int = None,
        notify_type: int = None,
        escalation_list: DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfigEscalationList = None,
        web_hook: str = None,
    ):
        self.silence_time = silence_time
        self.end_time = end_time
        self.start_time = start_time
        self.notify_type = notify_type
        self.escalation_list = escalation_list
        self.web_hook = web_hook

    def validate(self):
        if self.escalation_list:
            self.escalation_list.validate()

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.notify_type is not None:
            result['NotifyType'] = self.notify_type
        if self.escalation_list is not None:
            result['EscalationList'] = self.escalation_list.to_map()
        if self.web_hook is not None:
            result['WebHook'] = self.web_hook
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('NotifyType') is not None:
            self.notify_type = m.get('NotifyType')
        if m.get('EscalationList') is not None:
            temp_model = DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfigEscalationList()
            self.escalation_list = temp_model.from_map(m['EscalationList'])
        if m.get('WebHook') is not None:
            self.web_hook = m.get('WebHook')
        return self


class DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigInstances(TeaModel):
    def __init__(
        self,
        instance: List[str] = None,
    ):
        self.instance = instance

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance is not None:
            result['Instance'] = self.instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Instance') is not None:
            self.instance = m.get('Instance')
        return self


class DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfig(TeaModel):
    def __init__(
        self,
        task_type: str = None,
        group_name: str = None,
        group_id: int = None,
        task_option: DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigTaskOption = None,
        task_name: str = None,
        disabled: bool = None,
        alert_config: DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfig = None,
        task_scope: str = None,
        instances: DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigInstances = None,
        id: int = None,
    ):
        self.task_type = task_type
        self.group_name = group_name
        self.group_id = group_id
        self.task_option = task_option
        self.task_name = task_name
        self.disabled = disabled
        self.alert_config = alert_config
        self.task_scope = task_scope
        self.instances = instances
        self.id = id

    def validate(self):
        if self.task_option:
            self.task_option.validate()
        if self.alert_config:
            self.alert_config.validate()
        if self.instances:
            self.instances.validate()

    def to_map(self):
        result = dict()
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.task_option is not None:
            result['TaskOption'] = self.task_option.to_map()
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.disabled is not None:
            result['Disabled'] = self.disabled
        if self.alert_config is not None:
            result['AlertConfig'] = self.alert_config.to_map()
        if self.task_scope is not None:
            result['TaskScope'] = self.task_scope
        if self.instances is not None:
            result['Instances'] = self.instances.to_map()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('TaskOption') is not None:
            temp_model = DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigTaskOption()
            self.task_option = temp_model.from_map(m['TaskOption'])
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('Disabled') is not None:
            self.disabled = m.get('Disabled')
        if m.get('AlertConfig') is not None:
            temp_model = DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigAlertConfig()
            self.alert_config = temp_model.from_map(m['AlertConfig'])
        if m.get('TaskScope') is not None:
            self.task_scope = m.get('TaskScope')
        if m.get('Instances') is not None:
            temp_model = DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfigInstances()
            self.instances = temp_model.from_map(m['Instances'])
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeHostAvailabilityListResponseBodyTaskList(TeaModel):
    def __init__(
        self,
        node_task_config: List[DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfig] = None,
    ):
        self.node_task_config = node_task_config

    def validate(self):
        if self.node_task_config:
            for k in self.node_task_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['NodeTaskConfig'] = []
        if self.node_task_config is not None:
            for k in self.node_task_config:
                result['NodeTaskConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_task_config = []
        if m.get('NodeTaskConfig') is not None:
            for k in m.get('NodeTaskConfig'):
                temp_model = DescribeHostAvailabilityListResponseBodyTaskListNodeTaskConfig()
                self.node_task_config.append(temp_model.from_map(k))
        return self


class DescribeHostAvailabilityListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        total: int = None,
        task_list: DescribeHostAvailabilityListResponseBodyTaskList = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.total = total
        self.task_list = task_list
        self.code = code
        self.success = success

    def validate(self):
        if self.task_list:
            self.task_list.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.task_list is not None:
            result['TaskList'] = self.task_list.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('TaskList') is not None:
            temp_model = DescribeHostAvailabilityListResponseBodyTaskList()
            self.task_list = temp_model.from_map(m['TaskList'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeHostAvailabilityListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeHostAvailabilityListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeHostAvailabilityListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeLogMonitorAttributeRequest(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
    ):
        self.metric_name = metric_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        return self


class DescribeLogMonitorAttributeResponseBodyLogMonitorValueFilter(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
        operator: str = None,
    ):
        self.key = key
        self.value = value
        self.operator = operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        if self.operator is not None:
            result['Operator'] = self.operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        return self


class DescribeLogMonitorAttributeResponseBodyLogMonitorAggregates(TeaModel):
    def __init__(
        self,
        max: str = None,
        field_name: str = None,
        min: str = None,
        function: str = None,
        alias: str = None,
    ):
        self.max = max
        self.field_name = field_name
        self.min = min
        self.function = function
        self.alias = alias

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.max is not None:
            result['Max'] = self.max
        if self.field_name is not None:
            result['FieldName'] = self.field_name
        if self.min is not None:
            result['Min'] = self.min
        if self.function is not None:
            result['Function'] = self.function
        if self.alias is not None:
            result['Alias'] = self.alias
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Max') is not None:
            self.max = m.get('Max')
        if m.get('FieldName') is not None:
            self.field_name = m.get('FieldName')
        if m.get('Min') is not None:
            self.min = m.get('Min')
        if m.get('Function') is not None:
            self.function = m.get('Function')
        if m.get('Alias') is not None:
            self.alias = m.get('Alias')
        return self


class DescribeLogMonitorAttributeResponseBodyLogMonitor(TeaModel):
    def __init__(
        self,
        value_filter_relation: str = None,
        metric_name: str = None,
        value_filter: List[DescribeLogMonitorAttributeResponseBodyLogMonitorValueFilter] = None,
        sls_region_id: str = None,
        sls_logstore: str = None,
        aggregates: List[DescribeLogMonitorAttributeResponseBodyLogMonitorAggregates] = None,
        tumblingwindows: List[str] = None,
        group_id: int = None,
        groupbys: List[str] = None,
        log_id: int = None,
        metric_express: str = None,
        gmt_create: int = None,
        sls_project: str = None,
    ):
        self.value_filter_relation = value_filter_relation
        self.metric_name = metric_name
        self.value_filter = value_filter
        self.sls_region_id = sls_region_id
        self.sls_logstore = sls_logstore
        self.aggregates = aggregates
        self.tumblingwindows = tumblingwindows
        self.group_id = group_id
        self.groupbys = groupbys
        self.log_id = log_id
        self.metric_express = metric_express
        self.gmt_create = gmt_create
        self.sls_project = sls_project

    def validate(self):
        if self.value_filter:
            for k in self.value_filter:
                if k:
                    k.validate()
        if self.aggregates:
            for k in self.aggregates:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.value_filter_relation is not None:
            result['ValueFilterRelation'] = self.value_filter_relation
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        result['ValueFilter'] = []
        if self.value_filter is not None:
            for k in self.value_filter:
                result['ValueFilter'].append(k.to_map() if k else None)
        if self.sls_region_id is not None:
            result['SlsRegionId'] = self.sls_region_id
        if self.sls_logstore is not None:
            result['SlsLogstore'] = self.sls_logstore
        result['Aggregates'] = []
        if self.aggregates is not None:
            for k in self.aggregates:
                result['Aggregates'].append(k.to_map() if k else None)
        if self.tumblingwindows is not None:
            result['Tumblingwindows'] = self.tumblingwindows
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.groupbys is not None:
            result['Groupbys'] = self.groupbys
        if self.log_id is not None:
            result['LogId'] = self.log_id
        if self.metric_express is not None:
            result['MetricExpress'] = self.metric_express
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.sls_project is not None:
            result['SlsProject'] = self.sls_project
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ValueFilterRelation') is not None:
            self.value_filter_relation = m.get('ValueFilterRelation')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        self.value_filter = []
        if m.get('ValueFilter') is not None:
            for k in m.get('ValueFilter'):
                temp_model = DescribeLogMonitorAttributeResponseBodyLogMonitorValueFilter()
                self.value_filter.append(temp_model.from_map(k))
        if m.get('SlsRegionId') is not None:
            self.sls_region_id = m.get('SlsRegionId')
        if m.get('SlsLogstore') is not None:
            self.sls_logstore = m.get('SlsLogstore')
        self.aggregates = []
        if m.get('Aggregates') is not None:
            for k in m.get('Aggregates'):
                temp_model = DescribeLogMonitorAttributeResponseBodyLogMonitorAggregates()
                self.aggregates.append(temp_model.from_map(k))
        if m.get('Tumblingwindows') is not None:
            self.tumblingwindows = m.get('Tumblingwindows')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Groupbys') is not None:
            self.groupbys = m.get('Groupbys')
        if m.get('LogId') is not None:
            self.log_id = m.get('LogId')
        if m.get('MetricExpress') is not None:
            self.metric_express = m.get('MetricExpress')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('SlsProject') is not None:
            self.sls_project = m.get('SlsProject')
        return self


class DescribeLogMonitorAttributeResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        log_monitor: DescribeLogMonitorAttributeResponseBodyLogMonitor = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.log_monitor = log_monitor
        self.code = code
        self.success = success

    def validate(self):
        if self.log_monitor:
            self.log_monitor.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.log_monitor is not None:
            result['LogMonitor'] = self.log_monitor.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('LogMonitor') is not None:
            temp_model = DescribeLogMonitorAttributeResponseBodyLogMonitor()
            self.log_monitor = temp_model.from_map(m['LogMonitor'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeLogMonitorAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeLogMonitorAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeLogMonitorAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeLogMonitorListRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
        search_value: str = None,
        group_id: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.search_value = search_value
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search_value is not None:
            result['SearchValue'] = self.search_value
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SearchValue') is not None:
            self.search_value = m.get('SearchValue')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DescribeLogMonitorListResponseBodyLogMonitorListValueFilter(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
        operator: str = None,
    ):
        self.key = key
        self.value = value
        self.operator = operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        if self.operator is not None:
            result['Operator'] = self.operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        return self


class DescribeLogMonitorListResponseBodyLogMonitorList(TeaModel):
    def __init__(
        self,
        value_filter_relation: str = None,
        sls_logstore: str = None,
        metric_name: str = None,
        value_filter: List[DescribeLogMonitorListResponseBodyLogMonitorListValueFilter] = None,
        group_id: int = None,
        log_id: int = None,
        sls_region_id: str = None,
        gmt_create: int = None,
        sls_project: str = None,
    ):
        self.value_filter_relation = value_filter_relation
        self.sls_logstore = sls_logstore
        self.metric_name = metric_name
        self.value_filter = value_filter
        self.group_id = group_id
        self.log_id = log_id
        self.sls_region_id = sls_region_id
        self.gmt_create = gmt_create
        self.sls_project = sls_project

    def validate(self):
        if self.value_filter:
            for k in self.value_filter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.value_filter_relation is not None:
            result['ValueFilterRelation'] = self.value_filter_relation
        if self.sls_logstore is not None:
            result['SlsLogstore'] = self.sls_logstore
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        result['ValueFilter'] = []
        if self.value_filter is not None:
            for k in self.value_filter:
                result['ValueFilter'].append(k.to_map() if k else None)
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.log_id is not None:
            result['LogId'] = self.log_id
        if self.sls_region_id is not None:
            result['SlsRegionId'] = self.sls_region_id
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.sls_project is not None:
            result['SlsProject'] = self.sls_project
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ValueFilterRelation') is not None:
            self.value_filter_relation = m.get('ValueFilterRelation')
        if m.get('SlsLogstore') is not None:
            self.sls_logstore = m.get('SlsLogstore')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        self.value_filter = []
        if m.get('ValueFilter') is not None:
            for k in m.get('ValueFilter'):
                temp_model = DescribeLogMonitorListResponseBodyLogMonitorListValueFilter()
                self.value_filter.append(temp_model.from_map(k))
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('LogId') is not None:
            self.log_id = m.get('LogId')
        if m.get('SlsRegionId') is not None:
            self.sls_region_id = m.get('SlsRegionId')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('SlsProject') is not None:
            self.sls_project = m.get('SlsProject')
        return self


class DescribeLogMonitorListResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        total: int = None,
        log_monitor_list: List[DescribeLogMonitorListResponseBodyLogMonitorList] = None,
        code: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.log_monitor_list = log_monitor_list
        self.code = code
        self.success = success

    def validate(self):
        if self.log_monitor_list:
            for k in self.log_monitor_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        result['LogMonitorList'] = []
        if self.log_monitor_list is not None:
            for k in self.log_monitor_list:
                result['LogMonitorList'].append(k.to_map() if k else None)
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        self.log_monitor_list = []
        if m.get('LogMonitorList') is not None:
            for k in m.get('LogMonitorList'):
                temp_model = DescribeLogMonitorListResponseBodyLogMonitorList()
                self.log_monitor_list.append(temp_model.from_map(k))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeLogMonitorListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeLogMonitorListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeLogMonitorListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricDataRequest(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        metric_name: str = None,
        period: str = None,
        start_time: str = None,
        end_time: str = None,
        dimensions: str = None,
        express: str = None,
        length: str = None,
    ):
        self.namespace = namespace
        self.metric_name = metric_name
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions
        self.express = express
        self.length = length

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.period is not None:
            result['Period'] = self.period
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.express is not None:
            result['Express'] = self.express
        if self.length is not None:
            result['Length'] = self.length
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('Express') is not None:
            self.express = m.get('Express')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        return self


class DescribeMetricDataResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        period: str = None,
        datapoints: str = None,
        code: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.period = period
        self.datapoints = datapoints
        self.code = code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.period is not None:
            result['Period'] = self.period
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints
        if self.code is not None:
            result['Code'] = self.code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Datapoints') is not None:
            self.datapoints = m.get('Datapoints')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        return self


class DescribeMetricDataResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricDataResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricDataResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricLastRequest(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        metric_name: str = None,
        period: str = None,
        start_time: str = None,
        end_time: str = None,
        dimensions: str = None,
        next_token: str = None,
        length: str = None,
        express: str = None,
    ):
        self.namespace = namespace
        self.metric_name = metric_name
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions
        self.next_token = next_token
        self.length = length
        self.express = express

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.period is not None:
            result['Period'] = self.period
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.length is not None:
            result['Length'] = self.length
        if self.express is not None:
            result['Express'] = self.express
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        if m.get('Express') is not None:
            self.express = m.get('Express')
        return self


class DescribeMetricLastResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        message: str = None,
        period: str = None,
        datapoints: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.message = message
        self.period = period
        self.datapoints = datapoints
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.period is not None:
            result['Period'] = self.period
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Datapoints') is not None:
            self.datapoints = m.get('Datapoints')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricLastResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricLastResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricLastResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricListRequest(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        metric_name: str = None,
        period: str = None,
        start_time: str = None,
        end_time: str = None,
        dimensions: str = None,
        next_token: str = None,
        length: str = None,
        express: str = None,
    ):
        self.namespace = namespace
        self.metric_name = metric_name
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions
        self.next_token = next_token
        self.length = length
        self.express = express

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.period is not None:
            result['Period'] = self.period
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.length is not None:
            result['Length'] = self.length
        if self.express is not None:
            result['Express'] = self.express
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        if m.get('Express') is not None:
            self.express = m.get('Express')
        return self


class DescribeMetricListResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        message: str = None,
        period: str = None,
        datapoints: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.message = message
        self.period = period
        self.datapoints = datapoints
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.period is not None:
            result['Period'] = self.period
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Datapoints') is not None:
            self.datapoints = m.get('Datapoints')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricMetaListRequest(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        labels: str = None,
        metric_name: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.namespace = namespace
        self.labels = labels
        self.metric_name = metric_name
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeMetricMetaListResponseBodyResourcesResource(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        description: str = None,
        labels: str = None,
        unit: str = None,
        dimensions: str = None,
        namespace: str = None,
        periods: str = None,
        statistics: str = None,
    ):
        self.metric_name = metric_name
        self.description = description
        self.labels = labels
        self.unit = unit
        self.dimensions = dimensions
        self.namespace = namespace
        self.periods = periods
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.description is not None:
            result['Description'] = self.description
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.unit is not None:
            result['Unit'] = self.unit
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.periods is not None:
            result['Periods'] = self.periods
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('Unit') is not None:
            self.unit = m.get('Unit')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Periods') is not None:
            self.periods = m.get('Periods')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricMetaListResponseBodyResources(TeaModel):
    def __init__(
        self,
        resource: List[DescribeMetricMetaListResponseBodyResourcesResource] = None,
    ):
        self.resource = resource

    def validate(self):
        if self.resource:
            for k in self.resource:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resource'] = []
        if self.resource is not None:
            for k in self.resource:
                result['Resource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.resource = []
        if m.get('Resource') is not None:
            for k in m.get('Resource'):
                temp_model = DescribeMetricMetaListResponseBodyResourcesResource()
                self.resource.append(temp_model.from_map(k))
        return self


class DescribeMetricMetaListResponseBody(TeaModel):
    def __init__(
        self,
        total_count: str = None,
        message: str = None,
        request_id: str = None,
        resources: DescribeMetricMetaListResponseBodyResources = None,
        code: str = None,
        success: bool = None,
    ):
        self.total_count = total_count
        self.message = message
        self.request_id = request_id
        self.resources = resources
        self.code = code
        self.success = success

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Resources') is not None:
            temp_model = DescribeMetricMetaListResponseBodyResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricMetaListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricMetaListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricMetaListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricRuleCountRequest(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        metric_name: str = None,
    ):
        self.namespace = namespace
        self.metric_name = metric_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        return self


class DescribeMetricRuleCountResponseBodyMetricRuleCount(TeaModel):
    def __init__(
        self,
        ok: int = None,
        nodata: int = None,
        disable: int = None,
        total: int = None,
        alarm: int = None,
    ):
        self.ok = ok
        self.nodata = nodata
        self.disable = disable
        self.total = total
        self.alarm = alarm

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ok is not None:
            result['Ok'] = self.ok
        if self.nodata is not None:
            result['Nodata'] = self.nodata
        if self.disable is not None:
            result['Disable'] = self.disable
        if self.total is not None:
            result['Total'] = self.total
        if self.alarm is not None:
            result['Alarm'] = self.alarm
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ok') is not None:
            self.ok = m.get('Ok')
        if m.get('Nodata') is not None:
            self.nodata = m.get('Nodata')
        if m.get('Disable') is not None:
            self.disable = m.get('Disable')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Alarm') is not None:
            self.alarm = m.get('Alarm')
        return self


class DescribeMetricRuleCountResponseBody(TeaModel):
    def __init__(
        self,
        metric_rule_count: DescribeMetricRuleCountResponseBodyMetricRuleCount = None,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.metric_rule_count = metric_rule_count
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        if self.metric_rule_count:
            self.metric_rule_count.validate()

    def to_map(self):
        result = dict()
        if self.metric_rule_count is not None:
            result['MetricRuleCount'] = self.metric_rule_count.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricRuleCount') is not None:
            temp_model = DescribeMetricRuleCountResponseBodyMetricRuleCount()
            self.metric_rule_count = temp_model.from_map(m['MetricRuleCount'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricRuleCountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricRuleCountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricRuleCountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricRuleListRequest(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        enable_state: bool = None,
        namespace: str = None,
        page: int = None,
        page_size: int = None,
        alert_state: str = None,
        dimensions: str = None,
        rule_name: str = None,
        group_id: str = None,
        rule_ids: str = None,
    ):
        self.metric_name = metric_name
        self.enable_state = enable_state
        self.namespace = namespace
        self.page = page
        self.page_size = page_size
        self.alert_state = alert_state
        self.dimensions = dimensions
        self.rule_name = rule_name
        self.group_id = group_id
        self.rule_ids = rule_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.enable_state is not None:
            result['EnableState'] = self.enable_state
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.page is not None:
            result['Page'] = self.page
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.alert_state is not None:
            result['AlertState'] = self.alert_state
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.rule_ids is not None:
            result['RuleIds'] = self.rule_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('EnableState') is not None:
            self.enable_state = m.get('EnableState')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Page') is not None:
            self.page = m.get('Page')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('AlertState') is not None:
            self.alert_state = m.get('AlertState')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('RuleIds') is not None:
            self.rule_ids = m.get('RuleIds')
        return self


class DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsCritical(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        pre_condition: str = None,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.pre_condition = pre_condition
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.pre_condition is not None:
            result['PreCondition'] = self.pre_condition
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('PreCondition') is not None:
            self.pre_condition = m.get('PreCondition')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsInfo(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        pre_condition: str = None,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.pre_condition = pre_condition
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.pre_condition is not None:
            result['PreCondition'] = self.pre_condition
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('PreCondition') is not None:
            self.pre_condition = m.get('PreCondition')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsWarn(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        pre_condition: str = None,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.pre_condition = pre_condition
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.pre_condition is not None:
            result['PreCondition'] = self.pre_condition
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('PreCondition') is not None:
            self.pre_condition = m.get('PreCondition')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricRuleListResponseBodyAlarmsAlarmEscalations(TeaModel):
    def __init__(
        self,
        critical: DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsCritical = None,
        info: DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsInfo = None,
        warn: DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsWarn = None,
    ):
        self.critical = critical
        self.info = info
        self.warn = warn

    def validate(self):
        if self.critical:
            self.critical.validate()
        if self.info:
            self.info.validate()
        if self.warn:
            self.warn.validate()

    def to_map(self):
        result = dict()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Critical') is not None:
            temp_model = DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        if m.get('Info') is not None:
            temp_model = DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = DescribeMetricRuleListResponseBodyAlarmsAlarmEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        return self


class DescribeMetricRuleListResponseBodyAlarmsAlarm(TeaModel):
    def __init__(
        self,
        silence_time: int = None,
        metric_name: str = None,
        webhook: str = None,
        escalations: DescribeMetricRuleListResponseBodyAlarmsAlarmEscalations = None,
        contact_groups: str = None,
        source_type: str = None,
        namespace: str = None,
        effective_interval: str = None,
        no_effective_interval: str = None,
        mail_subject: str = None,
        rule_name: str = None,
        alert_state: str = None,
        rule_id: str = None,
        period: str = None,
        group_name: str = None,
        group_id: str = None,
        dimensions: str = None,
        enable_state: bool = None,
        resources: str = None,
    ):
        self.silence_time = silence_time
        self.metric_name = metric_name
        self.webhook = webhook
        self.escalations = escalations
        self.contact_groups = contact_groups
        self.source_type = source_type
        self.namespace = namespace
        self.effective_interval = effective_interval
        self.no_effective_interval = no_effective_interval
        self.mail_subject = mail_subject
        self.rule_name = rule_name
        self.alert_state = alert_state
        self.rule_id = rule_id
        self.period = period
        self.group_name = group_name
        self.group_id = group_id
        self.dimensions = dimensions
        self.enable_state = enable_state
        self.resources = resources

    def validate(self):
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.mail_subject is not None:
            result['MailSubject'] = self.mail_subject
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.alert_state is not None:
            result['AlertState'] = self.alert_state
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.period is not None:
            result['Period'] = self.period
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.enable_state is not None:
            result['EnableState'] = self.enable_state
        if self.resources is not None:
            result['Resources'] = self.resources
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Escalations') is not None:
            temp_model = DescribeMetricRuleListResponseBodyAlarmsAlarmEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('MailSubject') is not None:
            self.mail_subject = m.get('MailSubject')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('AlertState') is not None:
            self.alert_state = m.get('AlertState')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('EnableState') is not None:
            self.enable_state = m.get('EnableState')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        return self


class DescribeMetricRuleListResponseBodyAlarms(TeaModel):
    def __init__(
        self,
        alarm: List[DescribeMetricRuleListResponseBodyAlarmsAlarm] = None,
    ):
        self.alarm = alarm

    def validate(self):
        if self.alarm:
            for k in self.alarm:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Alarm'] = []
        if self.alarm is not None:
            for k in self.alarm:
                result['Alarm'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alarm = []
        if m.get('Alarm') is not None:
            for k in m.get('Alarm'):
                temp_model = DescribeMetricRuleListResponseBodyAlarmsAlarm()
                self.alarm.append(temp_model.from_map(k))
        return self


class DescribeMetricRuleListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        total: str = None,
        alarms: DescribeMetricRuleListResponseBodyAlarms = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.total = total
        self.alarms = alarms
        self.code = code
        self.success = success

    def validate(self):
        if self.alarms:
            self.alarms.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.alarms is not None:
            result['Alarms'] = self.alarms.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Alarms') is not None:
            temp_model = DescribeMetricRuleListResponseBodyAlarms()
            self.alarms = temp_model.from_map(m['Alarms'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricRuleListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricRuleListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricRuleListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricRuleTargetsRequest(TeaModel):
    def __init__(
        self,
        rule_id: str = None,
    ):
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class DescribeMetricRuleTargetsResponseBodyTargetsTarget(TeaModel):
    def __init__(
        self,
        id: str = None,
        arn: str = None,
        level: str = None,
    ):
        self.id = id
        self.arn = arn
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        if self.arn is not None:
            result['Arn'] = self.arn
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Arn') is not None:
            self.arn = m.get('Arn')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class DescribeMetricRuleTargetsResponseBodyTargets(TeaModel):
    def __init__(
        self,
        target: List[DescribeMetricRuleTargetsResponseBodyTargetsTarget] = None,
    ):
        self.target = target

    def validate(self):
        if self.target:
            for k in self.target:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Target'] = []
        if self.target is not None:
            for k in self.target:
                result['Target'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.target = []
        if m.get('Target') is not None:
            for k in m.get('Target'):
                temp_model = DescribeMetricRuleTargetsResponseBodyTargetsTarget()
                self.target.append(temp_model.from_map(k))
        return self


class DescribeMetricRuleTargetsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        targets: DescribeMetricRuleTargetsResponseBodyTargets = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.targets = targets
        self.code = code
        self.success = success

    def validate(self):
        if self.targets:
            self.targets.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.targets is not None:
            result['Targets'] = self.targets.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Targets') is not None:
            temp_model = DescribeMetricRuleTargetsResponseBodyTargets()
            self.targets = temp_model.from_map(m['Targets'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricRuleTargetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricRuleTargetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricRuleTargetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricRuleTemplateAttributeRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        template_id: str = None,
    ):
        self.name = name
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsCritical(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsInfo(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsWarn(TeaModel):
    def __init__(
        self,
        comparison_operator: str = None,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.comparison_operator = comparison_operator
        self.times = times
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalations(TeaModel):
    def __init__(
        self,
        critical: DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsCritical = None,
        info: DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsInfo = None,
        warn: DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsWarn = None,
    ):
        self.critical = critical
        self.info = info
        self.warn = warn

    def validate(self):
        if self.critical:
            self.critical.validate()
        if self.info:
            self.info.validate()
        if self.warn:
            self.warn.validate()

    def to_map(self):
        result = dict()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Critical') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        if m.get('Info') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplate(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        selector: str = None,
        webhook: str = None,
        escalations: DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalations = None,
        namespace: str = None,
        category: str = None,
        rule_name: str = None,
    ):
        self.metric_name = metric_name
        self.selector = selector
        self.webhook = webhook
        self.escalations = escalations
        self.namespace = namespace
        self.category = category
        self.rule_name = rule_name

    def validate(self):
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.selector is not None:
            result['Selector'] = self.selector
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.category is not None:
            result['Category'] = self.category
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Selector') is not None:
            self.selector = m.get('Selector')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Escalations') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplateEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplates(TeaModel):
    def __init__(
        self,
        alert_template: List[DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplate] = None,
    ):
        self.alert_template = alert_template

    def validate(self):
        if self.alert_template:
            for k in self.alert_template:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertTemplate'] = []
        if self.alert_template is not None:
            for k in self.alert_template:
                result['AlertTemplate'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_template = []
        if m.get('AlertTemplate') is not None:
            for k in m.get('AlertTemplate'):
                temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplatesAlertTemplate()
                self.alert_template.append(temp_model.from_map(k))
        return self


class DescribeMetricRuleTemplateAttributeResponseBodyResource(TeaModel):
    def __init__(
        self,
        description: str = None,
        alert_templates: DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplates = None,
        name: str = None,
        rest_version: str = None,
        template_id: str = None,
    ):
        self.description = description
        self.alert_templates = alert_templates
        self.name = name
        self.rest_version = rest_version
        self.template_id = template_id

    def validate(self):
        if self.alert_templates:
            self.alert_templates.validate()

    def to_map(self):
        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.alert_templates is not None:
            result['AlertTemplates'] = self.alert_templates.to_map()
        if self.name is not None:
            result['Name'] = self.name
        if self.rest_version is not None:
            result['RestVersion'] = self.rest_version
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('AlertTemplates') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResourceAlertTemplates()
            self.alert_templates = temp_model.from_map(m['AlertTemplates'])
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RestVersion') is not None:
            self.rest_version = m.get('RestVersion')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DescribeMetricRuleTemplateAttributeResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        resource: DescribeMetricRuleTemplateAttributeResponseBodyResource = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.resource = resource
        self.code = code
        self.success = success

    def validate(self):
        if self.resource:
            self.resource.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource is not None:
            result['Resource'] = self.resource.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Resource') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBodyResource()
            self.resource = temp_model.from_map(m['Resource'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricRuleTemplateAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricRuleTemplateAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricRuleTemplateAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricRuleTemplateListRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        keyword: str = None,
        template_id: int = None,
        page_number: int = None,
        page_size: int = None,
        history: bool = None,
    ):
        self.name = name
        self.keyword = keyword
        self.template_id = template_id
        self.page_number = page_number
        self.page_size = page_size
        self.history = history

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.history is not None:
            result['History'] = self.history
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('History') is not None:
            self.history = m.get('History')
        return self


class DescribeMetricRuleTemplateListResponseBodyTemplatesTemplateApplyHistoriesApplyHistory(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        group_name: str = None,
        apply_time: int = None,
    ):
        self.group_id = group_id
        self.group_name = group_name
        self.apply_time = apply_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.apply_time is not None:
            result['ApplyTime'] = self.apply_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('ApplyTime') is not None:
            self.apply_time = m.get('ApplyTime')
        return self


class DescribeMetricRuleTemplateListResponseBodyTemplatesTemplateApplyHistories(TeaModel):
    def __init__(
        self,
        apply_history: List[DescribeMetricRuleTemplateListResponseBodyTemplatesTemplateApplyHistoriesApplyHistory] = None,
    ):
        self.apply_history = apply_history

    def validate(self):
        if self.apply_history:
            for k in self.apply_history:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ApplyHistory'] = []
        if self.apply_history is not None:
            for k in self.apply_history:
                result['ApplyHistory'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.apply_history = []
        if m.get('ApplyHistory') is not None:
            for k in m.get('ApplyHistory'):
                temp_model = DescribeMetricRuleTemplateListResponseBodyTemplatesTemplateApplyHistoriesApplyHistory()
                self.apply_history.append(temp_model.from_map(k))
        return self


class DescribeMetricRuleTemplateListResponseBodyTemplatesTemplate(TeaModel):
    def __init__(
        self,
        apply_histories: DescribeMetricRuleTemplateListResponseBodyTemplatesTemplateApplyHistories = None,
        description: str = None,
        gmt_create: int = None,
        name: str = None,
        rest_version: int = None,
        gmt_modified: int = None,
        template_id: int = None,
    ):
        self.apply_histories = apply_histories
        self.description = description
        self.gmt_create = gmt_create
        self.name = name
        self.rest_version = rest_version
        self.gmt_modified = gmt_modified
        self.template_id = template_id

    def validate(self):
        if self.apply_histories:
            self.apply_histories.validate()

    def to_map(self):
        result = dict()
        if self.apply_histories is not None:
            result['ApplyHistories'] = self.apply_histories.to_map()
        if self.description is not None:
            result['Description'] = self.description
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.name is not None:
            result['Name'] = self.name
        if self.rest_version is not None:
            result['RestVersion'] = self.rest_version
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ApplyHistories') is not None:
            temp_model = DescribeMetricRuleTemplateListResponseBodyTemplatesTemplateApplyHistories()
            self.apply_histories = temp_model.from_map(m['ApplyHistories'])
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RestVersion') is not None:
            self.rest_version = m.get('RestVersion')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DescribeMetricRuleTemplateListResponseBodyTemplates(TeaModel):
    def __init__(
        self,
        template: List[DescribeMetricRuleTemplateListResponseBodyTemplatesTemplate] = None,
    ):
        self.template = template

    def validate(self):
        if self.template:
            for k in self.template:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Template'] = []
        if self.template is not None:
            for k in self.template:
                result['Template'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.template = []
        if m.get('Template') is not None:
            for k in m.get('Template'):
                temp_model = DescribeMetricRuleTemplateListResponseBodyTemplatesTemplate()
                self.template.append(temp_model.from_map(k))
        return self


class DescribeMetricRuleTemplateListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        total: int = None,
        templates: DescribeMetricRuleTemplateListResponseBodyTemplates = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.total = total
        self.templates = templates
        self.code = code
        self.success = success

    def validate(self):
        if self.templates:
            self.templates.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.templates is not None:
            result['Templates'] = self.templates.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Templates') is not None:
            temp_model = DescribeMetricRuleTemplateListResponseBodyTemplates()
            self.templates = temp_model.from_map(m['Templates'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMetricRuleTemplateListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricRuleTemplateListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricRuleTemplateListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMetricTopRequest(TeaModel):
    def __init__(
        self,
        period: str = None,
        namespace: str = None,
        metric_name: str = None,
        start_time: str = None,
        end_time: str = None,
        dimensions: str = None,
        orderby: str = None,
        order_desc: str = None,
        length: str = None,
        express: str = None,
    ):
        self.period = period
        self.namespace = namespace
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions
        self.orderby = orderby
        self.order_desc = order_desc
        self.length = length
        self.express = express

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.period is not None:
            result['Period'] = self.period
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.orderby is not None:
            result['Orderby'] = self.orderby
        if self.order_desc is not None:
            result['OrderDesc'] = self.order_desc
        if self.length is not None:
            result['Length'] = self.length
        if self.express is not None:
            result['Express'] = self.express
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('Orderby') is not None:
            self.orderby = m.get('Orderby')
        if m.get('OrderDesc') is not None:
            self.order_desc = m.get('OrderDesc')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        if m.get('Express') is not None:
            self.express = m.get('Express')
        return self


class DescribeMetricTopResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        period: str = None,
        datapoints: str = None,
        code: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.period = period
        self.datapoints = datapoints
        self.code = code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.period is not None:
            result['Period'] = self.period
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints
        if self.code is not None:
            result['Code'] = self.code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Datapoints') is not None:
            self.datapoints = m.get('Datapoints')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        return self


class DescribeMetricTopResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMetricTopResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMetricTopResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorGroupCategoriesRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
    ):
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategoriesMonitorGroupCategoryCategoryItem(TeaModel):
    def __init__(
        self,
        category: str = None,
        count: int = None,
    ):
        self.category = category
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.category is not None:
            result['Category'] = self.category
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategoriesMonitorGroupCategory(TeaModel):
    def __init__(
        self,
        category_item: List[DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategoriesMonitorGroupCategoryCategoryItem] = None,
    ):
        self.category_item = category_item

    def validate(self):
        if self.category_item:
            for k in self.category_item:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['CategoryItem'] = []
        if self.category_item is not None:
            for k in self.category_item:
                result['CategoryItem'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.category_item = []
        if m.get('CategoryItem') is not None:
            for k in m.get('CategoryItem'):
                temp_model = DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategoriesMonitorGroupCategoryCategoryItem()
                self.category_item.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategories(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        monitor_group_category: DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategoriesMonitorGroupCategory = None,
    ):
        self.group_id = group_id
        self.monitor_group_category = monitor_group_category

    def validate(self):
        if self.monitor_group_category:
            self.monitor_group_category.validate()

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.monitor_group_category is not None:
            result['MonitorGroupCategory'] = self.monitor_group_category.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('MonitorGroupCategory') is not None:
            temp_model = DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategoriesMonitorGroupCategory()
            self.monitor_group_category = temp_model.from_map(m['MonitorGroupCategory'])
        return self


class DescribeMonitorGroupCategoriesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        monitor_group_categories: DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategories = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.monitor_group_categories = monitor_group_categories
        self.code = code
        self.success = success

    def validate(self):
        if self.monitor_group_categories:
            self.monitor_group_categories.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.monitor_group_categories is not None:
            result['MonitorGroupCategories'] = self.monitor_group_categories.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MonitorGroupCategories') is not None:
            temp_model = DescribeMonitorGroupCategoriesResponseBodyMonitorGroupCategories()
            self.monitor_group_categories = temp_model.from_map(m['MonitorGroupCategories'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitorGroupCategoriesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorGroupCategoriesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorGroupCategoriesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorGroupDynamicRulesRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
    ):
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DescribeMonitorGroupDynamicRulesResponseBodyResourceResourceFiltersFilter(TeaModel):
    def __init__(
        self,
        value: str = None,
        function: str = None,
        name: str = None,
    ):
        self.value = value
        self.function = function
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.function is not None:
            result['Function'] = self.function
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Function') is not None:
            self.function = m.get('Function')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeMonitorGroupDynamicRulesResponseBodyResourceResourceFilters(TeaModel):
    def __init__(
        self,
        filter: List[DescribeMonitorGroupDynamicRulesResponseBodyResourceResourceFiltersFilter] = None,
    ):
        self.filter = filter

    def validate(self):
        if self.filter:
            for k in self.filter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Filter'] = []
        if self.filter is not None:
            for k in self.filter:
                result['Filter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.filter = []
        if m.get('Filter') is not None:
            for k in m.get('Filter'):
                temp_model = DescribeMonitorGroupDynamicRulesResponseBodyResourceResourceFiltersFilter()
                self.filter.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupDynamicRulesResponseBodyResourceResource(TeaModel):
    def __init__(
        self,
        filter_relation: str = None,
        filters: DescribeMonitorGroupDynamicRulesResponseBodyResourceResourceFilters = None,
        category: str = None,
    ):
        self.filter_relation = filter_relation
        self.filters = filters
        self.category = category

    def validate(self):
        if self.filters:
            self.filters.validate()

    def to_map(self):
        result = dict()
        if self.filter_relation is not None:
            result['FilterRelation'] = self.filter_relation
        if self.filters is not None:
            result['Filters'] = self.filters.to_map()
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FilterRelation') is not None:
            self.filter_relation = m.get('FilterRelation')
        if m.get('Filters') is not None:
            temp_model = DescribeMonitorGroupDynamicRulesResponseBodyResourceResourceFilters()
            self.filters = temp_model.from_map(m['Filters'])
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class DescribeMonitorGroupDynamicRulesResponseBodyResource(TeaModel):
    def __init__(
        self,
        resource: List[DescribeMonitorGroupDynamicRulesResponseBodyResourceResource] = None,
    ):
        self.resource = resource

    def validate(self):
        if self.resource:
            for k in self.resource:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resource'] = []
        if self.resource is not None:
            for k in self.resource:
                result['Resource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.resource = []
        if m.get('Resource') is not None:
            for k in m.get('Resource'):
                temp_model = DescribeMonitorGroupDynamicRulesResponseBodyResourceResource()
                self.resource.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupDynamicRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        resource: DescribeMonitorGroupDynamicRulesResponseBodyResource = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.resource = resource
        self.code = code
        self.success = success

    def validate(self):
        if self.resource:
            self.resource.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource is not None:
            result['Resource'] = self.resource.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Resource') is not None:
            temp_model = DescribeMonitorGroupDynamicRulesResponseBodyResource()
            self.resource = temp_model.from_map(m['Resource'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitorGroupDynamicRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorGroupDynamicRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorGroupDynamicRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorGroupInstanceAttributeRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        page_number: int = None,
        page_size: int = None,
        total: bool = None,
        category: str = None,
        keyword: str = None,
        instance_ids: str = None,
    ):
        self.group_id = group_id
        self.page_number = page_number
        self.page_size = page_size
        self.total = total
        self.category = category
        self.keyword = keyword
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total is not None:
            result['Total'] = self.total
        if self.category is not None:
            result['Category'] = self.category
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceRegion(TeaModel):
    def __init__(
        self,
        availability_zone: str = None,
        region_id: str = None,
    ):
        self.availability_zone = availability_zone
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.availability_zone is not None:
            result['AvailabilityZone'] = self.availability_zone
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AvailabilityZone') is not None:
            self.availability_zone = m.get('AvailabilityZone')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceVpc(TeaModel):
    def __init__(
        self,
        vswitch_instance_id: str = None,
        vpc_instance_id: str = None,
    ):
        self.vswitch_instance_id = vswitch_instance_id
        self.vpc_instance_id = vpc_instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.vswitch_instance_id is not None:
            result['VswitchInstanceId'] = self.vswitch_instance_id
        if self.vpc_instance_id is not None:
            result['VpcInstanceId'] = self.vpc_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VswitchInstanceId') is not None:
            self.vswitch_instance_id = m.get('VswitchInstanceId')
        if m.get('VpcInstanceId') is not None:
            self.vpc_instance_id = m.get('VpcInstanceId')
        return self


class DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceTagsTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceTags(TeaModel):
    def __init__(
        self,
        tag: List[DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceTagsTag] = None,
    ):
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceTagsTag()
                self.tag.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResource(TeaModel):
    def __init__(
        self,
        instance_name: str = None,
        region: DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceRegion = None,
        vpc: DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceVpc = None,
        dimension: str = None,
        tags: DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceTags = None,
        category: str = None,
        instance_id: str = None,
        network_type: str = None,
        desc: str = None,
    ):
        self.instance_name = instance_name
        self.region = region
        self.vpc = vpc
        self.dimension = dimension
        self.tags = tags
        self.category = category
        self.instance_id = instance_id
        self.network_type = network_type
        self.desc = desc

    def validate(self):
        if self.region:
            self.region.validate()
        if self.vpc:
            self.vpc.validate()
        if self.tags:
            self.tags.validate()

    def to_map(self):
        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.region is not None:
            result['Region'] = self.region.to_map()
        if self.vpc is not None:
            result['Vpc'] = self.vpc.to_map()
        if self.dimension is not None:
            result['Dimension'] = self.dimension
        if self.tags is not None:
            result['Tags'] = self.tags.to_map()
        if self.category is not None:
            result['Category'] = self.category
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.desc is not None:
            result['Desc'] = self.desc
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Region') is not None:
            temp_model = DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceRegion()
            self.region = temp_model.from_map(m['Region'])
        if m.get('Vpc') is not None:
            temp_model = DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceVpc()
            self.vpc = temp_model.from_map(m['Vpc'])
        if m.get('Dimension') is not None:
            self.dimension = m.get('Dimension')
        if m.get('Tags') is not None:
            temp_model = DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResourceTags()
            self.tags = temp_model.from_map(m['Tags'])
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('Desc') is not None:
            self.desc = m.get('Desc')
        return self


class DescribeMonitorGroupInstanceAttributeResponseBodyResources(TeaModel):
    def __init__(
        self,
        resource: List[DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResource] = None,
    ):
        self.resource = resource

    def validate(self):
        if self.resource:
            for k in self.resource:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resource'] = []
        if self.resource is not None:
            for k in self.resource:
                result['Resource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.resource = []
        if m.get('Resource') is not None:
            for k in m.get('Resource'):
                temp_model = DescribeMonitorGroupInstanceAttributeResponseBodyResourcesResource()
                self.resource.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupInstanceAttributeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        total: int = None,
        resources: DescribeMonitorGroupInstanceAttributeResponseBodyResources = None,
        code: int = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.resources = resources
        self.code = code
        self.success = success

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Resources') is not None:
            temp_model = DescribeMonitorGroupInstanceAttributeResponseBodyResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitorGroupInstanceAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorGroupInstanceAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorGroupInstanceAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorGroupInstancesRequest(TeaModel):
    def __init__(
        self,
        page_size: int = None,
        page_number: int = None,
        group_id: int = None,
        category: str = None,
        keyword: str = None,
        instance_ids: str = None,
    ):
        self.page_size = page_size
        self.page_number = page_number
        self.group_id = group_id
        self.category = category
        self.keyword = keyword
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.category is not None:
            result['Category'] = self.category
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class DescribeMonitorGroupInstancesResponseBodyResourcesResource(TeaModel):
    def __init__(
        self,
        instance_name: str = None,
        category: str = None,
        instance_id: str = None,
        id: int = None,
        region_id: str = None,
    ):
        self.instance_name = instance_name
        self.category = category
        self.instance_id = instance_id
        self.id = id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.category is not None:
            result['Category'] = self.category
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.id is not None:
            result['Id'] = self.id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeMonitorGroupInstancesResponseBodyResources(TeaModel):
    def __init__(
        self,
        resource: List[DescribeMonitorGroupInstancesResponseBodyResourcesResource] = None,
    ):
        self.resource = resource

    def validate(self):
        if self.resource:
            for k in self.resource:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resource'] = []
        if self.resource is not None:
            for k in self.resource:
                result['Resource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.resource = []
        if m.get('Resource') is not None:
            for k in m.get('Resource'):
                temp_model = DescribeMonitorGroupInstancesResponseBodyResourcesResource()
                self.resource.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupInstancesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        total: int = None,
        resources: DescribeMonitorGroupInstancesResponseBodyResources = None,
        code: int = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.resources = resources
        self.code = code
        self.success = success

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Resources') is not None:
            temp_model = DescribeMonitorGroupInstancesResponseBodyResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitorGroupInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorGroupInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorGroupInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorGroupNotifyPolicyListRequest(TeaModel):
    def __init__(
        self,
        policy_type: str = None,
        page_number: int = None,
        page_size: int = None,
        group_id: str = None,
    ):
        self.policy_type = policy_type
        self.page_number = page_number
        self.page_size = page_size
        self.group_id = group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.policy_type is not None:
            result['PolicyType'] = self.policy_type
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PolicyType') is not None:
            self.policy_type = m.get('PolicyType')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        return self


class DescribeMonitorGroupNotifyPolicyListResponseBodyNotifyPolicyListNotifyPolicy(TeaModel):
    def __init__(
        self,
        end_time: int = None,
        type: str = None,
        start_time: int = None,
        group_id: str = None,
        id: str = None,
    ):
        self.end_time = end_time
        self.type = type
        self.start_time = start_time
        self.group_id = group_id
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.type is not None:
            result['Type'] = self.type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeMonitorGroupNotifyPolicyListResponseBodyNotifyPolicyList(TeaModel):
    def __init__(
        self,
        notify_policy: List[DescribeMonitorGroupNotifyPolicyListResponseBodyNotifyPolicyListNotifyPolicy] = None,
    ):
        self.notify_policy = notify_policy

    def validate(self):
        if self.notify_policy:
            for k in self.notify_policy:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['NotifyPolicy'] = []
        if self.notify_policy is not None:
            for k in self.notify_policy:
                result['NotifyPolicy'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.notify_policy = []
        if m.get('NotifyPolicy') is not None:
            for k in m.get('NotifyPolicy'):
                temp_model = DescribeMonitorGroupNotifyPolicyListResponseBodyNotifyPolicyListNotifyPolicy()
                self.notify_policy.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupNotifyPolicyListResponseBody(TeaModel):
    def __init__(
        self,
        notify_policy_list: DescribeMonitorGroupNotifyPolicyListResponseBodyNotifyPolicyList = None,
        message: str = None,
        request_id: str = None,
        total: int = None,
        code: str = None,
        success: str = None,
    ):
        self.notify_policy_list = notify_policy_list
        self.message = message
        self.request_id = request_id
        self.total = total
        self.code = code
        self.success = success

    def validate(self):
        if self.notify_policy_list:
            self.notify_policy_list.validate()

    def to_map(self):
        result = dict()
        if self.notify_policy_list is not None:
            result['NotifyPolicyList'] = self.notify_policy_list.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NotifyPolicyList') is not None:
            temp_model = DescribeMonitorGroupNotifyPolicyListResponseBodyNotifyPolicyList()
            self.notify_policy_list = temp_model.from_map(m['NotifyPolicyList'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitorGroupNotifyPolicyListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorGroupNotifyPolicyListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorGroupNotifyPolicyListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorGroupsRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeMonitorGroupsRequest(TeaModel):
    def __init__(
        self,
        select_contact_groups: bool = None,
        page_number: int = None,
        page_size: int = None,
        keyword: str = None,
        instance_id: str = None,
        group_name: str = None,
        include_template_history: bool = None,
        type: str = None,
        dynamic_tag_rule_id: str = None,
        group_id: str = None,
        service_id: str = None,
        resource_group_id: str = None,
        tag: List[DescribeMonitorGroupsRequestTag] = None,
    ):
        self.select_contact_groups = select_contact_groups
        self.page_number = page_number
        self.page_size = page_size
        self.keyword = keyword
        self.instance_id = instance_id
        self.group_name = group_name
        self.include_template_history = include_template_history
        self.type = type
        self.dynamic_tag_rule_id = dynamic_tag_rule_id
        self.group_id = group_id
        self.service_id = service_id
        self.resource_group_id = resource_group_id
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.select_contact_groups is not None:
            result['SelectContactGroups'] = self.select_contact_groups
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.include_template_history is not None:
            result['IncludeTemplateHistory'] = self.include_template_history
        if self.type is not None:
            result['Type'] = self.type
        if self.dynamic_tag_rule_id is not None:
            result['DynamicTagRuleId'] = self.dynamic_tag_rule_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.service_id is not None:
            result['ServiceId'] = self.service_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SelectContactGroups') is not None:
            self.select_contact_groups = m.get('SelectContactGroups')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IncludeTemplateHistory') is not None:
            self.include_template_history = m.get('IncludeTemplateHistory')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('DynamicTagRuleId') is not None:
            self.dynamic_tag_rule_id = m.get('DynamicTagRuleId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('ServiceId') is not None:
            self.service_id = m.get('ServiceId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = DescribeMonitorGroupsRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupsResponseBodyResourcesResourceContactGroupsContactGroup(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeMonitorGroupsResponseBodyResourcesResourceContactGroups(TeaModel):
    def __init__(
        self,
        contact_group: List[DescribeMonitorGroupsResponseBodyResourcesResourceContactGroupsContactGroup] = None,
    ):
        self.contact_group = contact_group

    def validate(self):
        if self.contact_group:
            for k in self.contact_group:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContactGroup'] = []
        if self.contact_group is not None:
            for k in self.contact_group:
                result['ContactGroup'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact_group = []
        if m.get('ContactGroup') is not None:
            for k in m.get('ContactGroup'):
                temp_model = DescribeMonitorGroupsResponseBodyResourcesResourceContactGroupsContactGroup()
                self.contact_group.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupsResponseBodyResourcesResourceTagsTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeMonitorGroupsResponseBodyResourcesResourceTags(TeaModel):
    def __init__(
        self,
        tag: List[DescribeMonitorGroupsResponseBodyResourcesResourceTagsTag] = None,
    ):
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = DescribeMonitorGroupsResponseBodyResourcesResourceTagsTag()
                self.tag.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupsResponseBodyResourcesResourceTemplateIds(TeaModel):
    def __init__(
        self,
        template_id: List[str] = None,
    ):
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DescribeMonitorGroupsResponseBodyResourcesResource(TeaModel):
    def __init__(
        self,
        type: str = None,
        bind_url: str = None,
        service_id: str = None,
        contact_groups: DescribeMonitorGroupsResponseBodyResourcesResourceContactGroups = None,
        tags: DescribeMonitorGroupsResponseBodyResourcesResourceTags = None,
        group_founder_tag_key: str = None,
        template_ids: DescribeMonitorGroupsResponseBodyResourcesResourceTemplateIds = None,
        gmt_modified: int = None,
        group_founder_tag_value: str = None,
        group_name: str = None,
        group_id: int = None,
        dynamic_tag_rule_id: str = None,
        gmt_create: int = None,
    ):
        self.type = type
        self.bind_url = bind_url
        self.service_id = service_id
        self.contact_groups = contact_groups
        self.tags = tags
        self.group_founder_tag_key = group_founder_tag_key
        self.template_ids = template_ids
        self.gmt_modified = gmt_modified
        self.group_founder_tag_value = group_founder_tag_value
        self.group_name = group_name
        self.group_id = group_id
        self.dynamic_tag_rule_id = dynamic_tag_rule_id
        self.gmt_create = gmt_create

    def validate(self):
        if self.contact_groups:
            self.contact_groups.validate()
        if self.tags:
            self.tags.validate()
        if self.template_ids:
            self.template_ids.validate()

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.bind_url is not None:
            result['BindUrl'] = self.bind_url
        if self.service_id is not None:
            result['ServiceId'] = self.service_id
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups.to_map()
        if self.tags is not None:
            result['Tags'] = self.tags.to_map()
        if self.group_founder_tag_key is not None:
            result['GroupFounderTagKey'] = self.group_founder_tag_key
        if self.template_ids is not None:
            result['TemplateIds'] = self.template_ids.to_map()
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.group_founder_tag_value is not None:
            result['GroupFounderTagValue'] = self.group_founder_tag_value
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.dynamic_tag_rule_id is not None:
            result['DynamicTagRuleId'] = self.dynamic_tag_rule_id
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('BindUrl') is not None:
            self.bind_url = m.get('BindUrl')
        if m.get('ServiceId') is not None:
            self.service_id = m.get('ServiceId')
        if m.get('ContactGroups') is not None:
            temp_model = DescribeMonitorGroupsResponseBodyResourcesResourceContactGroups()
            self.contact_groups = temp_model.from_map(m['ContactGroups'])
        if m.get('Tags') is not None:
            temp_model = DescribeMonitorGroupsResponseBodyResourcesResourceTags()
            self.tags = temp_model.from_map(m['Tags'])
        if m.get('GroupFounderTagKey') is not None:
            self.group_founder_tag_key = m.get('GroupFounderTagKey')
        if m.get('TemplateIds') is not None:
            temp_model = DescribeMonitorGroupsResponseBodyResourcesResourceTemplateIds()
            self.template_ids = temp_model.from_map(m['TemplateIds'])
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('GroupFounderTagValue') is not None:
            self.group_founder_tag_value = m.get('GroupFounderTagValue')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('DynamicTagRuleId') is not None:
            self.dynamic_tag_rule_id = m.get('DynamicTagRuleId')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        return self


class DescribeMonitorGroupsResponseBodyResources(TeaModel):
    def __init__(
        self,
        resource: List[DescribeMonitorGroupsResponseBodyResourcesResource] = None,
    ):
        self.resource = resource

    def validate(self):
        if self.resource:
            for k in self.resource:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resource'] = []
        if self.resource is not None:
            for k in self.resource:
                result['Resource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.resource = []
        if m.get('Resource') is not None:
            for k in m.get('Resource'):
                temp_model = DescribeMonitorGroupsResponseBodyResourcesResource()
                self.resource.append(temp_model.from_map(k))
        return self


class DescribeMonitorGroupsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        total: int = None,
        resources: DescribeMonitorGroupsResponseBodyResources = None,
        code: int = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.resources = resources
        self.code = code
        self.success = success

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Resources') is not None:
            temp_model = DescribeMonitorGroupsResponseBodyResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitorGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorGroupsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitoringAgentAccessKeyResponseBody(TeaModel):
    def __init__(
        self,
        secret_key: str = None,
        request_id: str = None,
        message: str = None,
        access_key: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.secret_key = secret_key
        self.request_id = request_id
        self.message = message
        self.access_key = access_key
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.secret_key is not None:
            result['SecretKey'] = self.secret_key
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.access_key is not None:
            result['AccessKey'] = self.access_key
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SecretKey') is not None:
            self.secret_key = m.get('SecretKey')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('AccessKey') is not None:
            self.access_key = m.get('AccessKey')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitoringAgentAccessKeyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitoringAgentAccessKeyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitoringAgentAccessKeyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitoringAgentConfigResponseBody(TeaModel):
    def __init__(
        self,
        enable_active_alert: str = None,
        auto_install: bool = None,
        enable_install_agent_new_ecs: bool = None,
        request_id: str = None,
        message: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.enable_active_alert = enable_active_alert
        self.auto_install = auto_install
        self.enable_install_agent_new_ecs = enable_install_agent_new_ecs
        self.request_id = request_id
        self.message = message
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.enable_active_alert is not None:
            result['EnableActiveAlert'] = self.enable_active_alert
        if self.auto_install is not None:
            result['AutoInstall'] = self.auto_install
        if self.enable_install_agent_new_ecs is not None:
            result['EnableInstallAgentNewECS'] = self.enable_install_agent_new_ecs
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnableActiveAlert') is not None:
            self.enable_active_alert = m.get('EnableActiveAlert')
        if m.get('AutoInstall') is not None:
            self.auto_install = m.get('AutoInstall')
        if m.get('EnableInstallAgentNewECS') is not None:
            self.enable_install_agent_new_ecs = m.get('EnableInstallAgentNewECS')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitoringAgentConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitoringAgentConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitoringAgentConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitoringAgentHostsRequest(TeaModel):
    def __init__(
        self,
        key_word: str = None,
        host_name: str = None,
        instance_ids: str = None,
        serial_numbers: str = None,
        page_number: int = None,
        page_size: int = None,
        instance_region_id: str = None,
        aliyun_host: bool = None,
        status: str = None,
    ):
        self.key_word = key_word
        self.host_name = host_name
        self.instance_ids = instance_ids
        self.serial_numbers = serial_numbers
        self.page_number = page_number
        self.page_size = page_size
        self.instance_region_id = instance_region_id
        self.aliyun_host = aliyun_host
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key_word is not None:
            result['KeyWord'] = self.key_word
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        if self.serial_numbers is not None:
            result['SerialNumbers'] = self.serial_numbers
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.instance_region_id is not None:
            result['InstanceRegionId'] = self.instance_region_id
        if self.aliyun_host is not None:
            result['AliyunHost'] = self.aliyun_host
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('KeyWord') is not None:
            self.key_word = m.get('KeyWord')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        if m.get('SerialNumbers') is not None:
            self.serial_numbers = m.get('SerialNumbers')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('InstanceRegionId') is not None:
            self.instance_region_id = m.get('InstanceRegionId')
        if m.get('AliyunHost') is not None:
            self.aliyun_host = m.get('AliyunHost')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeMonitoringAgentHostsResponseBodyHostsHost(TeaModel):
    def __init__(
        self,
        serial_number: str = None,
        nat_ip: str = None,
        ali_uid: int = None,
        host_name: str = None,
        instance_id: str = None,
        network_type: str = None,
        is_aliyun_host: bool = None,
        eip_address: str = None,
        agent_version: str = None,
        eip_id: str = None,
        ip_group: str = None,
        region: str = None,
        instance_type_family: str = None,
        operating_system: str = None,
    ):
        self.serial_number = serial_number
        self.nat_ip = nat_ip
        self.ali_uid = ali_uid
        self.host_name = host_name
        self.instance_id = instance_id
        self.network_type = network_type
        self.is_aliyun_host = is_aliyun_host
        self.eip_address = eip_address
        self.agent_version = agent_version
        self.eip_id = eip_id
        self.ip_group = ip_group
        self.region = region
        self.instance_type_family = instance_type_family
        self.operating_system = operating_system

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.serial_number is not None:
            result['SerialNumber'] = self.serial_number
        if self.nat_ip is not None:
            result['NatIp'] = self.nat_ip
        if self.ali_uid is not None:
            result['AliUid'] = self.ali_uid
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.is_aliyun_host is not None:
            result['isAliyunHost'] = self.is_aliyun_host
        if self.eip_address is not None:
            result['EipAddress'] = self.eip_address
        if self.agent_version is not None:
            result['AgentVersion'] = self.agent_version
        if self.eip_id is not None:
            result['EipId'] = self.eip_id
        if self.ip_group is not None:
            result['IpGroup'] = self.ip_group
        if self.region is not None:
            result['Region'] = self.region
        if self.instance_type_family is not None:
            result['InstanceTypeFamily'] = self.instance_type_family
        if self.operating_system is not None:
            result['OperatingSystem'] = self.operating_system
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SerialNumber') is not None:
            self.serial_number = m.get('SerialNumber')
        if m.get('NatIp') is not None:
            self.nat_ip = m.get('NatIp')
        if m.get('AliUid') is not None:
            self.ali_uid = m.get('AliUid')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('isAliyunHost') is not None:
            self.is_aliyun_host = m.get('isAliyunHost')
        if m.get('EipAddress') is not None:
            self.eip_address = m.get('EipAddress')
        if m.get('AgentVersion') is not None:
            self.agent_version = m.get('AgentVersion')
        if m.get('EipId') is not None:
            self.eip_id = m.get('EipId')
        if m.get('IpGroup') is not None:
            self.ip_group = m.get('IpGroup')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('InstanceTypeFamily') is not None:
            self.instance_type_family = m.get('InstanceTypeFamily')
        if m.get('OperatingSystem') is not None:
            self.operating_system = m.get('OperatingSystem')
        return self


class DescribeMonitoringAgentHostsResponseBodyHosts(TeaModel):
    def __init__(
        self,
        host: List[DescribeMonitoringAgentHostsResponseBodyHostsHost] = None,
    ):
        self.host = host

    def validate(self):
        if self.host:
            for k in self.host:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Host'] = []
        if self.host is not None:
            for k in self.host:
                result['Host'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.host = []
        if m.get('Host') is not None:
            for k in m.get('Host'):
                temp_model = DescribeMonitoringAgentHostsResponseBodyHostsHost()
                self.host.append(temp_model.from_map(k))
        return self


class DescribeMonitoringAgentHostsResponseBody(TeaModel):
    def __init__(
        self,
        hosts: DescribeMonitoringAgentHostsResponseBodyHosts = None,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        page_total: int = None,
        total: int = None,
        code: str = None,
        success: bool = None,
    ):
        self.hosts = hosts
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.page_total = page_total
        self.total = total
        self.code = code
        self.success = success

    def validate(self):
        if self.hosts:
            self.hosts.validate()

    def to_map(self):
        result = dict()
        if self.hosts is not None:
            result['Hosts'] = self.hosts.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_total is not None:
            result['PageTotal'] = self.page_total
        if self.total is not None:
            result['Total'] = self.total
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Hosts') is not None:
            temp_model = DescribeMonitoringAgentHostsResponseBodyHosts()
            self.hosts = temp_model.from_map(m['Hosts'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageTotal') is not None:
            self.page_total = m.get('PageTotal')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitoringAgentHostsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitoringAgentHostsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitoringAgentHostsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitoringAgentProcessesRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeMonitoringAgentProcessesResponseBodyNodeProcessesNodeProcess(TeaModel):
    def __init__(
        self,
        process_name: str = None,
        process_id: int = None,
        group_id: str = None,
        command: str = None,
        process_user: str = None,
        instance_id: str = None,
    ):
        self.process_name = process_name
        self.process_id = process_id
        self.group_id = group_id
        self.command = command
        self.process_user = process_user
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.process_name is not None:
            result['ProcessName'] = self.process_name
        if self.process_id is not None:
            result['ProcessId'] = self.process_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.command is not None:
            result['Command'] = self.command
        if self.process_user is not None:
            result['ProcessUser'] = self.process_user
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ProcessName') is not None:
            self.process_name = m.get('ProcessName')
        if m.get('ProcessId') is not None:
            self.process_id = m.get('ProcessId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Command') is not None:
            self.command = m.get('Command')
        if m.get('ProcessUser') is not None:
            self.process_user = m.get('ProcessUser')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeMonitoringAgentProcessesResponseBodyNodeProcesses(TeaModel):
    def __init__(
        self,
        node_process: List[DescribeMonitoringAgentProcessesResponseBodyNodeProcessesNodeProcess] = None,
    ):
        self.node_process = node_process

    def validate(self):
        if self.node_process:
            for k in self.node_process:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['NodeProcess'] = []
        if self.node_process is not None:
            for k in self.node_process:
                result['NodeProcess'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_process = []
        if m.get('NodeProcess') is not None:
            for k in m.get('NodeProcess'):
                temp_model = DescribeMonitoringAgentProcessesResponseBodyNodeProcessesNodeProcess()
                self.node_process.append(temp_model.from_map(k))
        return self


class DescribeMonitoringAgentProcessesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        node_processes: DescribeMonitoringAgentProcessesResponseBodyNodeProcesses = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.node_processes = node_processes
        self.code = code
        self.success = success

    def validate(self):
        if self.node_processes:
            self.node_processes.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.node_processes is not None:
            result['NodeProcesses'] = self.node_processes.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('NodeProcesses') is not None:
            temp_model = DescribeMonitoringAgentProcessesResponseBodyNodeProcesses()
            self.node_processes = temp_model.from_map(m['NodeProcesses'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitoringAgentProcessesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitoringAgentProcessesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitoringAgentProcessesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitoringAgentStatusesRequest(TeaModel):
    def __init__(
        self,
        instance_ids: str = None,
    ):
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class DescribeMonitoringAgentStatusesResponseBodyNodeStatusListNodeStatus(TeaModel):
    def __init__(
        self,
        status: str = None,
        auto_install: bool = None,
        instance_id: str = None,
    ):
        self.status = status
        self.auto_install = auto_install
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.auto_install is not None:
            result['AutoInstall'] = self.auto_install
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('AutoInstall') is not None:
            self.auto_install = m.get('AutoInstall')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeMonitoringAgentStatusesResponseBodyNodeStatusList(TeaModel):
    def __init__(
        self,
        node_status: List[DescribeMonitoringAgentStatusesResponseBodyNodeStatusListNodeStatus] = None,
    ):
        self.node_status = node_status

    def validate(self):
        if self.node_status:
            for k in self.node_status:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['NodeStatus'] = []
        if self.node_status is not None:
            for k in self.node_status:
                result['NodeStatus'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_status = []
        if m.get('NodeStatus') is not None:
            for k in m.get('NodeStatus'):
                temp_model = DescribeMonitoringAgentStatusesResponseBodyNodeStatusListNodeStatus()
                self.node_status.append(temp_model.from_map(k))
        return self


class DescribeMonitoringAgentStatusesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        node_status_list: DescribeMonitoringAgentStatusesResponseBodyNodeStatusList = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.node_status_list = node_status_list
        self.code = code
        self.success = success

    def validate(self):
        if self.node_status_list:
            self.node_status_list.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.node_status_list is not None:
            result['NodeStatusList'] = self.node_status_list.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('NodeStatusList') is not None:
            temp_model = DescribeMonitoringAgentStatusesResponseBodyNodeStatusList()
            self.node_status_list = temp_model.from_map(m['NodeStatusList'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitoringAgentStatusesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitoringAgentStatusesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitoringAgentStatusesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitoringConfigResponseBody(TeaModel):
    def __init__(
        self,
        auto_install: bool = None,
        enable_install_agent_new_ecs: bool = None,
        request_id: str = None,
        message: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.auto_install = auto_install
        self.enable_install_agent_new_ecs = enable_install_agent_new_ecs
        self.request_id = request_id
        self.message = message
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.auto_install is not None:
            result['AutoInstall'] = self.auto_install
        if self.enable_install_agent_new_ecs is not None:
            result['EnableInstallAgentNewECS'] = self.enable_install_agent_new_ecs
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AutoInstall') is not None:
            self.auto_install = m.get('AutoInstall')
        if m.get('EnableInstallAgentNewECS') is not None:
            self.enable_install_agent_new_ecs = m.get('EnableInstallAgentNewECS')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeMonitoringConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitoringConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitoringConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMonitorResourceQuotaAttributeRequest(TeaModel):
    def __init__(
        self,
        show_used: bool = None,
    ):
        self.show_used = show_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.show_used is not None:
            result['ShowUsed'] = self.show_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ShowUsed') is not None:
            self.show_used = m.get('ShowUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaApi(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaCustomMonitor(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaEventMonitor(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorTask(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaPhone(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSMS(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaLogMonitor(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorOperatorProbe(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorEcsProbe(TeaModel):
    def __init__(
        self,
        quota_limit: int = None,
        quota_package: int = None,
        quota_used: int = None,
    ):
        self.quota_limit = quota_limit
        self.quota_package = quota_package
        self.quota_used = quota_used

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.quota_limit is not None:
            result['QuotaLimit'] = self.quota_limit
        if self.quota_package is not None:
            result['QuotaPackage'] = self.quota_package
        if self.quota_used is not None:
            result['QuotaUsed'] = self.quota_used
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuotaLimit') is not None:
            self.quota_limit = m.get('QuotaLimit')
        if m.get('QuotaPackage') is not None:
            self.quota_package = m.get('QuotaPackage')
        if m.get('QuotaUsed') is not None:
            self.quota_used = m.get('QuotaUsed')
        return self


class DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuota(TeaModel):
    def __init__(
        self,
        api: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaApi = None,
        expire_time: str = None,
        custom_monitor: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaCustomMonitor = None,
        event_monitor: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaEventMonitor = None,
        instance_id: str = None,
        site_monitor_task: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorTask = None,
        phone: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaPhone = None,
        suit_info: str = None,
        sms: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSMS = None,
        log_monitor: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaLogMonitor = None,
        site_monitor_operator_probe: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorOperatorProbe = None,
        site_monitor_ecs_probe: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorEcsProbe = None,
    ):
        self.api = api
        self.expire_time = expire_time
        self.custom_monitor = custom_monitor
        self.event_monitor = event_monitor
        self.instance_id = instance_id
        self.site_monitor_task = site_monitor_task
        self.phone = phone
        self.suit_info = suit_info
        self.sms = sms
        self.log_monitor = log_monitor
        self.site_monitor_operator_probe = site_monitor_operator_probe
        self.site_monitor_ecs_probe = site_monitor_ecs_probe

    def validate(self):
        if self.api:
            self.api.validate()
        if self.custom_monitor:
            self.custom_monitor.validate()
        if self.event_monitor:
            self.event_monitor.validate()
        if self.site_monitor_task:
            self.site_monitor_task.validate()
        if self.phone:
            self.phone.validate()
        if self.sms:
            self.sms.validate()
        if self.log_monitor:
            self.log_monitor.validate()
        if self.site_monitor_operator_probe:
            self.site_monitor_operator_probe.validate()
        if self.site_monitor_ecs_probe:
            self.site_monitor_ecs_probe.validate()

    def to_map(self):
        result = dict()
        if self.api is not None:
            result['Api'] = self.api.to_map()
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.custom_monitor is not None:
            result['CustomMonitor'] = self.custom_monitor.to_map()
        if self.event_monitor is not None:
            result['EventMonitor'] = self.event_monitor.to_map()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.site_monitor_task is not None:
            result['SiteMonitorTask'] = self.site_monitor_task.to_map()
        if self.phone is not None:
            result['Phone'] = self.phone.to_map()
        if self.suit_info is not None:
            result['SuitInfo'] = self.suit_info
        if self.sms is not None:
            result['SMS'] = self.sms.to_map()
        if self.log_monitor is not None:
            result['LogMonitor'] = self.log_monitor.to_map()
        if self.site_monitor_operator_probe is not None:
            result['SiteMonitorOperatorProbe'] = self.site_monitor_operator_probe.to_map()
        if self.site_monitor_ecs_probe is not None:
            result['SiteMonitorEcsProbe'] = self.site_monitor_ecs_probe.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Api') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaApi()
            self.api = temp_model.from_map(m['Api'])
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('CustomMonitor') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaCustomMonitor()
            self.custom_monitor = temp_model.from_map(m['CustomMonitor'])
        if m.get('EventMonitor') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaEventMonitor()
            self.event_monitor = temp_model.from_map(m['EventMonitor'])
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('SiteMonitorTask') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorTask()
            self.site_monitor_task = temp_model.from_map(m['SiteMonitorTask'])
        if m.get('Phone') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaPhone()
            self.phone = temp_model.from_map(m['Phone'])
        if m.get('SuitInfo') is not None:
            self.suit_info = m.get('SuitInfo')
        if m.get('SMS') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSMS()
            self.sms = temp_model.from_map(m['SMS'])
        if m.get('LogMonitor') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaLogMonitor()
            self.log_monitor = temp_model.from_map(m['LogMonitor'])
        if m.get('SiteMonitorOperatorProbe') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorOperatorProbe()
            self.site_monitor_operator_probe = temp_model.from_map(m['SiteMonitorOperatorProbe'])
        if m.get('SiteMonitorEcsProbe') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuotaSiteMonitorEcsProbe()
            self.site_monitor_ecs_probe = temp_model.from_map(m['SiteMonitorEcsProbe'])
        return self


class DescribeMonitorResourceQuotaAttributeResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        resource_quota: DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuota = None,
        code: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.resource_quota = resource_quota
        self.code = code

    def validate(self):
        if self.resource_quota:
            self.resource_quota.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_quota is not None:
            result['ResourceQuota'] = self.resource_quota.to_map()
        if self.code is not None:
            result['Code'] = self.code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceQuota') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBodyResourceQuota()
            self.resource_quota = temp_model.from_map(m['ResourceQuota'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        return self


class DescribeMonitorResourceQuotaAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeMonitorResourceQuotaAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeMonitorResourceQuotaAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeProductResourceTagKeyListRequest(TeaModel):
    def __init__(
        self,
        next_token: str = None,
    ):
        self.next_token = next_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class DescribeProductResourceTagKeyListResponseBodyTagKeys(TeaModel):
    def __init__(
        self,
        tag_key: List[str] = None,
    ):
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class DescribeProductResourceTagKeyListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        next_token: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        tag_keys: DescribeProductResourceTagKeyListResponseBodyTagKeys = None,
    ):
        self.message = message
        self.next_token = next_token
        self.request_id = request_id
        self.code = code
        self.success = success
        self.tag_keys = tag_keys

    def validate(self):
        if self.tag_keys:
            self.tag_keys.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.tag_keys is not None:
            result['TagKeys'] = self.tag_keys.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TagKeys') is not None:
            temp_model = DescribeProductResourceTagKeyListResponseBodyTagKeys()
            self.tag_keys = temp_model.from_map(m['TagKeys'])
        return self


class DescribeProductResourceTagKeyListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeProductResourceTagKeyListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeProductResourceTagKeyListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRuleAlertInitConfigListAlertInitConfig(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        evaluation_count: str = None,
        namespace: str = None,
        threshold: str = None,
        statistics: str = None,
        period: str = None,
    ):
        self.metric_name = metric_name
        self.evaluation_count = evaluation_count
        self.namespace = namespace
        self.threshold = threshold
        self.statistics = statistics
        self.period = period

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.period is not None:
            result['Period'] = self.period
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        return self


class DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRuleAlertInitConfigList(TeaModel):
    def __init__(
        self,
        alert_init_config: List[DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRuleAlertInitConfigListAlertInitConfig] = None,
    ):
        self.alert_init_config = alert_init_config

    def validate(self):
        if self.alert_init_config:
            for k in self.alert_init_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AlertInitConfig'] = []
        if self.alert_init_config is not None:
            for k in self.alert_init_config:
                result['AlertInitConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.alert_init_config = []
        if m.get('AlertInitConfig') is not None:
            for k in m.get('AlertInitConfig'):
                temp_model = DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRuleAlertInitConfigListAlertInitConfig()
                self.alert_init_config.append(temp_model.from_map(k))
        return self


class DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRule(TeaModel):
    def __init__(
        self,
        product: str = None,
        alert_init_config_list: DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRuleAlertInitConfigList = None,
    ):
        self.product = product
        self.alert_init_config_list = alert_init_config_list

    def validate(self):
        if self.alert_init_config_list:
            self.alert_init_config_list.validate()

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        if self.alert_init_config_list is not None:
            result['AlertInitConfigList'] = self.alert_init_config_list.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('AlertInitConfigList') is not None:
            temp_model = DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRuleAlertInitConfigList()
            self.alert_init_config_list = temp_model.from_map(m['AlertInitConfigList'])
        return self


class DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleList(TeaModel):
    def __init__(
        self,
        all_product_init_metric_rule: List[DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRule] = None,
    ):
        self.all_product_init_metric_rule = all_product_init_metric_rule

    def validate(self):
        if self.all_product_init_metric_rule:
            for k in self.all_product_init_metric_rule:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['AllProductInitMetricRule'] = []
        if self.all_product_init_metric_rule is not None:
            for k in self.all_product_init_metric_rule:
                result['AllProductInitMetricRule'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.all_product_init_metric_rule = []
        if m.get('AllProductInitMetricRule') is not None:
            for k in m.get('AllProductInitMetricRule'):
                temp_model = DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleListAllProductInitMetricRule()
                self.all_product_init_metric_rule.append(temp_model.from_map(k))
        return self


class DescribeProductsOfActiveMetricRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        all_product_init_metric_rule_list: DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleList = None,
        datapoints: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.all_product_init_metric_rule_list = all_product_init_metric_rule_list
        self.datapoints = datapoints
        self.code = code
        self.success = success

    def validate(self):
        if self.all_product_init_metric_rule_list:
            self.all_product_init_metric_rule_list.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.all_product_init_metric_rule_list is not None:
            result['AllProductInitMetricRuleList'] = self.all_product_init_metric_rule_list.to_map()
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AllProductInitMetricRuleList') is not None:
            temp_model = DescribeProductsOfActiveMetricRuleResponseBodyAllProductInitMetricRuleList()
            self.all_product_init_metric_rule_list = temp_model.from_map(m['AllProductInitMetricRuleList'])
        if m.get('Datapoints') is not None:
            self.datapoints = m.get('Datapoints')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeProductsOfActiveMetricRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeProductsOfActiveMetricRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeProductsOfActiveMetricRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeProjectMetaRequest(TeaModel):
    def __init__(
        self,
        labels: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.labels = labels
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeProjectMetaResponseBodyResourcesResource(TeaModel):
    def __init__(
        self,
        description: str = None,
        labels: str = None,
        namespace: str = None,
    ):
        self.description = description
        self.labels = labels
        self.namespace = namespace

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        return self


class DescribeProjectMetaResponseBodyResources(TeaModel):
    def __init__(
        self,
        resource: List[DescribeProjectMetaResponseBodyResourcesResource] = None,
    ):
        self.resource = resource

    def validate(self):
        if self.resource:
            for k in self.resource:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Resource'] = []
        if self.resource is not None:
            for k in self.resource:
                result['Resource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.resource = []
        if m.get('Resource') is not None:
            for k in m.get('Resource'):
                temp_model = DescribeProjectMetaResponseBodyResourcesResource()
                self.resource.append(temp_model.from_map(k))
        return self


class DescribeProjectMetaResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: str = None,
        page_number: str = None,
        total: str = None,
        resources: DescribeProjectMetaResponseBodyResources = None,
        code: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.total = total
        self.resources = resources
        self.code = code
        self.success = success

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total is not None:
            result['Total'] = self.total
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Resources') is not None:
            temp_model = DescribeProjectMetaResponseBodyResources()
            self.resources = temp_model.from_map(m['Resources'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeProjectMetaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeProjectMetaResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeProjectMetaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSiteMonitorAttributeRequest(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        include_alert: bool = None,
    ):
        self.task_id = task_id
        self.include_alert = include_alert

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.include_alert is not None:
            result['IncludeAlert'] = self.include_alert
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('IncludeAlert') is not None:
            self.include_alert = m.get('IncludeAlert')
        return self


class DescribeSiteMonitorAttributeResponseBodyMetricRulesMetricRule(TeaModel):
    def __init__(
        self,
        metric_name: str = None,
        evaluation_count: str = None,
        namespace: str = None,
        ok_actions: str = None,
        alarm_actions: str = None,
        period: str = None,
        rule_name: str = None,
        rule_id: str = None,
        comparison_operator: str = None,
        expression: str = None,
        dimensions: str = None,
        state_value: str = None,
        action_enable: str = None,
        level: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.metric_name = metric_name
        self.evaluation_count = evaluation_count
        self.namespace = namespace
        self.ok_actions = ok_actions
        self.alarm_actions = alarm_actions
        self.period = period
        self.rule_name = rule_name
        self.rule_id = rule_id
        self.comparison_operator = comparison_operator
        self.expression = expression
        self.dimensions = dimensions
        self.state_value = state_value
        self.action_enable = action_enable
        self.level = level
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.ok_actions is not None:
            result['OkActions'] = self.ok_actions
        if self.alarm_actions is not None:
            result['AlarmActions'] = self.alarm_actions
        if self.period is not None:
            result['Period'] = self.period
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.expression is not None:
            result['Expression'] = self.expression
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.state_value is not None:
            result['StateValue'] = self.state_value
        if self.action_enable is not None:
            result['ActionEnable'] = self.action_enable
        if self.level is not None:
            result['Level'] = self.level
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('OkActions') is not None:
            self.ok_actions = m.get('OkActions')
        if m.get('AlarmActions') is not None:
            self.alarm_actions = m.get('AlarmActions')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Expression') is not None:
            self.expression = m.get('Expression')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('StateValue') is not None:
            self.state_value = m.get('StateValue')
        if m.get('ActionEnable') is not None:
            self.action_enable = m.get('ActionEnable')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeSiteMonitorAttributeResponseBodyMetricRules(TeaModel):
    def __init__(
        self,
        metric_rule: List[DescribeSiteMonitorAttributeResponseBodyMetricRulesMetricRule] = None,
    ):
        self.metric_rule = metric_rule

    def validate(self):
        if self.metric_rule:
            for k in self.metric_rule:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['MetricRule'] = []
        if self.metric_rule is not None:
            for k in self.metric_rule:
                result['MetricRule'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.metric_rule = []
        if m.get('MetricRule') is not None:
            for k in m.get('MetricRule'):
                temp_model = DescribeSiteMonitorAttributeResponseBodyMetricRulesMetricRule()
                self.metric_rule.append(temp_model.from_map(k))
        return self


class DescribeSiteMonitorAttributeResponseBodySiteMonitorsOptionJson(TeaModel):
    def __init__(
        self,
        password: str = None,
        request_format: str = None,
        expect_value: str = None,
        response_content: str = None,
        time_out: int = None,
        failure_rate: float = None,
        header: str = None,
        cookie: str = None,
        ping_num: int = None,
        port: int = None,
        authentication: int = None,
        http_method: str = None,
        match_rule: int = None,
        request_content: str = None,
        username: str = None,
        traceroute: int = None,
        response_format: str = None,
        dns_type: str = None,
        dns_server: str = None,
    ):
        self.password = password
        self.request_format = request_format
        self.expect_value = expect_value
        self.response_content = response_content
        self.time_out = time_out
        self.failure_rate = failure_rate
        self.header = header
        self.cookie = cookie
        self.ping_num = ping_num
        self.port = port
        self.authentication = authentication
        self.http_method = http_method
        self.match_rule = match_rule
        self.request_content = request_content
        self.username = username
        self.traceroute = traceroute
        self.response_format = response_format
        self.dns_type = dns_type
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.password is not None:
            result['password'] = self.password
        if self.request_format is not None:
            result['request_format'] = self.request_format
        if self.expect_value is not None:
            result['expect_value'] = self.expect_value
        if self.response_content is not None:
            result['response_content'] = self.response_content
        if self.time_out is not None:
            result['time_out'] = self.time_out
        if self.failure_rate is not None:
            result['failure_rate'] = self.failure_rate
        if self.header is not None:
            result['header'] = self.header
        if self.cookie is not None:
            result['cookie'] = self.cookie
        if self.ping_num is not None:
            result['ping_num'] = self.ping_num
        if self.port is not None:
            result['port'] = self.port
        if self.authentication is not None:
            result['authentication'] = self.authentication
        if self.http_method is not None:
            result['http_method'] = self.http_method
        if self.match_rule is not None:
            result['match_rule'] = self.match_rule
        if self.request_content is not None:
            result['request_content'] = self.request_content
        if self.username is not None:
            result['username'] = self.username
        if self.traceroute is not None:
            result['traceroute'] = self.traceroute
        if self.response_format is not None:
            result['response_format'] = self.response_format
        if self.dns_type is not None:
            result['dns_type'] = self.dns_type
        if self.dns_server is not None:
            result['dns_server'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('password') is not None:
            self.password = m.get('password')
        if m.get('request_format') is not None:
            self.request_format = m.get('request_format')
        if m.get('expect_value') is not None:
            self.expect_value = m.get('expect_value')
        if m.get('response_content') is not None:
            self.response_content = m.get('response_content')
        if m.get('time_out') is not None:
            self.time_out = m.get('time_out')
        if m.get('failure_rate') is not None:
            self.failure_rate = m.get('failure_rate')
        if m.get('header') is not None:
            self.header = m.get('header')
        if m.get('cookie') is not None:
            self.cookie = m.get('cookie')
        if m.get('ping_num') is not None:
            self.ping_num = m.get('ping_num')
        if m.get('port') is not None:
            self.port = m.get('port')
        if m.get('authentication') is not None:
            self.authentication = m.get('authentication')
        if m.get('http_method') is not None:
            self.http_method = m.get('http_method')
        if m.get('match_rule') is not None:
            self.match_rule = m.get('match_rule')
        if m.get('request_content') is not None:
            self.request_content = m.get('request_content')
        if m.get('username') is not None:
            self.username = m.get('username')
        if m.get('traceroute') is not None:
            self.traceroute = m.get('traceroute')
        if m.get('response_format') is not None:
            self.response_format = m.get('response_format')
        if m.get('dns_type') is not None:
            self.dns_type = m.get('dns_type')
        if m.get('dns_server') is not None:
            self.dns_server = m.get('dns_server')
        return self


class DescribeSiteMonitorAttributeResponseBodySiteMonitorsIspCitiesIspCity(TeaModel):
    def __init__(
        self,
        city_name: str = None,
        city: str = None,
        isp_name: str = None,
        isp: str = None,
    ):
        self.city_name = city_name
        self.city = city
        self.isp_name = isp_name
        self.isp = isp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.city_name is not None:
            result['CityName'] = self.city_name
        if self.city is not None:
            result['City'] = self.city
        if self.isp_name is not None:
            result['IspName'] = self.isp_name
        if self.isp is not None:
            result['Isp'] = self.isp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CityName') is not None:
            self.city_name = m.get('CityName')
        if m.get('City') is not None:
            self.city = m.get('City')
        if m.get('IspName') is not None:
            self.isp_name = m.get('IspName')
        if m.get('Isp') is not None:
            self.isp = m.get('Isp')
        return self


class DescribeSiteMonitorAttributeResponseBodySiteMonitorsIspCities(TeaModel):
    def __init__(
        self,
        isp_city: List[DescribeSiteMonitorAttributeResponseBodySiteMonitorsIspCitiesIspCity] = None,
    ):
        self.isp_city = isp_city

    def validate(self):
        if self.isp_city:
            for k in self.isp_city:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['IspCity'] = []
        if self.isp_city is not None:
            for k in self.isp_city:
                result['IspCity'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.isp_city = []
        if m.get('IspCity') is not None:
            for k in m.get('IspCity'):
                temp_model = DescribeSiteMonitorAttributeResponseBodySiteMonitorsIspCitiesIspCity()
                self.isp_city.append(temp_model.from_map(k))
        return self


class DescribeSiteMonitorAttributeResponseBodySiteMonitors(TeaModel):
    def __init__(
        self,
        task_type: str = None,
        option_json: DescribeSiteMonitorAttributeResponseBodySiteMonitorsOptionJson = None,
        interval: str = None,
        task_state: str = None,
        task_name: str = None,
        address: str = None,
        isp_cities: DescribeSiteMonitorAttributeResponseBodySiteMonitorsIspCities = None,
        task_id: str = None,
    ):
        self.task_type = task_type
        self.option_json = option_json
        self.interval = interval
        self.task_state = task_state
        self.task_name = task_name
        self.address = address
        self.isp_cities = isp_cities
        self.task_id = task_id

    def validate(self):
        if self.option_json:
            self.option_json.validate()
        if self.isp_cities:
            self.isp_cities.validate()

    def to_map(self):
        result = dict()
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.option_json is not None:
            result['OptionJson'] = self.option_json.to_map()
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.task_state is not None:
            result['TaskState'] = self.task_state
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.address is not None:
            result['Address'] = self.address
        if self.isp_cities is not None:
            result['IspCities'] = self.isp_cities.to_map()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('OptionJson') is not None:
            temp_model = DescribeSiteMonitorAttributeResponseBodySiteMonitorsOptionJson()
            self.option_json = temp_model.from_map(m['OptionJson'])
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('TaskState') is not None:
            self.task_state = m.get('TaskState')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('Address') is not None:
            self.address = m.get('Address')
        if m.get('IspCities') is not None:
            temp_model = DescribeSiteMonitorAttributeResponseBodySiteMonitorsIspCities()
            self.isp_cities = temp_model.from_map(m['IspCities'])
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class DescribeSiteMonitorAttributeResponseBody(TeaModel):
    def __init__(
        self,
        metric_rules: DescribeSiteMonitorAttributeResponseBodyMetricRules = None,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        site_monitors: DescribeSiteMonitorAttributeResponseBodySiteMonitors = None,
    ):
        self.metric_rules = metric_rules
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.site_monitors = site_monitors

    def validate(self):
        if self.metric_rules:
            self.metric_rules.validate()
        if self.site_monitors:
            self.site_monitors.validate()

    def to_map(self):
        result = dict()
        if self.metric_rules is not None:
            result['MetricRules'] = self.metric_rules.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.site_monitors is not None:
            result['SiteMonitors'] = self.site_monitors.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MetricRules') is not None:
            temp_model = DescribeSiteMonitorAttributeResponseBodyMetricRules()
            self.metric_rules = temp_model.from_map(m['MetricRules'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('SiteMonitors') is not None:
            temp_model = DescribeSiteMonitorAttributeResponseBodySiteMonitors()
            self.site_monitors = temp_model.from_map(m['SiteMonitors'])
        return self


class DescribeSiteMonitorAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSiteMonitorAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSiteMonitorAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSiteMonitorDataRequest(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        type: str = None,
        metric_name: str = None,
        start_time: str = None,
        end_time: str = None,
        period: str = None,
        next_token: str = None,
        length: int = None,
    ):
        self.task_id = task_id
        self.type = type
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.next_token = next_token
        self.length = length

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.type is not None:
            result['Type'] = self.type
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.period is not None:
            result['Period'] = self.period
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.length is not None:
            result['Length'] = self.length
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        return self


class DescribeSiteMonitorDataResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        message: str = None,
        data: str = None,
        code: str = None,
        success: str = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.message = message
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.data is not None:
            result['Data'] = self.data
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSiteMonitorDataResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSiteMonitorDataResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSiteMonitorDataResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSiteMonitorListRequest(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        task_type: str = None,
        keyword: str = None,
        page: int = None,
        page_size: int = None,
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.keyword = keyword
        self.page = page
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.page is not None:
            result['Page'] = self.page
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Page') is not None:
            self.page = m.get('Page')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeSiteMonitorListResponseBodySiteMonitorsSiteMonitorOptionsJson(TeaModel):
    def __init__(
        self,
        password: str = None,
        request_format: str = None,
        expect_value: str = None,
        response_content: str = None,
        time_out: int = None,
        failure_rate: float = None,
        header: str = None,
        cookie: str = None,
        ping_num: int = None,
        port: int = None,
        authentication: int = None,
        http_method: str = None,
        match_rule: int = None,
        request_content: str = None,
        username: str = None,
        traceroute: int = None,
        response_format: str = None,
        dns_type: str = None,
        dns_server: str = None,
    ):
        self.password = password
        self.request_format = request_format
        self.expect_value = expect_value
        self.response_content = response_content
        self.time_out = time_out
        self.failure_rate = failure_rate
        self.header = header
        self.cookie = cookie
        self.ping_num = ping_num
        self.port = port
        self.authentication = authentication
        self.http_method = http_method
        self.match_rule = match_rule
        self.request_content = request_content
        self.username = username
        self.traceroute = traceroute
        self.response_format = response_format
        self.dns_type = dns_type
        self.dns_server = dns_server

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.password is not None:
            result['password'] = self.password
        if self.request_format is not None:
            result['request_format'] = self.request_format
        if self.expect_value is not None:
            result['expect_value'] = self.expect_value
        if self.response_content is not None:
            result['response_content'] = self.response_content
        if self.time_out is not None:
            result['time_out'] = self.time_out
        if self.failure_rate is not None:
            result['failure_rate'] = self.failure_rate
        if self.header is not None:
            result['header'] = self.header
        if self.cookie is not None:
            result['cookie'] = self.cookie
        if self.ping_num is not None:
            result['ping_num'] = self.ping_num
        if self.port is not None:
            result['port'] = self.port
        if self.authentication is not None:
            result['authentication'] = self.authentication
        if self.http_method is not None:
            result['http_method'] = self.http_method
        if self.match_rule is not None:
            result['match_rule'] = self.match_rule
        if self.request_content is not None:
            result['request_content'] = self.request_content
        if self.username is not None:
            result['username'] = self.username
        if self.traceroute is not None:
            result['traceroute'] = self.traceroute
        if self.response_format is not None:
            result['response_format'] = self.response_format
        if self.dns_type is not None:
            result['dns_type'] = self.dns_type
        if self.dns_server is not None:
            result['dns_server'] = self.dns_server
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('password') is not None:
            self.password = m.get('password')
        if m.get('request_format') is not None:
            self.request_format = m.get('request_format')
        if m.get('expect_value') is not None:
            self.expect_value = m.get('expect_value')
        if m.get('response_content') is not None:
            self.response_content = m.get('response_content')
        if m.get('time_out') is not None:
            self.time_out = m.get('time_out')
        if m.get('failure_rate') is not None:
            self.failure_rate = m.get('failure_rate')
        if m.get('header') is not None:
            self.header = m.get('header')
        if m.get('cookie') is not None:
            self.cookie = m.get('cookie')
        if m.get('ping_num') is not None:
            self.ping_num = m.get('ping_num')
        if m.get('port') is not None:
            self.port = m.get('port')
        if m.get('authentication') is not None:
            self.authentication = m.get('authentication')
        if m.get('http_method') is not None:
            self.http_method = m.get('http_method')
        if m.get('match_rule') is not None:
            self.match_rule = m.get('match_rule')
        if m.get('request_content') is not None:
            self.request_content = m.get('request_content')
        if m.get('username') is not None:
            self.username = m.get('username')
        if m.get('traceroute') is not None:
            self.traceroute = m.get('traceroute')
        if m.get('response_format') is not None:
            self.response_format = m.get('response_format')
        if m.get('dns_type') is not None:
            self.dns_type = m.get('dns_type')
        if m.get('dns_server') is not None:
            self.dns_server = m.get('dns_server')
        return self


class DescribeSiteMonitorListResponseBodySiteMonitorsSiteMonitor(TeaModel):
    def __init__(
        self,
        task_type: str = None,
        update_time: str = None,
        interval: str = None,
        task_state: str = None,
        options_json: DescribeSiteMonitorListResponseBodySiteMonitorsSiteMonitorOptionsJson = None,
        create_time: str = None,
        task_name: str = None,
        address: str = None,
        task_id: str = None,
    ):
        self.task_type = task_type
        self.update_time = update_time
        self.interval = interval
        self.task_state = task_state
        self.options_json = options_json
        self.create_time = create_time
        self.task_name = task_name
        self.address = address
        self.task_id = task_id

    def validate(self):
        if self.options_json:
            self.options_json.validate()

    def to_map(self):
        result = dict()
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.task_state is not None:
            result['TaskState'] = self.task_state
        if self.options_json is not None:
            result['OptionsJson'] = self.options_json.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.address is not None:
            result['Address'] = self.address
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('TaskState') is not None:
            self.task_state = m.get('TaskState')
        if m.get('OptionsJson') is not None:
            temp_model = DescribeSiteMonitorListResponseBodySiteMonitorsSiteMonitorOptionsJson()
            self.options_json = temp_model.from_map(m['OptionsJson'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('Address') is not None:
            self.address = m.get('Address')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class DescribeSiteMonitorListResponseBodySiteMonitors(TeaModel):
    def __init__(
        self,
        site_monitor: List[DescribeSiteMonitorListResponseBodySiteMonitorsSiteMonitor] = None,
    ):
        self.site_monitor = site_monitor

    def validate(self):
        if self.site_monitor:
            for k in self.site_monitor:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SiteMonitor'] = []
        if self.site_monitor is not None:
            for k in self.site_monitor:
                result['SiteMonitor'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.site_monitor = []
        if m.get('SiteMonitor') is not None:
            for k in m.get('SiteMonitor'):
                temp_model = DescribeSiteMonitorListResponseBodySiteMonitorsSiteMonitor()
                self.site_monitor.append(temp_model.from_map(k))
        return self


class DescribeSiteMonitorListResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        page_number: int = None,
        code: str = None,
        success: str = None,
        site_monitors: DescribeSiteMonitorListResponseBodySiteMonitors = None,
    ):
        self.total_count = total_count
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.page_number = page_number
        self.code = code
        self.success = success
        self.site_monitors = site_monitors

    def validate(self):
        if self.site_monitors:
            self.site_monitors.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.site_monitors is not None:
            result['SiteMonitors'] = self.site_monitors.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('SiteMonitors') is not None:
            temp_model = DescribeSiteMonitorListResponseBodySiteMonitors()
            self.site_monitors = temp_model.from_map(m['SiteMonitors'])
        return self


class DescribeSiteMonitorListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSiteMonitorListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSiteMonitorListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSiteMonitorQuotaResponseBodyData(TeaModel):
    def __init__(
        self,
        site_monitor_operator_quota_quota: int = None,
        second_monitor: bool = None,
        site_monitor_quota_task_used: int = None,
        site_monitor_task_quota: int = None,
        site_monitor_version: str = None,
        site_monitor_idc_quota: int = None,
    ):
        self.site_monitor_operator_quota_quota = site_monitor_operator_quota_quota
        self.second_monitor = second_monitor
        self.site_monitor_quota_task_used = site_monitor_quota_task_used
        self.site_monitor_task_quota = site_monitor_task_quota
        self.site_monitor_version = site_monitor_version
        self.site_monitor_idc_quota = site_monitor_idc_quota

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.site_monitor_operator_quota_quota is not None:
            result['SiteMonitorOperatorQuotaQuota'] = self.site_monitor_operator_quota_quota
        if self.second_monitor is not None:
            result['SecondMonitor'] = self.second_monitor
        if self.site_monitor_quota_task_used is not None:
            result['SiteMonitorQuotaTaskUsed'] = self.site_monitor_quota_task_used
        if self.site_monitor_task_quota is not None:
            result['SiteMonitorTaskQuota'] = self.site_monitor_task_quota
        if self.site_monitor_version is not None:
            result['SiteMonitorVersion'] = self.site_monitor_version
        if self.site_monitor_idc_quota is not None:
            result['SiteMonitorIdcQuota'] = self.site_monitor_idc_quota
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SiteMonitorOperatorQuotaQuota') is not None:
            self.site_monitor_operator_quota_quota = m.get('SiteMonitorOperatorQuotaQuota')
        if m.get('SecondMonitor') is not None:
            self.second_monitor = m.get('SecondMonitor')
        if m.get('SiteMonitorQuotaTaskUsed') is not None:
            self.site_monitor_quota_task_used = m.get('SiteMonitorQuotaTaskUsed')
        if m.get('SiteMonitorTaskQuota') is not None:
            self.site_monitor_task_quota = m.get('SiteMonitorTaskQuota')
        if m.get('SiteMonitorVersion') is not None:
            self.site_monitor_version = m.get('SiteMonitorVersion')
        if m.get('SiteMonitorIdcQuota') is not None:
            self.site_monitor_idc_quota = m.get('SiteMonitorIdcQuota')
        return self


class DescribeSiteMonitorQuotaResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: DescribeSiteMonitorQuotaResponseBodyData = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DescribeSiteMonitorQuotaResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSiteMonitorQuotaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSiteMonitorQuotaResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSiteMonitorQuotaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSiteMonitorStatisticsRequest(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        time_range: str = None,
        start_time: str = None,
        metric_name: str = None,
    ):
        self.task_id = task_id
        self.time_range = time_range
        self.start_time = start_time
        self.metric_name = metric_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.time_range is not None:
            result['TimeRange'] = self.time_range
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('TimeRange') is not None:
            self.time_range = m.get('TimeRange')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        return self


class DescribeSiteMonitorStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: str = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSiteMonitorStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSiteMonitorStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSiteMonitorStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSystemEventAttributeRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
        event_type: str = None,
        name: str = None,
        level: str = None,
        status: str = None,
        group_id: str = None,
        search_keywords: str = None,
        start_time: str = None,
        end_time: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.product = product
        self.event_type = event_type
        self.name = name
        self.level = level
        self.status = status
        self.group_id = group_id
        self.search_keywords = search_keywords
        self.start_time = start_time
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        if self.event_type is not None:
            result['EventType'] = self.event_type
        if self.name is not None:
            result['Name'] = self.name
        if self.level is not None:
            result['Level'] = self.level
        if self.status is not None:
            result['Status'] = self.status
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.search_keywords is not None:
            result['SearchKeywords'] = self.search_keywords
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('EventType') is not None:
            self.event_type = m.get('EventType')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('SearchKeywords') is not None:
            self.search_keywords = m.get('SearchKeywords')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeSystemEventAttributeResponseBodySystemEventsSystemEvent(TeaModel):
    def __init__(
        self,
        status: str = None,
        time: int = None,
        group_id: str = None,
        product: str = None,
        instance_name: str = None,
        resource_id: str = None,
        name: str = None,
        content: str = None,
        level: str = None,
        region_id: str = None,
    ):
        self.status = status
        self.time = time
        self.group_id = group_id
        self.product = product
        self.instance_name = instance_name
        self.resource_id = resource_id
        self.name = name
        self.content = content
        self.level = level
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.time is not None:
            result['Time'] = self.time
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.product is not None:
            result['Product'] = self.product
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.name is not None:
            result['Name'] = self.name
        if self.content is not None:
            result['Content'] = self.content
        if self.level is not None:
            result['Level'] = self.level
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeSystemEventAttributeResponseBodySystemEvents(TeaModel):
    def __init__(
        self,
        system_event: List[DescribeSystemEventAttributeResponseBodySystemEventsSystemEvent] = None,
    ):
        self.system_event = system_event

    def validate(self):
        if self.system_event:
            for k in self.system_event:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SystemEvent'] = []
        if self.system_event is not None:
            for k in self.system_event:
                result['SystemEvent'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.system_event = []
        if m.get('SystemEvent') is not None:
            for k in m.get('SystemEvent'):
                temp_model = DescribeSystemEventAttributeResponseBodySystemEventsSystemEvent()
                self.system_event.append(temp_model.from_map(k))
        return self


class DescribeSystemEventAttributeResponseBody(TeaModel):
    def __init__(
        self,
        system_events: DescribeSystemEventAttributeResponseBodySystemEvents = None,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: str = None,
    ):
        self.system_events = system_events
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        if self.system_events:
            self.system_events.validate()

    def to_map(self):
        result = dict()
        if self.system_events is not None:
            result['SystemEvents'] = self.system_events.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SystemEvents') is not None:
            temp_model = DescribeSystemEventAttributeResponseBodySystemEvents()
            self.system_events = temp_model.from_map(m['SystemEvents'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSystemEventAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSystemEventAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSystemEventAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSystemEventCountRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
        event_type: str = None,
        name: str = None,
        level: str = None,
        status: str = None,
        group_id: str = None,
        search_keywords: str = None,
        start_time: str = None,
        end_time: str = None,
    ):
        self.product = product
        self.event_type = event_type
        self.name = name
        self.level = level
        self.status = status
        self.group_id = group_id
        self.search_keywords = search_keywords
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        if self.event_type is not None:
            result['EventType'] = self.event_type
        if self.name is not None:
            result['Name'] = self.name
        if self.level is not None:
            result['Level'] = self.level
        if self.status is not None:
            result['Status'] = self.status
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.search_keywords is not None:
            result['SearchKeywords'] = self.search_keywords
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('EventType') is not None:
            self.event_type = m.get('EventType')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('SearchKeywords') is not None:
            self.search_keywords = m.get('SearchKeywords')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        return self


class DescribeSystemEventCountResponseBodySystemEventCountsSystemEventCount(TeaModel):
    def __init__(
        self,
        status: str = None,
        time: int = None,
        group_id: str = None,
        product: str = None,
        instance_name: str = None,
        num: int = None,
        resource_id: str = None,
        name: str = None,
        content: str = None,
        level: str = None,
        region_id: str = None,
    ):
        self.status = status
        self.time = time
        self.group_id = group_id
        self.product = product
        self.instance_name = instance_name
        self.num = num
        self.resource_id = resource_id
        self.name = name
        self.content = content
        self.level = level
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.time is not None:
            result['Time'] = self.time
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.product is not None:
            result['Product'] = self.product
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.num is not None:
            result['Num'] = self.num
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.name is not None:
            result['Name'] = self.name
        if self.content is not None:
            result['Content'] = self.content
        if self.level is not None:
            result['Level'] = self.level
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeSystemEventCountResponseBodySystemEventCounts(TeaModel):
    def __init__(
        self,
        system_event_count: List[DescribeSystemEventCountResponseBodySystemEventCountsSystemEventCount] = None,
    ):
        self.system_event_count = system_event_count

    def validate(self):
        if self.system_event_count:
            for k in self.system_event_count:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SystemEventCount'] = []
        if self.system_event_count is not None:
            for k in self.system_event_count:
                result['SystemEventCount'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.system_event_count = []
        if m.get('SystemEventCount') is not None:
            for k in m.get('SystemEventCount'):
                temp_model = DescribeSystemEventCountResponseBodySystemEventCountsSystemEventCount()
                self.system_event_count.append(temp_model.from_map(k))
        return self


class DescribeSystemEventCountResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        system_event_counts: DescribeSystemEventCountResponseBodySystemEventCounts = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.system_event_counts = system_event_counts
        self.code = code
        self.success = success

    def validate(self):
        if self.system_event_counts:
            self.system_event_counts.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.system_event_counts is not None:
            result['SystemEventCounts'] = self.system_event_counts.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SystemEventCounts') is not None:
            temp_model = DescribeSystemEventCountResponseBodySystemEventCounts()
            self.system_event_counts = temp_model.from_map(m['SystemEventCounts'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSystemEventCountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSystemEventCountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSystemEventCountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSystemEventHistogramRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
        event_type: str = None,
        name: str = None,
        level: str = None,
        status: str = None,
        group_id: str = None,
        search_keywords: str = None,
        start_time: str = None,
        end_time: str = None,
    ):
        self.product = product
        self.event_type = event_type
        self.name = name
        self.level = level
        self.status = status
        self.group_id = group_id
        self.search_keywords = search_keywords
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        if self.event_type is not None:
            result['EventType'] = self.event_type
        if self.name is not None:
            result['Name'] = self.name
        if self.level is not None:
            result['Level'] = self.level
        if self.status is not None:
            result['Status'] = self.status
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.search_keywords is not None:
            result['SearchKeywords'] = self.search_keywords
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('EventType') is not None:
            self.event_type = m.get('EventType')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('SearchKeywords') is not None:
            self.search_keywords = m.get('SearchKeywords')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        return self


class DescribeSystemEventHistogramResponseBodySystemEventHistogramsSystemEventHistogram(TeaModel):
    def __init__(
        self,
        end_time: int = None,
        start_time: int = None,
        count: int = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeSystemEventHistogramResponseBodySystemEventHistograms(TeaModel):
    def __init__(
        self,
        system_event_histogram: List[DescribeSystemEventHistogramResponseBodySystemEventHistogramsSystemEventHistogram] = None,
    ):
        self.system_event_histogram = system_event_histogram

    def validate(self):
        if self.system_event_histogram:
            for k in self.system_event_histogram:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SystemEventHistogram'] = []
        if self.system_event_histogram is not None:
            for k in self.system_event_histogram:
                result['SystemEventHistogram'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.system_event_histogram = []
        if m.get('SystemEventHistogram') is not None:
            for k in m.get('SystemEventHistogram'):
                temp_model = DescribeSystemEventHistogramResponseBodySystemEventHistogramsSystemEventHistogram()
                self.system_event_histogram.append(temp_model.from_map(k))
        return self


class DescribeSystemEventHistogramResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        system_event_histograms: DescribeSystemEventHistogramResponseBodySystemEventHistograms = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.system_event_histograms = system_event_histograms
        self.code = code
        self.success = success

    def validate(self):
        if self.system_event_histograms:
            self.system_event_histograms.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.system_event_histograms is not None:
            result['SystemEventHistograms'] = self.system_event_histograms.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SystemEventHistograms') is not None:
            temp_model = DescribeSystemEventHistogramResponseBodySystemEventHistograms()
            self.system_event_histograms = temp_model.from_map(m['SystemEventHistograms'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSystemEventHistogramResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSystemEventHistogramResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSystemEventHistogramResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTagKeyListRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeTagKeyListResponseBodyTagKeys(TeaModel):
    def __init__(
        self,
        tag_key: List[str] = None,
    ):
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class DescribeTagKeyListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        tag_keys: DescribeTagKeyListResponseBodyTagKeys = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.tag_keys = tag_keys

    def validate(self):
        if self.tag_keys:
            self.tag_keys.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.tag_keys is not None:
            result['TagKeys'] = self.tag_keys.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TagKeys') is not None:
            temp_model = DescribeTagKeyListResponseBodyTagKeys()
            self.tag_keys = temp_model.from_map(m['TagKeys'])
        return self


class DescribeTagKeyListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTagKeyListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTagKeyListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTagValueListRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
        tag_key: str = None,
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class DescribeTagValueListResponseBodyTagValues(TeaModel):
    def __init__(
        self,
        tag_value: List[str] = None,
    ):
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class DescribeTagValueListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        tag_values: DescribeTagValueListResponseBodyTagValues = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.tag_values = tag_values

    def validate(self):
        if self.tag_values:
            self.tag_values.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.tag_values is not None:
            result['TagValues'] = self.tag_values.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TagValues') is not None:
            temp_model = DescribeTagValueListResponseBodyTagValues()
            self.tag_values = temp_model.from_map(m['TagValues'])
        return self


class DescribeTagValueListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTagValueListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTagValueListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeUnhealthyHostAvailabilityRequest(TeaModel):
    def __init__(
        self,
        id: List[int] = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyListNodeTaskInstanceInstanceList(TeaModel):
    def __init__(
        self,
        string: List[str] = None,
    ):
        self.string = string

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.string is not None:
            result['String'] = self.string
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('String') is not None:
            self.string = m.get('String')
        return self


class DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyListNodeTaskInstance(TeaModel):
    def __init__(
        self,
        instance_list: DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyListNodeTaskInstanceInstanceList = None,
        id: int = None,
    ):
        self.instance_list = instance_list
        self.id = id

    def validate(self):
        if self.instance_list:
            self.instance_list.validate()

    def to_map(self):
        result = dict()
        if self.instance_list is not None:
            result['InstanceList'] = self.instance_list.to_map()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceList') is not None:
            temp_model = DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyListNodeTaskInstanceInstanceList()
            self.instance_list = temp_model.from_map(m['InstanceList'])
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyList(TeaModel):
    def __init__(
        self,
        node_task_instance: List[DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyListNodeTaskInstance] = None,
    ):
        self.node_task_instance = node_task_instance

    def validate(self):
        if self.node_task_instance:
            for k in self.node_task_instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['NodeTaskInstance'] = []
        if self.node_task_instance is not None:
            for k in self.node_task_instance:
                result['NodeTaskInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.node_task_instance = []
        if m.get('NodeTaskInstance') is not None:
            for k in m.get('NodeTaskInstance'):
                temp_model = DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyListNodeTaskInstance()
                self.node_task_instance.append(temp_model.from_map(k))
        return self


class DescribeUnhealthyHostAvailabilityResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
        unhealthy_list: DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyList = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.unhealthy_list = unhealthy_list

    def validate(self):
        if self.unhealthy_list:
            self.unhealthy_list.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        if self.unhealthy_list is not None:
            result['UnhealthyList'] = self.unhealthy_list.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('UnhealthyList') is not None:
            temp_model = DescribeUnhealthyHostAvailabilityResponseBodyUnhealthyList()
            self.unhealthy_list = temp_model.from_map(m['UnhealthyList'])
        return self


class DescribeUnhealthyHostAvailabilityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeUnhealthyHostAvailabilityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeUnhealthyHostAvailabilityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableActiveMetricRuleRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
    ):
        self.product = product

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        return self


class DisableActiveMetricRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DisableActiveMetricRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DisableActiveMetricRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DisableActiveMetricRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableEventRulesRequest(TeaModel):
    def __init__(
        self,
        rule_names: List[str] = None,
    ):
        self.rule_names = rule_names

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_names is not None:
            result['RuleNames'] = self.rule_names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleNames') is not None:
            self.rule_names = m.get('RuleNames')
        return self


class DisableEventRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DisableEventRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DisableEventRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DisableEventRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableHostAvailabilityRequest(TeaModel):
    def __init__(
        self,
        id: List[int] = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DisableHostAvailabilityResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DisableHostAvailabilityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DisableHostAvailabilityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DisableHostAvailabilityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableMetricRulesRequest(TeaModel):
    def __init__(
        self,
        rule_id: List[str] = None,
    ):
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class DisableMetricRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DisableMetricRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DisableMetricRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DisableMetricRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableSiteMonitorsRequest(TeaModel):
    def __init__(
        self,
        task_ids: str = None,
    ):
        self.task_ids = task_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_ids is not None:
            result['TaskIds'] = self.task_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskIds') is not None:
            self.task_ids = m.get('TaskIds')
        return self


class DisableSiteMonitorsResponseBodyData(TeaModel):
    def __init__(
        self,
        count: int = None,
    ):
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        return self


class DisableSiteMonitorsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: DisableSiteMonitorsResponseBodyData = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DisableSiteMonitorsResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DisableSiteMonitorsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DisableSiteMonitorsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DisableSiteMonitorsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableActiveMetricRuleRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
    ):
        self.product = product

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        return self


class EnableActiveMetricRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableActiveMetricRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableActiveMetricRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableActiveMetricRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableEventRulesRequest(TeaModel):
    def __init__(
        self,
        rule_names: List[str] = None,
    ):
        self.rule_names = rule_names

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_names is not None:
            result['RuleNames'] = self.rule_names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleNames') is not None:
            self.rule_names = m.get('RuleNames')
        return self


class EnableEventRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableEventRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableEventRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableEventRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableHostAvailabilityRequest(TeaModel):
    def __init__(
        self,
        id: List[int] = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class EnableHostAvailabilityResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableHostAvailabilityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableHostAvailabilityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableHostAvailabilityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableMetricRulesRequest(TeaModel):
    def __init__(
        self,
        rule_id: List[str] = None,
    ):
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class EnableMetricRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableMetricRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableMetricRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableMetricRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableSiteMonitorsRequest(TeaModel):
    def __init__(
        self,
        task_ids: str = None,
    ):
        self.task_ids = task_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_ids is not None:
            result['TaskIds'] = self.task_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskIds') is not None:
            self.task_ids = m.get('TaskIds')
        return self


class EnableSiteMonitorsResponseBodyData(TeaModel):
    def __init__(
        self,
        count: int = None,
    ):
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        return self


class EnableSiteMonitorsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: EnableSiteMonitorsResponseBodyData = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = EnableSiteMonitorsResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableSiteMonitorsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableSiteMonitorsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableSiteMonitorsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class InstallMonitoringAgentRequest(TeaModel):
    def __init__(
        self,
        force: bool = None,
        instance_ids: List[str] = None,
    ):
        self.force = force
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.force is not None:
            result['Force'] = self.force
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Force') is not None:
            self.force = m.get('Force')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class InstallMonitoringAgentResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class InstallMonitoringAgentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: InstallMonitoringAgentResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = InstallMonitoringAgentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyGroupMonitoringAgentProcessRequestAlertConfig(TeaModel):
    def __init__(
        self,
        silence_time: str = None,
        comparison_operator: str = None,
        webhook: str = None,
        times: str = None,
        escalations_level: str = None,
        no_effective_interval: str = None,
        effective_interval: str = None,
        threshold: str = None,
        statistics: str = None,
    ):
        self.silence_time = silence_time
        self.comparison_operator = comparison_operator
        self.webhook = webhook
        self.times = times
        self.escalations_level = escalations_level
        self.no_effective_interval = no_effective_interval
        self.effective_interval = effective_interval
        self.threshold = threshold
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.times is not None:
            result['Times'] = self.times
        if self.escalations_level is not None:
            result['EscalationsLevel'] = self.escalations_level
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('EscalationsLevel') is not None:
            self.escalations_level = m.get('EscalationsLevel')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class ModifyGroupMonitoringAgentProcessRequest(TeaModel):
    def __init__(
        self,
        id: str = None,
        group_id: str = None,
        match_express_filter_relation: str = None,
        alert_config: List[ModifyGroupMonitoringAgentProcessRequestAlertConfig] = None,
    ):
        self.id = id
        self.group_id = group_id
        self.match_express_filter_relation = match_express_filter_relation
        self.alert_config = alert_config

    def validate(self):
        if self.alert_config:
            for k in self.alert_config:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.match_express_filter_relation is not None:
            result['MatchExpressFilterRelation'] = self.match_express_filter_relation
        result['AlertConfig'] = []
        if self.alert_config is not None:
            for k in self.alert_config:
                result['AlertConfig'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('MatchExpressFilterRelation') is not None:
            self.match_express_filter_relation = m.get('MatchExpressFilterRelation')
        self.alert_config = []
        if m.get('AlertConfig') is not None:
            for k in m.get('AlertConfig'):
                temp_model = ModifyGroupMonitoringAgentProcessRequestAlertConfig()
                self.alert_config.append(temp_model.from_map(k))
        return self


class ModifyGroupMonitoringAgentProcessResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyGroupMonitoringAgentProcessResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyGroupMonitoringAgentProcessResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyGroupMonitoringAgentProcessResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyHostAvailabilityRequestTaskOption(TeaModel):
    def __init__(
        self,
        http_uri: str = None,
        telnet_or_ping_host: str = None,
        http_response_charset: str = None,
        http_post_content: str = None,
        http_response_match_content: str = None,
        http_method: str = None,
        http_negative: bool = None,
    ):
        self.http_uri = http_uri
        self.telnet_or_ping_host = telnet_or_ping_host
        self.http_response_charset = http_response_charset
        self.http_post_content = http_post_content
        self.http_response_match_content = http_response_match_content
        self.http_method = http_method
        self.http_negative = http_negative

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.http_uri is not None:
            result['HttpURI'] = self.http_uri
        if self.telnet_or_ping_host is not None:
            result['TelnetOrPingHost'] = self.telnet_or_ping_host
        if self.http_response_charset is not None:
            result['HttpResponseCharset'] = self.http_response_charset
        if self.http_post_content is not None:
            result['HttpPostContent'] = self.http_post_content
        if self.http_response_match_content is not None:
            result['HttpResponseMatchContent'] = self.http_response_match_content
        if self.http_method is not None:
            result['HttpMethod'] = self.http_method
        if self.http_negative is not None:
            result['HttpNegative'] = self.http_negative
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HttpURI') is not None:
            self.http_uri = m.get('HttpURI')
        if m.get('TelnetOrPingHost') is not None:
            self.telnet_or_ping_host = m.get('TelnetOrPingHost')
        if m.get('HttpResponseCharset') is not None:
            self.http_response_charset = m.get('HttpResponseCharset')
        if m.get('HttpPostContent') is not None:
            self.http_post_content = m.get('HttpPostContent')
        if m.get('HttpResponseMatchContent') is not None:
            self.http_response_match_content = m.get('HttpResponseMatchContent')
        if m.get('HttpMethod') is not None:
            self.http_method = m.get('HttpMethod')
        if m.get('HttpNegative') is not None:
            self.http_negative = m.get('HttpNegative')
        return self


class ModifyHostAvailabilityRequestAlertConfig(TeaModel):
    def __init__(
        self,
        notify_type: int = None,
        start_time: int = None,
        end_time: int = None,
        silence_time: int = None,
        web_hook: str = None,
    ):
        self.notify_type = notify_type
        self.start_time = start_time
        self.end_time = end_time
        self.silence_time = silence_time
        self.web_hook = web_hook

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.notify_type is not None:
            result['NotifyType'] = self.notify_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.web_hook is not None:
            result['WebHook'] = self.web_hook
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NotifyType') is not None:
            self.notify_type = m.get('NotifyType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('WebHook') is not None:
            self.web_hook = m.get('WebHook')
        return self


class ModifyHostAvailabilityRequestAlertConfigEscalationList(TeaModel):
    def __init__(
        self,
        value: str = None,
        metric_name: str = None,
        times: int = None,
        operator: str = None,
        aggregate: str = None,
    ):
        self.value = value
        self.metric_name = metric_name
        self.times = times
        self.operator = operator
        self.aggregate = aggregate

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.times is not None:
            result['Times'] = self.times
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.aggregate is not None:
            result['Aggregate'] = self.aggregate
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Aggregate') is not None:
            self.aggregate = m.get('Aggregate')
        return self


class ModifyHostAvailabilityRequest(TeaModel):
    def __init__(
        self,
        task_option: ModifyHostAvailabilityRequestTaskOption = None,
        alert_config: ModifyHostAvailabilityRequestAlertConfig = None,
        group_id: int = None,
        id: int = None,
        task_name: str = None,
        task_scope: str = None,
        alert_config_escalation_list: List[ModifyHostAvailabilityRequestAlertConfigEscalationList] = None,
        instance_list: List[str] = None,
    ):
        self.task_option = task_option
        self.alert_config = alert_config
        self.group_id = group_id
        self.id = id
        self.task_name = task_name
        self.task_scope = task_scope
        self.alert_config_escalation_list = alert_config_escalation_list
        self.instance_list = instance_list

    def validate(self):
        if self.task_option:
            self.task_option.validate()
        if self.alert_config:
            self.alert_config.validate()
        if self.alert_config_escalation_list:
            for k in self.alert_config_escalation_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.task_option is not None:
            result['TaskOption'] = self.task_option.to_map()
        if self.alert_config is not None:
            result['AlertConfig'] = self.alert_config.to_map()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.id is not None:
            result['Id'] = self.id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_scope is not None:
            result['TaskScope'] = self.task_scope
        result['AlertConfigEscalationList'] = []
        if self.alert_config_escalation_list is not None:
            for k in self.alert_config_escalation_list:
                result['AlertConfigEscalationList'].append(k.to_map() if k else None)
        if self.instance_list is not None:
            result['InstanceList'] = self.instance_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskOption') is not None:
            temp_model = ModifyHostAvailabilityRequestTaskOption()
            self.task_option = temp_model.from_map(m['TaskOption'])
        if m.get('AlertConfig') is not None:
            temp_model = ModifyHostAvailabilityRequestAlertConfig()
            self.alert_config = temp_model.from_map(m['AlertConfig'])
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskScope') is not None:
            self.task_scope = m.get('TaskScope')
        self.alert_config_escalation_list = []
        if m.get('AlertConfigEscalationList') is not None:
            for k in m.get('AlertConfigEscalationList'):
                temp_model = ModifyHostAvailabilityRequestAlertConfigEscalationList()
                self.alert_config_escalation_list.append(temp_model.from_map(k))
        if m.get('InstanceList') is not None:
            self.instance_list = m.get('InstanceList')
        return self


class ModifyHostAvailabilityResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyHostAvailabilityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyHostAvailabilityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyHostAvailabilityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyHostInfoRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        host_name: str = None,
    ):
        self.instance_id = instance_id
        self.host_name = host_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.host_name is not None:
            result['HostName'] = self.host_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        return self


class ModifyHostInfoResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyHostInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyHostInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyHostInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsInfo(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        statistics: str = None,
        comparison_operator: str = None,
        times: int = None,
    ):
        self.threshold = threshold
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsWarn(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        times: int = None,
        comparison_operator: str = None,
        statistics: str = None,
    ):
        self.threshold = threshold
        self.times = times
        self.comparison_operator = comparison_operator
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsCritical(TeaModel):
    def __init__(
        self,
        times: int = None,
        threshold: str = None,
        comparison_operator: str = None,
        statistics: str = None,
    ):
        self.times = times
        self.threshold = threshold
        self.comparison_operator = comparison_operator
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class ModifyMetricRuleTemplateRequestAlertTemplatesEscalations(TeaModel):
    def __init__(
        self,
        info: ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsInfo = None,
        warn: ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsWarn = None,
        critical: ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsCritical = None,
    ):
        self.info = info
        self.warn = warn
        self.critical = critical

    def validate(self):
        self.validate_required(self.info, 'info')
        if self.info:
            self.info.validate()
        self.validate_required(self.warn, 'warn')
        if self.warn:
            self.warn.validate()
        self.validate_required(self.critical, 'critical')
        if self.critical:
            self.critical.validate()

    def to_map(self):
        result = dict()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Info') is not None:
            temp_model = ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        if m.get('Critical') is not None:
            temp_model = ModifyMetricRuleTemplateRequestAlertTemplatesEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        return self


class ModifyMetricRuleTemplateRequestAlertTemplates(TeaModel):
    def __init__(
        self,
        escalations: ModifyMetricRuleTemplateRequestAlertTemplatesEscalations = None,
        metric_name: str = None,
        webhook: str = None,
        namespace: str = None,
        rule_name: str = None,
        period: int = None,
        selector: str = None,
        category: str = None,
    ):
        self.escalations = escalations
        self.metric_name = metric_name
        self.webhook = webhook
        self.namespace = namespace
        self.rule_name = rule_name
        self.period = period
        self.selector = selector
        self.category = category

    def validate(self):
        self.validate_required(self.escalations, 'escalations')
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.period is not None:
            result['Period'] = self.period
        if self.selector is not None:
            result['Selector'] = self.selector
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Escalations') is not None:
            temp_model = ModifyMetricRuleTemplateRequestAlertTemplatesEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Selector') is not None:
            self.selector = m.get('Selector')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class ModifyMetricRuleTemplateRequest(TeaModel):
    def __init__(
        self,
        template_id: int = None,
        name: str = None,
        description: str = None,
        rest_version: int = None,
        alert_templates: List[ModifyMetricRuleTemplateRequestAlertTemplates] = None,
    ):
        self.template_id = template_id
        self.name = name
        self.description = description
        self.rest_version = rest_version
        self.alert_templates = alert_templates

    def validate(self):
        if self.alert_templates:
            for k in self.alert_templates:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.rest_version is not None:
            result['RestVersion'] = self.rest_version
        result['AlertTemplates'] = []
        if self.alert_templates is not None:
            for k in self.alert_templates:
                result['AlertTemplates'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RestVersion') is not None:
            self.rest_version = m.get('RestVersion')
        self.alert_templates = []
        if m.get('AlertTemplates') is not None:
            for k in m.get('AlertTemplates'):
                temp_model = ModifyMetricRuleTemplateRequestAlertTemplates()
                self.alert_templates.append(temp_model.from_map(k))
        return self


class ModifyMetricRuleTemplateResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyMetricRuleTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyMetricRuleTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyMetricRuleTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyMonitorGroupRequest(TeaModel):
    def __init__(
        self,
        bind_urls: str = None,
        service_id: int = None,
        group_id: str = None,
        group_name: str = None,
        contact_groups: str = None,
    ):
        self.bind_urls = bind_urls
        self.service_id = service_id
        self.group_id = group_id
        self.group_name = group_name
        self.contact_groups = contact_groups

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bind_urls is not None:
            result['BindUrls'] = self.bind_urls
        if self.service_id is not None:
            result['ServiceId'] = self.service_id
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BindUrls') is not None:
            self.bind_urls = m.get('BindUrls')
        if m.get('ServiceId') is not None:
            self.service_id = m.get('ServiceId')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        return self


class ModifyMonitorGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyMonitorGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyMonitorGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyMonitorGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyMonitorGroupInstancesRequestInstances(TeaModel):
    def __init__(
        self,
        instance_name: str = None,
        category: str = None,
        instance_id: str = None,
        region_id: str = None,
    ):
        self.instance_name = instance_name
        self.category = category
        self.instance_id = instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.category is not None:
            result['Category'] = self.category
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ModifyMonitorGroupInstancesRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        instances: List[ModifyMonitorGroupInstancesRequestInstances] = None,
    ):
        self.group_id = group_id
        self.instances = instances

    def validate(self):
        if self.instances:
            for k in self.instances:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        result['Instances'] = []
        if self.instances is not None:
            for k in self.instances:
                result['Instances'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        self.instances = []
        if m.get('Instances') is not None:
            for k in m.get('Instances'):
                temp_model = ModifyMonitorGroupInstancesRequestInstances()
                self.instances.append(temp_model.from_map(k))
        return self


class ModifyMonitorGroupInstancesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyMonitorGroupInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyMonitorGroupInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyMonitorGroupInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifySiteMonitorRequest(TeaModel):
    def __init__(
        self,
        address: str = None,
        task_id: str = None,
        task_name: str = None,
        interval: str = None,
        isp_cities: str = None,
        options_json: str = None,
        alert_ids: str = None,
    ):
        self.address = address
        self.task_id = task_id
        self.task_name = task_name
        self.interval = interval
        self.isp_cities = isp_cities
        self.options_json = options_json
        self.alert_ids = alert_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.address is not None:
            result['Address'] = self.address
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.isp_cities is not None:
            result['IspCities'] = self.isp_cities
        if self.options_json is not None:
            result['OptionsJson'] = self.options_json
        if self.alert_ids is not None:
            result['AlertIds'] = self.alert_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Address') is not None:
            self.address = m.get('Address')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('IspCities') is not None:
            self.isp_cities = m.get('IspCities')
        if m.get('OptionsJson') is not None:
            self.options_json = m.get('OptionsJson')
        if m.get('AlertIds') is not None:
            self.alert_ids = m.get('AlertIds')
        return self


class ModifySiteMonitorResponseBodyData(TeaModel):
    def __init__(
        self,
        count: int = None,
    ):
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        return self


class ModifySiteMonitorResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: ModifySiteMonitorResponseBodyData = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ModifySiteMonitorResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifySiteMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifySiteMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifySiteMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class OpenCmsServiceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        order_id: str = None,
    ):
        self.request_id = request_id
        self.order_id = order_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        return self


class OpenCmsServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: OpenCmsServiceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = OpenCmsServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutContactRequestChannels(TeaModel):
    def __init__(
        self,
        sms: str = None,
        mail: str = None,
        ali_im: str = None,
        ding_web_hook: str = None,
    ):
        self.sms = sms
        self.mail = mail
        self.ali_im = ali_im
        self.ding_web_hook = ding_web_hook

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.sms is not None:
            result['SMS'] = self.sms
        if self.mail is not None:
            result['Mail'] = self.mail
        if self.ali_im is not None:
            result['AliIM'] = self.ali_im
        if self.ding_web_hook is not None:
            result['DingWebHook'] = self.ding_web_hook
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SMS') is not None:
            self.sms = m.get('SMS')
        if m.get('Mail') is not None:
            self.mail = m.get('Mail')
        if m.get('AliIM') is not None:
            self.ali_im = m.get('AliIM')
        if m.get('DingWebHook') is not None:
            self.ding_web_hook = m.get('DingWebHook')
        return self


class PutContactRequest(TeaModel):
    def __init__(
        self,
        channels: PutContactRequestChannels = None,
        contact_name: str = None,
        describe: str = None,
        lang: str = None,
    ):
        self.channels = channels
        self.contact_name = contact_name
        self.describe = describe
        self.lang = lang

    def validate(self):
        if self.channels:
            self.channels.validate()

    def to_map(self):
        result = dict()
        if self.channels is not None:
            result['Channels'] = self.channels.to_map()
        if self.contact_name is not None:
            result['ContactName'] = self.contact_name
        if self.describe is not None:
            result['Describe'] = self.describe
        if self.lang is not None:
            result['Lang'] = self.lang
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Channels') is not None:
            temp_model = PutContactRequestChannels()
            self.channels = temp_model.from_map(m['Channels'])
        if m.get('ContactName') is not None:
            self.contact_name = m.get('ContactName')
        if m.get('Describe') is not None:
            self.describe = m.get('Describe')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        return self


class PutContactResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutContactResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutContactResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutContactResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutContactGroupRequest(TeaModel):
    def __init__(
        self,
        contact_group_name: str = None,
        describe: str = None,
        enable_subscribed: bool = None,
        contact_names: List[str] = None,
    ):
        self.contact_group_name = contact_group_name
        self.describe = describe
        self.enable_subscribed = enable_subscribed
        self.contact_names = contact_names

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group_name is not None:
            result['ContactGroupName'] = self.contact_group_name
        if self.describe is not None:
            result['Describe'] = self.describe
        if self.enable_subscribed is not None:
            result['EnableSubscribed'] = self.enable_subscribed
        if self.contact_names is not None:
            result['ContactNames'] = self.contact_names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupName') is not None:
            self.contact_group_name = m.get('ContactGroupName')
        if m.get('Describe') is not None:
            self.describe = m.get('Describe')
        if m.get('EnableSubscribed') is not None:
            self.enable_subscribed = m.get('EnableSubscribed')
        if m.get('ContactNames') is not None:
            self.contact_names = m.get('ContactNames')
        return self


class PutContactGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutContactGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutContactGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutContactGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutCustomEventRequestEventInfo(TeaModel):
    def __init__(
        self,
        time: str = None,
        event_name: str = None,
        group_id: str = None,
        content: str = None,
    ):
        self.time = time
        self.event_name = event_name
        self.group_id = group_id
        self.content = content

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.time is not None:
            result['Time'] = self.time
        if self.event_name is not None:
            result['EventName'] = self.event_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.content is not None:
            result['Content'] = self.content
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('EventName') is not None:
            self.event_name = m.get('EventName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        return self


class PutCustomEventRequest(TeaModel):
    def __init__(
        self,
        event_info: List[PutCustomEventRequestEventInfo] = None,
    ):
        self.event_info = event_info

    def validate(self):
        if self.event_info:
            for k in self.event_info:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['EventInfo'] = []
        if self.event_info is not None:
            for k in self.event_info:
                result['EventInfo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.event_info = []
        if m.get('EventInfo') is not None:
            for k in m.get('EventInfo'):
                temp_model = PutCustomEventRequestEventInfo()
                self.event_info.append(temp_model.from_map(k))
        return self


class PutCustomEventResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        return self


class PutCustomEventResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutCustomEventResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutCustomEventResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutCustomEventRuleRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        rule_id: str = None,
        rule_name: str = None,
        event_name: str = None,
        contact_groups: str = None,
        webhook: str = None,
        effective_interval: str = None,
        period: str = None,
        email_subject: str = None,
        threshold: str = None,
        level: str = None,
    ):
        self.group_id = group_id
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.event_name = event_name
        self.contact_groups = contact_groups
        self.webhook = webhook
        self.effective_interval = effective_interval
        self.period = period
        self.email_subject = email_subject
        self.threshold = threshold
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.event_name is not None:
            result['EventName'] = self.event_name
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.period is not None:
            result['Period'] = self.period
        if self.email_subject is not None:
            result['EmailSubject'] = self.email_subject
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('EventName') is not None:
            self.event_name = m.get('EventName')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('EmailSubject') is not None:
            self.email_subject = m.get('EmailSubject')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class PutCustomEventRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutCustomEventRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutCustomEventRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutCustomEventRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutCustomMetricRequestMetricList(TeaModel):
    def __init__(
        self,
        type: str = None,
        metric_name: str = None,
        time: str = None,
        group_id: str = None,
        values: str = None,
        dimensions: str = None,
        period: str = None,
    ):
        self.type = type
        self.metric_name = metric_name
        self.time = time
        self.group_id = group_id
        self.values = values
        self.dimensions = dimensions
        self.period = period

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.time is not None:
            result['Time'] = self.time
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.values is not None:
            result['Values'] = self.values
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.period is not None:
            result['Period'] = self.period
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('Values') is not None:
            self.values = m.get('Values')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        return self


class PutCustomMetricRequest(TeaModel):
    def __init__(
        self,
        metric_list: List[PutCustomMetricRequestMetricList] = None,
    ):
        self.metric_list = metric_list

    def validate(self):
        if self.metric_list:
            for k in self.metric_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['MetricList'] = []
        if self.metric_list is not None:
            for k in self.metric_list:
                result['MetricList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.metric_list = []
        if m.get('MetricList') is not None:
            for k in m.get('MetricList'):
                temp_model = PutCustomMetricRequestMetricList()
                self.metric_list.append(temp_model.from_map(k))
        return self


class PutCustomMetricResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        return self


class PutCustomMetricResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutCustomMetricResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutCustomMetricResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutCustomMetricRuleRequest(TeaModel):
    def __init__(
        self,
        group_id: str = None,
        rule_id: str = None,
        rule_name: str = None,
        metric_name: str = None,
        resources: str = None,
        contact_groups: str = None,
        webhook: str = None,
        effective_interval: str = None,
        silence_time: int = None,
        period: str = None,
        email_subject: str = None,
        threshold: str = None,
        level: str = None,
        evaluation_count: int = None,
        statistics: str = None,
        comparison_operator: str = None,
    ):
        self.group_id = group_id
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.metric_name = metric_name
        self.resources = resources
        self.contact_groups = contact_groups
        self.webhook = webhook
        self.effective_interval = effective_interval
        self.silence_time = silence_time
        self.period = period
        self.email_subject = email_subject
        self.threshold = threshold
        self.level = level
        self.evaluation_count = evaluation_count
        self.statistics = statistics
        self.comparison_operator = comparison_operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.resources is not None:
            result['Resources'] = self.resources
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.period is not None:
            result['Period'] = self.period
        if self.email_subject is not None:
            result['EmailSubject'] = self.email_subject
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.level is not None:
            result['Level'] = self.level
        if self.evaluation_count is not None:
            result['EvaluationCount'] = self.evaluation_count
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('EmailSubject') is not None:
            self.email_subject = m.get('EmailSubject')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('EvaluationCount') is not None:
            self.evaluation_count = m.get('EvaluationCount')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        return self


class PutCustomMetricRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutCustomMetricRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutCustomMetricRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutCustomMetricRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutEventRuleRequestEventPattern(TeaModel):
    def __init__(
        self,
        event_type_list: List[str] = None,
        status_list: List[str] = None,
        product: str = None,
        level_list: List[str] = None,
        name_list: List[str] = None,
    ):
        self.event_type_list = event_type_list
        self.status_list = status_list
        self.product = product
        self.level_list = level_list
        self.name_list = name_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.event_type_list is not None:
            result['EventTypeList'] = self.event_type_list
        if self.status_list is not None:
            result['StatusList'] = self.status_list
        if self.product is not None:
            result['Product'] = self.product
        if self.level_list is not None:
            result['LevelList'] = self.level_list
        if self.name_list is not None:
            result['NameList'] = self.name_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventTypeList') is not None:
            self.event_type_list = m.get('EventTypeList')
        if m.get('StatusList') is not None:
            self.status_list = m.get('StatusList')
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('LevelList') is not None:
            self.level_list = m.get('LevelList')
        if m.get('NameList') is not None:
            self.name_list = m.get('NameList')
        return self


class PutEventRuleRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
        group_id: str = None,
        event_type: str = None,
        description: str = None,
        state: str = None,
        event_pattern: List[PutEventRuleRequestEventPattern] = None,
    ):
        self.rule_name = rule_name
        self.group_id = group_id
        self.event_type = event_type
        self.description = description
        self.state = state
        self.event_pattern = event_pattern

    def validate(self):
        if self.event_pattern:
            for k in self.event_pattern:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.event_type is not None:
            result['EventType'] = self.event_type
        if self.description is not None:
            result['Description'] = self.description
        if self.state is not None:
            result['State'] = self.state
        result['EventPattern'] = []
        if self.event_pattern is not None:
            for k in self.event_pattern:
                result['EventPattern'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('EventType') is not None:
            self.event_type = m.get('EventType')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('State') is not None:
            self.state = m.get('State')
        self.event_pattern = []
        if m.get('EventPattern') is not None:
            for k in m.get('EventPattern'):
                temp_model = PutEventRuleRequestEventPattern()
                self.event_pattern.append(temp_model.from_map(k))
        return self


class PutEventRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        data: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.data = data
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutEventRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutEventRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutEventRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutEventRuleTargetsRequestFcParameters(TeaModel):
    def __init__(
        self,
        function_name: str = None,
        region: str = None,
        service_name: str = None,
        id: str = None,
    ):
        self.function_name = function_name
        self.region = region
        self.service_name = service_name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.function_name is not None:
            result['FunctionName'] = self.function_name
        if self.region is not None:
            result['Region'] = self.region
        if self.service_name is not None:
            result['ServiceName'] = self.service_name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FunctionName') is not None:
            self.function_name = m.get('FunctionName')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ServiceName') is not None:
            self.service_name = m.get('ServiceName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsRequestContactParameters(TeaModel):
    def __init__(
        self,
        contact_group_name: str = None,
        level: str = None,
        id: str = None,
    ):
        self.contact_group_name = contact_group_name
        self.level = level
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group_name is not None:
            result['ContactGroupName'] = self.contact_group_name
        if self.level is not None:
            result['Level'] = self.level
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupName') is not None:
            self.contact_group_name = m.get('ContactGroupName')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsRequestMnsParameters(TeaModel):
    def __init__(
        self,
        region: str = None,
        queue: str = None,
        id: str = None,
    ):
        self.region = region
        self.queue = queue
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region is not None:
            result['Region'] = self.region
        if self.queue is not None:
            result['Queue'] = self.queue
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('Queue') is not None:
            self.queue = m.get('Queue')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsRequestWebhookParameters(TeaModel):
    def __init__(
        self,
        protocol: str = None,
        method: str = None,
        url: str = None,
        id: str = None,
    ):
        self.protocol = protocol
        self.method = method
        self.url = url
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.method is not None:
            result['Method'] = self.method
        if self.url is not None:
            result['Url'] = self.url
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('Method') is not None:
            self.method = m.get('Method')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsRequestSlsParameters(TeaModel):
    def __init__(
        self,
        log_store: str = None,
        region: str = None,
        project: str = None,
        id: str = None,
    ):
        self.log_store = log_store
        self.region = region
        self.project = project
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.log_store is not None:
            result['LogStore'] = self.log_store
        if self.region is not None:
            result['Region'] = self.region
        if self.project is not None:
            result['Project'] = self.project
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LogStore') is not None:
            self.log_store = m.get('LogStore')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('Project') is not None:
            self.project = m.get('Project')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
        fc_parameters: List[PutEventRuleTargetsRequestFcParameters] = None,
        contact_parameters: List[PutEventRuleTargetsRequestContactParameters] = None,
        mns_parameters: List[PutEventRuleTargetsRequestMnsParameters] = None,
        webhook_parameters: List[PutEventRuleTargetsRequestWebhookParameters] = None,
        sls_parameters: List[PutEventRuleTargetsRequestSlsParameters] = None,
    ):
        self.rule_name = rule_name
        self.fc_parameters = fc_parameters
        self.contact_parameters = contact_parameters
        self.mns_parameters = mns_parameters
        self.webhook_parameters = webhook_parameters
        self.sls_parameters = sls_parameters

    def validate(self):
        if self.fc_parameters:
            for k in self.fc_parameters:
                if k:
                    k.validate()
        if self.contact_parameters:
            for k in self.contact_parameters:
                if k:
                    k.validate()
        if self.mns_parameters:
            for k in self.mns_parameters:
                if k:
                    k.validate()
        if self.webhook_parameters:
            for k in self.webhook_parameters:
                if k:
                    k.validate()
        if self.sls_parameters:
            for k in self.sls_parameters:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        result['FcParameters'] = []
        if self.fc_parameters is not None:
            for k in self.fc_parameters:
                result['FcParameters'].append(k.to_map() if k else None)
        result['ContactParameters'] = []
        if self.contact_parameters is not None:
            for k in self.contact_parameters:
                result['ContactParameters'].append(k.to_map() if k else None)
        result['MnsParameters'] = []
        if self.mns_parameters is not None:
            for k in self.mns_parameters:
                result['MnsParameters'].append(k.to_map() if k else None)
        result['WebhookParameters'] = []
        if self.webhook_parameters is not None:
            for k in self.webhook_parameters:
                result['WebhookParameters'].append(k.to_map() if k else None)
        result['SlsParameters'] = []
        if self.sls_parameters is not None:
            for k in self.sls_parameters:
                result['SlsParameters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        self.fc_parameters = []
        if m.get('FcParameters') is not None:
            for k in m.get('FcParameters'):
                temp_model = PutEventRuleTargetsRequestFcParameters()
                self.fc_parameters.append(temp_model.from_map(k))
        self.contact_parameters = []
        if m.get('ContactParameters') is not None:
            for k in m.get('ContactParameters'):
                temp_model = PutEventRuleTargetsRequestContactParameters()
                self.contact_parameters.append(temp_model.from_map(k))
        self.mns_parameters = []
        if m.get('MnsParameters') is not None:
            for k in m.get('MnsParameters'):
                temp_model = PutEventRuleTargetsRequestMnsParameters()
                self.mns_parameters.append(temp_model.from_map(k))
        self.webhook_parameters = []
        if m.get('WebhookParameters') is not None:
            for k in m.get('WebhookParameters'):
                temp_model = PutEventRuleTargetsRequestWebhookParameters()
                self.webhook_parameters.append(temp_model.from_map(k))
        self.sls_parameters = []
        if m.get('SlsParameters') is not None:
            for k in m.get('SlsParameters'):
                temp_model = PutEventRuleTargetsRequestSlsParameters()
                self.sls_parameters.append(temp_model.from_map(k))
        return self


class PutEventRuleTargetsResponseBodyFailedMnsParametersMnsParameter(TeaModel):
    def __init__(
        self,
        region: str = None,
        queue: str = None,
        id: int = None,
    ):
        self.region = region
        self.queue = queue
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region is not None:
            result['Region'] = self.region
        if self.queue is not None:
            result['Queue'] = self.queue
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('Queue') is not None:
            self.queue = m.get('Queue')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsResponseBodyFailedMnsParameters(TeaModel):
    def __init__(
        self,
        mns_parameter: List[PutEventRuleTargetsResponseBodyFailedMnsParametersMnsParameter] = None,
    ):
        self.mns_parameter = mns_parameter

    def validate(self):
        if self.mns_parameter:
            for k in self.mns_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['MnsParameter'] = []
        if self.mns_parameter is not None:
            for k in self.mns_parameter:
                result['MnsParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.mns_parameter = []
        if m.get('MnsParameter') is not None:
            for k in m.get('MnsParameter'):
                temp_model = PutEventRuleTargetsResponseBodyFailedMnsParametersMnsParameter()
                self.mns_parameter.append(temp_model.from_map(k))
        return self


class PutEventRuleTargetsResponseBodyFailedFcParametersFcParameter(TeaModel):
    def __init__(
        self,
        function_name: str = None,
        region: str = None,
        service_name: str = None,
        id: int = None,
    ):
        self.function_name = function_name
        self.region = region
        self.service_name = service_name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.function_name is not None:
            result['FunctionName'] = self.function_name
        if self.region is not None:
            result['Region'] = self.region
        if self.service_name is not None:
            result['ServiceName'] = self.service_name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FunctionName') is not None:
            self.function_name = m.get('FunctionName')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ServiceName') is not None:
            self.service_name = m.get('ServiceName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutEventRuleTargetsResponseBodyFailedFcParameters(TeaModel):
    def __init__(
        self,
        fc_parameter: List[PutEventRuleTargetsResponseBodyFailedFcParametersFcParameter] = None,
    ):
        self.fc_parameter = fc_parameter

    def validate(self):
        if self.fc_parameter:
            for k in self.fc_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['FcParameter'] = []
        if self.fc_parameter is not None:
            for k in self.fc_parameter:
                result['FcParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.fc_parameter = []
        if m.get('FcParameter') is not None:
            for k in m.get('FcParameter'):
                temp_model = PutEventRuleTargetsResponseBodyFailedFcParametersFcParameter()
                self.fc_parameter.append(temp_model.from_map(k))
        return self


class PutEventRuleTargetsResponseBodyFailedContactParametersContactParameter(TeaModel):
    def __init__(
        self,
        contact_group_name: str = None,
        id: int = None,
        level: str = None,
    ):
        self.contact_group_name = contact_group_name
        self.id = id
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.contact_group_name is not None:
            result['ContactGroupName'] = self.contact_group_name
        if self.id is not None:
            result['Id'] = self.id
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContactGroupName') is not None:
            self.contact_group_name = m.get('ContactGroupName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class PutEventRuleTargetsResponseBodyFailedContactParameters(TeaModel):
    def __init__(
        self,
        contact_parameter: List[PutEventRuleTargetsResponseBodyFailedContactParametersContactParameter] = None,
    ):
        self.contact_parameter = contact_parameter

    def validate(self):
        if self.contact_parameter:
            for k in self.contact_parameter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContactParameter'] = []
        if self.contact_parameter is not None:
            for k in self.contact_parameter:
                result['ContactParameter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.contact_parameter = []
        if m.get('ContactParameter') is not None:
            for k in m.get('ContactParameter'):
                temp_model = PutEventRuleTargetsResponseBodyFailedContactParametersContactParameter()
                self.contact_parameter.append(temp_model.from_map(k))
        return self


class PutEventRuleTargetsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        failed_mns_parameters: PutEventRuleTargetsResponseBodyFailedMnsParameters = None,
        failed_fc_parameters: PutEventRuleTargetsResponseBodyFailedFcParameters = None,
        failed_parameter_count: str = None,
        failed_contact_parameters: PutEventRuleTargetsResponseBodyFailedContactParameters = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.failed_mns_parameters = failed_mns_parameters
        self.failed_fc_parameters = failed_fc_parameters
        self.failed_parameter_count = failed_parameter_count
        self.failed_contact_parameters = failed_contact_parameters
        self.code = code
        self.success = success

    def validate(self):
        if self.failed_mns_parameters:
            self.failed_mns_parameters.validate()
        if self.failed_fc_parameters:
            self.failed_fc_parameters.validate()
        if self.failed_contact_parameters:
            self.failed_contact_parameters.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.failed_mns_parameters is not None:
            result['FailedMnsParameters'] = self.failed_mns_parameters.to_map()
        if self.failed_fc_parameters is not None:
            result['FailedFcParameters'] = self.failed_fc_parameters.to_map()
        if self.failed_parameter_count is not None:
            result['FailedParameterCount'] = self.failed_parameter_count
        if self.failed_contact_parameters is not None:
            result['FailedContactParameters'] = self.failed_contact_parameters.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('FailedMnsParameters') is not None:
            temp_model = PutEventRuleTargetsResponseBodyFailedMnsParameters()
            self.failed_mns_parameters = temp_model.from_map(m['FailedMnsParameters'])
        if m.get('FailedFcParameters') is not None:
            temp_model = PutEventRuleTargetsResponseBodyFailedFcParameters()
            self.failed_fc_parameters = temp_model.from_map(m['FailedFcParameters'])
        if m.get('FailedParameterCount') is not None:
            self.failed_parameter_count = m.get('FailedParameterCount')
        if m.get('FailedContactParameters') is not None:
            temp_model = PutEventRuleTargetsResponseBodyFailedContactParameters()
            self.failed_contact_parameters = temp_model.from_map(m['FailedContactParameters'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutEventRuleTargetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutEventRuleTargetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutEventRuleTargetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutExporterOutputRequest(TeaModel):
    def __init__(
        self,
        dest_name: str = None,
        config_json: str = None,
        desc: str = None,
        dest_type: str = None,
    ):
        self.dest_name = dest_name
        self.config_json = config_json
        self.desc = desc
        self.dest_type = dest_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.dest_name is not None:
            result['DestName'] = self.dest_name
        if self.config_json is not None:
            result['ConfigJson'] = self.config_json
        if self.desc is not None:
            result['Desc'] = self.desc
        if self.dest_type is not None:
            result['DestType'] = self.dest_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DestName') is not None:
            self.dest_name = m.get('DestName')
        if m.get('ConfigJson') is not None:
            self.config_json = m.get('ConfigJson')
        if m.get('Desc') is not None:
            self.desc = m.get('Desc')
        if m.get('DestType') is not None:
            self.dest_type = m.get('DestType')
        return self


class PutExporterOutputResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutExporterOutputResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutExporterOutputResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutExporterOutputResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutExporterRuleRequest(TeaModel):
    def __init__(
        self,
        rule_name: str = None,
        namespace: str = None,
        metric_name: str = None,
        target_windows: str = None,
        describe: str = None,
        dst_names: List[str] = None,
    ):
        self.rule_name = rule_name
        self.namespace = namespace
        self.metric_name = metric_name
        self.target_windows = target_windows
        self.describe = describe
        self.dst_names = dst_names

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.target_windows is not None:
            result['TargetWindows'] = self.target_windows
        if self.describe is not None:
            result['Describe'] = self.describe
        if self.dst_names is not None:
            result['DstNames'] = self.dst_names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('TargetWindows') is not None:
            self.target_windows = m.get('TargetWindows')
        if m.get('Describe') is not None:
            self.describe = m.get('Describe')
        if m.get('DstNames') is not None:
            self.dst_names = m.get('DstNames')
        return self


class PutExporterRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutExporterRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutExporterRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutExporterRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutGroupMetricRuleRequestEscalationsCritical(TeaModel):
    def __init__(
        self,
        statistics: str = None,
        comparison_operator: str = None,
        threshold: str = None,
        times: int = None,
    ):
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class PutGroupMetricRuleRequestEscalationsWarn(TeaModel):
    def __init__(
        self,
        statistics: str = None,
        comparison_operator: str = None,
        threshold: str = None,
        times: int = None,
    ):
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class PutGroupMetricRuleRequestEscalationsInfo(TeaModel):
    def __init__(
        self,
        statistics: str = None,
        comparison_operator: str = None,
        threshold: str = None,
        times: int = None,
    ):
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class PutGroupMetricRuleRequestEscalations(TeaModel):
    def __init__(
        self,
        critical: PutGroupMetricRuleRequestEscalationsCritical = None,
        warn: PutGroupMetricRuleRequestEscalationsWarn = None,
        info: PutGroupMetricRuleRequestEscalationsInfo = None,
    ):
        self.critical = critical
        self.warn = warn
        self.info = info

    def validate(self):
        self.validate_required(self.critical, 'critical')
        if self.critical:
            self.critical.validate()
        self.validate_required(self.warn, 'warn')
        if self.warn:
            self.warn.validate()
        self.validate_required(self.info, 'info')
        if self.info:
            self.info.validate()

    def to_map(self):
        result = dict()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Critical') is not None:
            temp_model = PutGroupMetricRuleRequestEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        if m.get('Warn') is not None:
            temp_model = PutGroupMetricRuleRequestEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        if m.get('Info') is not None:
            temp_model = PutGroupMetricRuleRequestEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        return self


class PutGroupMetricRuleRequest(TeaModel):
    def __init__(
        self,
        escalations: PutGroupMetricRuleRequestEscalations = None,
        group_id: str = None,
        rule_id: str = None,
        category: str = None,
        rule_name: str = None,
        namespace: str = None,
        metric_name: str = None,
        dimensions: str = None,
        effective_interval: str = None,
        no_effective_interval: str = None,
        silence_time: int = None,
        period: str = None,
        interval: str = None,
        webhook: str = None,
        email_subject: str = None,
        contact_groups: str = None,
    ):
        self.escalations = escalations
        self.group_id = group_id
        self.rule_id = rule_id
        self.category = category
        self.rule_name = rule_name
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.effective_interval = effective_interval
        self.no_effective_interval = no_effective_interval
        self.silence_time = silence_time
        self.period = period
        self.interval = interval
        self.webhook = webhook
        self.email_subject = email_subject
        self.contact_groups = contact_groups

    def validate(self):
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.category is not None:
            result['Category'] = self.category
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.period is not None:
            result['Period'] = self.period
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.email_subject is not None:
            result['EmailSubject'] = self.email_subject
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Escalations') is not None:
            temp_model = PutGroupMetricRuleRequestEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('EmailSubject') is not None:
            self.email_subject = m.get('EmailSubject')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        return self


class PutGroupMetricRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutGroupMetricRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutGroupMetricRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutGroupMetricRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutLogMonitorRequestAggregates(TeaModel):
    def __init__(
        self,
        field_name: str = None,
        function: str = None,
        alias: str = None,
    ):
        self.field_name = field_name
        self.function = function
        self.alias = alias

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.field_name is not None:
            result['FieldName'] = self.field_name
        if self.function is not None:
            result['Function'] = self.function
        if self.alias is not None:
            result['Alias'] = self.alias
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FieldName') is not None:
            self.field_name = m.get('FieldName')
        if m.get('Function') is not None:
            self.function = m.get('Function')
        if m.get('Alias') is not None:
            self.alias = m.get('Alias')
        return self


class PutLogMonitorRequestGroupbys(TeaModel):
    def __init__(
        self,
        field_name: str = None,
        alias: str = None,
    ):
        self.field_name = field_name
        self.alias = alias

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.field_name is not None:
            result['FieldName'] = self.field_name
        if self.alias is not None:
            result['Alias'] = self.alias
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FieldName') is not None:
            self.field_name = m.get('FieldName')
        if m.get('Alias') is not None:
            self.alias = m.get('Alias')
        return self


class PutLogMonitorRequestValueFilter(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
        operator: str = None,
    ):
        self.key = key
        self.value = value
        self.operator = operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        if self.operator is not None:
            result['Operator'] = self.operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        return self


class PutLogMonitorRequest(TeaModel):
    def __init__(
        self,
        log_id: str = None,
        sls_region_id: str = None,
        sls_project: str = None,
        sls_logstore: str = None,
        metric_name: str = None,
        metric_express: str = None,
        group_id: str = None,
        value_filter_relation: str = None,
        tumblingwindows: str = None,
        unit: str = None,
        aggregates: List[PutLogMonitorRequestAggregates] = None,
        groupbys: List[PutLogMonitorRequestGroupbys] = None,
        value_filter: List[PutLogMonitorRequestValueFilter] = None,
    ):
        self.log_id = log_id
        self.sls_region_id = sls_region_id
        self.sls_project = sls_project
        self.sls_logstore = sls_logstore
        self.metric_name = metric_name
        self.metric_express = metric_express
        self.group_id = group_id
        self.value_filter_relation = value_filter_relation
        self.tumblingwindows = tumblingwindows
        self.unit = unit
        self.aggregates = aggregates
        self.groupbys = groupbys
        self.value_filter = value_filter

    def validate(self):
        if self.aggregates:
            for k in self.aggregates:
                if k:
                    k.validate()
        if self.groupbys:
            for k in self.groupbys:
                if k:
                    k.validate()
        if self.value_filter:
            for k in self.value_filter:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.log_id is not None:
            result['LogId'] = self.log_id
        if self.sls_region_id is not None:
            result['SlsRegionId'] = self.sls_region_id
        if self.sls_project is not None:
            result['SlsProject'] = self.sls_project
        if self.sls_logstore is not None:
            result['SlsLogstore'] = self.sls_logstore
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.metric_express is not None:
            result['MetricExpress'] = self.metric_express
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.value_filter_relation is not None:
            result['ValueFilterRelation'] = self.value_filter_relation
        if self.tumblingwindows is not None:
            result['Tumblingwindows'] = self.tumblingwindows
        if self.unit is not None:
            result['Unit'] = self.unit
        result['Aggregates'] = []
        if self.aggregates is not None:
            for k in self.aggregates:
                result['Aggregates'].append(k.to_map() if k else None)
        result['Groupbys'] = []
        if self.groupbys is not None:
            for k in self.groupbys:
                result['Groupbys'].append(k.to_map() if k else None)
        result['ValueFilter'] = []
        if self.value_filter is not None:
            for k in self.value_filter:
                result['ValueFilter'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LogId') is not None:
            self.log_id = m.get('LogId')
        if m.get('SlsRegionId') is not None:
            self.sls_region_id = m.get('SlsRegionId')
        if m.get('SlsProject') is not None:
            self.sls_project = m.get('SlsProject')
        if m.get('SlsLogstore') is not None:
            self.sls_logstore = m.get('SlsLogstore')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('MetricExpress') is not None:
            self.metric_express = m.get('MetricExpress')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('ValueFilterRelation') is not None:
            self.value_filter_relation = m.get('ValueFilterRelation')
        if m.get('Tumblingwindows') is not None:
            self.tumblingwindows = m.get('Tumblingwindows')
        if m.get('Unit') is not None:
            self.unit = m.get('Unit')
        self.aggregates = []
        if m.get('Aggregates') is not None:
            for k in m.get('Aggregates'):
                temp_model = PutLogMonitorRequestAggregates()
                self.aggregates.append(temp_model.from_map(k))
        self.groupbys = []
        if m.get('Groupbys') is not None:
            for k in m.get('Groupbys'):
                temp_model = PutLogMonitorRequestGroupbys()
                self.groupbys.append(temp_model.from_map(k))
        self.value_filter = []
        if m.get('ValueFilter') is not None:
            for k in m.get('ValueFilter'):
                temp_model = PutLogMonitorRequestValueFilter()
                self.value_filter.append(temp_model.from_map(k))
        return self


class PutLogMonitorResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        log_id: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.log_id = log_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.log_id is not None:
            result['LogId'] = self.log_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('LogId') is not None:
            self.log_id = m.get('LogId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutLogMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutLogMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutLogMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutMetricRuleTargetsRequestTargets(TeaModel):
    def __init__(
        self,
        arn: str = None,
        level: str = None,
        id: str = None,
    ):
        self.arn = arn
        self.level = level
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.arn is not None:
            result['Arn'] = self.arn
        if self.level is not None:
            result['Level'] = self.level
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Arn') is not None:
            self.arn = m.get('Arn')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class PutMetricRuleTargetsRequest(TeaModel):
    def __init__(
        self,
        rule_id: str = None,
        targets: List[PutMetricRuleTargetsRequestTargets] = None,
    ):
        self.rule_id = rule_id
        self.targets = targets

    def validate(self):
        if self.targets:
            for k in self.targets:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        result['Targets'] = []
        if self.targets is not None:
            for k in self.targets:
                result['Targets'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        self.targets = []
        if m.get('Targets') is not None:
            for k in m.get('Targets'):
                temp_model = PutMetricRuleTargetsRequestTargets()
                self.targets.append(temp_model.from_map(k))
        return self


class PutMetricRuleTargetsResponseBodyFailDataTargetsTarget(TeaModel):
    def __init__(
        self,
        id: str = None,
        arn: str = None,
        level: str = None,
    ):
        self.id = id
        self.arn = arn
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        if self.arn is not None:
            result['Arn'] = self.arn
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Arn') is not None:
            self.arn = m.get('Arn')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class PutMetricRuleTargetsResponseBodyFailDataTargets(TeaModel):
    def __init__(
        self,
        target: List[PutMetricRuleTargetsResponseBodyFailDataTargetsTarget] = None,
    ):
        self.target = target

    def validate(self):
        if self.target:
            for k in self.target:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Target'] = []
        if self.target is not None:
            for k in self.target:
                result['Target'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.target = []
        if m.get('Target') is not None:
            for k in m.get('Target'):
                temp_model = PutMetricRuleTargetsResponseBodyFailDataTargetsTarget()
                self.target.append(temp_model.from_map(k))
        return self


class PutMetricRuleTargetsResponseBodyFailData(TeaModel):
    def __init__(
        self,
        targets: PutMetricRuleTargetsResponseBodyFailDataTargets = None,
    ):
        self.targets = targets

    def validate(self):
        if self.targets:
            self.targets.validate()

    def to_map(self):
        result = dict()
        if self.targets is not None:
            result['Targets'] = self.targets.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Targets') is not None:
            temp_model = PutMetricRuleTargetsResponseBodyFailDataTargets()
            self.targets = temp_model.from_map(m['Targets'])
        return self


class PutMetricRuleTargetsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        fail_data: PutMetricRuleTargetsResponseBodyFailData = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.fail_data = fail_data
        self.code = code
        self.success = success

    def validate(self):
        if self.fail_data:
            self.fail_data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.fail_data is not None:
            result['FailData'] = self.fail_data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('FailData') is not None:
            temp_model = PutMetricRuleTargetsResponseBodyFailData()
            self.fail_data = temp_model.from_map(m['FailData'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutMetricRuleTargetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutMetricRuleTargetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutMetricRuleTargetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutMonitorGroupDynamicRuleRequestGroupRulesFilters(TeaModel):
    def __init__(
        self,
        value: str = None,
        function: str = None,
        name: str = None,
    ):
        self.value = value
        self.function = function
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.value is not None:
            result['Value'] = self.value
        if self.function is not None:
            result['Function'] = self.function
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Function') is not None:
            self.function = m.get('Function')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class PutMonitorGroupDynamicRuleRequestGroupRules(TeaModel):
    def __init__(
        self,
        filter_relation: str = None,
        filters: List[PutMonitorGroupDynamicRuleRequestGroupRulesFilters] = None,
        category: str = None,
    ):
        self.filter_relation = filter_relation
        self.filters = filters
        self.category = category

    def validate(self):
        if self.filters:
            for k in self.filters:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.filter_relation is not None:
            result['FilterRelation'] = self.filter_relation
        result['Filters'] = []
        if self.filters is not None:
            for k in self.filters:
                result['Filters'].append(k.to_map() if k else None)
        if self.category is not None:
            result['Category'] = self.category
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FilterRelation') is not None:
            self.filter_relation = m.get('FilterRelation')
        self.filters = []
        if m.get('Filters') is not None:
            for k in m.get('Filters'):
                temp_model = PutMonitorGroupDynamicRuleRequestGroupRulesFilters()
                self.filters.append(temp_model.from_map(k))
        if m.get('Category') is not None:
            self.category = m.get('Category')
        return self


class PutMonitorGroupDynamicRuleRequest(TeaModel):
    def __init__(
        self,
        group_id: int = None,
        group_rules: List[PutMonitorGroupDynamicRuleRequestGroupRules] = None,
    ):
        self.group_id = group_id
        self.group_rules = group_rules

    def validate(self):
        if self.group_rules:
            for k in self.group_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        result['GroupRules'] = []
        if self.group_rules is not None:
            for k in self.group_rules:
                result['GroupRules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        self.group_rules = []
        if m.get('GroupRules') is not None:
            for k in m.get('GroupRules'):
                temp_model = PutMonitorGroupDynamicRuleRequestGroupRules()
                self.group_rules.append(temp_model.from_map(k))
        return self


class PutMonitorGroupDynamicRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutMonitorGroupDynamicRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutMonitorGroupDynamicRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutMonitorGroupDynamicRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutMonitoringConfigRequest(TeaModel):
    def __init__(
        self,
        auto_install: bool = None,
        enable_install_agent_new_ecs: bool = None,
    ):
        self.auto_install = auto_install
        self.enable_install_agent_new_ecs = enable_install_agent_new_ecs

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.auto_install is not None:
            result['AutoInstall'] = self.auto_install
        if self.enable_install_agent_new_ecs is not None:
            result['EnableInstallAgentNewECS'] = self.enable_install_agent_new_ecs
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AutoInstall') is not None:
            self.auto_install = m.get('AutoInstall')
        if m.get('EnableInstallAgentNewECS') is not None:
            self.enable_install_agent_new_ecs = m.get('EnableInstallAgentNewECS')
        return self


class PutMonitoringConfigResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutMonitoringConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutMonitoringConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutMonitoringConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutResourceMetricRuleRequestEscalationsCritical(TeaModel):
    def __init__(
        self,
        statistics: str = None,
        comparison_operator: str = None,
        threshold: str = None,
        times: int = None,
    ):
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class PutResourceMetricRuleRequestEscalationsWarn(TeaModel):
    def __init__(
        self,
        statistics: str = None,
        comparison_operator: str = None,
        threshold: str = None,
        times: int = None,
    ):
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class PutResourceMetricRuleRequestEscalationsInfo(TeaModel):
    def __init__(
        self,
        statistics: str = None,
        comparison_operator: str = None,
        threshold: str = None,
        times: int = None,
    ):
        self.statistics = statistics
        self.comparison_operator = comparison_operator
        self.threshold = threshold
        self.times = times

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        return self


class PutResourceMetricRuleRequestEscalations(TeaModel):
    def __init__(
        self,
        critical: PutResourceMetricRuleRequestEscalationsCritical = None,
        warn: PutResourceMetricRuleRequestEscalationsWarn = None,
        info: PutResourceMetricRuleRequestEscalationsInfo = None,
    ):
        self.critical = critical
        self.warn = warn
        self.info = info

    def validate(self):
        self.validate_required(self.critical, 'critical')
        if self.critical:
            self.critical.validate()
        self.validate_required(self.warn, 'warn')
        if self.warn:
            self.warn.validate()
        self.validate_required(self.info, 'info')
        if self.info:
            self.info.validate()

    def to_map(self):
        result = dict()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Critical') is not None:
            temp_model = PutResourceMetricRuleRequestEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        if m.get('Warn') is not None:
            temp_model = PutResourceMetricRuleRequestEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        if m.get('Info') is not None:
            temp_model = PutResourceMetricRuleRequestEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        return self


class PutResourceMetricRuleRequest(TeaModel):
    def __init__(
        self,
        escalations: PutResourceMetricRuleRequestEscalations = None,
        rule_id: str = None,
        rule_name: str = None,
        namespace: str = None,
        metric_name: str = None,
        resources: str = None,
        contact_groups: str = None,
        webhook: str = None,
        effective_interval: str = None,
        no_effective_interval: str = None,
        silence_time: int = None,
        period: str = None,
        interval: str = None,
        email_subject: str = None,
    ):
        self.escalations = escalations
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.namespace = namespace
        self.metric_name = metric_name
        self.resources = resources
        self.contact_groups = contact_groups
        self.webhook = webhook
        self.effective_interval = effective_interval
        self.no_effective_interval = no_effective_interval
        self.silence_time = silence_time
        self.period = period
        self.interval = interval
        self.email_subject = email_subject

    def validate(self):
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.resources is not None:
            result['Resources'] = self.resources
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.period is not None:
            result['Period'] = self.period
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.email_subject is not None:
            result['EmailSubject'] = self.email_subject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Escalations') is not None:
            temp_model = PutResourceMetricRuleRequestEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('EmailSubject') is not None:
            self.email_subject = m.get('EmailSubject')
        return self


class PutResourceMetricRuleResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutResourceMetricRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutResourceMetricRuleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutResourceMetricRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutResourceMetricRulesRequestRulesEscalationsInfo(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        times: int = None,
        statistics: str = None,
        comparison_operator: str = None,
    ):
        self.threshold = threshold
        self.times = times
        self.statistics = statistics
        self.comparison_operator = comparison_operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.times is not None:
            result['Times'] = self.times
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        return self


class PutResourceMetricRulesRequestRulesEscalationsWarn(TeaModel):
    def __init__(
        self,
        threshold: str = None,
        comparison_operator: str = None,
        times: int = None,
        statistics: str = None,
    ):
        self.threshold = threshold
        self.comparison_operator = comparison_operator
        self.times = times
        self.statistics = statistics

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        if self.times is not None:
            result['Times'] = self.times
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class PutResourceMetricRulesRequestRulesEscalationsCritical(TeaModel):
    def __init__(
        self,
        times: int = None,
        threshold: str = None,
        statistics: str = None,
        comparison_operator: str = None,
    ):
        self.times = times
        self.threshold = threshold
        self.statistics = statistics
        self.comparison_operator = comparison_operator

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.times is not None:
            result['Times'] = self.times
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        if self.comparison_operator is not None:
            result['ComparisonOperator'] = self.comparison_operator
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Times') is not None:
            self.times = m.get('Times')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        if m.get('ComparisonOperator') is not None:
            self.comparison_operator = m.get('ComparisonOperator')
        return self


class PutResourceMetricRulesRequestRulesEscalations(TeaModel):
    def __init__(
        self,
        info: PutResourceMetricRulesRequestRulesEscalationsInfo = None,
        warn: PutResourceMetricRulesRequestRulesEscalationsWarn = None,
        critical: PutResourceMetricRulesRequestRulesEscalationsCritical = None,
    ):
        self.info = info
        self.warn = warn
        self.critical = critical

    def validate(self):
        self.validate_required(self.info, 'info')
        if self.info:
            self.info.validate()
        self.validate_required(self.warn, 'warn')
        if self.warn:
            self.warn.validate()
        self.validate_required(self.critical, 'critical')
        if self.critical:
            self.critical.validate()

    def to_map(self):
        result = dict()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        if self.warn is not None:
            result['Warn'] = self.warn.to_map()
        if self.critical is not None:
            result['Critical'] = self.critical.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Info') is not None:
            temp_model = PutResourceMetricRulesRequestRulesEscalationsInfo()
            self.info = temp_model.from_map(m['Info'])
        if m.get('Warn') is not None:
            temp_model = PutResourceMetricRulesRequestRulesEscalationsWarn()
            self.warn = temp_model.from_map(m['Warn'])
        if m.get('Critical') is not None:
            temp_model = PutResourceMetricRulesRequestRulesEscalationsCritical()
            self.critical = temp_model.from_map(m['Critical'])
        return self


class PutResourceMetricRulesRequestRules(TeaModel):
    def __init__(
        self,
        escalations: PutResourceMetricRulesRequestRulesEscalations = None,
        metric_name: str = None,
        no_effective_interval: str = None,
        effective_interval: str = None,
        rule_id: str = None,
        resources: str = None,
        silence_time: int = None,
        webhook: str = None,
        contact_groups: str = None,
        namespace: str = None,
        email_subject: str = None,
        period: str = None,
        rule_name: str = None,
        interval: str = None,
    ):
        self.escalations = escalations
        self.metric_name = metric_name
        self.no_effective_interval = no_effective_interval
        self.effective_interval = effective_interval
        self.rule_id = rule_id
        self.resources = resources
        self.silence_time = silence_time
        self.webhook = webhook
        self.contact_groups = contact_groups
        self.namespace = namespace
        self.email_subject = email_subject
        self.period = period
        self.rule_name = rule_name
        self.interval = interval

    def validate(self):
        self.validate_required(self.escalations, 'escalations')
        if self.escalations:
            self.escalations.validate()

    def to_map(self):
        result = dict()
        if self.escalations is not None:
            result['Escalations'] = self.escalations.to_map()
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.no_effective_interval is not None:
            result['NoEffectiveInterval'] = self.no_effective_interval
        if self.effective_interval is not None:
            result['EffectiveInterval'] = self.effective_interval
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.resources is not None:
            result['Resources'] = self.resources
        if self.silence_time is not None:
            result['SilenceTime'] = self.silence_time
        if self.webhook is not None:
            result['Webhook'] = self.webhook
        if self.contact_groups is not None:
            result['ContactGroups'] = self.contact_groups
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.email_subject is not None:
            result['EmailSubject'] = self.email_subject
        if self.period is not None:
            result['Period'] = self.period
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.interval is not None:
            result['Interval'] = self.interval
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Escalations') is not None:
            temp_model = PutResourceMetricRulesRequestRulesEscalations()
            self.escalations = temp_model.from_map(m['Escalations'])
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('NoEffectiveInterval') is not None:
            self.no_effective_interval = m.get('NoEffectiveInterval')
        if m.get('EffectiveInterval') is not None:
            self.effective_interval = m.get('EffectiveInterval')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('Resources') is not None:
            self.resources = m.get('Resources')
        if m.get('SilenceTime') is not None:
            self.silence_time = m.get('SilenceTime')
        if m.get('Webhook') is not None:
            self.webhook = m.get('Webhook')
        if m.get('ContactGroups') is not None:
            self.contact_groups = m.get('ContactGroups')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('EmailSubject') is not None:
            self.email_subject = m.get('EmailSubject')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        return self


class PutResourceMetricRulesRequest(TeaModel):
    def __init__(
        self,
        rules: List[PutResourceMetricRulesRequestRules] = None,
    ):
        self.rules = rules

    def validate(self):
        if self.rules:
            for k in self.rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Rules'] = []
        if self.rules is not None:
            for k in self.rules:
                result['Rules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.rules = []
        if m.get('Rules') is not None:
            for k in m.get('Rules'):
                temp_model = PutResourceMetricRulesRequestRules()
                self.rules.append(temp_model.from_map(k))
        return self


class PutResourceMetricRulesResponseBodyFailedListResultTargetResult(TeaModel):
    def __init__(
        self,
        success: bool = None,
        code: str = None,
        message: str = None,
    ):
        self.success = success
        self.code = code
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.success is not None:
            result['Success'] = self.success
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        return self


class PutResourceMetricRulesResponseBodyFailedListResultTarget(TeaModel):
    def __init__(
        self,
        result: PutResourceMetricRulesResponseBodyFailedListResultTargetResult = None,
        rule_id: str = None,
    ):
        self.result = result
        self.rule_id = rule_id

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        result = dict()
        if self.result is not None:
            result['Result'] = self.result.to_map()
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Result') is not None:
            temp_model = PutResourceMetricRulesResponseBodyFailedListResultTargetResult()
            self.result = temp_model.from_map(m['Result'])
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class PutResourceMetricRulesResponseBodyFailedListResult(TeaModel):
    def __init__(
        self,
        target: List[PutResourceMetricRulesResponseBodyFailedListResultTarget] = None,
    ):
        self.target = target

    def validate(self):
        if self.target:
            for k in self.target:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Target'] = []
        if self.target is not None:
            for k in self.target:
                result['Target'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.target = []
        if m.get('Target') is not None:
            for k in m.get('Target'):
                temp_model = PutResourceMetricRulesResponseBodyFailedListResultTarget()
                self.target.append(temp_model.from_map(k))
        return self


class PutResourceMetricRulesResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        failed_list_result: PutResourceMetricRulesResponseBodyFailedListResult = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.failed_list_result = failed_list_result
        self.code = code
        self.success = success

    def validate(self):
        if self.failed_list_result:
            self.failed_list_result.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.failed_list_result is not None:
            result['FailedListResult'] = self.failed_list_result.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('FailedListResult') is not None:
            temp_model = PutResourceMetricRulesResponseBodyFailedListResult()
            self.failed_list_result = temp_model.from_map(m['FailedListResult'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutResourceMetricRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutResourceMetricRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutResourceMetricRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveTagsRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class RemoveTagsRequest(TeaModel):
    def __init__(
        self,
        tag: List[RemoveTagsRequestTag] = None,
        group_ids: List[str] = None,
    ):
        self.tag = tag
        self.group_ids = group_ids

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        if self.group_ids is not None:
            result['GroupIds'] = self.group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = RemoveTagsRequestTag()
                self.tag.append(temp_model.from_map(k))
        if m.get('GroupIds') is not None:
            self.group_ids = m.get('GroupIds')
        return self


class RemoveTagsResponseBodyTag(TeaModel):
    def __init__(
        self,
        tags: List[str] = None,
    ):
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class RemoveTagsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        tag: RemoveTagsResponseBodyTag = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.tag = tag
        self.code = code
        self.success = success

    def validate(self):
        if self.tag:
            self.tag.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.tag is not None:
            result['Tag'] = self.tag.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Tag') is not None:
            temp_model = RemoveTagsResponseBodyTag()
            self.tag = temp_model.from_map(m['Tag'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveTagsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveTagsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveTagsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SendDryRunSystemEventRequest(TeaModel):
    def __init__(
        self,
        product: str = None,
        event_name: str = None,
        group_id: str = None,
        event_content: str = None,
    ):
        self.product = product
        self.event_name = event_name
        self.group_id = group_id
        self.event_content = event_content

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.product is not None:
            result['Product'] = self.product
        if self.event_name is not None:
            result['EventName'] = self.event_name
        if self.group_id is not None:
            result['GroupId'] = self.group_id
        if self.event_content is not None:
            result['EventContent'] = self.event_content
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Product') is not None:
            self.product = m.get('Product')
        if m.get('EventName') is not None:
            self.event_name = m.get('EventName')
        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')
        if m.get('EventContent') is not None:
            self.event_content = m.get('EventContent')
        return self


class SendDryRunSystemEventResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: str = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SendDryRunSystemEventResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SendDryRunSystemEventResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SendDryRunSystemEventResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UninstallMonitoringAgentRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class UninstallMonitoringAgentResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UninstallMonitoringAgentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UninstallMonitoringAgentResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UninstallMonitoringAgentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


