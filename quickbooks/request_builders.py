import json
import datetime
import pytz


class BaseBuilder(object):

    def __init__(self):
        self.request = {}

    def to_json(self):
        return json.dumps(self.request)

    @staticmethod
    def convert_date(date):
        """Converts a datetime object into a UTC QBOL compatible string date."""
        # Convert to UTC.
        utcdate = date.astimezone(pytz.UTC)
        # Save to the appropriate format.
        return utcdate.strftime('%Y-%m-%dZ')


class AccountRequestBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def name(self, value):
        self.request['Name'] = value
        return self

    def description(self, value):
        self.request['Description'] = value
        return self

    def account_type_bank(self):
        self.__set_account_type('Bank')
        return self

    def account_type_expense(self):
        self.__set_account_type('Expense')
        return self

    def account_type_receivable(self):
        self.__set_account_type('Accounts Receivable')
        return self

    def __set_account_type(self, value):
        self.request['AccountType'] = value

    def account_sub_type_receivable(self):
        self.__set_account_sub_type('AccountsReceivable')
        return self

    def __set_account_sub_type(self, value):
        self.request['AccountSubType'] = value


#region LineBuilder
class LineBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def amount(self, value):
        self.request['Amount'] = value
        return self

    def description(self, value):
        self.request['Description'] = value
        return self

    def __detail_type(self, value):
        self.request['DetailTypeDetailType'] = value
        return self


class SalesItemLineBuilder(LineBuilder):

    def __init__(self):
        LineBuilder.__init__(self)
        __detail_type('SalesItemLineDetail')

    def sales_item_line_detail(self, sales_item_lime_detail_builder):
        self.request['SalesItemLineDetail'] = sales_item_lime_detail_builder.request
        return self


class SalesItemLineDetailBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def item_ref(self, ref_builder):
        self.request['ItemRef'] = ref_builder.request

    def tax_code_ref(self, ref_builder):
        self.request['TaxCodeRef'] = ref_builder.request

#endregion


class InvoiceRequestBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['Line'] = []

    def add_line(self, line_request_builder):
        self.request['Line'].append(line_request_builder.request)
        return self

    def customer_ref(self, customer_ref_builder):
        self.request['CustomerRef'] = customer_ref_builder.request
        return self


class TaxServiceRequestBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)
        self.request['TaxRateDetails'] = []

    def tax_code(self, value):
        self.request['TaxCode'] = value
        return self

    def add_rate_detail(self, tax_rate_details_builder):
        self.request['TaxRateDetails'].append(tax_rate_details_builder.request)
        return self


class TaxRateDetailsBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)

    def name(self, value):
        self.request['TaxRateName'] = value
        return self

    def rate_id(self, value):
        self.request['TaxRateId'] = value
        return self

    def rate(self, value):
        self.request['RateValue'] = value
        return self

    def agency_id(self, value):
        self.request['TaxAgencyId'] = value
        return self

    def applicable_on_sales(self):
        self.__applicable_on('Sales')
        return self

    def applicable_on_purchase(self):
        self.__applicable_on('Purchase')
        return self

    def __applicable_on(self, value):
        self.request['TaxApplicableOn'] = value

#region ReferenceBuilder
class RefBuilder(BaseBuilder):
    def __init__(self):
        BaseBuilder.__init__(self)

    def name(self, value):
        """Name (Optional)."""
        self.request['name'] = value
        return self

    def type(self, value):
        self.request['type'] = value
        return self

    def value(self, value):
        """Reference object Id."""
        self.request['value'] = value
        return self


class ItemRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)


class CustomerRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)


class AccountRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)


class TaxCodeRefBuilder(RefBuilder):
    def __init__(self):
        RefBuilder.__init__(self)
#endregion


class PaymentRequestBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)

    def customer_ref(self, customer_ref_builder):
        self.request['CustomerRef'] = customer_ref_builder.request
        return self

    def ar_account_ref(self, account_ref_builder):
        self.request['ARAccountRef'] = account_ref_builder.request
        return self

    def total_amount(self, value):
        self.request['TotalAmt'] = value
        return self

    def transaction_date(self, date):
        self.request['TxnDate'] = BaseBuilder.convert_date(date)
        return self
